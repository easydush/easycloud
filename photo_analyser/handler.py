import base64
import json
import os
import uuid
import io
import boto3
import requests
from PIL import Image

from utils import unchecked_photo

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
API_KEY = os.getenv('API_KEY')
MESSAGE_QUEUE_URL = os.getenv('MESSAGE_QUEUE_URL')
YANDEX_VISION_TYPE = "FACE_DETECTION"
YANDEX_VISION_API = "https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze"

AUTH_HEADERS = {'Authorization': f'Api-Key {API_KEY}', 'Content-Type': 'application/json'}

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

sqs = session.resource(
    service_name='sqs',
    endpoint_url='https://message-queue.api.cloud.yandex.net',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='ru-central1'
)

message_queue = sqs.Queue(url=MESSAGE_QUEUE_URL)


def change_photo(data, content, object_id, bucket_id):
    faces_response = requests.post(
        YANDEX_VISION_API,
        headers=AUTH_HEADERS,
        data=data
    ).json()

    try:
        faces_json = faces_response['results'][0]['results'][0]['faceDetection']['faces']
        pillow_image = Image.open(io.BytesIO(content))
        faces = []
        for index, face in enumerate(faces_json):
            coordinate_1 = face['boundingBox']['vertices'][0]
            coordinate_2 = face['boundingBox']['vertices'][2]
            cropped = pillow_image.crop((int(coordinate_1['x']), int(coordinate_1['y']),
                                         int(coordinate_2['x']), int(coordinate_2['y'])))
            img_bytes = io.BytesIO()
            cropped.save(img_bytes, format='jpeg')
            album_name = object_id[:object_id.find('/')]
            object_name = object_id[object_id.rfind('/') + 1:]
            object_storage_name = f"{album_name}/faces/{object_name}-{uuid.uuid1()}.jpeg"
            s3.upload_fileobj(io.BytesIO(img_bytes.getvalue()), bucket_id, object_storage_name)
            faces.append(object_storage_name)

        message_body = {'faces': str(faces), 'parent': object_id}
        message_queue.send_message(MessageBody=message_body)

    except KeyError as e:
        print(e)


def handler(event, context):
    bucket_id = event['messages'][0]['details']['bucket_id']
    object_id = event['messages'][0]['details']['object_id']

    if unchecked_photo(object_id):
        s3_response_object = s3.get_object(Bucket=bucket_id, Key=object_id)
        content = s3_response_object['Body'].read()
        encoded_object = base64.b64encode(content)

        data = json.dumps(
            {
                "analyze_specs": [
                    {
                        "content": encoded_object.decode('ascii'),
                        "features": [
                            {
                                "type": YANDEX_VISION_TYPE
                            }
                        ]
                    }
                ]
            },
            indent=4
        )
        change_photo(data, content, object_id, bucket_id)

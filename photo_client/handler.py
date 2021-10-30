import argparse
from os import listdir
import boto3
import os
from dotenv import load_dotenv

from exceptions import NoDataException, NoArgumentsException, NoSuchPathException
from utils import correct_extension, is_dir

load_dotenv()

COMMANDS = ['upload', 'download', 'list']
BUCKET_NAME = os.getenv('BUCKET_NAME')

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=COMMANDS)
parser.add_argument('-p', dest='path', required=False)
parser.add_argument('-a', dest='album', required=False)
command = parser.parse_args()


def upload(path, album):
    if not path:
        raise NoArgumentsException
    if not is_dir(path):
        raise NoSuchPathException

    files = [file for file in listdir(path) if correct_extension(file)]
    for file in files:
        print(f'Uploading {file}')
        pathname = f'{album}/{file}' if album else file
        s3.upload_file(f'{path}/{file}', BUCKET_NAME, pathname)


def get_files_from_album(album=''):
    try:
        if album:
            album = f'{album}/'
        return s3.list_objects(Bucket=BUCKET_NAME, Prefix=album)['Contents']
    except KeyError:
        raise NoDataException


def download(path, album):
    if not path or not album:
        raise NoArgumentsException
    if not is_dir(path):
        raise NoSuchPathException

    files = get_files_from_album(album)
    print(f'Downloading photos from {album}')
    for file in files:
        if not correct_extension(file["Key"]):
            continue
        filename = os.path.basename(file["Key"])
        print(filename)
        s3.download_file(BUCKET_NAME, file['Key'], f'{path}/{filename}')


def list_objects(album=''):
    if not album:
        album = ''
    print('Files in cloud:\n')

    for key in get_files_from_album(album):
        print(key['Key'])


try:
    if command.command == 'list':
        list_objects(command.album)
    elif command.command == 'upload':
        upload(command.path, command.album)
    elif command.command == 'download':
        download(command.path, command.album)
except Exception as e:
    print(e)

import requests
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')


def send_message(json):
    return requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json=json)


def send_photo(data, files):
    return requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto', data=data, files=files)


NOT_FOUND = {
    'statusCode': 200,
    'body': 'Команда не найдена.',
}

OK = {
    'statusCode': 200,
    'body': 'Ok',
}

NO_PHOTO = {
    'statusCode': 200,
    'body': 'Нет фото!',
}

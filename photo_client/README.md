## Запуск
### Настройка окружения хранилища
Для настройки создайте в домашнем каталоге файлы конфигурации и задайте в них:

Статический ключ в файле .aws/credentials:

    [default]
            aws_access_key_id = <id>
            aws_secret_access_key = <secretKey>
Регион по умолчанию в файле .aws/config:

    [default]
            region=ru-central1


### Настройка проекта
Переименуйте файл .env.template в .env и задайте свои значения переменных в нем.
Запустите команду
    pip install -r requirements.txt

### Запуск
    python photo_client/handler.py *command*
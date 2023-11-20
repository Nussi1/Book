# Каталог книг

Этот проект представляет собой веб-приложение для управления каталогом книг.

## Установка

Для установки проекта необходимо выполнить следующие шаги:

1. Клонировать репозиторий на локальный компьютер:

    ```bash
    git clone https://github.com/username/каталог-книг.git
    ```

2. Установить зависимости:

    ```bash
    pip install -r requirements.txt
    ```

3. Применить миграции:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

## Запуск

Чтобы запустить проект локально, выполните следующую команду:

```bash
        python manage.py runserver
```

## Ссылка на порту

Вы можете открыть приложение в вашем браузере, перейдя по адресу http://127.0.0.1:8000/.

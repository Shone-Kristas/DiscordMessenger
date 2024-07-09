# Рассылка сообщений в Discord

<br>

## Оглавление
- [Технологии](#технологии)
- [Описание](#описание)
- [Установка](#установка)
- [Запуск](#запуск)
- [Автор](#автор)

<br>

## Технологии

[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?logo=FastAPI)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?logo=PostgreSQL)](https://www.postgresql.org/)
[![asyncpg](https://img.shields.io/badge/-asyncpg-464646?logo=asyncpg)](https://magicstack.github.io/asyncpg/current/)
[![requests](https://img.shields.io/badge/-requests-464646?logo=requests)](https://pypi.org/project/requests/)
[![sqlalchemy](https://img.shields.io/badge/-sqlalchemy-464646?logo=sqlalchemy)](https://docs.sqlalchemy.org/en/20/orm/)
[![apscheduler](https://img.shields.io/badge/-apscheduler-464646?logo=apscheduler)](https://apscheduler.readthedocs.io/en/3.x/)
[![docker](https://img.shields.io/badge/-Docker-464646?logo=docker)](https://www.docker.com/)
[![docker_compose](https://img.shields.io/badge/-Docker%20Compose-464646?logo=docker)](https://docs.docker.com/compose/)




[⬆️Оглавление](#оглавление)

<br>

## Описание

Этот проект представляет собой backend-приложение для организации рассылки сообщений в Discord. 
Он предоставляет удобный интерфейс для загрузки аккаунтов, управления списком пользователей и 
настройки сообщений для рассылки по заданному расписанию.

Основные функции:

   - Загрузка данных аккаунтов из CSV файла с указанием логина и пароля.
   - Загрузка списка пользователей (по их ID) из CSV файла.
   - Ввод сообщения для рассылки через интерфейс приложения.
   - Установка времени отправки сообщения в формате чч:мм
   - Создание задачи в планировщике задач для отправки сообщений по указанному времени.
   - Автоматический запуск рассылки в заданное время.

Логика работы:

   - Используя логин и пароль из загруженных аккаунтов, приложение получает Discord токен, необходимый для отправки сообщений.
   - С использованием токена и ID пользователей из загруженного списка, приложение получает ID чата (channel ID), куда будет направлено сообщение.
   - Отправка подготовленного сообщения каждому пользователю по полученному ID чата.

Формат в котором должны быть загружаемые данные в CSV файлах, можно посмотреть открыв файлы со следующими названиями:
```bash
accounts_upload.csv
user_data.csv
```

[⬆️Оглавление](#оглавление)

<br>

## Установка

Клонируйте репозиторий с GitHub:

```bash
git clone https://github.com/Shone-Kristas/DiscordMessenger.git
```

Подразумевается, что на локальной машине, или на удаленном сервере, уже установлены Docker и Docker Compose.

[⬆️Оглавление](#оглавление)

<br>

## Запуск

Из корневой директории проекта выполните команду:
```bash
docker compose up --build
```
* Простой пользовательский интерфейс [http://localhost:8000/static/app.html](http://localhost:8000/static/app.html)
* Swagger [http://localhost:8000/docs](http://localhost:8000/docs)

[⬆️Оглавление](#оглавление)

<br>

## Автор:
[Nickolay](https://github.com/Shone-Kristas)

[⬆️В начало](#Рассылка-сообщений-в-Discord)

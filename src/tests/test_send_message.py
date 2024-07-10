import pytest
import requests
import responses
import json

from ..trigger import send_message, MESSAGE_URL


# Тест успешной отправки сообщения
@responses.activate
def test_send_message_success(capfd):
    token = "fake_token"
    channel_id = "12345"
    message = "Test message!"

    # Мокируем успешный ответ от сервера
    responses.add(
        responses.POST,
        MESSAGE_URL.format(channel_id),
        json={'id': 'message_id'},
        status=200
    )

    # Вызываем функцию
    send_message(token, channel_id, message)

    # Проверяем вывод функции
    captured = capfd.readouterr()
    assert "Message sent" in captured.out


# Тест неудачной отправки сообщения
@responses.activate
def test_send_message_failure(capfd):
    token = "fake_token"
    channel_id = "12345"
    message = "Test message!"

    # Мокируем неудачный ответ от сервера
    responses.add(
        responses.POST,
        MESSAGE_URL.format(channel_id),
        json={'message': 'Failed to send message'},
        status=400
    )

    # Вызываем функцию
    send_message(token, channel_id, message)

    # Проверяем вывод функции
    captured = capfd.readouterr()
    assert "Failed to send message" in captured.out
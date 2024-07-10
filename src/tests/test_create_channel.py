import pytest
import requests
import responses
import json

from ..trigger import create_channel, CHANNEL_URL


# Тест успешного создания канала
@responses.activate
def test_create_channel_success():
    token = "fake_token"
    user_id = "12345"

    # Мокируем успешный ответ от сервера
    responses.add(
        responses.POST,
        CHANNEL_URL,
        json={'id': 'new_channel_id'},
        status=200
    )

    # Вызываем функцию
    channel_id = create_channel(token, user_id)

    # Проверяем, что возвращен корректный идентификатор канала
    assert channel_id == 'new_channel_id'


# Тест неудачного создания канала
@responses.activate
def test_create_channel_failure():
    token = "fake_token"
    user_id = "12345"

    # Мокируем неудачный ответ от сервера
    responses.add(
        responses.POST,
        CHANNEL_URL,
        json={'message': 'Failed to create channel'},
        status=400
    )

    # Проверяем, что функция выбрасывает исключение при неудачном создании канала
    with pytest.raises(Exception, match='Failed to create channel'):
        create_channel(token, user_id)
import pytest
import requests
import responses
import json

from ..trigger import login_to_discord, LOGIN_URL


# Тест успешного логина
@responses.activate
def test_login_to_discord_success():
    email = "test@example.com"
    password = "correct_password"

    # Мокируем успешный ответ от Discord
    responses.add(
        responses.POST,
        LOGIN_URL,
        json={'token': 'fake_token'},
        status=200
    )

    # Вызываем функцию
    token = login_to_discord(email, password)

    # Проверяем, что возвращен корректный токен
    assert token == 'fake_token'


# Тест неудачного логина
@responses.activate
def test_login_to_discord_failure():
    email = "test@example.com"
    password = "wrong_password"

    # Мокируем неудачный ответ от Discord
    responses.add(
        responses.POST,
        LOGIN_URL,
        json={'message': 'Invalid credentials'},
        status=401
    )

    # Проверяем, что функция выбрасывает исключение при неудачном логине
    with pytest.raises(Exception, match='Failed to log in'):
        login_to_discord(email, password)
import requests
import json


# URL для входа в аккаунт
LOGIN_URL = 'https://discord.com/api/v9/auth/login'
# URL для создания канала общения
CHANNEL_URL = 'https://discord.com/api/v9/users/@me/channels'
# URL для отправки сообщения
MESSAGE_URL = 'https://discord.com/api/v9/channels/{}/messages'

def login_to_discord(email, password):
    payload = {
        'login': email,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.post(LOGIN_URL, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()['token']
    else:
        raise Exception('Failed to log in')

def create_channel(token, user_id):
    payload = {
        'recipient_id': user_id
    }
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.post(CHANNEL_URL, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        return response.json()['id']
    else:
        raise Exception('Failed to create channel')

def send_message(token, channel_id, message):
    payload = {
        'content': message
    }
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.post(MESSAGE_URL.format(channel_id), data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print('Message sent')
    else:
        print('Failed to send message')


def schedule_message(email, password, user_id, message):
    token = login_to_discord(email, password)
    channel_id = create_channel(token, user_id)
    send_message(token, channel_id, message)
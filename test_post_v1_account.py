import pprint

import requests
from json import loads


def test_post_v1_account():
    # Регистрация пользователя

    login = 'morugova_test453439514_5353'
    password = '123456789'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    print('код создания пользователя: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # Получить письма из почтового сервера

    params = {
        'limit': '50',
    }

    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print('получение писем из почтового сервера: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен

    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']

        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print('токен: ')
            print(token)

    assert token is not None, f"Токен для пользователя {login} не был получен"
    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)
    print('урл активации пользователя: ')
    print(f'http://5.63.153.31:5051/v1/account/{token}')
    print('активация пользователя: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # # Авторизоваться
    headers = {
        'accept': 'text/plain',
        'Content-Type': 'application/json',
    }

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://5.63.153.31:5051/v1/account/login', headers=headers, json=json_data)
    print('авторизация пользователя: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

import pprint
from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi



def test_post_v1_account():
    # Регистрация пользователя
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')
    login = 'morugova_test345234544444_45'
    password = '123456789'
    email = f'{login}@mail.ru'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    print('код создания пользователя: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    print('получение писем из почтового сервера: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен
    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login} не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print('урл активации пользователя: ')
    print(f'http://5.63.153.31:5051/v1/account/{token}')
    print('активация пользователя: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Сменить почтовый ящик пользователя
    print('старый почтовый ящик: ')
    print(email)

    email = change_email_by_old_email(email)

    print('до смены почтового ящика у пользователя: ')
    print('login: ')
    print(password)
    print('password: ')
    print(login)
    print('email: ')
    print(email)

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    print('json_data: ')
    pprint.pprint(json_data)
    response = account_api.put_v1_account_email(json_data)
    print('смена почтового ящика у пользователя: ')
    print(response)

    print('новый почтовый ящик: ')
    print(email)

    assert response.status_code == 200, "Почтовый ящик не был сменён"


    # подтвердить новый почтовый ящик пользователя
    ## Получить письма из почтового сервера

    response = mailhog_api.get_api_v2_messages()
    print('получение писем из почтового сервера: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    ## Получить активационный токен
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Токен для пользователя {login} не был получен"

    ## Активация пользователя
    response = account_api.put_v1_account_token(token=token)
    print('урл активации пользователя: ')
    print(f'http://5.63.153.31:5051/v1/account/{token}')
    print('активация пользователя: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # # Авторизоваться
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = login_api.post_v1_account_login(json_data=json_data)
    print('авторизация пользователя: ')
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # # запросить инфо о пользователе
    # print('новый токен: ')
    # print(token)
    # response = account_api.get_v1_account(token)
    #
    # print('запрос пользователя после смены почтового ящика: ')
    # print(response)


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']

        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token

def change_email_by_old_email(
        email
):
    email = f'string_{email}'
    return email

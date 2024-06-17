import time
from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi
from retrying import retry


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(function):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f"Попытка получения токена номер {count}")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения активационного токена!")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"Пользователь не был создан {response.json()}"
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return response

    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
        return response

    def change_email(self, login: str, password: str, email: str):
        email = f'string_{email}'
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data)
        assert response.status_code == 200, "Почтовый ящик не был сменён"
        token = self.get_new_activation_token_by_login(login, email)
        assert token is not None, f"Токен для пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не был активирован"
        return response

    def get_auth_account_token(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        # response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        # assert response.status_code == 201, f"Пользователь не был создан {response.json()}"
        token = self.get_activation_token_by_login(login=login)
        assert token is not None, f"Токен для пользователя {login} не был получен"

    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={
                "login": login,
                "password": password
            }
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def reset_user_password(self, login: str, email: str):
        response = self.dm_account_api.account_api.post_v1_account_password(
            json_data={
                'login': login,
                'email': email,
            }
        )
        assert response.status_code == 200, f"Пароль не был сброшен"

    def change_registered_user_password(self, login: str, email: str, oldPassword: str, newPassword: str):
        token = self.get_reset_token_by_login(email=email) #(login=login)
        assert token is not None, f"Токен для сброса пароля пользователя {login} не был получен"
        response = self.dm_account_api.account_api.put_v1_account_password(
            json_data={
                "login": login,
                "token": token,
                "oldPassword": oldPassword,
                "newPassword": newPassword,
            }
        )
        assert response.status_code == 200, f"Пароль не был изменён"

    # def unreset_user_password(self, login: str, email: str):
    #     # меняем новый пароль на старый, чтобы следующий прогон был успешен
    #     # со старыми данными из фикстуры авторизации пользователя
    #     token = self.get_reset_token_by_login(login=login)
    #     assert token is not None, f"Токен для сброса пароля пользователя {email} не был получен"
    #     response = self.dm_account_api.account_api.put_v1_account_password(
    #         json_data={
    #             "login": login,
    #             "token": token,
    #             "oldPassword": "987654321",
    #             "newPassword": "123456789"
    #         }
    #     )
    #     assert response.status_code == 200, f"Пароль не был изменён"

    def logout_user(self, **kwargs):
        response = self.dm_account_api.login_api.delete_v1_account_login(**kwargs)
        assert response.status_code == 204, f"Пользователь не был разлогинен"

    def logout_user_all(self, **kwargs):
        response = self.dm_account_api.login_api.delete_v1_account_login_all(**kwargs)
        assert response.status_code == 204, f"Пользователь не был разлогинен из всех устройств"

    @retry(
        stop_max_attempt_number=5,
        retry_on_result=retry_if_result_none,
        wait_fixed=1000
    )
    def get_activation_token_by_login(
            self,
            login,
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']

            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token

    @retry(
        stop_max_attempt_number=5,
        retry_on_result=retry_if_result_none,
        wait_fixed=1000
    )
    def get_new_activation_token_by_login(
            self,
            login,
            email
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            user_new_email = item['Content']['Headers']['To'][0]

            if user_login == login and user_new_email == email:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]

        return token

    @retry(
        stop_max_attempt_number=5,
        retry_on_result=retry_if_result_none,
        wait_fixed=1000
    )
    def get_reset_token_by_login(
            self,
            # login,
            email
    ):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            user_email = item['Content']['Headers']['To'][0]
            # subject = f"=?utf-8?b?0J/QvtC00YLQstC10YDQttC00LXQvdC40LUg0YHQsdGA0L7RgdCw?= =?utf-8?b?INC/0LDRgNC+0LvRjyDQvdCwIERNLkFNINC00LvRjw==?= {login}"
            subject_letter = item['Content']['Headers']['Subject'][0]

            # if subject_letter == subject:
            if user_email == email: #user_login == login:
                token = user_data['ConfirmationLinkUri'].split('/')[-1]
        return token

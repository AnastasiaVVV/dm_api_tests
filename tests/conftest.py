import datetime
from collections import namedtuple

import pytest

from helpers.account_helper import AccountHelper

from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

import random
import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            # sort_keys=True,
        )
    ]
)


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture(scope="function")
def auth_account_helper(mailhog_api, prepare_user):
    # account_helper = AccountHelper()
    # account_helper.create_user(...)
    # account_helper.auth_client(...)

    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)

    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)

    account_helper.default_login = login
    account_helper.default_password = password
    account_helper.default_email = email

    account_helper.auth_client(
        login=account_helper.default_login,
        password=account_helper.default_password
    )
    return account_helper



@pytest.fixture
def prepare_user():
    now = datetime.datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S_%f")
    login = f'morugova_test.{data}'
    password = '123456789'
    email = f'{login}@mail.ru'
    User = namedtuple("user", ["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user

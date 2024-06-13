def test_put_v1_account_password(auth_account_helper):
    login = auth_account_helper.default_login
    email = f"string_{auth_account_helper.default_login}@mail.ru"
    auth_account_helper.reset_user_password(login=login, email=email)

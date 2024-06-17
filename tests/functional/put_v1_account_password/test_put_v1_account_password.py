def test_put_v1_account_password(auth_account_helper):
    login = auth_account_helper.default_login
    email = f"string_{auth_account_helper.default_login}@mail.ru"
    # auth_account_helper.reset_user_password(login=login, email=email, oldPassword='123456789', newPassword='987654321')
    auth_account_helper.reset_user_password(login=login, email=email)
    auth_account_helper.change_registered_user_password(
        login=login, email=email, oldPassword='123456789', newPassword='987654321'
    )
    auth_account_helper.change_registered_user_password(
        login=login, email=email, oldPassword='123456789', newPassword='987654321',
    )

def test_put_v1_account_password(auth_account_helper):#(account_helper, prepare_user):
    # login = prepare_user.login
    # password = prepare_user.password
    # email = prepare_user.email

    login = auth_account_helper.default_login
    password = auth_account_helper.default_password
    email = f"string_{auth_account_helper.default_login}@mail.ru"
    # auth_account_helper.reset_user_password(login=login, email=email, oldPassword='123456789', newPassword='987654321')
    # auth_account_helper.reset_user_password(login=login, email=email)
    auth_account_helper.change_registered_user_password(
        login=login, email=email, old_password=password, new_password='987654321',
    )
    auth_account_helper.user_login(login=login, password='987654321')
    # account_helper.change_registered_user_password(
    #     login=login, email=email, old_password='987654321', new_password='123456789'
    # )
    # auth_account_helper.user_login(login=login, password='987654321')

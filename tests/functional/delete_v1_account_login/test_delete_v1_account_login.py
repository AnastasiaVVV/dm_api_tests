def test_delete_v1_account_login(auth_account_helper):
    auth_account_helper.logout_user()


def test_delete_v1_account_login_v2(account_helper, prepare_user):
    # Идея кейса такая:
    # register_user()
    # response = login_user()
    # token = response.headers['token']
    #
    # logout_user(headers=token)

    # "X-Dm-Auth-Token": response.headers["X-Dm-Auth-Token"]
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password)
    token = response.headers['X-Dm-Auth-Token']
    account_helper.logout_user(headers={"X-Dm-Auth-Token": token})

def test_delete_v1_account_login_all(auth_account_helper):
    auth_account_helper.logout_user_all()


def test_delete_v1_account_login_all_v2(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    account_helper.register_new_user(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password)
    token = response.headers['X-Dm-Auth-Token']
    account_helper.logout_user_all(
        headers={
            "X-Dm-Auth-Token": token
        }
    )

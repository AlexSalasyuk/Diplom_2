import pytest
from helpers.user_data import generate_user_data
from helpers.api import register_user, login_user, delete_user

@pytest.fixture
def user_token():
    user = generate_user_data()
    register_resp = register_user(user)
    assert register_resp.status_code == 200

    token = login_user({'email': user['email'], 'password': user['password']}).json().get('accessToken')
    yield {'token': token, 'user': user}
    delete_user(token)

import allure
import pytest
from helpers.api import login_user
from helpers.messages import USER_LOGIN_ERROR


@allure.title('Проверить логин пользователя')
class TestUserLogin:

    @allure.title('Проверить, что можно залогиниться под существующим пользователем — код 200 и accessToken')
    def test_login_existing_user_returns_200(self, user_token):
        creds = user_token['user']

        with allure.step('Отправить запрос на логин повторно'):
            response = login_user({'email': creds['email'], 'password': creds['password']})

        with allure.step('Проверить статус код 200 и наличие accessToken в теле'):
            assert response.status_code == 200
            assert 'accessToken' in response.json()

    @allure.title('Проверить, что нельзя залогиниться с неверным логином или паролем — код 401')
    @pytest.mark.parametrize('field_to_spoil', ['email', 'password'])
    def test_login_invalid_credentials_returns_401(self, user_token, field_to_spoil):
        creds = user_token['user']

        wrong_payload = {
            'email': creds['email'],
            'password': creds['password']
        }
        wrong_payload[field_to_spoil] = 'wrong_' + wrong_payload[field_to_spoil]

        with allure.step(f'Отправить запрос на логин с неправильным {field_to_spoil}'):
            response = login_user(wrong_payload)

        with allure.step('Проверить ошибку, статус код 401 и сообщение email or password are incorrect'):
            assert response.status_code == 401
            assert response.json()['message'] == USER_LOGIN_ERROR

import pytest
import allure

from helpers.messages import REGISTER_USER_ERROR_EXIST, REGISTER_USER_ERROR_FIELDS
from helpers.user_data import generate_user_data
from helpers.api import register_user, delete_user


@allure.title('Проверить создание пользователя: валидные и невалидные кейсы')
class TestRegisterUser:

    @allure.title('Проверить, что можно создать уникального пользователя — код 200 и accessToken')
    def test_register_unique_user_returns_200(self):
        user = generate_user_data()

        with allure.step('Отправить запрос на регистрацию нового пользователя'):
            response = register_user(user)

        with allure.step('Проверить статус код 200 и наличие accessToken в теле'):
            assert response.status_code == 200
            assert 'accessToken' in response.json()

        with allure.step('Удалить пользователя после теста'):
            token = response.json()['accessToken']
            delete_user(token)

    @allure.title('Проверить, что нельзя зарегистрировать уже существующего пользователя — код 403')
    def test_register_existing_user_returns_403(self):
        user = generate_user_data()

        with allure.step('Создать пользователя первый раз'):
            response_1 = register_user(user)
            token = response_1.json()['accessToken']

        with allure.step('Создать пользователя повторно'):
            response_2 = register_user(user)

        with allure.step('Проверить ошибку, статус код 403 и сообщение User already exists'):
            assert response_2.status_code == 403
            assert response_2.json()['message'] == REGISTER_USER_ERROR_EXIST

        with allure.step('Удалить пользователя после теста'):
            delete_user(token)

    @allure.title('Проверить, что нельзя создать пользователя без обязательных полей — код 403')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_register_user_missing_required_field_returns_403(self, missing_field):
        user = generate_user_data()
        user.pop(missing_field)

        with allure.step(f'Удалить поле {missing_field} и отправить запрос на регистрацию'):
            response = register_user(user)

        with allure.step('Проверить ошибку, статус код 403 и сообщение Email, password and name are required fields'):
            assert response.status_code == 403
            assert response.json()['message'] == REGISTER_USER_ERROR_FIELDS

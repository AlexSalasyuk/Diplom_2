import allure
import pytest

from helpers.messages import USER_UPDATE_ERROR_UNAUTH
from helpers.user_data import generate_user_data
from helpers.api import register_user, delete_user, update_user


@allure.title('Проверить изменение данных пользователя')
class TestUserUpdate:

    @allure.title('Проверить, что можно изменить данные авторизованного пользователя — код 200')
    @pytest.mark.parametrize('field_to_update, value', [
        ('email', 'updated_user@yandex.ru'),
        ('name', 'UpdatedName'),
        ('password', 'UpdatedPassword666')
    ])
    def test_update_user_with_auth_returns_200(self, user_token, field_to_update, value):
        token = user_token['token']
        headers = {'Authorization': token}
        updated_data = {field_to_update: value}

        with allure.step(f'Отправить запрос на изменение поля {field_to_update} с авторизацией'):
            response = update_user(token, updated_data)

        with allure.step('Проверить статус код 200 и тело с обновлёнными данными'):
            assert response.status_code == 200
            if field_to_update == 'password':
                # Сервер не возвращает password в теле ответа, требование безопасности
                assert 'user' in response.json()
            else:
                assert response.json()['user'][field_to_update] == value


    @allure.title('Проверить,что нельзя изменить данные без авторизации — код 401')
    @pytest.mark.parametrize('field_to_update, value', [
        ('email', 'unauth_user@yandex.ru'),
        ('name', 'Unauthorized'),
        ('password', 'NoAuthPassword666')
    ])
    def test_update_user_without_auth_returns_401(self, field_to_update, value):
        user = generate_user_data()

        with allure.step('Создать пользователя (но не использовать токен)'):
            reg_response = register_user(user)
            token = reg_response.json()['accessToken']

        update_data = {field_to_update: value}

        with allure.step(f'Изменить поле {field_to_update} без авторизации'):
            response = update_user(token=None, data=update_data)

        with allure.step('Проверить ошибку, статус код 401 и сообщение You should be authorised'):
            assert response.status_code == 401
            assert response.json()['message'] == USER_UPDATE_ERROR_UNAUTH

        with allure.step('Удалить пользователя после теста'):
            delete_user(token)

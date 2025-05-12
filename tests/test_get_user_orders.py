import allure
from helpers.api import get_user_orders


@allure.title('Проверить получение заказов пользователя')
class TestGetUserOrders:

    def test_get_orders_with_auth_returns_200(self, user_token):
        token = user_token['token']

        with allure.step('Отправить запрос с токеном'):
            response = get_user_orders(token)

        with allure.step('Проверить, статус код 200 и тело'):
            assert response.status_code == 200
            assert 'orders' in response.json()

    @allure.title('Проверить, что неавторизованный пользователь не может получить заказы — код 401')
    def test_get_orders_without_auth_returns_401(self):
        with allure.step('Отправить запрос без токена'):
            response = get_user_orders(token=None)

        with allure.step('Проверить ошибку, статус код 401 и сообщение You should be authorised'):
            assert response.status_code == 401
            assert response.json()['message'] == 'You should be authorised'

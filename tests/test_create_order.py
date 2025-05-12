import allure
from helpers.api import create_order


@allure.title('Проверить создание заказа')
class TestCreateOrder:

    @allure.title('Проверить, что можно создать заказ с авторизацией и ингредиентами — код 200')
    def test_create_order_with_auth_and_ingredients_returns_200(self, user_token):
        token = user_token['token']

        ingredients = ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa75']  # валидные ID

        with allure.step('Отправить запрос на создание заказа с авторизацией'):
            response = create_order(token, ingredients)

        with allure.step('Проверить статус код 200 и тело'):
            assert response.status_code == 200
            assert 'number' in response.json()['order']

    @allure.title('Проверить, что можно создать заказ без авторизации с ингредиентами — код 200')
    def test_create_order_without_auth_returns_200(self):
        ingredients = ['61c0c5a71d1f82001bdaaa6d', '61c0c5a71d1f82001bdaaa75']

        with allure.step('Отправить запрос заказа без токена с ингредиентами'):
            response = create_order(token=None, ingredients=ingredients)

        with allure.step('Проверить статус код 200 и тело'):
            assert response.status_code == 200
            assert 'number' in response.json()['order']

    @allure.title('Проверить, что нельзя создать заказ без ингредиентов — код 400')
    def test_create_order_without_ingredients_returns_400(self):
        with allure.step('Отправить пустой список ингредиентов'):
            response = create_order(token=None, ingredients=[])

        with allure.step('Проверить ошибку, статус код 400, и сообщение Ingredient ids must be provided'):
            assert response.status_code == 400
            assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Проверить, что нельзя создать заказ с неверным хешем ингредиентов — код 500')
    def test_create_order_with_invalid_ingredient_returns_500(self):
        invalid_ingredients = ['1', '2']

        with allure.step('Отправить запрос с невалидными хешем ингредиентов'):
            response = create_order(token=None, ingredients=invalid_ingredients)

        with allure.step('Проверить ошибку, статус код 500, и сообщение Internal Server Error'):
            assert response.status_code == 500
            assert 'Internal Server Error' in response.text

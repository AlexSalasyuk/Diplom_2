import allure
from helpers.api import create_order
from helpers.messages import CREATE_ORDER_ERROR_NO_INGREDIENTS, CREATE_ORDER_ERROR_INVALID_HASH
from helpers.test_data import VALID_INGREDIENT_IDS, INVALID_HASH_INGREDIENT_IDS


@allure.title('Проверить создание заказа')
class TestCreateOrder:

    @allure.title('Проверить, что можно создать заказ с авторизацией и ингредиентами — код 200')
    def test_create_order_with_auth_and_ingredients_returns_200(self, user_token):
        token = user_token['token']

        with allure.step('Отправить запрос на создание заказа с авторизацией'):
            response = create_order(token, VALID_INGREDIENT_IDS)

        with allure.step('Проверить статус код 200 и тело'):
            assert response.status_code == 200
            assert 'number' in response.json()['order']

    @allure.title('Проверить, что можно создать заказ без авторизации с ингредиентами — код 200')
    def test_create_order_without_auth_returns_200(self):
        with allure.step('Отправить запрос заказа без токена с ингредиентами'):
            response = create_order(token=None, ingredients=VALID_INGREDIENT_IDS)

        with allure.step('Проверить статус код 200 и тело'):
            assert response.status_code == 200
            assert 'number' in response.json()['order']

    @allure.title('Проверить, что нельзя создать заказ без ингредиентов — код 400')
    def test_create_order_without_ingredients_returns_400(self):
        with allure.step('Отправить пустой список ингредиентов'):
            response = create_order(token=None, ingredients=[])

        with allure.step('Проверить ошибку, статус код 400, и сообщение Ingredient ids must be provided'):
            assert response.status_code == 400
            assert response.json()['message'] == CREATE_ORDER_ERROR_NO_INGREDIENTS

    @allure.title('Проверить, что нельзя создать заказ с неверным хешем ингредиентов — код 500')
    def test_create_order_with_invalid_ingredient_returns_500(self):
        with allure.step('Отправить запрос с невалидными хешем ингредиентов'):
            response = create_order(token=None, ingredients=INVALID_HASH_INGREDIENT_IDS)

        with allure.step('Проверить ошибку, статус код 500, и сообщение Internal Server Error'):
            assert response.status_code == 500
            assert CREATE_ORDER_ERROR_INVALID_HASH in response.text

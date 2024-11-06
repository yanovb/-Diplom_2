import allure
from actions import Actions
from errors import Errors
from ingredients_id import INGREDIENTS_ID
from routes import Routes


class TestOrder:
    @allure.title('Создание заказа авторизованным пользователем')
    @allure.description(
        'Проверка, что при создании заказа авторизованным пользователем все ингридиенты добавлены и в ответе код 200'
    )
    def test_create_order_with_auth_success(self, fixture):
        r = fixture['made_order']
        added_ingredients_id = list(map(lambda ingredient: ingredient['_id'], r.json()['order']['ingredients']))

        assert r.status_code == 200 and added_ingredients_id == fixture['ingredients']

    @allure.title('Создание заказа без авторизации')
    @allure.description(
        'Проверка, что при создании заказа без авторизации возвращается код 200, но ингридиенты не добавлены'
    )
    def test_create_order_without_auth(self):
        ingredients = Actions.get_random_ingredients(Routes.INGREDIENTS_ROUTE)
        r = Actions.create_order(Routes.ORDERS_ROUTE, ingredients)

        assert r.status_code == 200 and 'ingredients' not in r.json()['order']

    @allure.title('Создание заказа без ингридиентов')
    @allure.description(
        'Проверка, что при создания заказа без ингридиентов возвращается код 400 и сообщение об отсутствии ингридиетов'
    )
    def test_create_order_without_ingredients(self):
        ingredients = []
        r = Actions.create_order(Routes.ORDERS_ROUTE, ingredients)

        assert r.status_code == 400 and r.json()['message'] == Errors.NO_INGREDIENT

    @allure.title('Создание заказа c неправильными id ингридиентов')
    @allure.description(
        'Проверка, что при создания заказа c неправильными id ингридиентов возвращается код 400 и сообщение об ошибке'
    )
    def test_create_order_with_wrong_ingredients_id(self):
        ingredients = INGREDIENTS_ID
        r = Actions.create_order(Routes.ORDERS_ROUTE, ingredients)

        assert r.status_code == 400 and r.json()['message'] == Errors.WRONG_INGREDIENTS

    @allure.title('Получение списка заказов авторизованного пользователя')
    @allure.description('Проверка, что раннее сделанный заказ есть в списке заказов')
    def test_get_orders(self, fixture):
        order_id = fixture['made_order'].json()['order']['_id']
        token = fixture['authorized_user'].json()['accessToken']
        r = Actions.get_orders(Routes.ORDERS_ROUTE, token)

        assert r.status_code == 200 and r.json()['orders'][0]['_id'] == order_id

    @allure.title('Запрос списка заказов без авторизации')
    @allure.description(
        'Проверка, что при запросе списка заказов без авторизации возвращается "You should be authorised"'
    )
    def test_get_orders_without_auth(self):
        r = Actions.get_orders(Routes.ORDERS_ROUTE)

        assert r.status_code == 401 and r.json()['message'] == Errors.NO_AUTH

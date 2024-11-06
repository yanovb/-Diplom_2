import pytest
from actions import Actions
from routes import Routes
from users_data import UsersData


@pytest.fixture(scope='function')
def fixture():
    created_user = Actions.make_user(Routes.REGISTER_ROUTE, UsersData.NEW_USER)
    authorized_user = Actions.make_auth(Routes.LOGIN_ROUTE, UsersData.NEW_USER)
    token = authorized_user.json()['accessToken']
    ingredients = Actions.get_random_ingredients(Routes.INGREDIENTS_ROUTE)
    made_order = Actions.create_order(Routes.ORDERS_ROUTE, ingredients, token)
    result = {
        'created_user': created_user,
        'authorized_user': authorized_user,
        'made_order': made_order,
        'ingredients': ingredients
    }

    yield result

    token = authorized_user.json()['accessToken']
    r = Actions.delete_user(Routes.USER_ROUTE, token)
    assert r.status_code == 202 and r.json()['success'] is True

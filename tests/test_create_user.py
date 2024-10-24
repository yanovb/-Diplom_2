import allure
import pytest
from actions import Actions
from routes import Routes
from users_data import UsersData


class TestCreateUser:
    @allure.title('Проверка успешной регистрации')
    @allure.description(
        'Проверка, что при успешной регистрации нового пользователя возвращается статус 200 и "success": True'
    )
    def test_user_create_success(self, fixture):
        r = fixture['created_user']

        assert r.status_code == 200 and r.json()['success'] is True

    @allure.title('Попытка регистрации существующего пользователя')
    @allure.description(
        'Проверка, что при попытке регистрации существующего пользователя возвращается код 403 и "success": false'
    )
    def test_user_create_already_created(self):
        r = Actions.make_user(Routes.REGISTER_ROUTE, UsersData.OLD_USER)

        assert r.status_code == 403 and r.json()['success'] is False

    @allure.title('Попытка регистрации пользователя без параметра')
    @allure.description(
        'Проверка, что при попытке регистрации пользователя без параметра возвращается код 403 и "success": false'
    )
    @pytest.mark.parametrize('param', ['email', 'password', 'name'])
    def test_user_create_with_out_any_param(self, param):
        r = Actions.make_user_without_param(Routes.REGISTER_ROUTE, UsersData.OLD_USER, param)

        assert r.status_code == 403 and r.json()['success'] is False

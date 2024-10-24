import allure
from actions import Actions
from routes import Routes
from users_data import UsersData


class TestAuthUser:
    @allure.title('Проверка успешной авторизации')
    @allure.description('Проверка, что при успешной авторизации возвращается статус 200 и "success": True')
    def test_auth_user_success(self, fixture):
        r = fixture['authorized_user']

        assert r.status_code == 200 and r.json()['success'] is True

    @allure.title('Проверка авторизации с некорректыми кредами')
    @allure.description('Попытка авторизации несуществующим пользователем')
    def test_auth_with_wrong_accesses(self):
        r = Actions.make_auth(Routes.LOGIN_ROUTE, UsersData.WRONG_ACCESSES)

        assert r.status_code == 401 and r.json()['message'] == "email or password are incorrect"
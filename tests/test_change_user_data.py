import allure
from actions import Actions
from routes import Routes
from users_data import UsersData


class TestChangeUserData:
    @allure.title('Редактирование всех полей пользователя')
    @allure.description('Проверка, что все поля редактируются и в ответе статус 200 и "success": true')
    def test_change_user_data_with_auth(self, fixture):
        token = fixture['authorized_user'].json()['accessToken']
        r = Actions.change_user_data(Routes.USER_ROUTE, UsersData.NEW_USER_DATA, token)

        assert r.status_code == 200 and r.json()['success'] is True

    @allure.title('Попытка редактирование пользователя без авторизации')
    @allure.description(
        'Проверка, что при попытке отредактировать пользователя без авторизации возвращает статус 401 и "success": false'
    )
    def test_change_user_data_without_auth(self):
        r = Actions.change_user_data(Routes.USER_ROUTE, UsersData.NEW_USER_DATA)

        assert r.status_code == 401 and r.json()['success'] is False

import requests
from core.constants import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from utils.data_generator import DataGenerator
from api.api_manager import ApiManager
from api.auth_api import AuthAPI

class TestAuthAPI:
    def test_register_user(self, api_manager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_login_success(self, requester, registered_user):
        response = requester.send_request(
            method='POST',
            endpoint=LOGIN_ENDPOINT,
            data={
                "email": registered_user["email"],
                "password": registered_user["password"]
            },
            expected_status=200
        )
        response_data = response.json()
        assert 'user' in response_data
        assert response_data['user']["email"] == registered_user["email"], "Email не совпадает"
        assert "accessToken" in response_data, "accessToken пользователя отсутствует в ответе"
        assert "refreshToken" in response_data, "refreshToken пользователя отсутствует в ответе"
        assert "expiresIn" in response_data, "expiresIn пользователя отсутствует в ответе"


    def test_login_with_invalid_password(self, requester, registered_user):
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data={
                "email": registered_user["email"],
                "password": "invalid_password"
            },
            expected_status=401
        )
        data = response.json()
        assert "логин" in data['message'].lower(), "Сообщение об ошибке некорректно"
        assert "user" not in data
        assert "accessToken" not in data
        assert "refreshToken" not in data
        assert "expiresIn" not in data

    def test_login_with_nonexistent_email(self, requester):
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data={
                "email": "nonexistent@example.com",
                "password": "some_password"
            },
            expected_status=401
        )
        data = response.json()
        print(data)
        assert "логин" in data['message'].lower(), "Сообщение об ошибке некорректно"
        assert 'error' in data
        assert "user" not in data
        assert "accessToken" not in data
        assert "refreshToken" not in data
        assert "expiresIn" not in data

    def test_login_with_empty_body(self, requester):
        response = requester.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data={},
            expected_status=401
        )
        data = response.json()
        assert 'message' in data
        assert 'error' in data
        assert "user" not in data
        assert "accessToken" not in data
        assert "refreshToken" not in data
        assert "expiresIn" not in data




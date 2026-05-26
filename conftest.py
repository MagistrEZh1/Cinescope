from faker import Faker
import pytest
import requests

from api.api_manager import ApiManager
from core.constants import BASE_URL, MOVIES_BASE_URL, REGISTER_ENDPOINT, ADMIN_EMAIL, ADMIN_PASSWORD
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator

faker = Faker()

@pytest.fixture(scope="session")
def test_user():
    return DataGenerator.generate_user()

@pytest.fixture(scope="session")
def registered_user(requester, test_user):
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=[201, 409]  # принимаем оба статуса
    )
    registered_user = test_user.copy()
    if response.status_code == 201:
        registered_user["id"] = response.json()["id"]
    return registered_user

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session, MOVIES_BASE_URL)

@pytest.fixture(scope="session")
def authenticated_api_manager(api_manager):
    """
    Аутентифицированный ApiManager с админскими кредами.
    """
    api_manager.auth_api.authenticate((ADMIN_EMAIL, ADMIN_PASSWORD))
    return api_manager


@pytest.fixture
def created_movie(authenticated_api_manager):
    """
    Создаёт фильм перед тестом и удаляет после.
    """
    movie_data = DataGenerator.generate_movie()
    response = authenticated_api_manager.movies_api.create_movie(movie_data)
    movie = response.json()
    yield movie
    authenticated_api_manager.movies_api.delete_movie(movie["id"], expected_status=[200, 404])
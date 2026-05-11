from faker import Faker
import pytest
import requests

from api.api_manager import ApiManager
from core.constants import BASE_URL, REGISTER_ENDPOINT
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
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session, BASE_URL)
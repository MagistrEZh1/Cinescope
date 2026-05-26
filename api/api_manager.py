from api.auth_api import AuthAPI
from api.user_api import UserAPI
from api.movies_api import MoviesAPI


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session, base_url):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session, base_url)
        self.movies_api = MoviesAPI(session, base_url)


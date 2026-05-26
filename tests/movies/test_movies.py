import pytest
from utils.data_generator import DataGenerator


class TestMoviesAPI:

    def test_create_movie(self, authenticated_api_manager, created_movie):
        """Позитивный тест создания фильма"""
        assert "id" in created_movie
        assert "name" in created_movie
        assert "price" in created_movie

    def test_get_movie_by_id(self, authenticated_api_manager, created_movie):
        """Получение фильма по id"""
        movie_id = created_movie["id"]
        response = authenticated_api_manager.movies_api.get_movie_by_id(movie_id)
        data = response.json()
        assert data["id"] == movie_id
        assert data["name"] == created_movie["name"]
        assert data["price"] == created_movie["price"]

    def test_get_movies_filter_by_location(self, authenticated_api_manager, created_movie):
        """Проверка фильтрации по location"""
        location = created_movie["location"]
        movie_id = created_movie["id"]
        page = 1
        found = False

        while not found:
            response = authenticated_api_manager.movies_api.get_movies(
                params={"location": location, "pageSize": 20, "page": page},
                need_logging=False  # вот здесь
            )
            data = response.json()
            movies = data["movies"]
            if any(m["id"] == movie_id for m in movies):
                found = True
                break
            if page >= data["pageCount"]:
                break
            page += 1

        assert found, "Созданный фильм должен быть в результатах фильтрации"

    def test_patch_movie_price(self, authenticated_api_manager, created_movie):
        """Позитивный тест обновления цены фильма"""
        movie_id = created_movie["id"]
        response = authenticated_api_manager.movies_api.patch_movie(movie_id, {"price": 999})
        data = response.json()
        assert data["price"] == 999

    def test_delete_movie(self, authenticated_api_manager):
        """Позитивный тест удаления фильма"""
        movie_data = DataGenerator.generate_movie()
        movie = authenticated_api_manager.movies_api.create_movie(movie_data).json()
        movie_id = movie["id"]

        authenticated_api_manager.movies_api.delete_movie(movie_id)
        authenticated_api_manager.movies_api.get_movie_by_id(movie_id, expected_status=404)

    def test_create_movie_without_price(self, authenticated_api_manager):
        """Негативный тест - создание без цены"""
        movie_data = DataGenerator.generate_movie()
        del movie_data["price"]
        response = authenticated_api_manager.movies_api.create_movie(movie_data, expected_status=400)
        data = response.json()
        assert "price" in str(data["message"])

    def test_create_movie_with_invalid_genre(self, authenticated_api_manager):
        """Негативный тест - несуществующий жанр"""
        movie_data = DataGenerator.generate_movie(genre_id=99999999)
        response = authenticated_api_manager.movies_api.create_movie(movie_data, expected_status=400)
        data = response.json()
        assert "некоррект" in data["message"].lower()

    def test_create_movie_with_empty_body(self, authenticated_api_manager):
        """Негативный тест - пустое тело"""
        response = authenticated_api_manager.movies_api.create_movie({}, expected_status=400)
        data = response.json()
        assert "name" in str(data["message"])

    def test_patch_movie_invalid_price(self, authenticated_api_manager, created_movie):
        """Негативный тест - невалидная цена при обновлении"""
        movie_id = created_movie["id"]
        response = authenticated_api_manager.movies_api.patch_movie(
            movie_id, {"price": "сто"}, expected_status=400
        )
        data = response.json()
        assert "price" in str(data["message"])

    def test_get_nonexistent_movie(self, authenticated_api_manager):
        """Негативный тест - получение несуществующего фильма"""
        authenticated_api_manager.movies_api.get_movie_by_id(99999999, expected_status=404)
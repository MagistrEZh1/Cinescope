import requests

class TestBookings:
    BASE_URL = "https://restful-booker.herokuapp.com"
    HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
    }
    json = {
    "username": "admin",
    "password": "password123"
    }

    def get_token(self):
        response = requests.post(
            f"{self.BASE_URL}/auth",
            headers=self.HEADERS,
            json=self.json
        )
        assert response.status_code == 200, "Ошибка авторизации"
        token = response.json().get("token")
        assert token is not None, "В ответе не оказалось токена"
        return token

    def test_create_new_booking_put(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)

        # Получаем токен авторизации
        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        booking_data = {
            "firstname": "Ryan",
            "lastname": "Gosling",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }

        # Создаём бронирование
        create_booking = session.post(f"{self.BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == "Ryan", "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == 150000, "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == "Gosling", "Заданная фамилия не совпадает"

        new_booking_data = {
            "firstname": "Megan",
            "lastname": "Fox",
            "totalprice": 270000,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2024-02-18",
                "checkout": "2024-03-02"
            },
            "additionalneeds": "Gym"
        }

        create_new_booking = session.put(f"{self.BASE_URL}/booking/{booking_id}", json=new_booking_data)
        assert create_new_booking.status_code == 200, "Ошибка при создании брони"

        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["firstname"] == "Megan", "Заданное имя не совпадает"
        assert get_booking.json()["lastname"] == "Fox", "Заданная фамилия не совпадает"
        assert get_booking.json()["totalprice"] == 270000, "Заданная цена не совпадает"
        assert get_booking.json()["depositpaid"] == False, "Нужен депозит"
        assert get_booking.json()["bookingdates"]["checkin"] == "2024-02-18", "Дата заселения не совпадает"
        assert get_booking.json()["bookingdates"]["checkout"] == "2024-03-02", "Дата отъезда не совпадает"
        assert get_booking.json()["additionalneeds"] == "Gym", "Допы не нужны"

        print(get_booking.json())

        # Удаляем бронирование
        deleted_booking = session.delete(f"{self.BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"


    def test_change_booking_patch(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)

        # Получаем токен авторизации
        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        booking_data = {
            "firstname": "Ryan",
            "lastname": "Gosling",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }

        # Создаём бронирование
        create_booking = session.post(f"{self.BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == "Ryan", "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == 150000, "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == "Gosling", "Заданная фамилия не совпадает"

        change_booking_data = {
            "firstname": "Mathew",
            "lastname": "McConaughey"
        }

        print(change_booking_data)

        create_new_booking_patch = session.patch(f"{self.BASE_URL}/booking/{booking_id}", json=change_booking_data)
        assert create_new_booking_patch.status_code == 200, "Ошибка при создании брони"

        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["firstname"] == "Mathew", "Заданное имя не совпадает"
        assert get_booking.json()["lastname"] == "McConaughey", "Заданная фамилия не совпадает"

        data = get_booking.json()
        assert data["totalprice"] == 150000
        assert data["depositpaid"] == True
        assert data["bookingdates"]["checkin"] == "2024-04-05"
        assert data["bookingdates"]["checkout"] == "2024-04-08"
        assert data["additionalneeds"] == "Piano"

        print(data)

        # Удаляем бронирование
        deleted_booking = session.delete(f"{self.BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

    def test_negative_post(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)

        # Получаем токен авторизации
        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        booking_data = {
            "firstname": "Ryan",
            "lastname": "Gosling",
            "totalprice": 150000,
            "depositpaid": True,
            "additionalneeds": "Piano"
        }

        create_booking = session.post(f"{self.BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code <= 199 or create_booking.status_code >= 300, f"Бронь была создана с кодом {create_booking.status_code}, хотя должна была быть ошибка"

    def test_negative_get(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)

        # Получаем токен авторизации
        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        booking_id = 999999
        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "GET вернул успешный код, хотя бронь с таким ID не должна существовать"

    def test_negative_put(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)

        # Получаем токен авторизации
        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        booking_data = {
            "firstname": "Ryan",
            "lastname": "Gosling",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }

        # Создаём бронирование
        create_booking = session.post(f"{self.BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == "Ryan", "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == 150000, "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == "Gosling", "Заданная фамилия не совпадает"

        new_booking_data = {
            "firstname": "Megan",
            "lastname": "Fox",
            "totalprice": 270000,
            "bookingdates": {
                "checkin": "2024-02-18",
                "checkout": "2024-03-02"
            },
            "additionalneeds": "Gym"
        }

        create_new_booking = session.put(f"{self.BASE_URL}/booking/{booking_id}", json=new_booking_data)
        assert  400 <= create_new_booking.status_code < 500, "Должна быть ошибка от сервера, так как передали не все поля"

        deleted_booking = session.delete(f"{self.BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = session.get(f"{self.BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

    def test_negative_patch(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)

        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        # Создаём корректное бронирование
        booking_data = {
            "firstname": "Ryan",
            "lastname": "Gosling",
            "totalprice": 150000,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-04-05",
                "checkout": "2024-04-08"
            },
            "additionalneeds": "Piano"
        }
        create_booking = session.post(f"{self.BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None

        # Пытаемся передать поле, которого нет в API
        patch_data = {"has_pets": True}  # неизвестное поле
        patch_response = session.patch(f"{self.BASE_URL}/booking/{booking_id}", json=patch_data)

        # Проверяем, что сервер вернул 200 (так работает API)
        assert patch_response.status_code == 200

        # Проверяем, что неизвестное поле не появилось в ответе
        response_json = patch_response.json()
        assert "has_pets" not in response_json, "Сервер не должен добавлять неизвестные поля"

        # Удаляем бронирование
        deleted_booking = session.delete(f"{self.BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201

    def test_negative_delete(self):
        session = requests.Session()
        session.headers.update(self.HEADERS)

        # Получаем токен авторизации
        token = self.get_token()
        session.headers.update({"Cookie": f"token={token}"})

        fake_booking_id = 9999999

        # Удаляем бронирование
        deleted_booking = session.delete(f"{self.BASE_URL}/booking/{fake_booking_id}")
        assert deleted_booking.status_code == 405, "Сервер должен вернуть ошибку, так как некорректная авторизация"
        print(f"Ответ сервера: {deleted_booking.status_code} — {deleted_booking.text}")



















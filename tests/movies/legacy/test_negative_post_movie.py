import requests
from pyexpat.errors import messages

from api.auth_client import get_auth_token

def test_create_movie_without_price():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
        "name": "Название фильма",
        "imageUrl": "https://image.url",
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }

    response = requests.post(url=url, json=payload, headers=headers)
    assert response.status_code == 400

    data = response.json()
    assert "price" in data['message'][0], 'Иначе поле не является обязательным для передачи в запросе'
    print(data)

def test_create_movie_with_invalid_genreId():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
        "name": "Дракон",
        "imageUrl": "https://image.url",
        "price": 100,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 99999999
    }
    response = requests.post(url=url, json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    print(data)
    assert "некоррект" in data["message"].lower()

def test_create_movie_with_empty_body():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {}
    response = requests.post(url=url, json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    print(data)
    assert 'name' in data['message'][0]

def test_create_movie_with_string_price():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
        "name": "Дракон",
        "imageUrl": "https://image.url",
        "price": '100',
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 3
    }
    response = requests.post(url=url, json=payload, headers=headers)
    assert response.status_code == 400
    data = response.json()
    print(data)
    assert 'price' in str(data['message'])

import uuid
def test_create_movie_price_zero():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()

    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    payload = {
        "name": f"Фильм {uuid.uuid4()}",
        "imageUrl": "https://image.url",
        "price": 0,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 3
    }

    response = requests.post(url=url, json=payload, headers=headers)

    assert response.status_code == 400

    data = response.json()
    print(data)










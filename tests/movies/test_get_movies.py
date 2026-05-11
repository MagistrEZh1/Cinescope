import requests
from api.auth_client import get_auth_token
import uuid

def test_create_movie():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
        "name": f"Фильм {uuid.uuid4()}",
        "imageUrl": "https://image.url",
        "price": 100,
        "description": "Описание фильма",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }
    response = requests.post(url=url,json=payload,headers=headers)
    assert response.status_code == 201, 'Сервер должен подтвердить создание ресурса статусом кодом 201'

    data = response.json()
    print(data)
    assert 'id' in data, 'Некорректный запрос на сервер, т.к. id не создался'
    assert data["name"] == payload["name"], 'Данные не совпадают'
    assert data["imageUrl"] == payload["imageUrl"], 'Данные не совпадают'
    assert data["price"] == payload["price"], 'Данные не совпадают'
    assert data["description"] == payload["description"], 'Данные не совпадают'
    assert data["location"] == payload["location"], 'Данные не совпадают'
    assert data["published"] == payload["published"], 'Данные не совпадают'
    assert data["genreId"] == payload["genreId"], 'Данные не совпадают'

    movie_id = data["id"] #Сохраняем id созданного фильма для дальнейших проверок
    get_url = url + '/' + str(movie_id)  # Формируем URL для получения фильма по id

    get_response = requests.get(url=get_url,headers=headers)
    assert get_response.status_code == 200, 'Ошибка, фильм не создался'
    data = get_response.json()
    assert data["name"] == payload["name"], 'Данные не совпадают'
    assert data["imageUrl"] == payload["imageUrl"], 'Данные не совпадают'
    assert data["price"] == payload["price"], 'Данные не совпадают'
    assert data["description"] == payload["description"], 'Данные не совпадают'
    assert data["location"] == payload["location"], 'Данные не совпадают'
    assert data["published"] == payload["published"], 'Данные не совпадают'
    assert data["genreId"] == payload["genreId"], 'Данные не совпадают'

    response_delete = requests.delete(url=get_url, headers=headers)
    assert response_delete.status_code == 200, 'Фильм не удалился, еще валяется в базе'

    response_get = requests.get(url=get_url, headers=headers)
    assert response_get.status_code == 404, 'Фильм все еще в базе, а должен был быть удален'
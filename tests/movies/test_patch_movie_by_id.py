import requests
from api.auth_client import get_auth_token
import uuid

def test_patch_movie_price():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
        "name": f"Фильм {uuid.uuid4()}",
        "imageUrl": "https://image.url",
        "price": 100,
        "description": "Про девочку",
        "location": "SPB",
        "published": True,
        "genreId": 3
    }
    post_response = requests.post(url=url, json=payload, headers=headers)
    assert post_response.status_code == 201

    data = post_response.json()
    movie_id = data['id']
    patch_url = url + "/" + str(movie_id)
    patch_payload = {
        "price": 150,
    }
    patch_response = requests.patch(url=patch_url, json=patch_payload, headers=headers)
    assert patch_response.status_code == 200

    get_response = requests.get(url=patch_url, headers=headers)
    assert get_response.status_code == 200
    data = get_response.json()
    assert data['price'] == 150

    delete_response = requests.delete(url=patch_url, headers=headers)
    assert delete_response.status_code == 200, 'Фильм не удалился, еще валяется в базе'

    response_get = requests.get(url=patch_url, headers=headers)
    assert response_get.status_code == 404

def test_patch_movie_invalid_price():
    url = "https://api.dev-cinescope.coconutqa.ru/movies"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
        "name": f"Фильм {uuid.uuid4()}",
        "imageUrl": "https://image.url",
        "price": 300,
        "description": "Про девочку",
        "location": "SPB",
        "published": True,
        "genreId": 2
    }
    post_response = requests.post(url=url, json=payload, headers=headers)
    assert post_response.status_code == 201
    data = post_response.json()
    # print(data)

    movie_id = data['id']
    patch_url = url + "/" + str(movie_id)
    patch_payload = {
        "price": 'триста',
    }
    patch_response = requests.patch(url=patch_url, json=patch_payload, headers=headers)
    assert patch_response.status_code == 400
    patch_data = patch_response.json()
    print(patch_data)
    assert 'price' in str(patch_data['message'])

    get_response = requests.get(url=patch_url, headers=headers)
    assert get_response.status_code == 200
    data = get_response.json()
    # print(data)
    assert data['price'] == 300

    delete_response = requests.delete(url=patch_url, headers=headers)
    assert delete_response.status_code == 200

    response_get = requests.get(url=patch_url, headers=headers)
    assert response_get.status_code == 404










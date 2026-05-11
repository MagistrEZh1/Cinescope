import requests
from api.auth_client import get_auth_token
import uuid

def test_delete_review_by_movie_id():
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
    new_movie_response = requests.post(url=url, json=payload, headers=headers)
    assert new_movie_response.status_code == 201
    new_movie_data = new_movie_response.json()
    print(new_movie_data)
    movie_id = new_movie_data['id']
    reviews_url = f'{url}/{movie_id}/reviews'

    review_payload = {
    "rating": 7,
    "text": "Нормальный отзыв"
    }
    post_review_response = requests.post(url=reviews_url, json=review_payload, headers=headers)
    assert post_review_response.status_code == 201

    get_review_response = requests.get(url=reviews_url)
    assert get_review_response.status_code == 200
    reviews_data = get_review_response.json()
    assert isinstance(reviews_data, list)
    assert len(reviews_data) > 0

    delete_review_response = requests.delete(url=reviews_url, headers=headers)
    assert delete_review_response.status_code == 200

    get_deleted_review_response = requests.get(url=reviews_url)
    assert get_deleted_review_response.status_code == 200

    deleted_reviews_data = get_deleted_review_response.json()
    assert isinstance(deleted_reviews_data, list)
    assert len(deleted_reviews_data) == 0

    movie_id_url = f'{url}/{movie_id}'
    delete_movie_response = requests.delete(url=movie_id_url, headers=headers)
    assert delete_movie_response.status_code == 200

    get_deleted_id_movie_response = requests.get(url=movie_id_url)
    assert get_deleted_id_movie_response.status_code == 404










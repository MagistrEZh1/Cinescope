import requests
from api.auth_client import get_auth_token
import uuid

def test_hide_review_by_movie_id():
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
        "rating": 10,
        "text": "Наилучшее кино!"
    }
    post_review_response = requests.post(url=reviews_url, json=review_payload, headers=headers)
    assert post_review_response.status_code == 201

    get_reviews_response = requests.get(url=reviews_url)
    assert get_reviews_response.status_code == 200
    get_reviews_response_data = get_reviews_response.json()
    print(get_reviews_response_data)


import requests
from api.auth_client import get_auth_token
import uuid

def test_update_review_by_movie_id():
    movie_url = "https://api.dev-cinescope.coconutqa.ru/movies"
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
    post_movie_response = requests.post(url=movie_url, json=payload, headers=headers)
    assert post_movie_response.status_code == 201
    data_movie = post_movie_response.json()
    print(data_movie)
    movie_id = data_movie['id']
    reviews_url = f"{movie_url}/{movie_id}/reviews"

    review_payload = {
        "rating": 8,
        "text": "Очень хорошее кино"
    }
    review_response = requests.post(url=reviews_url, json=review_payload, headers=headers)
    assert review_response.status_code == 201
    data_review = review_response.json()
    print(data_review)

    change_review_payload = {
        "rating": 3,
        "text": "Неудачное кино"
    }
    change_review_response = requests.put(url=reviews_url, json=change_review_payload, headers=headers)
    assert change_review_response.status_code == 200
    data_change_review = change_review_response.json()
    print(data_change_review)
    assert change_review_payload['rating'] == data_change_review['rating']
    assert change_review_payload['text'] == data_change_review['text']

    get_change_reviews = requests.get(url=reviews_url, headers=headers)
    assert get_change_reviews.status_code == 200
    data_get_change_review = get_change_reviews.json()
    print(data_get_change_review)
    assert isinstance(data_get_change_review, list)
    assert len(data_get_change_review) > 0
    review = data_get_change_review[0]
    assert review['rating'] == change_review_payload['rating']
    assert review['text'] == change_review_payload['text']

    movie_id_url = f"{movie_url}/{movie_id}"
    delete_movie_response = requests.delete(url=movie_id_url, headers=headers)
    assert delete_movie_response.status_code == 200
    get_after_delete_movie = requests.get(url=movie_id_url)
    assert get_after_delete_movie.status_code == 404



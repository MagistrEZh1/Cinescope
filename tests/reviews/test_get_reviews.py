import requests
from api.auth_client import get_auth_token
import uuid

def test_create_review_and_get_reviews_by_movie_id():
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
    post_movie_response = requests.post(url = movie_url, json = payload, headers=headers)
    assert post_movie_response.status_code == 201
    data_movie = post_movie_response.json()
    print(data_movie)
    movie_id = data_movie['id']
    reviews_url = f"{movie_url}/{movie_id}/reviews"
    get_review_response = requests.get(url = reviews_url)
    assert get_review_response.status_code == 200
    data_review = get_review_response.json()
    print(data_review)
    assert len(data_review) == 0
    assert isinstance(data_review, list)

    review_payload = {
        "rating": 9,
        "text": "Очень хорошее кино"
    }
    post_review_response = requests.post(url=reviews_url, json=review_payload, headers=headers)
    assert post_review_response.status_code == 201
    data_post_review = post_review_response.json()
    print(data_post_review)

    get_reviews_after_post_response = requests.get(url=reviews_url)
    assert get_reviews_after_post_response.status_code == 200
    reviews_after_post_data = get_reviews_after_post_response.json()
    print(reviews_after_post_data)
    assert len(reviews_after_post_data) > 0
    assert isinstance(reviews_after_post_data, list)
    review = reviews_after_post_data[0]
    assert review['rating'] == review_payload['rating']
    assert review['text'] == review_payload['text']

    movie_id_url = f"{movie_url}/{movie_id}"
    delete_movie_response = requests.delete(url=movie_id_url, headers=headers)
    assert delete_movie_response.status_code == 200
    get_after_delete_movie = requests.get(url=movie_id_url)
    assert get_after_delete_movie.status_code == 404











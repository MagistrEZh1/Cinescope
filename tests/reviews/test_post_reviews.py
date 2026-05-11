import requests
from api.auth_client import get_auth_token
import uuid

def test_create_review_with_invalid_rating():
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
        "rating": 'пять',
        "text": "Очень хорошее кино"
    }
    post_review_response = requests.post(url=reviews_url, json=review_payload, headers=headers)
    assert post_review_response.status_code == 400
    error_data = post_review_response.json()
    print(error_data)
    assert 'rating' in str(error_data['message'])

    get_reviews_response = requests.get(url=reviews_url)
    assert get_reviews_response.status_code == 200
    reviews_data = get_reviews_response.json()
    print(reviews_data)
    assert isinstance(reviews_data, list)
    assert len(reviews_data) == 0

    movie_id_url = f"{movie_url}/{movie_id}"
    delete_movie_response = requests.delete(url=movie_id_url, headers=headers)
    assert delete_movie_response.status_code == 200
    get_after_delete_movie = requests.get(url=movie_id_url)
    assert get_after_delete_movie.status_code == 404



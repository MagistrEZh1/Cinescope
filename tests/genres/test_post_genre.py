import requests
from api.auth_client import get_auth_token
import uuid

def test_create_and_delete_genre():
    url = "https://api.dev-cinescope.coconutqa.ru/genres"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
        'name': f'Жанр {uuid.uuid4()}'
    }
    create_genre_response = requests.post(url=url, json=payload, headers=headers)
    assert create_genre_response.status_code == 201
    create_genre_data = create_genre_response.json()
    # print(create_genre_id_data)
    assert 'id' in create_genre_data
    assert payload['name'] == create_genre_data['name']

    genre_id = create_genre_data['id']
    get_genre_id_url = f'{url}/{genre_id}'
    delete_genre_response = requests.delete(url=get_genre_id_url, headers=headers)
    assert delete_genre_response.status_code == 200

    get_deleted_response = requests.get(url=get_genre_id_url, headers=headers)
    assert get_deleted_response.status_code == 404

def test_create_genre_with_empty_body():
    url = "https://api.dev-cinescope.coconutqa.ru/genres"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    payload = {
    }
    negative_response = requests.post(url=url, json=payload, headers=headers)
    assert negative_response.status_code == 400
    negative_data = negative_response.json()
    print(negative_data)
    assert 'message' in negative_data
    assert 'name' in str(negative_data['message'])

# def test_create_genre_with_empty_name():
#     url = "https://api.dev-cinescope.coconutqa.ru/genres"
#     TOKEN = get_auth_token()
#     headers = {
#         "Authorization": f"Bearer {TOKEN}"
#     }
#     payload = {
#         'name': ''
#     }
#     empty_name_response = requests.post(url=url, json=payload, headers=headers)
#     assert empty_name_response.status_code == 201
#     empty_name_data = empty_name_response.json()
#     print(empty_name_data)



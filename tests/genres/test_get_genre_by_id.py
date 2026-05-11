import requests

def test_get_genre_by_id():
    url = "https://api.dev-cinescope.coconutqa.ru/genres"
    response = requests.get(url=url)
    assert response.status_code == 200
    data = response.json()
    get_id = data[0]['id']
    get_id_url = f'{url}/{get_id}'
    get_id_response = requests.get(url=get_id_url)
    assert get_id_response.status_code == 200
    get_id_data = get_id_response.json()
    print(get_id_data)
    assert get_id_data['id'] == get_id
    assert 'name' in get_id_data

def test_get_genre_with_invalid_id():
    url = "https://api.dev-cinescope.coconutqa.ru/genres/9999"
    response = requests.get(url=url)
    print(response.json())
    assert response.status_code == 404

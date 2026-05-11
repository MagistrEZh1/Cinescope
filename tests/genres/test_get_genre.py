import requests

def test_get_genres():
    url = "https://api.dev-cinescope.coconutqa.ru/genres"
    response = requests.get(url=url)
    assert response.status_code == 200
    get_data = response.json()
    print(get_data)
    assert isinstance(get_data, list)
    assert get_data
    assert 'id' in get_data[0]
    assert 'name' in get_data[0]
import requests
from api.auth_client import get_auth_token

def test_delete_genre_by_id():
    url = "https://api.dev-cinescope.coconutqa.ru/genres/99999999"
    TOKEN = get_auth_token()
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }
    delete_response = requests.delete(url=url, headers=headers)
    assert delete_response.status_code == 404
    delete_data = delete_response.json()
    print(delete_data)
    assert 'message' in delete_data
    assert 'Жанр не найден' in str(delete_data['message'])

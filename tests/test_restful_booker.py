import pytest
from core.constants import BASE_URL


class TestBookings:

    # ---------- POSITIVE ----------

    def test_create_booking(self, auth_session, booking_data):
        response = auth_session.post(
            f"{BASE_URL}/booking",
            json=booking_data
        )

        assert response.status_code == 200

        data = response.json()
        booking_id = data.get("bookingid")

        assert booking_id, "bookingid не найден в ответе"
        assert data["booking"] == booking_data

        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_get_booking(self, auth_session, booking_data):
        create_resp = auth_session.post(
            f"{BASE_URL}/booking",
            json=booking_data
        )

        booking_id = create_resp.json()["bookingid"]

        get_resp = auth_session.get(
            f"{BASE_URL}/booking/{booking_id}"
        )

        assert get_resp.status_code == 200
        assert get_resp.json() == booking_data

        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_update_booking_put(self, auth_session, booking_data):
        create_resp = auth_session.post(
            f"{BASE_URL}/booking",
            json=booking_data
        )
        booking_id = create_resp.json()["bookingid"]

        new_data = {
            "firstname": "Megan",
            "lastname": "Fox",
            "totalprice": 270000,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-02-18",
                "checkout": "2026-03-02"
            },
            "additionalneeds": "Gym"
        }

        update_resp = auth_session.put(
            f"{BASE_URL}/booking/{booking_id}",
            json=new_data
        )

        assert update_resp.status_code == 200

        get_resp = auth_session.get(
            f"{BASE_URL}/booking/{booking_id}"
        )

        assert get_resp.json() == new_data

        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_change_booking_patch(self, auth_session, booking_data):
        create_resp = auth_session.post(
            f"{BASE_URL}/booking",
            json=booking_data
        )
        booking_id = create_resp.json()["bookingid"]

        patch_data = {
            "firstname": "Mathew",
            "lastname": "McConaughey"
        }

        patch_resp = auth_session.patch(
            f"{BASE_URL}/booking/{booking_id}",
            json=patch_data
        )

        assert patch_resp.status_code == 200

        get_resp = auth_session.get(
            f"{BASE_URL}/booking/{booking_id}"
        )

        data = get_resp.json()

        assert data["firstname"] == "Mathew"
        assert data["lastname"] == "McConaughey"

        for key in ["totalprice", "depositpaid", "bookingdates", "additionalneeds"]:
            assert data[key] == booking_data[key]

        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

    def test_delete_booking(self, auth_session, booking_data):
        create_resp = auth_session.post(
            f"{BASE_URL}/booking",
            json=booking_data
        )
        booking_id = create_resp.json()["bookingid"]

        delete_resp = auth_session.delete(
            f"{BASE_URL}/booking/{booking_id}"
        )

        assert delete_resp.status_code == 201

        get_resp = auth_session.get(
            f"{BASE_URL}/booking/{booking_id}"
        )

        assert get_resp.status_code == 404

    # ---------- NEGATIVE ----------

    def test_negative_create_booking(self, auth_session):
        invalid_data = {
            "firstname": "Bad",
            "lastname": "Data"
        }

        response = auth_session.post(
            f"{BASE_URL}/booking",
            json=invalid_data
        )

        assert response.status_code >= 400

    @pytest.mark.parametrize("booking_id", [0, -1, 9999999])
    def test_negative_get_booking(self, auth_session, booking_id):
        response = auth_session.get(
            f"{BASE_URL}/booking/{booking_id}"
        )

        assert response.status_code == 404

    def test_negative_update_booking_put(self, auth_session, booking_data):
        create_resp = auth_session.post(
            f"{BASE_URL}/booking",
            json=booking_data
        )
        booking_id = create_resp.json()["bookingid"]

        invalid_data = {
            "firstname": "OnlyName"
        }

        response = auth_session.put(
            f"{BASE_URL}/booking/{booking_id}",
            json=invalid_data
        )

        assert response.status_code >= 400

        auth_session.delete(f"{BASE_URL}/booking/{booking_id}")

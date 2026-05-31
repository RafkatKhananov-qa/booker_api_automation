import allure

from api.auth_api import create_token
from api.booking_api import create_booking, delete_booking, get_booking
from utils.assertions import assert_status_code, assert_field_in_response_message


@allure.feature("Delete Booking")
class TestDeleteBooking:
    @allure.story("Успешное удаление брони")
    @allure.title("Удаление брони и проверка недоступности")
    def test_del_001_002(self, request_context, api_headers, api_headers_with_cookie):
        r = create_token(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = delete_booking(request_context, booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 201)

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 404)

    @allure.story("Негативные сценарии удаления брони")
    @allure.title("Удаление несуществующей брони")
    def test_del_003(self, request_context, api_headers, api_headers_with_cookie):
        r = create_token(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = delete_booking(request_context, 4575765756, headers=api_headers_with_cookie(token))
        assert_status_code(r, 405)

    @allure.story("Негативные сценарии удаления брони")
    @allure.title("Удаление брони без токена")
    def test_del_004(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = delete_booking(request_context, booking_id, headers=api_headers)
        assert_status_code(r, 403)

    @allure.story("Негативные сценарии удаления брони")
    @allure.title("Удаление брони с неверным токеном")
    def test_del_005(self, request_context, api_headers, api_headers_with_cookie):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = delete_booking(request_context, booking_id, headers=api_headers_with_cookie("87987fgfdgfdg"))
        assert_status_code(r, 403)

    @allure.story("Негативные сценарии удаления брони")
    @allure.title("Повторное удаление уже удалённой брони")
    def test_del_006(self, request_context, api_headers, api_headers_with_cookie):
        r = create_token(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = delete_booking(request_context, booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 201)

        r = delete_booking(request_context, booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 405)

    @allure.story("Успешное удаление брони")
    @allure.title("Проверка тела ответа при удалении брони")
    def test_del_007(self, request_context, api_headers, api_headers_with_cookie):
        r = create_token(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = delete_booking(request_context, booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 201)
        assert r.text() == "Created"

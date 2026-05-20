import allure

from api.auth_api import create_token
from api.booking_api import create_booking, update_booking, patch_booking
from data.payloads import (BOOKING_EMPTY_FIRSTNAME_PAYLOAD, UPDATED_BOOKING_PAYLOAD,
                           UPDATED_FIRSTNAME_BOOKING_PAYLOAD, UPDATED_PRICE_BOOKING_PAYLOAD,
                           UPDATED_DEPOSITPAID_BOOKING_PAYLOAD)
from data.schemas import BOOKING_SCHEMA
from utils.assertions import (assert_status_code,
                              assert_field_in_response_message, assert_response_fields)
from jsonschema import validate


@allure.feature("Update Booking")
class TestUpdateBooking:
    @allure.story("Успешное обновление брони")
    @allure.title("Полное обновление брони (PUT) с токеном")
    def test_put_001(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 200)
        response_data = r.json()

        assert_response_fields(
            response_data,
            UPDATED_BOOKING_PAYLOAD
        )

    @allure.story("Успешное обновление брони")
    @allure.title("Частичное обновление брони (PATCH) с токеном")
    def test_put_002(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = patch_booking(booking_id, headers=api_headers_with_cookie(token),
                          payload={"firstname": "Jackson"})
        assert_status_code(r, 200)
        response_data = r.json()

        assert_response_fields(
            response_data,
            UPDATED_FIRSTNAME_BOOKING_PAYLOAD
        )

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление несуществующей брони")
    def test_put_003(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = update_booking(999999, headers=api_headers_with_cookie(token))
        assert_status_code(r, 405)

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление без токена")
    def test_put_004(self, api_headers):
        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(booking_id, headers=api_headers)
        assert_status_code(r, 403)

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление с неверным токеном")
    def test_put_005(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(booking_id, headers=api_headers_with_cookie("56d620e8836e02b1"))
        assert_status_code(r, 403)

    @allure.story("Негативные сценарии обновления брони")
    @allure.title("Обновление с невалидными данными")
    def test_put_006(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(booking_id, headers=api_headers_with_cookie(token),
                           payload=BOOKING_EMPTY_FIRSTNAME_PAYLOAD)
        assert_status_code(r, 200)
        response_data = r.json()

        assert_response_fields(
            response_data,
            BOOKING_EMPTY_FIRSTNAME_PAYLOAD
        )

    @allure.story("Успешное обновление брони")
    @allure.title("Обновление с изменением дат")
    def test_put_007(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 200)
        response_data = r.json()

        assert_response_fields(
            response_data,
            UPDATED_BOOKING_PAYLOAD
        )

    @allure.story("Успешное обновление брони")
    @allure.title("Валидация схемы после обновления")
    def test_put_008(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = update_booking(booking_id, headers=api_headers_with_cookie(token))
        assert_status_code(r, 200)
        response_data = r.json()

        assert_response_fields(
            response_data,
            UPDATED_BOOKING_PAYLOAD
        )

        validate(instance=r.json(), schema=BOOKING_SCHEMA)

    @allure.story("Успешное обновление брони")
    @allure.title("PATCH: обновление только totalprice")
    def test_patch_001(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = patch_booking(booking_id, headers=api_headers_with_cookie(token),
                          payload={"totalprice": 500})
        assert_status_code(r, 200)
        response_data = r.json()

        assert_response_fields(
            response_data,
            UPDATED_PRICE_BOOKING_PAYLOAD
        )

    @allure.story("Успешное обновление брони")
    @allure.title("PATCH: обновление только depositpaid")
    def test_patch_002(self, api_headers, api_headers_with_cookie):
        r = create_token(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "token")
        token = r.json()["token"]

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = patch_booking(booking_id, headers=api_headers_with_cookie(token),
                          payload={"depositpaid": False})
        assert_status_code(r, 200)
        response_data = r.json()

        assert_response_fields(
            response_data,
            UPDATED_DEPOSITPAID_BOOKING_PAYLOAD
        )

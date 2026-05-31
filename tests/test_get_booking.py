import allure

from api.booking_api import get_bookings, get_booking, create_booking
from data.schemas import BOOKING_SCHEMA, BOOKINGS_LIST_SCHEMA
from utils.assertions import (assert_status_code, assert_array_not_empty,
                              assert_headers_in_response,
                              assert_field_in_response_message)
from jsonschema import validate


@allure.feature("Get Booking")
class TestGetBooking:
    @allure.story("Получение списка броней")
    @allure.title("Получение всех броней")
    def test_get_001(self, request_context):
        r = get_bookings(request_context)
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Фильтрация списка броней")
    @allure.title("Фильтрация по firstname")
    def test_get_002(self, request_context):
        r = get_bookings(request_context, firstname="John")
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Фильтрация списка броней")
    @allure.title("Фильтрация по lastname")
    def test_get_003(self, request_context):
        r = get_bookings(request_context, lastname="Doe")
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Фильтрация списка броней")
    @allure.title("Фильтрация по датам (checkin/checkout)")
    def test_get_004(self, request_context, api_headers):
        r = create_booking(request_context, api_headers, checkin="2026-04-01", checkout="2026-04-30")
        assert_status_code(r, 200)

        r = get_bookings(request_context, checkin="2026-04-01", checkout="2026-04-30")
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Получение брони по ID")
    @allure.title("Получение существующей брони по ID")
    def test_get_005(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)

        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        validate(instance=r.json(), schema=BOOKING_SCHEMA)

    @allure.story("Получение брони по ID")
    @allure.title("Получение несуществующей брони по ID")
    def test_get_006(self, request_context):
        r = get_booking(request_context, 45434545)
        assert_status_code(r, 404)

    @allure.story("Получение списка броней")
    @allure.title("Валидация схемы ответа списка броней")
    def test_get_007(self, request_context):
        r = get_bookings(request_context)
        assert_status_code(r, 200)
        assert_array_not_empty(r)
        validate(instance=r.json(), schema=BOOKINGS_LIST_SCHEMA)

    @allure.story("Получение брони по ID")
    @allure.title("Валидация схемы ответа одной брони")
    def test_get_008(self, request_context, api_headers):
        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)
        validate(instance=r.json(), schema=BOOKING_SCHEMA)

    @allure.story("Получение списка броней")
    @allure.title("Проверка заголовков ответа")
    def test_get_009(self, request_context, api_headers):
        r = get_bookings(request_context)
        assert_headers_in_response(r)

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_headers_in_response(r)

    @allure.story("Получение списка броней")
    @allure.title("Проверка времени ответа")
    def test_get_010(self, request_context, api_headers):
        r = get_bookings(request_context)
        assert_status_code(r, 200)

        r = create_booking(request_context, headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(request_context, booking_id)
        assert_status_code(r, 200)

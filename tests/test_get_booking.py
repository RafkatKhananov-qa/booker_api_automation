import allure

from api.booking_api import get_bookings, get_booking, create_booking
from data.schemas import BOOKING_SCHEMA, BOOKINGS_LIST_SCHEMA
from utils.assertions import (assert_status_code, assert_array_not_empty,
                              assert_headers_in_response, assert_response_time,
                              assert_field_in_response_message)
from jsonschema import validate


@allure.feature("Get Booking")
class TestGetBooking:
    @allure.story("Получение списка броней")
    @allure.title("Получение всех броней")
    def test_get_001(self):
        r = get_bookings()
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Фильтрация списка броней")
    @allure.title("Фильтрация по firstname")
    def test_get_002(self):
        r = get_bookings(firstname="John")
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Фильтрация списка броней")
    @allure.title("Фильтрация по lastname")
    def test_get_003(self):
        r = get_bookings(lastname="Doe")
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Фильтрация списка броней")
    @allure.title("Фильтрация по датам (checkin/checkout)")
    def test_get_004(self, api_headers):
        r = create_booking(api_headers, checkin="2026-04-01", checkout="2026-04-30")
        assert_status_code(r, 200)

        r = get_bookings(checkin="2026-04-01", checkout="2026-04-30")
        assert_status_code(r, 200)
        assert_array_not_empty(r)

    @allure.story("Получение брони по ID")
    @allure.title("Получение существующей брони по ID")
    def test_get_005(self, api_headers):
        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)

        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(booking_id)
        assert_status_code(r, 200)
        validate(instance=r.json(), schema=BOOKING_SCHEMA)

    @allure.story("Получение брони по ID")
    @allure.title("Получение несуществующей брони по ID")
    def test_get_006(self):
        r = get_booking(45434545)
        assert_status_code(r, 404)

    @allure.story("Получение списка броней")
    @allure.title("Валидация схемы ответа списка броней")
    def test_get_007(self):
        r = get_bookings()
        assert_status_code(r, 200)
        assert_array_not_empty(r)
        validate(instance=r.json(), schema=BOOKINGS_LIST_SCHEMA)

    @allure.story("Получение брони по ID")
    @allure.title("Валидация схемы ответа одной брони")
    def test_get_008(self, api_headers):
        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(booking_id)
        assert_status_code(r, 200)
        validate(instance=r.json(), schema=BOOKING_SCHEMA)

    @allure.story("Получение списка броней")
    @allure.title("Проверка заголовков ответа")
    def test_get_009(self, api_headers):
        r = get_bookings()
        assert_headers_in_response(r)

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(booking_id)
        assert_headers_in_response(r)

    @allure.story("Получение списка броней")
    @allure.title("Проверка времени ответа")
    def test_get_010(self, api_headers):
        r = get_bookings()
        assert_response_time(r, 2.0)

        r = create_booking(headers=api_headers)
        assert_status_code(r, 200)
        assert_field_in_response_message(r, "bookingid")
        booking_id = r.json()["bookingid"]

        r = get_booking(booking_id)
        assert_response_time(r, 2.0)

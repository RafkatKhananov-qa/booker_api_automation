from api.auth_api import create_token
from api.booking_api import create_booking, get_booking, update_booking
from utils.assertions import (assert_status_code, assert_field_in_response_message,
                              assert_response_message,
                              assert_field_not_in_response_message,
                              assert_field_value_type)


def test_auth_001(api_headers):
    r = create_token(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "token")


def test_auth_002(api_headers):
    r = create_token(headers=api_headers, password="wrongpass")
    assert_status_code(r, 200)
    assert_response_message(r, "reason", "Bad credentials")
    assert_field_not_in_response_message(r, "token")


def test_auth_003(api_headers):
    r = create_token(headers=api_headers, username="fakeuser")
    assert_status_code(r, 200)
    assert_response_message(r, "reason", "Bad credentials")
    assert_field_not_in_response_message(r, "token")


def test_auth_004(api_headers, api_headers_with_cookie):
    r = create_token(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "token")
    token = r.json()["token"]

    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "bookingid")
    booking_id = r.json()["bookingid"]

    r = get_booking(booking_id)
    assert_status_code(r, 200)
    assert_response_message(r, "firstname", "John")

    r = update_booking(booking_id, headers=api_headers_with_cookie(token))
    assert_status_code(r, 200)
    assert_response_message(r, "firstname", "Dannie")

    r = get_booking(booking_id)
    assert_status_code(r, 200)
    assert_response_message(r, "firstname", "Dannie")


def test_auth_005(api_headers, api_headers_with_cookie):
    r = create_token(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "token")

    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "bookingid")
    booking_id = r.json()["bookingid"]

    r = get_booking(booking_id)
    assert_status_code(r, 200)
    assert_response_message(r, "firstname", "John")

    r = update_booking(booking_id, headers=api_headers_with_cookie("45547"))
    assert_status_code(r, 403)


def test_auth_006(api_headers):
    r = create_token(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "token")

    r = create_booking(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "bookingid")
    booking_id = r.json()["bookingid"]

    r = get_booking(booking_id)
    assert_status_code(r, 200)
    assert_response_message(r, "firstname", "John")

    r = update_booking(booking_id, headers=api_headers)
    assert_status_code(r, 403)


def test_auth_007(api_headers):
    r = create_token(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "token")
    assert_field_value_type(r, "token", str)


def test_auth_008(api_headers):
    r = create_token(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "token")
    assert_field_value_type(r, "token", str)
    token_1 = r.json()["token"]

    r = create_token(headers=api_headers)
    assert_status_code(r, 200)
    assert_field_in_response_message(r, "token")
    assert_field_value_type(r, "token", str)
    token_2 = r.json()["token"]

    assert token_1 != token_2

import requests

from config.secret_config import BASE_URL
from data.payloads import BOOKING_PAYLOAD, UPDATED_BOOKING_PAYLOAD


def create_booking(
        headers: dict,
        checkin=None,
        checkout=None,
        **kwargs
):
    payload = BOOKING_PAYLOAD.copy()

    payload["bookingdates"] = payload["bookingdates"].copy()

    if checkin:
        payload["bookingdates"]["checkin"] = checkin

    if checkout:
        payload["bookingdates"]["checkout"] = checkout

    payload.update(kwargs)

    return requests.post(
        f"{BASE_URL}/booking",
        headers=headers,
        json=payload
    )


def get_bookings(firstname=None, lastname=None,
                 checkin=None, checkout=None):
    params = {}

    if firstname:
        params["firstname"] = firstname

    if lastname:
        params["lastname"] = lastname

    if checkin:
        params["checkin"] = checkin

    if checkout:
        params["checkout"] = checkout

    return requests.get(
        f"{BASE_URL}/booking",
        params=params
    )


def get_booking(booking_id: int):
    return requests.get(f"{BASE_URL}/booking/{booking_id}")


def update_booking(booking_id: int, headers: dict):
    return requests.put(f"{BASE_URL}/booking/{booking_id}",
                        headers=headers,
                        json=UPDATED_BOOKING_PAYLOAD)


def patch_booking(booking_id: int, headers: dict):
    return requests.patch(f"{BASE_URL}/booking/{booking_id}",
                          headers=headers,
                          json={"totalprice": 200})


def delete_booking(booking_id: int, headers: dict):
    return requests.delete(f"{BASE_URL}/booking/{booking_id}",
                           headers=headers)

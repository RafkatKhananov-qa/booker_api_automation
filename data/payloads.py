BOOKING_PAYLOAD = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {"checkin": '2026-01-01', "checkout": '2026-01-05'}
}

UPDATED_BOOKING_PAYLOAD = {
    "firstname": "Dannie",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-01-01",
        "checkout": "2026-01-05"
    },
    "additionalneeds": "Breakfast"
}

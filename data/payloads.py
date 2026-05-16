BOOKING_PAYLOAD = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-01-01",
        "checkout": "2026-01-05"
    }
}

UPDATED_BOOKING_PAYLOAD = {
    "firstname": "Dannie",
    "lastname": "Brown",
    "totalprice": 200,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2026-01-02",
        "checkout": "2026-01-06"
    },
    "additionalneeds": "Breakfast"
}

UPDATED_FIRSTNAME_BOOKING_PAYLOAD = {
    "firstname": "Jackson",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-01-01",
        "checkout": "2026-01-05"
    }
}

UPDATED_PRICE_BOOKING_PAYLOAD = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 500,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-01-01",
        "checkout": "2026-01-05"
    }
}

UPDATED_DEPOSITPAID_BOOKING_PAYLOAD = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2026-01-01",
        "checkout": "2026-01-05"
    }
}

BOOKING_EMPTY_FIRSTNAME_PAYLOAD = {
      "firstname": "",
      "lastname": "Doe",
      "totalprice": 100,
      "depositpaid": True,
      "bookingdates": {
          "checkin": "2026-01-01",
          "checkout": "2026-01-05"
      }
}

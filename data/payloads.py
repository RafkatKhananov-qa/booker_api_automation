from datetime import date, timedelta


BOOKING_PAYLOAD = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": str(date.today() + timedelta(days=1)),
        "checkout": str(date.today() + timedelta(days=5))
    }
}

UPDATED_BOOKING_PAYLOAD = {
    "firstname": "Dannie",
    "lastname": "Brown",
    "totalprice": 200,
    "depositpaid": False,
    "bookingdates": {
        "checkin": str(date.today() + timedelta(days=1)),
        "checkout": str(date.today() + timedelta(days=7))
    },
    "additionalneeds": "Breakfast"
}

UPDATED_FIRSTNAME_BOOKING_PAYLOAD = {
    "firstname": "Jackson",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": True,
    "bookingdates": {
        "checkin": str(date.today() + timedelta(days=1)),
        "checkout": str(date.today() + timedelta(days=5))
    }
}

UPDATED_PRICE_BOOKING_PAYLOAD = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 500,
    "depositpaid": True,
    "bookingdates": {
        "checkin": str(date.today() + timedelta(days=1)),
        "checkout": str(date.today() + timedelta(days=5))
    }
}

UPDATED_DEPOSITPAID_BOOKING_PAYLOAD = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 100,
    "depositpaid": False,
    "bookingdates": {
        "checkin": str(date.today() + timedelta(days=1)),
        "checkout": str(date.today() + timedelta(days=5))
    }
}

BOOKING_EMPTY_FIRSTNAME_PAYLOAD = {
      "firstname": "",
      "lastname": "Doe",
      "totalprice": 100,
      "depositpaid": True,
      "bookingdates": {
          "checkin": str(date.today() + timedelta(days=1)),
          "checkout": str(date.today() + timedelta(days=5))
      }
}


NOT_VALID_PAYLOAD = "not valid json {{"

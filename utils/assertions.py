import allure


@allure.step("Проверить статус-код")
def assert_status_code(response, expected_code):
    assert response.status_code == expected_code, (
        f"Неверный статус ответа: {response.status_code}"
    )


@allure.step("Проверить значение поля в ответе сервера")
def assert_response_message(response, field_name, expected_message):
    assert response.json()[field_name] == expected_message, (
        f"Сообщение не соответствует ожидаемому: {response.json()[field_name]}"
    )


@allure.step("Проверить, что поле есть в ответе сервера")
def assert_field_in_response_message(response, field_name):
    assert field_name in response.json()


@allure.step("Проверить, что поля нет в ответе сервера")
def assert_field_not_in_response_message(response, field_name):
    assert field_name not in response.json()


@allure.step("Проверить, что время ответа меньше ожидаемого времени")
def assert_response_time(response, sec: float):
    assert response.elapsed.total_seconds() < sec


@allure.step("Проверить тип поля в ответе сервера")
def assert_field_value_type(response, field_name, field_type):
    assert isinstance(response.json()[field_name], field_type)


@allure.step("Проверить, что ответ сервера сожержит данные")
def assert_array_not_empty(response):
    assert response.json()


@allure.step("Проверить headers в ответе сервера")
def assert_headers_in_response(response):
    assert "Content-Type" in response.headers
    assert "Content-Length" in response.headers
    assert response.headers["Content-Type"] == "application/json; charset=utf-8"
    assert int(response.headers["Content-Length"]) > 0


@allure.step("Проверить поля ответа")
def assert_response_fields(response_json, expected_data):
    for key, value in expected_data.items():
        assert response_json[key] == value

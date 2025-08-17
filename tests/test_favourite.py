import pytest
import allure
import requests
from core.clients.endpoints import Endpoints
from core.models.ajax import Response

@allure.feature("API Избранное")
@allure.story("Тестирование добавления товара в избранное")
def test_add_to_favorites(api_client):
    # Обновление cookies перед запросом
    api_client.refresh_session_cookies()
    php_sessid = api_client.session.cookies.get("PHPSESSID")
    if not php_sessid:
        pytest.fail("PHPSESSID не найден в cookies сессии")

    # Данные формы для POST-запроса
    data = {
        "is_ajax_post": "Y",
        "sessid": php_sessid,
        "lang": "ru",
        "action": "favorite",
        "state": "1",
        "SITE_ID": "s1",
        "ID": "12244",  # Используем ID из LITE_VIEWED_ITEMS_s1
        "IBLOCK_ID": "38"
    }

    with allure.step("Отправка POST-запроса для добавления товара в избранное"):
        print("Endpoint:", Endpoints.AJAX_ENDPOINT.value)
        response = api_client.post(endpoint=Endpoints.AJAX_ENDPOINT.value, json=data)

    with allure.step("Проверка кода состояния ответа"):
        assert response.status_code == 200, f"Ожидался код состояния 200, получен {response.status_code}"

    with allure.step("Проверка содержимого ответа"):
        print("Response Headers:", dict(response.headers))
        print("Raw Response Content:", response.text)
        try:
            response_json = response.json()
            print("API Response:", response_json)
        except requests.exceptions.JSONDecodeError as e:
            pytest.fail(f"Не удалось разобрать ответ как JSON: {e}\nСодержимое ответа: {response.text}\nЗаголовки ответа: {dict(response.headers)}")

    with allure.step("Разбор и валидация JSON-ответа"):
        validated_response = Response(**response_json)

    with allure.step("Проверка данных ответа"):
        if not validated_response.success:
            pytest.fail(f"API request failed: {validated_response.error}")
        assert validated_response.success is True, "Ожидалось, что success будет True"
        assert validated_response.error == "", "Ожидалась пустая строка в поле error"
        assert validated_response.items == {"12244": 12244}, "Ожидались соответствующие элементы в items"
        assert validated_response.count == 1, "Ожидалось, что count будет равен 1"
        assert validated_response.title == "Избранные товары", "Ожидался соответствующий заголовок"
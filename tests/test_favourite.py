import pytest
import requests
from pydantic import BaseModel, Field
import allure


# Pydantic модель для валидации ответа
class FavoriteResponse(BaseModel):
    success: bool
    error: str
    items: list | dict  # Разрешаем list или dict для items
    count: int
    title: str | None = Field(None, alias="title")  # Делаем title необязательным


@allure.feature("API Избранное")
@allure.story("Тестирование добавления товара в избранное")
def test_add_to_favorites():
    url = "https://promminer.ru/ajax/item.php"

    # Данные формы для POST-запроса
    data = {
        "is_ajax_post": "Y",
        "sessid": "",
        "lang": "ru",
        "action": "favorite",
        "state": "1",
        "SITE_ID": "s1",
        "ID": "5253",
        "IBLOCK_ID": "38"
    }

    # Cookies для заголовка
    cookies = (
        "tmr_lvid=950bf4cca1c08bbc61cff403c1407a61; "
        "tmr_lvidTS=1754460759776; "
        "_ym_uid=1754460760764763746; "
        "_ym_d=1754460760; "
        "_ct=2200000000397000047; "
        "_ct_client_global_id=73870687-a297-51ae-bb3d-d8b93efca522; "
        "_ym_debug=null; "
        "prefers-color-scheme=dark; "
        "scroll_block=null; "
        "cted=modId%3D68bqwp0k%3Bya_client_id%3D1754460760764763746; "
        "_ct_site_id=54220; "
        "LITE_VIEWED_ITEMS_s1=%7B%224573%22%3A%5B%221755102712410%22%2C%2212244%22%2C%2238%22%5D%7D; "
        "PHPSESSID=zHvFcfPzqtNz45d2VnSfQpaLKNiWGN2j; "
        "_ym_visorc=w; "
        "_ym_isad=2; "
        "_ct_ids=68bqwp0k%3A54220%3A619619272; "
        "_ct_session_id=619619272; "
        "domain_sid=mC9KdGyL3pN25KwqWOBe0%3A1755180382023; "
        "call_s=___68bqwp0k.1755182190.619619272.480723:1367711|2___; "
        "tmr_detect=0%7C1755180392938"
    )

    headers = {
        "Cookie": cookies
    }

    with allure.step("Отправка POST-запроса для добавления товара в избранное"):
        # Отключаем проверку SSL (небезопасно, только для тестирования)
        response = requests.post(url, data=data, headers=headers, verify=False)

    with allure.step("Проверка кода состояния ответа"):
        assert response.status_code == 200, f"Ожидался код состояния 200, получен {response.status_code}"

    with allure.step("Вывод сырого ответа для отладки"):
        allure.attach(str(response.json()), name="Сырой JSON-ответ", attachment_type=allure.attachment_type.JSON)

    with allure.step("Разбор и валидация JSON-ответа"):
        response_json = response.json()
        validated_response = FavoriteResponse(**response_json)

    # with allure.step("Проверка данных ответа"):
    #     if not validated_response.success:
    #         allure.attach(validated_response.error, name="Ошибка API", attachment_type=allure.attachment_type.TEXT)
    #         pytest.fail(f"API вернул неуспешный ответ: {validated_response.error}")
    #
    #     assert validated_response.items == {"5253": 5253}, "Ожидались элементы {'5253': 5253}"
    #     assert validated_response.count == 1, "Ожидалось, что count будет равен 1"
    #     assert validated_response.title == "Избранные товары", "Ожидался заголовок 'Избранные товары'"

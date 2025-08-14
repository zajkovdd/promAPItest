import allure
import pytest
from pydantic import ValidationError
from requests import HTTPError
from tests.conftest import api_client
from core.clients.endpoints import PetEndpoints
from core.models.pet import Pet, PetStatus, Category, Tag

@allure.title('Позитивный тест: добавление нового питомца')
@allure.description('Проверяет успешное создание нового питомца через эндпоинт /pet с валидными данными.')
def test_add_new_pet(api_client):
    # Подготовка данных для отправки
    with allure.step('Создание данных для отправки'):
        payload = Pet(
            id=1,
            name="Buddy",
            category=Category(id=1, name="Dogs"),
            photoUrls=["https://example.com/pet1.jpg"],
            tags=[Tag(id=1, name="friendly")],
            status=PetStatus.AVAILABLE
        )

    # Отправка запроса на добавление питомца
    with allure.step('Отправка POST-запроса для добавления питомца'):
        try:
            response = api_client.post(
                PetEndpoints.PET_ENDPOINT.value,  # Используем .value для получения строки
                data=payload.dict(),  # Преобразуем Pydantic-модель в словарь
                status_code=200
            )
        except HTTPError as e:
            allure.attach(str(e), name="HTTPError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Не удалось добавить питомца: {str(e)}")

    # Валидация структуры ответа
    with allure.step('Проверка структуры ответа'):
        try:
            response_data = Pet(**response)  # Валидируем ответ как Pydantic-модель
            assert response_data.id == payload.id, f"Ожидался ID питомца {payload.id}, получено {response_data.id}"
            assert response_data.name == payload.name, f"Ожидалось имя питомца {payload.name}, получено {response_data.name}"
            assert response_data.status == payload.status, f"Ожидался статус {payload.status}, получено {response_data.status}"
            assert response_data.category.name == payload.category.name, \
                f"Ожидалось имя категории {payload.category.name}, получено {response_data.category.name}"
        except ValidationError as e:
            allure.attach(str(e), name="ValidationError", attachment_type=allure.attachment_type.TEXT)
            pytest.fail(f"Ошибка валидации ответа: {str(e)}")

    return response

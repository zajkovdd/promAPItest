

import allure
import pytest
from requests import HTTPError

from core.clients.api_client import APIClient
from core.clients.endpoints import PetEndpoints
from core.models.pet import PetStatus, Pet, Category, Tag


@pytest.fixture(scope='session')
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def create_pet(api_client):
    """Фикстура для создания питомца с заданным статусом."""
    def _create_pet(status: PetStatus):
        with allure.step(f'Создание питомца со статусом {status}'):
            payload = Pet(
                id=hash(status) % 10000,  # Уникальный ID на основе статуса
                name=f"Pet_{status}",
                category=Category(id=1, name="Dogs"),
                photoUrls=["https://example.com/pet.jpg"],
                tags=[Tag(id=hash(status) % 10000, name=f"test_{status}")],
                status=status
            )
            try:
                response = api_client.post(
                    PetEndpoints.PET_ENDPOINT.value,
                    data=payload.model_dump(),
                    status_code=200
                )
                return response
            except HTTPError as e:
                pytest.fail(f"Не удалось создать питомца: {str(e)}")
    return _create_pet
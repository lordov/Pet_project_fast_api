import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from main import app
from api.users.schemas import UserCreate, UserOut

client = TestClient(app)


@pytest.mark.asyncio
@patch("api.auth.router.get_async_session", new_callable=AsyncMock)
@patch("api.auth.router.regisrty_user", new_callable=AsyncMock)
async def test_sign_up(mock_regisrty_user, mock_get_async_session):
    new_user = UserCreate(
        email="0x7Z@example.com",
        username="Bob",
        password="12345678",
        fullname="Bob Smith"
    )
    user_out = UserOut(
        id=1,
        email="0x7Z@example.com",
        username="Bob",
        fullname="Bob Smith"
    )
    mock_regisrty_user.return_value = user_out

    response = client.post(
        "/auth/sign_up",
        json=new_user.model_dump()
    )

    response_json = response.json()
    assert response.status_code == 201
    assert "id" in response_json
    assert response_json["email"] == "0x7Z@example.com"
    assert response_json["username"] == "Bob"
    assert response_json["fullname"] == "Bob Smith"
    


@pytest.mark.asyncio
@patch("api.auth.router.get_async_session", new_callable=AsyncMock)
@patch("api.auth.router.regisrty_user", new_callable=AsyncMock)
async def test_sign_up_validation_error(mock_regisrty_user, mock_get_async_session):
    # Отправляем запрос с некорректными данными
    invalid_user_data = {
        "email": "invalid-email",  # Некорректный формат email
        "username": "",             # Пустое обязательное поле
        "password": "short",        # Слишком короткий пароль
        "fullname": "Bob Smith"
    }

    response = client.post(
        "/auth/sign_up",
        json=invalid_user_data
    )

    # Проверяем, что статус код 422 и что ошибки соответствуют ожидаемым
    assert response.status_code == 422
    errors = response.json()
    assert all(key in error for error in errors for key in ("msg", "field", "your_input"))
    assert any(len(error["field"]) > 0 for error in errors)
    

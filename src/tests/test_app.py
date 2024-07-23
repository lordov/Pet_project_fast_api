from fastapi.testclient import TestClient
from main import app


client = TestClient(app)



def test_calculate_sum():
    # Test case 1: валидные входные данные
    response = client.get("/sum/?a=5&b=10")
    assert response.status_code == 200
    assert response.json() == {"result": 15}

    # Test case 2: отрицательные числа
    response = client.get("/sum/?a=-8&b=-3")
    assert response.status_code == 200
    assert response.json() == {"result": -11}

    # Test case 3: ноль и положительное число
    response = client.get("/sum/?a=0&b=7")
    assert response.status_code == 200
    assert response.json() == {"result": 7}

    # Test case 4: одно число не введено
    response = client.get("/sum/?a=3")
    # Специфический json для 422
    assert response.status_code == 422  # Unprocessable Entity

    assert response.json() == [
        {
            'field': 'b',
            'msg': 'Field required',
            'your_input': None
        }
    ]

# Здесь нужен Mock зависимостей
def test_sign_up():
    # Test case 1: валидные входные данные
    response = client.post(
        "/auth/sign_up",
        json={
            "email": "0x7Z@example.com",
            "username": "Bob",
            "password": "12345678",
            "fullname": "Bob Smith"
        }
    )
    response_json = response.json()
    assert response.status_code == 201
    assert "id" in response_json
    assert response_json["email"] == "0x7Z@example.com"
    assert response_json["username"] == "Bob"
    assert response_json["fullname"] == "Bob Smith"
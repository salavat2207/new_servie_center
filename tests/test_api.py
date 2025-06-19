# tests/test_api.py

def test_create_request(client):
    response = client.post("/requests/", json={
        "city_id": 1,
        "phone": "89001234567",
        "description": "Не включается экран"
    })
    assert response.status_code == 200


def test_get_requests(client):
    response = client.get("/requests/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_create_request_invalid_data(client):
    response = client.post("/requests/", json={
        "city_id": None,
        "phone": "",
        "description": ""
    })
    assert response.status_code == 422
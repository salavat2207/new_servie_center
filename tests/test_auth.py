def test_unauthorized_access(client):
    response = client.get("/admin/products")
    assert response.status_code in (401, 403)


def test_login_wrong_password(client):
    response = client.post("/token", data={
        "username": "admin",
        "password": "wrongpass"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert response.status_code == 401


def test_authorized_access(client):
    login = client.post("/token", data={
        "username": "admin",
        "password": "adminpass"
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    response = client.get("/admin/products", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
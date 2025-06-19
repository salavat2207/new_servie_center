from app import crud
from app.schemas import RepairRequestCreate

def test_create_request_model(db):
    data = RepairRequestCreate(
        city_id=1,
        phone="89001234567",
        description="Экран разбит"
    )
    request = crud.create_request(db, data)
    assert request.description == "Экран разбит"
    assert request.phone == "89001234567"
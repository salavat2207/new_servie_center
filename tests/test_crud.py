from app import crud
from app.schemas import RepairRequestCreate

def test_create_request(db):
    data = RepairRequestCreate(
        city_id=1,
        phone="89001234567",
        description="Не включается экран"
    )
    request = crud.create_request(db, data)
    assert request.phone == "89001234567"
    assert request.description == "Не включается экран"
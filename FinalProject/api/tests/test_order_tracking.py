import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..dependencies.database import Base, get_db
from ..models import model_loader  # noqa: F401 - registers every model with Base
from ..models.orders import Order
from ..routers.orders import router as orders_router


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

Base.metadata.create_all(bind=test_engine)

app_under_test = FastAPI()
app_under_test.include_router(orders_router)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app_under_test.dependency_overrides[get_db] = override_get_db
client = TestClient(app_under_test)


@pytest.fixture(autouse=True)
def clear_orders():
    db = TestingSessionLocal()
    db.query(Order).delete()
    db.commit()
    db.close()


def create_test_order():
    response = client.post(
        "/orders/",
        json={
            "customer_name": "Tracking Test",
            "description": "Test order for tracking",
        },
    )
    assert response.status_code == 200
    return response.json()


def test_create_and_track_order():
    created_order = create_test_order()

    assert created_order["tracking_number"]
    assert created_order["status"] == "received"

    response = client.get(
        f"/orders/track/{created_order['tracking_number']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == created_order["id"]
    assert response.json()["status"] == "received"


def test_unknown_tracking_number_returns_404():
    response = client.get("/orders/track/not-a-real-tracking-number")

    assert response.status_code == 404
    assert response.json()["detail"] == "Tracking number not found!"


def test_update_order_status():
    created_order = create_test_order()

    response = client.patch(
        f"/orders/{created_order['id']}/status",
        json={"status": "preparing"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "preparing"

    tracking_response = client.get(
        f"/orders/track/{created_order['tracking_number']}"
    )
    assert tracking_response.json()["status"] == "preparing"


def test_update_status_for_missing_order_returns_404():
    response = client.patch(
        "/orders/999/status",
        json={"status": "preparing"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Id not found!"


def test_invalid_status_returns_422():
    created_order = create_test_order()

    response = client.patch(
        f"/orders/{created_order['id']}/status",
        json={"status": "some-invalid-status"},
    )

    assert response.status_code == 422

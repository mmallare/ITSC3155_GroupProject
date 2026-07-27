from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..dependencies.database import Base, get_db
from ..models import model_loader  # noqa: F401 - registers every model with Base
from ..models.promotions import Promotion
from ..routers.promotions import router as promotions_router


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
app_under_test.include_router(promotions_router)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app_under_test.dependency_overrides[get_db] = override_get_db
client = TestClient(app_under_test)


@pytest.fixture(autouse=True)
def clear_promotions():
    db = TestingSessionLocal()
    db.query(Promotion).delete()
    db.commit()
    db.close()


def promotion_payload(
    promo_code="SAVE10",
    discount_percent=10,
    is_active=True,
    expiration_date=None,
):
    if expiration_date is None:
        expiration_date = datetime.now() + timedelta(days=30)

    return {
        "promo_code": promo_code,
        "expiration_date": expiration_date.isoformat(),
        "discount_percent": discount_percent,
        "is_active": is_active,
    }


def create_test_promotion(**overrides):
    response = client.post(
        "/promotions/",
        json=promotion_payload(**overrides),
    )
    assert response.status_code == 200
    return response.json()


def test_create_read_update_and_delete_promotion():
    created = create_test_promotion(promo_code=" save10 ")

    assert created["promo_code"] == "SAVE10"
    assert Decimal(created["discount_percent"]) == Decimal("10")
    assert created["is_active"] is True

    read_response = client.get(f"/promotions/{created['id']}")
    assert read_response.status_code == 200
    assert read_response.json()["promo_code"] == "SAVE10"

    list_response = client.get("/promotions/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    update_response = client.put(
        f"/promotions/{created['id']}",
        json={"discount_percent": 20, "is_active": False},
    )
    assert update_response.status_code == 200
    assert Decimal(update_response.json()["discount_percent"]) == Decimal("20")
    assert update_response.json()["is_active"] is False

    delete_response = client.delete(f"/promotions/{created['id']}")
    assert delete_response.status_code == 204
    assert client.get(f"/promotions/{created['id']}").status_code == 404


def test_duplicate_promo_code_returns_400():
    create_test_promotion(promo_code="save10")

    response = client.post(
        "/promotions/",
        json=promotion_payload(promo_code="SAVE10"),
    )

    assert response.status_code == 400


def test_valid_promo_code_returns_discount():
    created = create_test_promotion(promo_code="save10")

    response = client.get("/promotions/validate/save10")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert Decimal(response.json()["discount_percent"]) == Decimal("10")


def test_unknown_promo_code_returns_404():
    response = client.get("/promotions/validate/DOES-NOT-EXIST")

    assert response.status_code == 404
    assert response.json()["detail"] == "Promotion code not found!"


def test_inactive_promo_code_returns_400():
    create_test_promotion(promo_code="INACTIVE", is_active=False)

    response = client.get("/promotions/validate/INACTIVE")

    assert response.status_code == 400
    assert response.json()["detail"] == "Promotion is inactive!"


def test_expired_promo_code_returns_400():
    create_test_promotion(
        promo_code="EXPIRED",
        expiration_date=datetime.now() - timedelta(days=1),
    )

    response = client.get("/promotions/validate/EXPIRED")

    assert response.status_code == 400
    assert response.json()["detail"] == "Promotion has expired!"


@pytest.mark.parametrize("discount_percent", [-1, 101])
def test_invalid_discount_percent_returns_422(discount_percent):
    response = client.post(
        "/promotions/",
        json=promotion_payload(discount_percent=discount_percent),
    )

    assert response.status_code == 422

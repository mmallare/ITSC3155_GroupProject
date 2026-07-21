from fastapi.testclient import TestClient
from ..controllers import cart as controller
from ..main import app
import pytest
from ..models import cart as model
from decimal import Decimal

client = TestClient(app)

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_cart(db_session):
    cart_data = {
        "subtotal": 20.35,
        "coupon": "15OFF",
        "quantity": 3,
        "customer_id": 1,
        "menu_item_id": 1
    }

    cart_object = model.Cart(**cart_data)

    created_cart = controller.create(db_session, cart_object)

    assert created_cart is not None
    assert created_cart.subtotal == 20.35
    assert created_cart.coupon == "15OFF"
    assert created_cart.quantity == 3
    assert created_cart.customer_id == 1
    assert created_cart.menu_item_id == 1

def test_read_all(db_session):
    cart_data = [
        model.Cart(
            id=1,
            subtotal=Decimal("14.98"),
            coupon="15OFF",
            quantity=2,
            customer_id=1,
            menu_item_id=1
        ),
        model.Cart(
            id=2,
            subtotal=Decimal("19.98"),
            coupon="10OFF",
            quantity=1,
            customer_id=2,
            menu_item_id=3
        )
    ]
    db_session.query.return_value.all.return_value = cart_data

    result = controller.read_all(db=db_session)

    assert result == cart_data
    assert len(result) == len(cart_data)
    assert result[0].id == 1
    assert result[1].id == 2
    assert result[0].subtotal == Decimal("14.98")
    assert result[1].subtotal == Decimal("19.98")

def test_read_one_cart(db_session):
    cart_data = model.Cart(
        id=1,
        subtotal=Decimal("14.98"),
        coupon="15OFF",
        quantity=2,
        customer_id=1,
        menu_item_id=1
    )
        # This simulates finding a cart object in the database
    db_session.query.return_value.filter.return_value.first.return_value = cart_data

        # Call read_one_cart function
    result = controller.read_one_cart(db=db_session, cart_id=1)

        # Assertions
    assert result is cart_data
    assert result.id == 1
    assert result.subtotal == Decimal("14.98")
    assert result.coupon == "15OFF"
    assert result.quantity == 2
    assert result.customer_id == 1
    assert result.menu_item_id == 1

def test_delete_cart(db_session):
    cart_data = model.Cart(
        id=1,
        subtotal=Decimal("14.98"),
        coupon="15OFF",
        quantity=2,
        customer_id=1,
        menu_item_id=1
    )

    # Mock the query used in the controller
    cart_query = db_session.query.return_value.filter.return_value
    cart_query.first.return_value = cart_data

    # Call delete_cart function
    deleted_cart = controller.delete_cart(db=db_session, cart_id=1)

    assert deleted_cart is cart_data







from ..controllers import cart as controller
import pytest
from ..schemas import cart as schema


class FakeCart:
    id = 1

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


@pytest.fixture
def fake_cart_model(monkeypatch):
    monkeypatch.setattr(controller.model, "Cart", FakeCart)
    return FakeCart


def test_create_cart(db_session, fake_cart_model):
    cart_data = {
        "table_number": 4,
        "subtotal": 19.50,
        "coupon": "SAVE10",
        "quantity": 2,
        "customer_id": 1,
        "menu_item_id": 3,
    }

    cart_object = schema.CartCreate(**cart_data)

    created_cart = controller.create(db_session, cart_object)

    assert created_cart is not None
    assert created_cart.table_number == 4
    assert created_cart.subtotal == 19.50
    assert created_cart.coupon == "SAVE10"
    assert created_cart.quantity == 2
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(created_cart)


def test_read_all_carts(db_session, fake_cart_model):
    cart = FakeCart(table_number=4, subtotal=19.50, coupon="SAVE10", quantity=2, customer_id=1, menu_item_id=3)
    db_session.query.return_value.all.return_value = [cart]

    result = controller.read_all(db_session)

    assert result == [cart]
    db_session.query.assert_called_once_with(FakeCart)


def test_read_one_cart(db_session, fake_cart_model):
    cart = FakeCart(table_number=4, subtotal=19.50, coupon="SAVE10", quantity=2, customer_id=1, menu_item_id=3)
    db_session.query.return_value.filter.return_value.first.return_value = cart

    result = controller.read_one(db_session, item_id=1)

    assert result == cart
    db_session.query.return_value.filter.assert_called_once()


def test_update_cart(db_session, fake_cart_model):
    cart = FakeCart(table_number=4, subtotal=19.50, coupon="SAVE10", quantity=2, customer_id=1, menu_item_id=3)
    filter_query = db_session.query.return_value.filter.return_value
    filter_query.first.return_value = cart

    request = schema.CartUpdate(table_number=7, subtotal=21.00, coupon="SAVE15", quantity=3)

    result = controller.update(db_session, item_id=1, request=request)

    assert result == cart
    filter_query.update.assert_called_once_with(
        {"table_number": 7, "subtotal": 21.0, "coupon": "SAVE15", "quantity": 3},
        synchronize_session=False,
    )
    db_session.commit.assert_called_once()


def test_delete_cart(db_session, fake_cart_model):
    cart = FakeCart(table_number=4, subtotal=19.50, coupon="SAVE10", quantity=2, customer_id=1, menu_item_id=3)
    filter_query = db_session.query.return_value.filter.return_value
    filter_query.first.return_value = cart

    response = controller.delete(db_session, item_id=1)

    assert response.status_code == 204
    filter_query.delete.assert_called_once_with(synchronize_session=False)
    db_session.commit.assert_called_once()
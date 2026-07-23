from ..controllers import orders as controller
import pytest
from ..schemas import orders as schema


class FakeOrder:
    id = 1

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


@pytest.fixture
def fake_order_model(monkeypatch):
    monkeypatch.setattr(controller.model, "Order", FakeOrder)
    return FakeOrder


def test_create_order(db_session, fake_order_model):
    order_data = {
        "table_number": 4,
        "customer_name": "John Doe",
        "description": "Test order"
    }

    order_object = schema.OrderCreate(**order_data)

    created_order = controller.create(db_session, order_object)

    assert created_order is not None
    assert created_order.table_number == 4
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"
    db_session.add.assert_called_once()
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(created_order)


def test_read_all_orders(db_session, fake_order_model):
    order = FakeOrder(table_number=4, customer_name="John Doe", description="Test order")
    db_session.query.return_value.all.return_value = [order]

    result = controller.read_all(db_session)

    assert result == [order]
    db_session.query.assert_called_once_with(FakeOrder)


def test_read_one_order(db_session, fake_order_model):
    order = FakeOrder(table_number=4, customer_name="John Doe", description="Test order")
    db_session.query.return_value.filter.return_value.first.return_value = order

    result = controller.read_one(db_session, item_id=1)

    assert result == order
    db_session.query.return_value.filter.assert_called_once()


def test_update_order(db_session, fake_order_model):
    order = FakeOrder(table_number=4, customer_name="John Doe", description="Test order")
    filter_query = db_session.query.return_value.filter.return_value
    filter_query.first.return_value = order

    request = schema.OrderUpdate(table_number=7, customer_name="Jane Doe", description="Updated order")

    result = controller.update(db_session, item_id=1, request=request)

    assert result == order
    filter_query.update.assert_called_once_with(
        {"table_number": 7, "customer_name": "Jane Doe", "description": "Updated order"},
        synchronize_session=False,
    )
    db_session.commit.assert_called_once()


def test_delete_order(db_session, fake_order_model):
    order = FakeOrder(table_number=4, customer_name="John Doe", description="Test order")
    filter_query = db_session.query.return_value.filter.return_value
    filter_query.first.return_value = order

    response = controller.delete(db_session, item_id=1)

    assert response.status_code == 204
    filter_query.delete.assert_called_once_with(synchronize_session=False)
    db_session.commit.assert_called_once()

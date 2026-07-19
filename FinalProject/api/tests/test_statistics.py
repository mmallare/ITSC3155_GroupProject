from decimal import Decimal

from ..controllers import statistics as controller
from ..schemas import statistics as schema


def test_create_statistic(mocker):
    db_session = mocker.Mock()
    fake_statistic = mocker.Mock()

    statistic_model = mocker.patch.object(
        controller.model,
        "Statistic",
        return_value=fake_statistic
    )

    request = schema.StatisticCreate(
        menu_item_id=1,
        menu_order_count=10,
        rating_score=Decimal("4.50"),
        avg_money_spent=Decimal("12.99"),
        peak_hours_traffic="6 PM - 8 PM",
        frequency=5
    )

    result = controller.create(
        db=db_session,
        request=request
    )

    statistic_model.assert_called_once_with(
        menu_item_id=1,
        menu_order_count=10,
        rating_score=Decimal("4.50"),
        avg_money_spent=Decimal("12.99"),
        peak_hours_traffic="6 PM - 8 PM",
        frequency=5
    )

    db_session.add.assert_called_once_with(fake_statistic)
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(fake_statistic)

    assert result is fake_statistic
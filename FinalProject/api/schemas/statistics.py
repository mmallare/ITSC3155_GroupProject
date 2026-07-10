from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from decimal import Decimal

class StatisticBase(BaseModel):
    menu_item_id: int
    menu_order_count: Optional[int] = 0
    rating_score: Optional[Decimal] = None
    avg_money_spent: Optional[Decimal] = None
    peak_hours_traffic: Optional[str] = None
    frequency: Optional[int] = None


class StatisticCreate(StatisticBase):
    pass


class StatisticUpdate(BaseModel):
    menu_order_count: Optional[int] = None
    rating_score: Optional[Decimal] = None
    avg_money_spent: Optional[Decimal] = None
    peak_hours_traffic: Optional[str] = None
    frequency: Optional[int] = None


class Statistic(StatisticBase):
    id: int

    class ConfigDict:
        from_attributes = True
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from decimal import Decimal

class MenuItemBase(BaseModel):
    item_name: str
    item_price: Decimal
    calories: Optional[int] = None


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    item_name: Optional[str] = None
    item_price: Optional[Decimal] = None
    calories: Optional[int] = None


class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
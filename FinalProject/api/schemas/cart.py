from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .order_details import OrderDetail
from decimal import Decimal

class CartBase(BaseModel):
    subtotal: Decimal
    coupon: Optional[str] = None
    quantity: int
    customer_id: int
    menu_item_id: int


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    subtotal: Optional[Decimal] = None
    coupon: Optional[str] = None
    quantity: Optional[int] = None


class Cart(CartBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
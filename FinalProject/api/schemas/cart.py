from typing import Optional
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class CartBase(BaseModel):
    table_number: int
    subtotal: Decimal
    coupon: Optional[str] = None
    quantity: int
    customer_id: int
    menu_item_id: int


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    table_number: Optional[int] = None
    subtotal: Optional[Decimal] = None
    coupon: Optional[str] = None
    quantity: Optional[int] = None


class Cart(CartBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
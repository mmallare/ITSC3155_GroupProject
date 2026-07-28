from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict
from .order_details import OrderDetail


OrderStatus = Literal[
    "received",
    "preparing",
    "ready",
    "out_for_delivery",
    "completed",
    "cancelled"
]



class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: str
    status: OrderStatus
    order_details: Optional[list[OrderDetail]] = None

    model_config = ConfigDict(from_attributes=True)

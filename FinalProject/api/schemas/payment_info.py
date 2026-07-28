from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from .order_details import OrderDetail
from decimal import Decimal

class PaymentInformationBase(BaseModel):
    card_info: str
    status: Optional[str] = None
    payment_type: Optional[str] = None
    customer_id: int


class PaymentInformationCreate(PaymentInformationBase):
    pass


class PaymentInformationUpdate(BaseModel):
    card_info: Optional[str] = None
    status: Optional[str] = None
    payment_type: Optional[str] = None


class PaymentInformation(PaymentInformationBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
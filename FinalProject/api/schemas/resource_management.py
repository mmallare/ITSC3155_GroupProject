from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from decimal import Decimal

class ResourceManagementBase(BaseModel):
    amount_of_item: Decimal
    unit: str


class ResourceManagementCreate(ResourceManagementBase):
    pass


class ResourceManagementUpdate(BaseModel):
    amount_of_item: Optional[Decimal] = None
    unit: Optional[str] = None


class ResourceManagement(ResourceManagementBase):
    id: int

    class ConfigDict:
        from_attributes = True
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class PromotionBase(BaseModel):
    promo_code: str = Field(min_length=1, max_length=50)
    expiration_date: datetime
    discount_percent: Decimal = Field(ge=0, le=100)
    is_active: bool = True

    model_config = ConfigDict(str_strip_whitespace=True)


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    promo_code: Optional[str] = Field(default=None, min_length=1, max_length=50)
    expiration_date: Optional[datetime] = None
    discount_percent: Optional[Decimal] = Field(default=None, ge=0, le=100)
    is_active: Optional[bool] = None

    model_config = ConfigDict(str_strip_whitespace=True)


class Promotion(PromotionBase):
    id: int

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

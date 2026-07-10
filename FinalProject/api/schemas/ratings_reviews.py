from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from decimal import Decimal

class RatingReviewBase(BaseModel):
    review_text: Optional[str] = None
    score: int
    customer_id: int


class RatingReviewCreate(RatingReviewBase):
    pass


class RatingReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[int] = None


class RatingReview(RatingReviewBase):
    id: int

    class ConfigDict:
        from_attributes = True
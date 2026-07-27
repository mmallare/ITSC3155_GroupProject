from sqlalchemy import Boolean, Column, Integer, String, DECIMAL, DATETIME
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(50), nullable=False, unique=True)
    expiration_date = Column(DATETIME, nullable=False)
    discount_percent = Column(DECIMAL(5, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

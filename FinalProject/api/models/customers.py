from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(300))

    ratings_reviews = relationship("RatingReview", back_populates="customer")
    payment_information = relationship("PaymentInformation", back_populates="customer")
    cart_items = relationship("Cart", back_populates="customer")
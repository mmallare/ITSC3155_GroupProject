from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    subtotal = Column(DECIMAL(8, 2), nullable=False)
    coupon = Column(String(50))
    quantity = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)

    customer = relationship("Customer", back_populates="cart_items")
    menu_item = relationship("MenuItem", back_populates="cart_items")
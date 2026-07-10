from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_name = Column(String(150), nullable=False)
    item_price = Column(DECIMAL(6, 2), nullable=False)
    calories = Column(Integer)

    cart_items = relationship("Cart", back_populates="menu_item")
    statistics = relationship("Statistic", back_populates="menu_item")
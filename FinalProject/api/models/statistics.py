from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class Statistic(Base):
    __tablename__ = "statistics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    menu_order_count = Column(Integer, default=0)
    rating_score = Column(DECIMAL(3, 2))
    avg_money_spent = Column(DECIMAL(8, 2))
    peak_hours_traffic = Column(String(100))
    frequency = Column(Integer)

    menu_item = relationship("MenuItem", back_populates="statistics")
from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class RatingReview(Base):
    __tablename__ = "ratings_reviews"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    review_text = Column(String(500))
    score = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="ratings_reviews")
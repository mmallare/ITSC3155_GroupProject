from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class PaymentInformation(Base):
    __tablename__ = "payment_information"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    card_info = Column(String(255), nullable=False)
    status = Column(String(50))
    payment_type = Column(String(50))
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    customer = relationship("Customer", back_populates="payment_information")
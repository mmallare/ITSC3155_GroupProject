from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from ..dependencies.database import Base

class ResourceManagement(Base):
    __tablename__ = "resource_management"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    amount_of_item = Column(DECIMAL(10, 2), nullable=False)
    unit = Column(String(50), nullable=False)
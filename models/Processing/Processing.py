from sqlalchemy import Column, Integer, String, Numeric, Boolean
from utils.Base import Base


class LBProcessing(Base):
    __tablename__ = 'lb_processing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cultive = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    quantity_numeric = Column(Numeric, nullable=True)
    is_type = Column(Boolean, nullable=True)
    type = Column(String, nullable=True)
    classification = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
    
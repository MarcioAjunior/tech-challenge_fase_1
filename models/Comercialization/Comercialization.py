from sqlalchemy import Column, Integer, String, Numeric, Boolean
from utils.Base import Base


class LBComercialization(Base):
    __tablename__ = 'lb_comercialization'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    quantity_numeric = Column(Numeric, nullable=True)
    is_type = Column(Boolean, nullable=True)
    type = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
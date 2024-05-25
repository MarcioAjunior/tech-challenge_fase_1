from sqlalchemy import Column, Integer, String, Numeric
from utils.Base import Base


class LBImportation(Base):
    __tablename__ = 'lb_importation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String, nullable=True)
    quantity = Column(String, nullable=True)
    quantity_numeric = Column(Numeric, nullable=True)
    value = Column(String, nullable=True)
    value_numeric = Column(Numeric, nullable=True)
    classification = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
    
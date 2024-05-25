from sqlalchemy import Column, Integer, String,  Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Qtds(Base):
    __tablename__ = 'lb_qtty_by_year'

    id = Column(Integer, primary_key=True)
    id_produto = Column(Integer, nullable=False)
    qtty_made = Column(Numeric, nullable=True)
    qtty_exported = Column(Numeric, nullable=True)
    qtty_imported = Column(Numeric, nullable=True)
    qtty_commercialized = Column(Numeric, nullable=True)
    qtty_processed = Column(Numeric, nullable=True)
    year = Column(Integer, nullable=False)
    
    
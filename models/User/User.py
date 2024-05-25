from sqlalchemy import Column, Integer, String
from utils.Base import Base

class LBUser(Base):
    __tablename__ = 'lb_users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    
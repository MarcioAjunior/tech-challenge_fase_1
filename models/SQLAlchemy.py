from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.Base import Base

class SQLAlchemyManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine('sqlite:///database.db')
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
            
            Base.metadata.create_all(cls._instance.engine)
            
        return cls._instance

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

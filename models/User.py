from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from .SQLAlchemy import SQLAlchemyManager
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
import jwt
from .JWT import SECRET_KEY, ALGORITHM 
from typing import Optional

Base = declarative_base()

ERRORS = {
    400 : 'Erro, Não foi possível cadastrar Usuário',
    409 : 'Conflito, usuario com email %s já existe !',
    404 : 'Email ou senha incorretos !',
}

class User(Base):
    __tablename__ = 'lb_users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

   
class UserRegister(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    email: str = Field(pattern='^[a-zA-Z0-9]+@[a-zA-Z0-9]+')
    password: str = Field(min_length=5, max_length=20)
    
    @staticmethod
    def encript_pass(password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
        
    @staticmethod
    def create_access_token():
        pass
        
    def save_user(self):
        with SQLAlchemyManager() as session:
            try:
                self.password = UserRegister.encript_pass(self.password)
                user = User(name=self.name, email=self.email, password=self.password)
                session.add(user)
                session.commit()
                return self
            except IntegrityError as e:
                session.rollback()
                user = session.query(User).filter_by(email=self.email).first()
                if user:
                    return (409, ERRORS.get(409) % self.email)
                return (400, ERRORS.get(400))
            except Exception as e:
                session.rollback()
                print(e)
                return (400, ERRORS.get(400))
    
class UserLogin(BaseModel):
    email : str #= Field(min_length=5, max_length=20)
    password : str #=  Field(min_length=5, max_length=20)
    token: str = Field(None)
    
    @staticmethod
    def dencript_pass(password, hashed_password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, hashed_password)
    
    @staticmethod
    def create_access_token(user : dict):
        encoded_jwt = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_credentials(self):        
        with SQLAlchemyManager() as session:
            try:
                user = session.query(User).filter_by(email=self.email).first()
                if not user:
                    return (404, ERRORS.get(404))     
                success_login = UserLogin.dencript_pass(self.password, user.password)
                if success_login:
                    self.token = UserLogin.create_access_token(user={"email" : user.email})
                    if self.token is not None:
                        return self
                return (404, ERRORS.get(404))   
            except Exception as e:
                print(e)
                return (404, ERRORS.get(404))          

class ForgotPassUser(BaseModel):
    email : str
    
    

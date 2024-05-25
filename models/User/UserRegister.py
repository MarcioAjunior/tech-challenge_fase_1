from models.User.User import LBUser
from models.User.ERRORS import ERRORS
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from ..SQLAlchemy import SQLAlchemyManager
from sqlalchemy.exc import IntegrityError

class UserRegisterResponse(BaseModel):
    name: str
    email: str

class UserRegister(BaseModel):
    name: str = Field(min_length=5, max_length=20)
    email: str = Field(pattern='^[a-zA-Z0-9]+@[a-zA-Z0-9]+')
    password: str = Field(min_length=5, max_length=20)
    
    @staticmethod
    def encript_pass(password):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
        
        
    def save_user(self):
        with SQLAlchemyManager() as session:
            try:
                user = session.query(LBUser).filter_by(email=self.email).first()
                if user:
                    return (409, ERRORS.get(409) % self.email)
                self.password = UserRegister.encript_pass(self.password)
                user = LBUser(name=self.name, email=self.email, password=self.password)
                session.add(user)
                session.commit()
                return UserRegisterResponse(name=user.name, email=user.email)
            except Exception as e:
                session.rollback()
                print(e)
                return (500, ERRORS.get(500))
            
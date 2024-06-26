from models.User.User import LBUser
from models.User.ERRORS import ERRORS
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from models.SQLAlchemy import SQLAlchemyManager
from utils.JWT import SECRET_KEY, ALGORITHM 
import jwt

class UserLoginResponse(BaseModel):
    username : str
    email :str
    token : str

class UserLogin(BaseModel):
    username : str = None
    password : str =  None
    
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
                user = session.query(LBUser).filter_by(username=self.username).first()
                if not user:
                    return (404, f'Não encontrado uma conta para o usuário : {self.username}')     
                success_login = UserLogin.dencript_pass(self.password, user.password)
                if success_login:
                    token = UserLogin.create_access_token(user={"username" : user.username})
                    if token is not None:
                        return UserLoginResponse(username=user.username, email=user.email, token=token) 
                return (404, ERRORS.get(404))   
            except Exception as e:
                print(e)
                return (500, ERRORS.get(500))   
             
from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import RequestValidationError

from models import (
    UserRegister, UserRegisterResponse, UserLogin, UserLoginResponse,
    ProductionRequest, ProcessingRequest, ComercializationRequest,
    ImportationRequest, ExportationRequest
)
from models.docs import (
    docs_register, docs_login, docs_production,
    docs_processing, docs_commercialization,
    docs_importation, docs_exportation
)
from helpers import validations, verify_token

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app.add_exception_handler(RequestValidationError, validations)

@app.post('/register', status_code=201, responses=docs_register)
async def register_user(user: UserRegister, response: Response):
    user = user.save_user()
    if not isinstance(user, UserRegisterResponse):
        raise HTTPException(status_code=user[0], detail=user[1])
    response.status_code = 201
    return {"detail": user}

@app.post('/login', status_code=200, responses=docs_login)
async def login_user(user: UserLogin):
    user = user.verify_credentials()
    if not isinstance(user, UserLoginResponse):
        raise HTTPException(status_code=user[0], detail=user[1])
    return {"detail": user}

@app.get('/production', responses=docs_production)
async def get_production(production: ProductionRequest, token: str = Depends(verify_token)):
    need_scraping = production.verify_need_scraping()
    if need_scraping:
        production.scraping()
    results = production.load()
    return {"detail": results}

@app.get('/processing', status_code=200, responses=docs_processing)
async def get_processing(processing: ProcessingRequest, token: str = Depends(verify_token)):
    need_scraping = processing.verify_need_scraping()
    if need_scraping:
        processing.scraping()
    results = processing.load()
    return {"detail": results}

@app.get('/commercialization', status_code=200, responses=docs_commercialization)
async def get_commercialization(commercialization: ComercializationRequest, token: str = Depends(verify_token)):
    need_scraping = commercialization.verify_need_scraping()
    if need_scraping:
        commercialization.scraping()
    results = commercialization.load()
    return {"detail": results}

@app.get('/importation', status_code=200, responses=docs_importation)
async def get_importation(importation: ImportationRequest, token: str = Depends(verify_token)):
    need_scraping = importation.verify_need_scraping()
    if need_scraping:
        importation.scraping()
    results = importation.load()
    return {"detail": results}

@app.get('/exportation', status_code=200, responses=docs_exportation)
async def get_exportation(exportation: ExportationRequest, token: str = Depends(verify_token)):
    need_scraping = exportation.verify_need_scraping()
    if need_scraping:
        exportation.scraping()
    results = exportation.load()
    return {"detail": results}

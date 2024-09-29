from fastapi import APIRouter, Depends, FastAPI,Header,Query
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from models.userLogin import UserLogin
from Controllers.Controller_login import LoginController
from Controllers.token import Token
from starlette.responses import JSONResponse

app = FastAPI()
userAPI = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") # obtém o token de quem logou no sistema através da rota login

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/validar-token", tags=["login"])
async def validar_token(Authorization: Header= Depends(oauth2_scheme) ):
    print(Authorization)
    return LoginController.retornar_token(Authorization)

@app.get("/validar-token-dados", tags=["login"])
async def validar_token_dados(Authorization: str):
    print(Authorization)
    return LoginController.retornar_token(Authorization)


@app.get("/validar-token-admin", tags=["login"])
async def validar_token_admin(Authorization: Header= Depends(oauth2_scheme) ):
   return LoginController.retornar_token_admin(Authorization)

@app.get("/tipo-usuario/{token}", tags=["login"])
async def retornar_tipo_usuario(token:str):#Authorization: Annotated[str, Header()]
    return LoginController.tipo_token(token)

   
@app.post("/login", tags=["login"])
async def login_for_access_token(user_data: UserLogin) :
    controller = LoginController()
    return controller.login(user_data.username, user_data.password)

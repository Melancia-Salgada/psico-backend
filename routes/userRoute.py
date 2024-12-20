from fastapi import APIRouter, FastAPI, Depends, Header
from routes.loginRoute import validar_token, validar_token_admin
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from models.userModel import User,Psicologo, Admin
#importando controllers
from Controllers.Controller_user import ControllerUser

app = FastAPI()
userAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@userAPI.post("/novo-usuario-admin", tags=["usuarios"])
async def createUserAdmin(adm:Admin): # , Authorization: Annotated[Header, Depends(validar_token_admin)]
     return ControllerUser.insertUser(adm)

@userAPI.get("/listar-usuarios", tags=["usuarios"])
async def listarUsuarios(Authorization: Annotated[Header, Depends(validar_token)]): 
     print(Authorization)
     return ControllerUser.getAllUsers()

@userAPI.get("/buscar-usuario/{username}", tags=["usuarios"]) 
async def buscarUsuario(username:str, Authorization: Annotated[Header, Depends(validar_token)]): #
     return ControllerUser.getUser(username)

@userAPI.get("/editar-usuario/{email}", tags=["usuarios"])
async def editarUsuario(email:str, Authorization: Annotated[Header, Depends(validar_token)]):
     user = ControllerUser.getUser(email)
     return user # para carregar os dados do usuário encontrado na página de atualizar dados

@userAPI.patch("/atualizar-usuario/{email}", tags=["usuarios"]) 
async def atualizarUsuario(user:User, email, Authorization: Annotated[Header, Depends(validar_token)] ): 
     return ControllerUser.updateUser(dict(user), email)

@userAPI.delete("/deletar-usuario/{username}", tags=["usuarios"])
async def excluirUsuarios(username:str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerUser.deleteUser(username)

#rotas relacionadas com a solicitação de cadastro

@userAPI.post("/solicitar-codigo-confirmacao", tags=["cadastro"])
async def CreatePsi(psi:Psicologo):
     return await ControllerUser.obterCodigoConfirmacao(psi)

@userAPI.post("/novo-psicologo/{codigo}", tags=["cadastro"])
async def CreatePsi(psi:Psicologo,codigo):
     return await ControllerUser.insertPsi(psi,codigo)


@userAPI.get("/listar-psicologos-pendentes", tags=["cadastro"])
async def listarUsuariosPendentes(Authorization: Annotated[Header, Depends(validar_token_admin)]):
     #print(Authorization)
     return ControllerUser.getAllUsersPendentes()


@userAPI.patch("/aprovar-psicologo/{CPF}", tags=["usuarios"]) 
async def aprovarPsi(CPF:str): #,Authorization: Annotated[Header, Depends(validar_token_admin)]
     return ControllerUser.aprovarPsi(CPF)

@userAPI.patch("/desaprovar-psicologo/{CPF}", tags=["usuarios"]) 
async def desaprovarPsi(CPF):  #,Authorization: Annotated[Header, Depends(validar_token_admin)]
     return ControllerUser.desaprovarPsi(CPF)

@userAPI.get("/get-faturamento/{email}", tags=["usuarios"])
async def getFaturamento(email):
     return ControllerUser.getFaturamento(email)
     


app.include_router(userAPI)
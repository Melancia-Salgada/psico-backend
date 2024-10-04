from typing import Annotated
from fastapi import APIRouter, FastAPI, Depends,Header
from models.pacienteModel import Paciente
from fastapi.middleware.cors import CORSMiddleware
from Controllers.controller_paciente import ControllerPaciente
from routes.loginRoute import validar_token


app = FastAPI()
pacienteAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


#Rota de teste, nao colocar em producao pf
@pacienteAPI.post('/novo-paciente', tags=["usuarios"])
async def createPaciente(paciente : Paciente):
     return await ControllerPaciente.insertPacienteTest(paciente)

@pacienteAPI.get("/todos-pacientes", tags=["usuarios"])
async def listarPacientes(): #Authorization: Annotated[Header, Depends(validar_token)]
     return ControllerPaciente.getAllPacientes()

@pacienteAPI.patch("/atualizar-paciente/{nomeCompleto}", tags="usuarios")
async def atualizarPaciente(nomeCompleto : str, paciente : Paciente, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerPaciente.updatePaciente(dict(paciente), nomeCompleto)

@pacienteAPI.patch("/desativar-paciente", tags= "usuarios")
async def desativarPaciente(paciente : Paciente, Authorization: Annotated[Header, Depends(validar_token)]):
     ControllerPaciente.desativarPaciente(paciente)
     
@pacienteAPI.get("/buscar-paciente/{nomeCompleto}", tags =["usuarios"])
async def buscarPaciente(nomeCompleto : str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerPaciente.buscarPaciente(nomeCompleto)
     

app.include_router(pacienteAPI)
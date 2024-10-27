from typing import Annotated
from fastapi import APIRouter, FastAPI, Depends,Header
from models.pacienteModel import Paciente,dadosClinicos
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

@pacienteAPI.post('/novo-paciente', tags=["usuarios"])
async def createPaciente(paciente : Paciente, Authorization: Annotated[Header, Depends(validar_token)]):
     return await ControllerPaciente.insertPaciente(paciente, Authorization)

@pacienteAPI.get("/todos-pacientes", tags=["usuarios"])
async def listarPacientes(Authorization: Annotated[Header, Depends(validar_token)]): 
     return ControllerPaciente.getAllPacientes(Authorization)

@pacienteAPI.patch("/atualizar-paciente/{email}", tags=["usuarios"])
async def atualizarPaciente(email : str, paciente : Paciente, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerPaciente.updatePaciente(dict(paciente), email)

@pacienteAPI.patch("/desativar-paciente/{email}", tags=["usuarios"])
async def desativarPaciente(email : str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerPaciente.desativarPaciente(email)

@pacienteAPI.patch("/ativar-paciente/{email}", tags=["usuarios"])
async def ativarPaciente(email : str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerPaciente.ativarPaciente(email)

     
@pacienteAPI.get("/buscar-paciente/{email}", tags =["usuarios"])
async def buscarPaciente(email : str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerPaciente.buscarPaciente(email)

@pacienteAPI.post("/registrar-dado-clinico/{email_paciente}", tags=["usuarios"])
async def createDadoClinico(registro : dadosClinicos, email_paciente:str,Authorization: Annotated[Header, Depends(validar_token)]):
     print("chegou na rota")
     return ControllerPaciente.registrar_dado_clinico(email_paciente,dict(registro))

@pacienteAPI.get("/listar-dados-clinicos/{email}", tags =["usuarios"])
async def retornarDadosClinicos(email : str, Authorization: Annotated[Header, Depends(validar_token)]):
     return ControllerPaciente.listar_dado_clinico(email)
     

app.include_router(pacienteAPI)
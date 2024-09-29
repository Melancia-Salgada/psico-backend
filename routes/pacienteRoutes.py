from fastapi import APIRouter, FastAPI, Depends,Header
from Controllers.Controller_user import ControllerUser
from models.pacienteModel import Paciente
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
pacienteAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


@pacienteAPI.get("/todos-pacientes", tags=["usuarios"])
async def listarPacientes():
     return ControllerUser.getAllPacientes()

@pacienteAPI.patch("/atualizar-paciente/{nomeCompleto}")
async def atualizarPaciente(nomeCompleto:str, paciente:Paciente):
     return ControllerUser.updatePaciente(dict(paciente), nomeCompleto)

@pacienteAPI.get("/buscar-paciente/{email}", tags=["pacientes"])
async def buscarPaciente(email:str):
     return ControllerUser.buscarPaciente(email)

app.include_router(pacienteAPI)
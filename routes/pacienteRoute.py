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


#Rota de teste, nao colocar em producao pf
@pacienteAPI.post('/novo-paciente', tags=["usuarios"])
async def createPaciente(paciente : Paciente):
     return await ControllerUser.insertPacienteTest(paciente)

@pacienteAPI.get("/todos-pacientes", tags=["usuarios"])
async def listarPacientes():
     return ControllerUser.getAllPacientes()

@pacienteAPI.patch("/atualizar-paciente/{nomeCompleto}", tags="usuarios")
async def atualizarPaciente(nomeCompleto:str, paciente:Paciente):
     return ControllerUser.updatePaciente(dict(paciente), nomeCompleto)

@pacienteAPI.get("/buscar-paciente/{email}", tags=["pacientes"])
async def buscarPaciente(email:str):
     return ControllerUser.buscarPaciente(email)

@pacienteAPI.patch("/desativar-paciente", tags= "usuarios")
async def desativarPaciente(paciente : Paciente):
     ControllerUser.desativarPaciente(paciente)
     

app.include_router(pacienteAPI)
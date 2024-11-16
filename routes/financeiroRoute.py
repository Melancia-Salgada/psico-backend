from typing import Annotated
from fastapi import APIRouter, FastAPI, Depends,Header
from models.pacienteModel import Paciente
from fastapi.middleware.cors import CORSMiddleware
from Controllers.controller_paciente import ControllerPaciente
from Controllers.Controller_financeiro import Controller_Recibo
from routes.loginRoute import validar_token


app = FastAPI()
financeiroAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@financeiroAPI.post('/novo-recibo/{email_paciente}', tags=["recibo"])
async def createRecibo(email_paciente:str, Authorization: Annotated[Header, Depends(validar_token)]):
     return Controller_Recibo.emitirRecibo(email_paciente, Authorization)


app.include_router(financeiroAPI)
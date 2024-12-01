from typing import Annotated
from fastapi import APIRouter, FastAPI, Depends,Header
from models.pacienteModel import Paciente
from fastapi.middleware.cors import CORSMiddleware
from Controllers.controller_paciente import ControllerPaciente
from Controllers.Controller_financeiro import Controller_Recibo
from Controllers.Controller_financeiro import Controller_Recibo
from models.pacienteModel import EmailCobrando
from routes.loginRoute import validar_token
from services.Email import ControllerEmail


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
 
@financeiroAPI.get("/todos-devedores/{email}", tags=["usuarios"])
async def listarDevedores(email : str): #Authorization : Annotated[Header, Depends(validar_token)]
     return Controller_Recibo.getAllPacientesDevedores({"email" : email})

@financeiroAPI.get("/valor-devido/{emailPsi}", tags=["usuarios"])
async def getValorDevido(emailPsi : str):
     return Controller_Recibo.somarValorDevido(Controller_Recibo.getAllPacientesDevedores({"email" : emailPsi}))
 
@financeiroAPI.patch("/agregar-faturamento/{emailPaciente}", tags = ["usuarios"])
async def agregarFaturamento(emailPaciente : str):
    print("Email do paciente na rota: " + emailPaciente)
    Controller_Recibo.adicionarFaturamentoMensal(emailPaciente)
    
@financeiroAPI.post("/email-cobranca", tags=["recibo"])
async def naoPago(dadosCliente : EmailCobrando):
    return await ControllerPaciente.setPacienteNaoPago(dadosCliente)
    


app.include_router(financeiroAPI)
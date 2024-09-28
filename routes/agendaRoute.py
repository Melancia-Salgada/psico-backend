from fastapi import APIRouter, Depends, FastAPI,Header,Query
from routes.loginRoute import validar_token, validar_token_admin, validar_token_dados
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from models.userModel import User,Psicologo,Admin
from models.agendamentoModel import Agendamento
from GoogleCalendarApi.googleAgenda import GoogleCalendar

app = FastAPI()
agendaAPI = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

@agendaAPI.post("/novo-agendamento", tags=["agendamentos"])
async def createAgendamento(evento:Agendamento,Authorization: Annotated[Header, Depends(validar_token)]):
    controller = GoogleCalendar()
    print(Authorization)
    psicologo_logado = await validar_token_dados(Authorization)
    print(psicologo_logado)
    return controller.insert_event(evento, psicologo_logado)

@agendaAPI.get("/listar-agendas", tags=["agendamentos"])
async def listarAgendas(Authorization: Annotated[Header, Depends(validar_token)]):
    controller = GoogleCalendar()
    return controller.listar_calendarios()

app.include_router(agendaAPI)
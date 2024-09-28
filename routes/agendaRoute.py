from fastapi import APIRouter, Depends, FastAPI,Header,Query
from routes.loginRoute import validar_token, validar_token_admin
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
    print(evento)
    return controller.insert_event(evento)

app.include_router(agendaAPI)
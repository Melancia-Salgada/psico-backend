from fastapi import APIRouter, Depends, FastAPI,Header,Query
from routes.loginRoute import validar_token
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
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
    return controller.insert_event(evento, Authorization)

@agendaAPI.get("/listar-agendamentos", tags=["agendamentos"])
async def createAgendamento(Authorization: Annotated[Header, Depends(validar_token)]):
    controller = GoogleCalendar()
    return controller.listar_eventos(Authorization)

@agendaAPI.patch("/atualizar-agendamento/{eventId}", tags=["agendamentos"])
async def atualizarAgendamentos(eventId:str,evento: Agendamento,Authorization: Annotated[Header, Depends(validar_token)]):
    controller = GoogleCalendar()
    return controller.updateAgendamento(eventId, evento, Authorization)

@agendaAPI.delete("/excluir-agendamento/{eventId}", tags=["agendamentos"])
async def excluirAgendamentos(eventId:str,Authorization: Annotated[Header, Depends(validar_token)]):
    controller = GoogleCalendar()
    return controller.deletarAgendamento(eventId, Authorization)

@agendaAPI.get("/listar-agendas", tags=["agendamentos"])
async def listarAgendas(Authorization: Annotated[Header, Depends(validar_token)]):
    controller = GoogleCalendar()
    return controller.listar_calendarios()

@agendaAPI.post("/enviar-lembrete", tags=["agendamentos"])
async def enviarLembreteConsulta(evento:Agendamento, Authorization: Annotated[Header, Depends(validar_token)]):
    controller = GoogleCalendar()
    return await controller.enviarLembreteConfirmacao(evento)

app.include_router(agendaAPI)
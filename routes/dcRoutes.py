from fastapi import APIRouter, FastAPI, Depends,Header
from Controllers.Controller_dadosClinicos import ControllerDadosClinicos, dadosClinicos
from models.dadosClinicos import dadosClinicos
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

@pacienteAPI.post('/novo-dadosClinicos', tags=["dados clinicos"])
async def createDadosClinicos(dadosClinicos : dadosClinicos):
     return await ControllerDadosClinicos.insertDadosClinicos(dadosClinicos)


@pacienteAPI.get("/buscar-dadosclinicos/{email}", tags=["dados clinicos"])
async def buscarDadosClinicos(email:str):
     return ControllerDadosClinicos.buscarDadosClinicos(email)

app.include_router(pacienteAPI)
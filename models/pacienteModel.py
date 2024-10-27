from pydantic import BaseModel
from typing import List
import datetime

class dadosClinicos(BaseModel):
   
    email_paciente: str
    data: datetime
    horario: datetime
    relato:str |None = None
    sintomas_sentimentos: str |None = None
    conduta: str |None = None
    tecnicas_abordagens: str |None = None
    conexao_sessao_anterior: str |None = None


class Paciente(BaseModel):
    nomeCompleto : str
    sexo : str
    idade : int
    telefone : str
    email : str
    grupo : str 
    valor: float
    nomeCompletoResponsavel : str
    telefoneResponsavel : str
    emailPsi : str
    dados_clinicos: List[dadosClinicos] |None = None
    tipo : str | None = "Paciente"
    status: str | None = "Ativo"
from pydantic import BaseModel
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
    
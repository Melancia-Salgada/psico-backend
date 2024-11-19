from pydantic import BaseModel
from typing import List, Optional

class dadosClinicos(BaseModel):
    data: Optional[str] = None
    horario: Optional[str] = None
    relato: Optional[str] = None
    sintomas_sentimentos: Optional[str] = None
    conduta: Optional[str] = None
    tecnicas_abordagens: Optional[str] = None
    conexao_sessao_anterior: Optional[str] = None

class Paciente(BaseModel):
    nomeCompleto: str
    nascimento: str
    telefone: str
    email: str
    cpf:str
    grupo: str | None = None
    endereco: str | None = None
    complemento: str | None = None
    cep: str | None = None
    nomeCompletoResponsavel: str | None = None
    telefoneResponsavel: str | None = None
    cpfResponsavel:str | None = None
    emailPsi: str
    dados_clinicos: List[dadosClinicos] | None = []
    tipo: Optional[str] = "Paciente"
    status: Optional[str] = "Ativo"

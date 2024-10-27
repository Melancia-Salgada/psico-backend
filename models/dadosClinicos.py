from pydantic import BaseModel

class dadosClinicos(BaseModel):
    nomeCompleto: str
    sexo: str
    idade: str
    telefone: str
    email: str
    grupo: str
    observacao: str
    valor: str
    nomeCompletoResponsavel: str
    telefoneResponsavel: str
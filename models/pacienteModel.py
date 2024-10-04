from pydantic import BaseModel


class Paciente(BaseModel):
    nomeCompleto : str
    sexo : str
    idade : int
    telefone : str
    email : str
    grupo : str 
    nomeCompletoResponsavel : str
    telefoneResponsavel : str
    emailPsi : str
    tipo : str | None = "Paciente"
    status: str | None = "Ativo"
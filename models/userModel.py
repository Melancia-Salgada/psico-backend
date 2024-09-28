from pydantic import BaseModel

class User(BaseModel): 
    username: str
    password:str
    tipo: str


class Psicologo(BaseModel): 
    username: str
    password:str
    phonenumber:str
    email:str
    CRP:str
    CPF:str
    tipo: str |None = "Psicólogo"
    status: str | None = "Pendente"
    
    
    
class Paciente(BaseModel):
    nomeCompleto : str
    sexo : str
    idade : int
    telefone : str
    email : str
    grupo : str 
    nomeCompletoResponsavel : str
    telefoneResponsavel : str
    tipo : str | None = "Paciente"



class Admin(BaseModel): 
    username: str
    password:str
    phonenumber:str
    email:str
    CPF: str
    tipo: str |None = "Administrador"


#usuário padrão do banco
usuario_admin = {
  "username": "system",
  "password": "admin123",
  "phonenumber": "11988655418",
  "email": "devslindos@outlook.com",
  "tipo":"Administrador"
}

  


    
  


from pydantic import BaseModel

class User(BaseModel): 
    username: str
    password:str
    tipo: str


class Psicologo(BaseModel): 
    username: str
    password:str
    phonenumber:str |None = None
    email:str
    CRP:str
    CPF:str
    CPNJ: str |None = None
    tipo: str |None = "Psicólogo"
    status: str | None = "Pendente"

class Admin(BaseModel):
    password:str
    phonenumber:str
    email:str
    CPF: str
    tipo: str |None = "Administrador"


usuario_admin = Admin(
    username="system",
    password="admin123",
    phonenumber="1234567890",  # Substitua pelo número real
    email="system@example.com",  # Substitua pelo email real
    CPF="123.456.789-00"  # Substitua pelo CPF real
)

# Convertendo para JSON
usuario_admin_json = dict(usuario_admin)
print(usuario_admin_json)





  


    
  


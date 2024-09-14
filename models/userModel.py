from pydantic import BaseModel

class User(BaseModel): 
    username: str
    password:str
    tipo: str


class Psicologo(BaseModel): 
    username: str
    password:str
    tipo: str |None = "Psicólogo"
    status: str | None = "pendente"



class Admin(BaseModel): 
    username: str
    password:str
    tipo: str |None = "Administrador"
  
   
    
  


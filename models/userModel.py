from pydantic import BaseModel

class User(BaseModel): 
    username: str
    password:str
    pokename:str
    pokeid:int
    poketype:str
    cep:str
    logradouro:str
    bairro:str
    estado:str
  


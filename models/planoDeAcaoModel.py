from pydantic import BaseModel

class PlanoDeAcao(BaseModel):
    email : str
    texto : str
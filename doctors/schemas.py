from pydantic import BaseModel
from typing import Union

class Doctor(BaseModel):
    name:str
    email:str
    specialization:str
    number:str
    imagepath:str
    available:str
    password:str

class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token : str
    token_data : str

class TokenData(BaseModel):
    email: Union[str, None] = None
    doc_id:int
    
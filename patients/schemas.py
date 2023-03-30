from pydantic import BaseModel
from typing import Optional

class Patient(BaseModel):
    name:str
    email:str
    number:str
    address:str
    password:str

class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token : str
    token_data : str

class TokenData(BaseModel):
    name : Optional[str] = None
    pat_id:int


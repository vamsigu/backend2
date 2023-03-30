from pydantic import BaseModel

class Admin(BaseModel):
    name:str
    age:int
    email:str
    address:str
    number:str
    password:str

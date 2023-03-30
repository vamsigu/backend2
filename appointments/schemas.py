from pydantic import BaseModel

class Appointment(BaseModel):
    pname:str
    age:int
    address:str
    dname:str
    specialization:str
    day:str
    slot:str
    pat_id:int
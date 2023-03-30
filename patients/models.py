from .database import Base
from sqlalchemy import Column,Integer,String

class Patient(Base):
    __tablename__ = "Patients"

    pat_id = Column(Integer,primary_key=True,index = True)
    name = Column(String(255))
    email = Column(String(255),unique=True)
    number = Column(String(255))
    address = Column(String(255))
    password = Column(String(255))


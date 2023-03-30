from .database import Base
from sqlalchemy import Column,Integer,String

class Doctor2(Base):
    __tablename__ = "Doctors"

    doc_id = Column(Integer,primary_key=True,index = True)
    name = Column(String(255))
    email = Column(String(255),unique=True)
    specialization = Column(String(255))
    number = Column(String(255))
    imagepath = Column(String(255))
    available = Column(String(255))
    password = Column(String(255))


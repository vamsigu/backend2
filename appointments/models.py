from .database import Base
from sqlalchemy import Column,Integer,String

class Appointment(Base):
    __tablename__ = "Appointments"

    appoint_id = Column(Integer,primary_key=True,index = True)
    pname = Column(String(255))
    age = Column(Integer)
    address = Column(String(255))
    dname = Column(String(255))
    specialization = Column(String(255))
    day = Column(String(255))
    slot = Column(String(255))
    pat_id=Column(Integer)
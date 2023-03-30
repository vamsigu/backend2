from .database import Base
from sqlalchemy import Column,Integer,String

class Admin(Base):
    __tablename__ = "Admin"

    admin_id = Column(Integer,primary_key=True,index = True)
    name = Column(String(255))
    age = Column(Integer)
    email = Column(String(255))
    address = Column(String(255))
    number = Column(String(255))
    password = Column(String(255))
    
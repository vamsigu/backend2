from .database import Base
from sqlalchemy import Column,Integer,String

class Member(Base):
    __tablename__ = "Members"

    member_id = Column(Integer,primary_key=True,index = True)
    pat_id = Column(Integer)
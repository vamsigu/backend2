from fastapi import FastAPI,Depends,status
from fastapi.middleware.cors import CORSMiddleware
from . import models,schemas
from .database import engine,SessionLocal
from sqlalchemy.orm import Session


models.Base.metadata.create_all(engine)

app=FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
origins = [
    "http://localhost:4200",
    "https://localhost:50",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/members', tags=["Members"])
def create_member(request:schemas.Member,db:Session=Depends(get_db)):
    new_member=models.Member(pat_id=request.pat_id)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    db.close()
    return new_member

@app.get('/members',tags=["Members"])
def get_member(db:Session=Depends(get_db)):
    members= db.query(models.Member).all()
    return members

@app.get('/members/{id}',tags=['Members'])
def get_member(id,db:Session=Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.member_id==id).first()
    return member

@app.put('/members/{id}',status_code=status.HTTP_202_ACCEPTED,tags = ['Members'])
def update(id,request : schemas.Member,db : Session = Depends(get_db)):
    db.query(models.Member).filter(models.Member.member_id == id).update(request.dict())
    db.commit()
    return 'updated' 

@app.delete('/members/{id}',status_code=status.HTTP_204_NO_CONTENT,tags = ['Members'])
def delete(id,db : Session = Depends(get_db)):
    db.query(models.Member).filter(models.Member.member_id == id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted'

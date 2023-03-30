from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models,schemas
from .database import SessionLocal,engine
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
    "https://localhost:90",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/admin')
def create_admin(request:schemas.Admin,db:Session=Depends(get_db)):
    new_admin=models.Admin(name=request.name,age=request.age,email=request.email,address=request.address,number=request.number,password=request.password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin

@app.get('/admin')
def get_admins(db:Session=Depends(get_db)):
    admins = db.query(models.Admin).all()
    return admins

@app.get('/admin/{id}')
def get_admin(id:int,db:Session=Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.admin_id==id).first()
    return admin
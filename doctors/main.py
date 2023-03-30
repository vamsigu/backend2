from fastapi import FastAPI,Depends,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import models,schemas,Oauth2,Token
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
    "http://localhost:60"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/doctors', tags=['Doctors'])
def create_doctor(request:schemas.Doctor, db:Session=Depends(get_db)):
    new_doctor=models.Doctor2(name=request.name,email=request.email,specialization=request.specialization,number=request.number,imagepath=request.imagepath,available=request.available,password=request.password)
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)
    return new_doctor

@app.get('/doctors/{doc_id}',tags = ['Doctors'])
def get_doctor(doc_id,db:Session =Depends(get_db)):
    doctor = db.query(models.Doctor2).filter(models.Doctor2.doc_id == doc_id).first()
    return doctor

@app.get('/doctors',tags = ['Doctors'])
def get(db:Session =Depends(get_db)):
    doctors = db.query(models.Doctor2).all()
    return doctors

@app.put('/doctors/{doc_id}',status_code=status.HTTP_202_ACCEPTED,tags = ['Doctors'])
def update(doc_id,request : schemas.Doctor,db : Session = Depends(get_db)):
    db.query(models.Doctor2).filter(models.Doctor2.doc_id == doc_id).update(request.dict())
    db.commit()
    return 'updated'

@app.delete('/doctors/{doc_id}',status_code=status.HTTP_204_NO_CONTENT,tags = ['Doctors'])
def delete(doc_id,db : Session = Depends(get_db)):
    db.query(models.Doctor2).filter(models.Doctor2.doc_id == doc_id).delete(synchronize_session=False)
    db.commit()
    return 'deleted'


@app.post('/login',tags=['Authentication'])
def login(request:schemas.Login,db:Session = Depends(get_db)):
    doctor = db.query(models.Doctor2).filter(models.Doctor2.email == request.username).first()
    if not doctor:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail=f'Invalid Credentials')

    access_token=Token.create_access_token(data={"subid":doctor.doc_id})
    current_user = Oauth2.get_current_user(access_token)
    return {"access_token": access_token}
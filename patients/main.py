from fastapi import FastAPI,Depends,status,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import models,schemas
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from . import Oauth2
from . import Token


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
    "https://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/patients' ,tags=['Patients'])
def create_patient(request : schemas.Patient,db : Session = Depends(get_db)):
    new_patient = models.Patient(name=request.name,email=request.email,password=request.password,number=request.number,address=request.address)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    db.close()
    return new_patient

@app.get('/patients/{pat_id}',tags = ['Patients'])
def get_patient(pat_id,db:Session =Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.pat_id == pat_id).first()
    return patient


@app.get('/patients',tags = ['Patients'])
def get(db:Session =Depends(get_db)):
    patients = db.query(models.Patient).all()
    return patients


@app.put('/patients/{pat_id}',status_code=status.HTTP_202_ACCEPTED,tags = ['Patients'])
def update(pat_id,request : schemas.Patient,db : Session = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.pat_id == pat_id).update(request.dict())
    db.commit()
    return 'updated' 

@app.delete('/patients/{pat_id}',status_code=status.HTTP_204_NO_CONTENT,tags = ['Patients'])
def delete(pat_id,db : Session = Depends(get_db)):
    db.query(models.Patient).filter(models.Patient.pat_id == pat_id).delete(synchronize_session=False)
    db.commit()
    return 'Done'

@app.post('/login',tags=['Authentication'])
def login(request:schemas.Login,db:Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.email == request.username).first()
    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail='Invalid Credentials')

    access_token=Token.create_access_token(data={"subid":patient.pat_id})
    current_user = Oauth2.get_current_user(access_token)
    return {"access_token":access_token}


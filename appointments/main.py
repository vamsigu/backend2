from fastapi import FastAPI,Depends,status
from fastapi.middleware.cors import CORSMiddleware
from . import models
from . import schemas
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
    "https://localhost:40",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post('/appointment',tags = ['Appointments'])
def create_appointment(request: schemas.Appointment,db : Session = Depends(get_db)):
     appoint = models.Appointment(pname=request.pname,age=request.age,address=request.address,dname=request.dname,specialization=request.specialization,slot=request.slot,day=request.day,pat_id=request.pat_id)
     db.add(appoint)
     db.commit()
     db.refresh(appoint)     
     return appoint

@app.get('/appointment',tags=['Appointments'])
def get_appointments(db:Session=Depends(get_db)):
    appointments=db.query(models.Appointment).all()
    return appointments

@app.get('/patientappointment/{pat_id}',tags=['Appointments'])
def get_appointment(pat_id,db:Session=Depends(get_db)):
    appointments = db.query(models.Appointment).filter(models.Appointment.pat_id==pat_id).all()
    return appointments

@app.get('/appointments/{doc}',tags=['Appointments'])
def get_appointment(doc,db:Session=Depends(get_db)):
    appointments = db.query(models.Appointment).filter(models.Appointment.dname==doc).all()
    return appointments

@app.get('/appointment/{app_id}',tags=['Appointments'])
def get_appointment(app_id,db:Session=Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.appoint_id==app_id).first()
    return appointment

@app.put('/appointment/{app_id}',tags=['Appointments'])
def update_appointment(app_id:int,request:schemas.Appointment,db:Session=Depends(get_db)):
    db.query(models.Appointment).filter(models.Appointment.appoint_id == app_id).update(request.dict())
    db.commit()
    return 'updated'

@app.delete('/appointment/{app_id}',tags=['Appointments'])
def delete_appointment(app_id:int,db:Session=Depends(get_db)):
    db.query(models.Appointment).filter(models.Appointment.appoint_id == app_id).delete(synchronize_session=False)
    db.commit()
    return 'Deleted'
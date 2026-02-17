from fastapi import FastAPI, HTTPException,status
from typing import Optional
from pydantic import BaseModel,EmailStr
from firebase_config import db

class Registration(BaseModel):
    name: str
    mail_id: EmailStr
    password: str

class Login(BaseModel):
    mail_id: EmailStr
    password: str

class Create_Task(BaseModel):
    mail:EmailStr
    task_name: str
    description: Optional[str]=None



app=FastAPI()

@app.post("/register",status_code=status.HTTP_201_CREATED)
def registration(user_reg : Registration):
    user_ref=db.collection("users").document(user_reg.mail_id)
    if user_ref.get().exists:
        raise HTTPException(status_code=400,detail="User aldready exist")
    user_ref.set({"name":user_reg.name,"password":user_reg.password})
    return {"message":"User created successfully"}


@app.post("/login")
def login(user_log:Login):
    user_ref=db.collection("users").document(user_log.mail_id)
    user=user_ref.get()
    if not user.exists:
        raise HTTPException(status_code=400,detail="user dont exists")
    user_data=user.to_dict()
    if user_log.password==user_data["password"]:
        return {"message":"login successfull"}



@app.post("/create_task")
def create_tast(task:Create_Task):
    user_ref=db.collection("users").document(task.mail).collection("tasks").document()
    user_ref.set({"name":task.task_name,"description":task.description,"status":"pending"})
    return {"message":"Task added successfully"}












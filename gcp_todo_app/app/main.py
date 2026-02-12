from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel,EmailStr

class Registration(BaseModel):
    name: str
    mail_id: EmailStr
    password: str

class Login(BaseModel):
    mail_id: EmailStr
    password: str

users={}


app=FastAPI()

@app.post("/register",status_code=status.HTTP_201_CREATED)
def registration(user_reg : Registration):
    if user_reg.mail_id in users:
        raise HTTPException(status_code=400,detail="User aldready exist")
    users[user_reg.mail_id]={"name":user_reg.name,"password":user_reg.password,"tasks":[]}
    return {"message":"User created successfully"}


@app.post("/login")
def login(user_log:Login):
    if user_log.mail_id in users and user_log.password==users[user_log.mail_id]["password"]:
        return {"message":"login successfull"}
    else:
        raise HTTPException(status_code=400,detail="invalid password")













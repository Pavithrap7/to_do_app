from fastapi import FastAPI, HTTPException,status
from typing import Optional
from pydantic import BaseModel,EmailStr
from app.firebase_config import get_db
db=get_db()

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
    else:
        raise HTTPException(status_code=401,detail="invalid password")



@app.post("/create_task")
def create_tast(task:Create_Task):
    try:
        user_ref=db.collection("users").document(task.mail).collection("tasks").document()
        user_ref.set({"name":task.task_name,"description":task.description,"status":"pending"})
        return {"message":"Task added successfully"}
    except Exception as err:
        return err
        

@app.get("/show_tasks/{mail_id}")
def show_task(mail_id:str):
    try:
        user_ref=db.collection("users").document(mail_id).collection("tasks")
        tasks=user_ref.stream()
        task=[]
        for i in tasks:
            task.append(i.to_dict())
        if not task:
            raise HTTPException(detail="no tasks found")
        return task
    except Exception as err:
        return err



@app.delete("/delete_task")
def delete_task(mail: str, task_name: str = None):
    """
    Delete tasks:
    - If task_name provided → delete that task only
    - Else → delete all tasks of that user
    """
    global tasks_db

    if mail not in tasks_db:
        raise HTTPException(status_code=404, detail="User not found")

    if task_name:
        # delete specific task
        original_count = len(tasks_db[mail])
        tasks_db[mail] = [t for t in tasks_db[mail] if t["name"] != task_name]
        deleted_count = original_count - len(tasks_db[mail])
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": f"Task '{task_name}' deleted for {mail}"}
    else:
        # delete all tasks of that user
        tasks_db[mail].clear()
        return {"message": f"All tasks deleted for {mail}"}








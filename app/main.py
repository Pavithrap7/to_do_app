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
def show_task(mail_id: str):
    """
    Returns all tasks for a user. If no tasks exist, returns an empty list.
    """
    try:
        tasks_ref = db.collection("users").document(mail_id).collection("tasks")
        tasks = [t.to_dict() for t in tasks_ref.stream()]
        return tasks  # will be [] if no tasks
    except Exception as err:
        return {"error": str(err)}


@app.delete("/delete_task")
def delete_task(mail: str, task_name: str = None):
    """
    Delete tasks for a user.
    - If task_name is provided: delete that specific task.
    - If task_name is None: delete all tasks.
    Returns a message even if no tasks exist.
    """
    tasks_ref = db.collection("users").document(mail).collection("tasks")
    tasks = list(tasks_ref.stream())

    if not tasks:
        return {"message": f"No tasks found for {mail}"}

    if task_name:
        deleted = False
        for t in tasks:
            if t.to_dict()["name"] == task_name:
                t.reference.delete()
                deleted = True
        if deleted:
            return {"message": f"Task '{task_name}' deleted for {mail}"}
        else:
            return {"message": f"Task '{task_name}' not found for {mail}"}
    else:
        for t in tasks:
            t.reference.delete()
        return {"message": f"All tasks deleted for {mail}"}



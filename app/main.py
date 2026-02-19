from fastapi import FastAPI, HTTPException, status
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.firebase_config import get_db

app = FastAPI()

# ====== DO NOT initialize DB here ======
# db = get_db()   <-- remove this line
db = None  # placeholder

# Initialize DB safely when FastAPI starts
@app.on_event("startup")
def startup_event():
    global db
    db = get_db()


# ====== Your Models ======
class Registration(BaseModel):
    name: str
    mail_id: EmailStr
    password: str

class Login(BaseModel):
    mail_id: EmailStr
    password: str

class Create_Task(BaseModel):
    mail: EmailStr
    task_name: str
    description: Optional[str] = None

# ====== Your Endpoints ======
@app.post("/register", status_code=status.HTTP_201_CREATED)
def registration(user_reg: Registration):
    if db is None:
        raise RuntimeError("Database not initialized")
    user_ref = db.collection("users").document(user_reg.mail_id)
    if user_ref.get().exists:
        raise HTTPException(status_code=400, detail="User already exists")
    user_ref.set({"name": user_reg.name, "password": user_reg.password})
    return {"message": "User created successfully"}

@app.post("/login")
def login(user_log: Login):
    if db is None:
        raise RuntimeError("Database not initialized")
    user_ref = db.collection("users").document(user_log.mail_id)
    user = user_ref.get()
    if not user.exists:
        raise HTTPException(status_code=400, detail="User does not exist")
    user_data = user.to_dict()
    if user_log.password == user_data["password"]:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid password")

@app.post("/create_task")
def create_task(task: Create_Task):
    if db is None:
        raise RuntimeError("Database not initialized")
    task_ref = db.collection("users").document(task.mail).collection("tasks").document()
    task_ref.set({"name": task.task_name, "description": task.description, "status": "pending"})
    return {"message": "Task added successfully"}


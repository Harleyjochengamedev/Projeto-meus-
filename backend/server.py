from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Header
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import httpx
from enum import Enum

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

EMERGENT_AUTH_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

# Enums
class TaskCategory(str, Enum):
    TASK = "task"
    STUDY = "study"
    PR = "pr"
    BUG = "bug"
    PROJECT = "project"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class SprintStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

class TimeEntryType(str, Enum):
    POMODORO = "pomodoro"
    MANUAL = "manual"

# Models
class UserSettings(BaseModel):
    pomodoro_duration: int = 25
    short_break: int = 5
    long_break: int = 15
    pomodoros_until_long_break: int = 4

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    settings: UserSettings = UserSettings()
    created_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: TaskCategory = TaskCategory.TASK
    priority: TaskPriority = TaskPriority.MEDIUM
    tags: List[str] = []
    estimated_time: Optional[int] = None
    sprint_id: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[TaskCategory] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    tags: Optional[List[str]] = None
    estimated_time: Optional[int] = None
    actual_time: Optional[int] = None
    sprint_id: Optional[str] = None

class Task(BaseModel):
    model_config = ConfigDict(extra="ignore")
    task_id: str
    user_id: str
    title: str
    description: Optional[str] = None
    category: TaskCategory
    priority: TaskPriority
    status: TaskStatus = TaskStatus.TODO
    tags: List[str] = []
    estimated_time: Optional[int] = None
    actual_time: int = 0
    sprint_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

class SprintCreate(BaseModel):
    name: str
    goal: Optional[str] = None
    start_date: datetime
    end_date: datetime

class Sprint(BaseModel):
    model_config = ConfigDict(extra="ignore")
    sprint_id: str
    user_id: str
    name: str
    goal: Optional[str] = None
    start_date: datetime
    end_date: datetime
    status: SprintStatus = SprintStatus.ACTIVE
    created_at: datetime

class TimeEntryCreate(BaseModel):
    task_id: str
    duration: int
    entry_type: TimeEntryType = TimeEntryType.MANUAL

class TimeEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    entry_id: str
    user_id: str
    task_id: str
    start_time: datetime
    end_time: datetime
    duration: int
    entry_type: TimeEntryType
    created_at: datetime

# Helper Functions
async def get_current_user(request: Request, authorization: Optional[str] = Header(None)) -> User:
    session_token = request.cookies.get("session_token")
    
    if not session_token and authorization:
        if authorization.startswith("Bearer "):
            session_token = authorization.replace("Bearer ", "")
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    session_doc = await db.user_sessions.find_one({"session_token": session_token}, {"_id": 0})
    if not session_doc:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    expires_at = session_doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired")
    
    user_doc = await db.users.find_one({"user_id": session_doc["user_id"]}, {"_id": 0})
    if not user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    if isinstance(user_doc.get("created_at"), str):
        user_doc["created_at"] = datetime.fromisoformat(user_doc["created_at"])
    
    return User(**user_doc)

# Auth Routes
@api_router.get("/")
async def root():
    return {"message": "DevFlow API", "status": "online"}

@api_router.post("/auth/callback")
async def auth_callback(session_id: str, response: Response):
    async with httpx.AsyncClient() as client:
        try:
            auth_response = await client.get(
                EMERGENT_AUTH_URL,
                headers={"X-Session-ID": session_id}
            )
            auth_response.raise_for_status()
            auth_data = auth_response.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to get session data: {str(e)}")
    
    session_token = auth_data.get("session_token")
    email = auth_data.get("email")
    name = auth_data.get("name")
    picture = auth_data.get("picture")
    
    existing_user = await db.users.find_one({"email": email}, {"_id": 0})
    
    if existing_user:
        user_id = existing_user["user_id"]
        await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"name": name, "picture": picture}}
        )
    else:
        user_id = f"user_{uuid.uuid4().hex[:12]}"
        user_doc = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
            "settings": UserSettings().model_dump(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(user_doc)
    
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    session_doc = {
        "session_token": session_token,
        "user_id": user_id,
        "expires_at": expires_at.isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.user_sessions.insert_one(session_doc)
    
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=7*24*60*60
    )
    
    user_data = await db.users.find_one({"user_id": user_id}, {"_id": 0})
    if isinstance(user_data.get("created_at"), str):
        user_data["created_at"] = datetime.fromisoformat(user_data["created_at"])
    
    return User(**user_data)

@api_router.get("/auth/me", response_model=User)
async def get_me(request: Request, authorization: Optional[str] = Header(None)):
    return await get_current_user(request, authorization)

@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})
    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out successfully"}

# Task Routes
@api_router.get("/tasks", response_model=List[Task])
async def get_tasks(
    request: Request,
    authorization: Optional[str] = Header(None),
    status: Optional[str] = None,
    category: Optional[str] = None,
    sprint_id: Optional[str] = None
):
    user = await get_current_user(request, authorization)
    
    query = {"user_id": user.user_id}
    if status:
        query["status"] = status
    if category:
        query["category"] = category
    if sprint_id:
        query["sprint_id"] = sprint_id
    
    tasks_cursor = db.tasks.find(query, {"_id": 0}).sort("created_at", -1)
    tasks = await tasks_cursor.to_list(length=1000)
    
    for task in tasks:
        if isinstance(task.get("created_at"), str):
            task["created_at"] = datetime.fromisoformat(task["created_at"])
        if isinstance(task.get("updated_at"), str):
            task["updated_at"] = datetime.fromisoformat(task["updated_at"])
        if task.get("completed_at") and isinstance(task["completed_at"], str):
            task["completed_at"] = datetime.fromisoformat(task["completed_at"])
    
    return [Task(**task) for task in tasks]

@api_router.post("/tasks", response_model=Task)
async def create_task(
    task_data: TaskCreate,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    task_id = f"task_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)
    
    task_doc = {
        "task_id": task_id,
        "user_id": user.user_id,
        **task_data.model_dump(),
        "status": TaskStatus.TODO.value,
        "actual_time": 0,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "completed_at": None
    }
    
    await db.tasks.insert_one(task_doc)
    
    task_doc["created_at"] = now
    task_doc["updated_at"] = now
    return Task(**task_doc)

@api_router.get("/tasks/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    task_doc = await db.tasks.find_one({"task_id": task_id, "user_id": user.user_id}, {"_id": 0})
    if not task_doc:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if isinstance(task_doc.get("created_at"), str):
        task_doc["created_at"] = datetime.fromisoformat(task_doc["created_at"])
    if isinstance(task_doc.get("updated_at"), str):
        task_doc["updated_at"] = datetime.fromisoformat(task_doc["updated_at"])
    if task_doc.get("completed_at") and isinstance(task_doc["completed_at"], str):
        task_doc["completed_at"] = datetime.fromisoformat(task_doc["completed_at"])
    
    return Task(**task_doc)

@api_router.put("/tasks/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    task_doc = await db.tasks.find_one({"task_id": task_id, "user_id": user.user_id}, {"_id": 0})
    if not task_doc:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = {k: v for k, v in task_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    if task_update.status == TaskStatus.DONE and task_doc.get("status") != TaskStatus.DONE.value:
        update_data["completed_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.tasks.update_one(
        {"task_id": task_id},
        {"$set": update_data}
    )
    
    updated_task = await db.tasks.find_one({"task_id": task_id}, {"_id": 0})
    if isinstance(updated_task.get("created_at"), str):
        updated_task["created_at"] = datetime.fromisoformat(updated_task["created_at"])
    if isinstance(updated_task.get("updated_at"), str):
        updated_task["updated_at"] = datetime.fromisoformat(updated_task["updated_at"])
    if updated_task.get("completed_at") and isinstance(updated_task["completed_at"], str):
        updated_task["completed_at"] = datetime.fromisoformat(updated_task["completed_at"])
    
    return Task(**updated_task)

@api_router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    result = await db.tasks.delete_one({"task_id": task_id, "user_id": user.user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}

# Sprint Routes
@api_router.get("/sprints", response_model=List[Sprint])
async def get_sprints(
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    sprints_cursor = db.sprints.find({"user_id": user.user_id}, {"_id": 0}).sort("created_at", -1)
    sprints = await sprints_cursor.to_list(length=100)
    
    for sprint in sprints:
        if isinstance(sprint.get("created_at"), str):
            sprint["created_at"] = datetime.fromisoformat(sprint["created_at"])
        if isinstance(sprint.get("start_date"), str):
            sprint["start_date"] = datetime.fromisoformat(sprint["start_date"])
        if isinstance(sprint.get("end_date"), str):
            sprint["end_date"] = datetime.fromisoformat(sprint["end_date"])
    
    return [Sprint(**sprint) for sprint in sprints]

@api_router.post("/sprints", response_model=Sprint)
async def create_sprint(
    sprint_data: SprintCreate,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    sprint_id = f"sprint_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc)
    
    sprint_doc = {
        "sprint_id": sprint_id,
        "user_id": user.user_id,
        **sprint_data.model_dump(),
        "status": SprintStatus.ACTIVE.value,
        "created_at": now.isoformat()
    }
    
    if isinstance(sprint_doc["start_date"], datetime):
        sprint_doc["start_date"] = sprint_doc["start_date"].isoformat()
    if isinstance(sprint_doc["end_date"], datetime):
        sprint_doc["end_date"] = sprint_doc["end_date"].isoformat()
    
    await db.sprints.insert_one(sprint_doc)
    
    sprint_doc["created_at"] = now
    sprint_doc["start_date"] = sprint_data.start_date
    sprint_doc["end_date"] = sprint_data.end_date
    
    return Sprint(**sprint_doc)

# Time Entry Routes
@api_router.post("/time-entries", response_model=TimeEntry)
async def create_time_entry(
    entry_data: TimeEntryCreate,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    task_doc = await db.tasks.find_one({"task_id": entry_data.task_id, "user_id": user.user_id}, {"_id": 0})
    if not task_doc:
        raise HTTPException(status_code=404, detail="Task not found")
    
    entry_id = f"entry_{uuid.uuid4().hex[:12]}"
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=entry_data.duration)
    
    entry_doc = {
        "entry_id": entry_id,
        "user_id": user.user_id,
        "task_id": entry_data.task_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration": entry_data.duration,
        "entry_type": entry_data.entry_type.value,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.time_entries.insert_one(entry_doc)
    
    # Update task actual_time
    await db.tasks.update_one(
        {"task_id": entry_data.task_id},
        {"$inc": {"actual_time": entry_data.duration}}
    )
    
    entry_doc["start_time"] = start_time
    entry_doc["end_time"] = end_time
    entry_doc["created_at"] = datetime.now(timezone.utc)
    
    return TimeEntry(**entry_doc)

@api_router.get("/time-entries")
async def get_time_entries(
    request: Request,
    authorization: Optional[str] = Header(None),
    date: Optional[str] = None
):
    user = await get_current_user(request, authorization)
    
    query = {"user_id": user.user_id}
    
    if date:
        date_obj = datetime.fromisoformat(date).replace(tzinfo=timezone.utc)
        start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        query["start_time"] = {"$gte": start_of_day.isoformat(), "$lt": end_of_day.isoformat()}
    
    entries_cursor = db.time_entries.find(query, {"_id": 0}).sort("created_at", -1)
    entries = await entries_cursor.to_list(length=1000)
    
    return entries

# Dashboard Routes
@api_router.get("/dashboard/overview")
async def get_dashboard_overview(
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    
    # Tasks today (due today or in progress)
    tasks_today = await db.tasks.count_documents({
        "user_id": user.user_id,
        "status": {"$ne": TaskStatus.DONE.value}
    })
    
    # Tasks completed today
    tasks_completed_today = await db.tasks.count_documents({
        "user_id": user.user_id,
        "status": TaskStatus.DONE.value,
        "completed_at": {"$gte": today.isoformat(), "$lt": tomorrow.isoformat()}
    })
    
    # Time entries today
    entries_today_cursor = db.time_entries.find({
        "user_id": user.user_id,
        "start_time": {"$gte": today.isoformat(), "$lt": tomorrow.isoformat()}
    }, {"_id": 0})
    entries_today = await entries_today_cursor.to_list(length=1000)
    total_time_today = sum(entry["duration"] for entry in entries_today)
    
    # Active sprints
    active_sprints = await db.sprints.count_documents({
        "user_id": user.user_id,
        "status": SprintStatus.ACTIVE.value
    })
    
    # Tasks by category
    tasks_by_category = {}
    for category in TaskCategory:
        count = await db.tasks.count_documents({
            "user_id": user.user_id,
            "category": category.value,
            "status": {"$ne": TaskStatus.DONE.value}
        })
        tasks_by_category[category.value] = count
    
    return {
        "tasks_today": tasks_today,
        "tasks_completed_today": tasks_completed_today,
        "total_time_today": total_time_today,
        "active_sprints": active_sprints,
        "tasks_by_category": tasks_by_category
    }

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
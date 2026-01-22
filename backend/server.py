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

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

EMERGENT_AUTH_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

# Models
class GamingProfile(BaseModel):
    games: List[str] = []
    platform: str = "PC"
    style: str = "Casual"
    communication: str = "Texto"
    tolerance: int = 3
    goal: str = "Diversão"

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    gaming_profile: Optional[GamingProfile] = None
    availability_schedule: Optional[Dict[str, List[str]]] = {}
    created_at: datetime

class ProfileUpdate(BaseModel):
    gaming_profile: GamingProfile
    availability_schedule: Optional[Dict[str, List[str]]] = {}

class Match(BaseModel):
    model_config = ConfigDict(extra="ignore")
    match_id: str
    user1_id: str
    user2_id: str
    compatibility_score: float
    reasons: List[str]
    status: str = "pending"
    created_at: datetime

class MatchAction(BaseModel):
    match_id: str
    action: str

class ChatMessage(BaseModel):
    message_id: str
    sender_id: str
    text: str
    timestamp: datetime

class Chat(BaseModel):
    model_config = ConfigDict(extra="ignore")
    chat_id: str
    match_id: str
    messages: List[ChatMessage] = []
    created_at: datetime

class MessageCreate(BaseModel):
    text: str

class Rating(BaseModel):
    model_config = ConfigDict(extra="ignore")
    rating_id: str
    rater_id: str
    rated_user_id: str
    communication: int
    respect: int
    teamwork: int
    created_at: datetime

class RatingCreate(BaseModel):
    rated_user_id: str
    communication: int = Field(ge=1, le=5)
    respect: int = Field(ge=1, le=5)
    teamwork: int = Field(ge=1, le=5)

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

def calculate_compatibility_score(user1: User, user2: User) -> tuple[float, List[str]]:
    score = 0.0
    reasons = []
    
    profile1 = user1.gaming_profile
    profile2 = user2.gaming_profile
    
    if not profile1 or not profile2:
        return 0.0, ["Perfis incompletos"]
    
    # Style match (35%)
    if profile1.style == profile2.style:
        score += 35.0
        reasons.append(f"Ambos jogam no estilo {profile1.style}")
    
    # Schedule overlap (25%)
    schedule1 = user1.availability_schedule or {}
    schedule2 = user2.availability_schedule or {}
    overlap_count = 0
    total_slots = 0
    for day in schedule1:
        if day in schedule2:
            slots1 = set(schedule1[day])
            slots2 = set(schedule2[day])
            overlap = slots1.intersection(slots2)
            overlap_count += len(overlap)
            total_slots += max(len(slots1), len(slots2))
    
    if total_slots > 0:
        schedule_score = (overlap_count / total_slots) * 25.0
        score += schedule_score
        if overlap_count > 0:
            reasons.append(f"Horários compatíveis ({overlap_count} slots)")
    
    # Communication match (20%)
    if profile1.communication == profile2.communication:
        score += 20.0
        reasons.append(f"Comunicação via {profile1.communication}")
    
    # Tolerance compatibility (20%)
    tolerance_diff = abs(profile1.tolerance - profile2.tolerance)
    tolerance_score = max(0, 20.0 - (tolerance_diff * 4))
    score += tolerance_score
    if tolerance_diff <= 1:
        reasons.append("Nível de tolerância similar")
    
    return round(score, 1), reasons

# Auth Routes
@api_router.get("/auth/google")
async def auth_google(redirect_url: str):
    emergent_auth_url = f"https://auth.emergentagent.com/?redirect={redirect_url}"
    return {"auth_url": emergent_auth_url}

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
            "gaming_profile": None,
            "availability_schedule": {},
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

# Profile Routes
@api_router.get("/profile", response_model=User)
async def get_profile(request: Request, authorization: Optional[str] = Header(None)):
    return await get_current_user(request, authorization)

@api_router.put("/profile")
async def update_profile(
    profile_update: ProfileUpdate,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    user = await get_current_user(request, authorization)
    
    update_data = {
        "gaming_profile": profile_update.gaming_profile.model_dump(),
        "availability_schedule": profile_update.availability_schedule or {}
    }
    
    await db.users.update_one(
        {"user_id": user.user_id},
        {"$set": update_data}
    )
    
    updated_user = await db.users.find_one({"user_id": user.user_id}, {"_id": 0})
    if isinstance(updated_user.get("created_at"), str):
        updated_user["created_at"] = datetime.fromisoformat(updated_user["created_at"])
    
    return User(**updated_user)

# Matchmaking Routes
@api_router.get("/matches", response_model=List[Dict[str, Any]])
async def get_matches(
    request: Request,
    authorization: Optional[str] = Header(None),
    limit: int = 20
):
    current_user = await get_current_user(request, authorization)
    
    if not current_user.gaming_profile:
        return []
    
    # Get other users with profiles
    other_users_cursor = db.users.find(
        {
            "user_id": {"$ne": current_user.user_id},
            "gaming_profile": {"$ne": None}
        },
        {"_id": 0}
    ).limit(limit)
    
    other_users = await other_users_cursor.to_list(length=limit)
    
    matches = []
    for user_doc in other_users:
        if isinstance(user_doc.get("created_at"), str):
            user_doc["created_at"] = datetime.fromisoformat(user_doc["created_at"])
        
        other_user = User(**user_doc)
        score, reasons = calculate_compatibility_score(current_user, other_user)
        
        existing_match = await db.matches.find_one({
            "$or": [
                {"user1_id": current_user.user_id, "user2_id": other_user.user_id},
                {"user1_id": other_user.user_id, "user2_id": current_user.user_id}
            ]
        }, {"_id": 0})
        
        if existing_match and existing_match.get("status") != "pending":
            continue
        
        matches.append({
            "user": other_user.model_dump(),
            "compatibility_score": score,
            "reasons": reasons,
            "match_id": existing_match["match_id"] if existing_match else None
        })
    
    matches.sort(key=lambda x: x["compatibility_score"], reverse=True)
    return matches

@api_router.post("/matches/action")
async def match_action(
    action_data: MatchAction,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    current_user = await get_current_user(request, authorization)
    match_id = action_data.match_id
    action = action_data.action
    
    if action not in ["like", "skip"]:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    existing_match = await db.matches.find_one({"match_id": match_id}, {"_id": 0})
    
    if not existing_match:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if action == "skip":
        await db.matches.update_one(
            {"match_id": match_id},
            {"$set": {"status": "rejected"}}
        )
        return {"message": "Match rejected"}
    
    if action == "like":
        await db.matches.update_one(
            {"match_id": match_id},
            {"$set": {"status": "accepted"}}
        )
        
        chat_id = f"chat_{uuid.uuid4().hex[:12]}"
        chat_doc = {
            "chat_id": chat_id,
            "match_id": match_id,
            "messages": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.chats.insert_one(chat_doc)
        
        return {"message": "Match accepted", "chat_id": chat_id}

@api_router.post("/matches/create")
async def create_match(
    other_user_id: str,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    current_user = await get_current_user(request, authorization)
    
    other_user_doc = await db.users.find_one({"user_id": other_user_id}, {"_id": 0})
    if not other_user_doc:
        raise HTTPException(status_code=404, detail="User not found")
    
    if isinstance(other_user_doc.get("created_at"), str):
        other_user_doc["created_at"] = datetime.fromisoformat(other_user_doc["created_at"])
    
    other_user = User(**other_user_doc)
    score, reasons = calculate_compatibility_score(current_user, other_user)
    
    match_id = f"match_{uuid.uuid4().hex[:12]}"
    match_doc = {
        "match_id": match_id,
        "user1_id": current_user.user_id,
        "user2_id": other_user_id,
        "compatibility_score": score,
        "reasons": reasons,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.matches.insert_one(match_doc)
    
    return {"match_id": match_id, "compatibility_score": score, "reasons": reasons}

# Chat Routes
@api_router.get("/chats/{match_id}", response_model=Chat)
async def get_chat(
    match_id: str,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    current_user = await get_current_user(request, authorization)
    
    match_doc = await db.matches.find_one({"match_id": match_id}, {"_id": 0})
    if not match_doc:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if current_user.user_id not in [match_doc["user1_id"], match_doc["user2_id"]]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    chat_doc = await db.chats.find_one({"match_id": match_id}, {"_id": 0})
    if not chat_doc:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    if isinstance(chat_doc.get("created_at"), str):
        chat_doc["created_at"] = datetime.fromisoformat(chat_doc["created_at"])
    
    for msg in chat_doc.get("messages", []):
        if isinstance(msg.get("timestamp"), str):
            msg["timestamp"] = datetime.fromisoformat(msg["timestamp"])
    
    return Chat(**chat_doc)

@api_router.post("/chats/{match_id}/message")
async def send_message(
    match_id: str,
    message: MessageCreate,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    current_user = await get_current_user(request, authorization)
    
    match_doc = await db.matches.find_one({"match_id": match_id}, {"_id": 0})
    if not match_doc:
        raise HTTPException(status_code=404, detail="Match not found")
    
    if current_user.user_id not in [match_doc["user1_id"], match_doc["user2_id"]]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    message_id = f"msg_{uuid.uuid4().hex[:12]}"
    new_message = {
        "message_id": message_id,
        "sender_id": current_user.user_id,
        "text": message.text,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    await db.chats.update_one(
        {"match_id": match_id},
        {"$push": {"messages": new_message}}
    )
    
    return new_message

# Rating Routes
@api_router.post("/ratings")
async def create_rating(
    rating_data: RatingCreate,
    request: Request,
    authorization: Optional[str] = Header(None)
):
    current_user = await get_current_user(request, authorization)
    
    rated_user = await db.users.find_one({"user_id": rating_data.rated_user_id}, {"_id": 0})
    if not rated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    rating_id = f"rating_{uuid.uuid4().hex[:12]}"
    rating_doc = {
        "rating_id": rating_id,
        "rater_id": current_user.user_id,
        "rated_user_id": rating_data.rated_user_id,
        "communication": rating_data.communication,
        "respect": rating_data.respect,
        "teamwork": rating_data.teamwork,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.ratings.insert_one(rating_doc)
    
    return {"rating_id": rating_id, "message": "Rating submitted"}

@api_router.get("/ratings/{user_id}")
async def get_user_ratings(user_id: str):
    ratings_cursor = db.ratings.find({"rated_user_id": user_id}, {"_id": 0})
    ratings = await ratings_cursor.to_list(length=100)
    
    if not ratings:
        return {
            "user_id": user_id,
            "average_communication": 0,
            "average_respect": 0,
            "average_teamwork": 0,
            "total_ratings": 0
        }
    
    total = len(ratings)
    avg_comm = sum(r["communication"] for r in ratings) / total
    avg_resp = sum(r["respect"] for r in ratings) / total
    avg_team = sum(r["teamwork"] for r in ratings) / total
    
    return {
        "user_id": user_id,
        "average_communication": round(avg_comm, 1),
        "average_respect": round(avg_resp, 1),
        "average_teamwork": round(avg_team, 1),
        "total_ratings": total
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
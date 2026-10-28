"""
L11 — Streamlit + FastAPI: Backend  (STARTER)
===============================================
Run with (once implemented):
    uvicorn backend:app --reload --port 8000

Your goal: build an authenticated task API.

Endpoints to implement:
    POST /auth/token           — accept username+password, return {"access_token": ..., "username": ...}
    GET  /tasks                — return the current user's tasks (auth required)
    POST /tasks                — create a task for the current user (auth required)
    PATCH /tasks/{id}/complete — mark a task as done (auth required)

Authentication scheme:
    • For simplicity, encode the token as base64-encoded JSON:
        import base64, json
        payload = json.dumps({"sub": username})
        token = base64.b64encode(payload.encode()).decode()
    • Clients send: Authorization: Bearer <token>
    • Use FastAPI's HTTPBearer security scheme to extract the token

Data storage:
    • In-memory dicts: TASKS (username → list of tasks), NEXT_IDS (username → int)
    • No database needed
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime
import base64, json

app = FastAPI(title="Task API with Auth")

# TODO: Add CORSMiddleware with allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

security = HTTPBearer()

# ── In-memory data ────────────────────────────────────────────────────────────
# TODO: Create a USERS dict: {username: password} with at least "demo": "demo"
USERS = {"demo":"DeMo","Vicky":"Password"}

# TODO: Create TASKS dict: {username: [list of task dicts]}
# TODO: Create NEXT_IDS dict: {username: int} for auto-increment IDs
TASKS: dict[str, list] = {
    "Vicky": [
        {"id": 1, "title": "Complete Module 5 Final", "done": False},
        {"id": 2, "title": "Complete Module 6 Final", "done": False},
        {"id": 3, "title": "Complete Module 3 Final", "done": True},
        {"id": 4, "title": "Complete Module 6.13 Homework", "done": False},
    ],
    "demo": []
}

NEXT_IDS: dict[str, int] = {
    "Vicky": 5,
    "demo": 1
}
# ── Request body models ───────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str

# ── Token helpers ─────────────────────────────────────────────────────────────
# TODO: Implement make_token(username) → str
#   Encode {"sub": username} as base64 JSON
def make_token(username: str) -> str:
    payload = json.dumps({"sub": username})
    token = base64.b64encode(payload.encode()).decode()
    return token

# TODO: Implement decode_token(token) → str
#   Decode base64 JSON → return username, raise HTTPException(401) if invalid
def decode_token(token: str) -> str:
    try:
        payload = base64.b64decode(token, validate=True).decode()
        data = json.loads(payload)
        username = data["sub"]

        if not isinstance(username, str) or username not in USERS:
            raise ValueError("Invalid username")

        return username

    except (ValueError, KeyError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"}
        )

# ── Auth dependency ───────────────────────────────────────────────────────────
# TODO: Implement get_current_user(credentials) → str
#   Use decode_token on credentials.credentials
#   Raise 401 if username not in USERS
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    username = decode_token(credentials.credentials)

    if username not in USERS:
        raise HTTPException(
            status_code=401,
            detail="Invalid user"
        )

    return username

# ── Routes ────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class TaskCreate(BaseModel):
    title: str

# TODO: POST /auth/token
#   - Check username + password against USERS
#   - Raise HTTPException(401) if wrong
#   - Call TASKS.setdefault and NEXT_IDS.setdefault to initialise data for new users
#   - Return {"access_token": make_token(username), "token_type": "bearer", "username": username}
@app.post("/auth/token")
def login(body: LoginRequest):
    if USERS.get(body.username) != body.password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )

    TASKS.setdefault(body.username, [])
    NEXT_IDS.setdefault(body.username, 1)

    return {
        "access_token": make_token(body.username),
        "token_type": "bearer",
        "username": body.username
    }

# TODO: GET /tasks — protected with Depends(get_current_user)
#   Return TASKS.get(username, [])
@app.get("/tasks")
def get_tasks(username: str = Depends(get_current_user)):
    return TASKS.get(username, [])


# TODO: POST /tasks — protected
#   Create a task dict {id, title, done: False, created_at}
#   Append to TASKS[username], increment NEXT_IDS[username], return the task
@app.post("/tasks", status_code=201)
def create_task(body: TaskCreate, username: str = Depends(get_current_user)):
    task = {
        "id": NEXT_IDS.setdefault(username, 1),
        "title": body.title,
        "done": False,
        "created_at": datetime.now().isoformat()
    }

    TASKS.setdefault(username, []).append(task)
    NEXT_IDS[username] += 1

    return task


# TODO: PATCH /tasks/{task_id}/complete — protected
#   Find the task, set done=True, return it
#   Raise HTTPException(404) if not found
@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int, username: str = Depends(get_current_user)):
    for task in TASKS.get(username, []):
        if task["id"] == task_id:
            task["done"] = True
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


@app.get("/")
def root():
    return {"message": "Backend is running. Visit /docs for interactive API docs."}
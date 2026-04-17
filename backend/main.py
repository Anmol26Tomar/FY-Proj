from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from sqlalchemy.orm import Session

# We import the real LangGraph logic from our src tree instead of the old mock
from src.graph import perform_research
from src.database import SessionLocal, User
from src.auth import verify_password, get_password_hash, create_access_token

app = FastAPI(title="Scholar-Agent API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    query: str
    draft: str
    logs: List[str]

class UserSignup(BaseModel):
    full_name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Scholar-Agent Backend (LangGraph Enabled) is Running"}

@app.post("/api/research", response_model=ResearchResponse)
async def start_research(request: ResearchRequest):
    # This invokes our LangGraph state machine utilizing ArXiv + dummy LLMs
    result = perform_research(request.query)
    
    return ResearchResponse(
        query=result["query"],
        draft=result["draft"],
        logs=result.get("logs", [])
    )

@app.post("/api/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token({"sub": new_user.email, "name": new_user.full_name})
    return {"access_token": token, "token_type": "bearer", "user": {"email": user.email, "name": user.full_name}}

@app.post("/api/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": db_user.email, "name": db_user.full_name})
    return {"access_token": token, "token_type": "bearer", "user": {"email": db_user.email, "name": db_user.full_name}}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

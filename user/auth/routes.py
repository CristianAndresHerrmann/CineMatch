from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User
from schemas.user import UserCreate, UserOut
from schemas.auth import LoginRequest, LoginResponse
from auth.utils import hash_password, verify_password, create_access_token
from uuid import uuid4

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    import sys
    print(f"[DEBUG] type(user): {type(user)}", file=sys.stderr)
    print(f"[DEBUG] user: {user}", file=sys.stderr)
    if hasattr(user, 'password'):
        print(f"[DEBUG] user.password: {user.password}", file=sys.stderr)
    else:
        print("[DEBUG] user has no attribute 'password'", file=sys.stderr)
    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="Password must not exceed 72 characters.")
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=409, detail="Username or email already exists")
    db_user = User(id=uuid4(), username=user.username, email=user.email, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return LoginResponse(access_token=token, user_id=str(user.id))

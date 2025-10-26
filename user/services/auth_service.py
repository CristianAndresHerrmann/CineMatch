from sqlalchemy.orm import Session
from db.models import User
from auth.utils import hash_password, verify_password, create_access_token
from schemas.user import UserCreate
from schemas.auth import LoginRequest, LoginResponse
from fastapi import HTTPException
from uuid import uuid4


def register_user(user: UserCreate, db: Session) -> User:
    if len(user.password) > 72:
        raise HTTPException(status_code=400, detail="Password must not exceed 72 characters.")
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=409, detail="Username or email already exists")
    db_user = User(id=uuid4(), username=user.username,
                email=user.email, password_hash=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(request: LoginRequest, db: Session) -> LoginResponse:
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return LoginResponse(access_token=token, user_id=str(user.id))

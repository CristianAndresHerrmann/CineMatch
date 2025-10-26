
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import User
from schemas.user import UserOut, UserPreferences
from services.user_service import update_user_preferences, get_user_preferences
from core.dependencies import get_db, get_current_user

router = APIRouter()

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/me/preferences", response_model=UserPreferences)
def get_preferences(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    genres = get_user_preferences(current_user, db)
    return UserPreferences(genres=genres)

@router.put("/me/preferences", response_model=UserPreferences)
def update_preferences(preferences: UserPreferences, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    update_user_preferences(current_user, preferences, db)
    return preferences

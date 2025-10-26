from sqlalchemy.orm import Session
from db.models import User, UserGenre
from schemas.user import UserPreferences
from fastapi import HTTPException

def update_user_preferences(user: User, preferences: UserPreferences, db: Session) -> User:
    # Elimina preferencias anteriores
    db.query(UserGenre).filter(UserGenre.user_id == user.id).delete()
    # Agrega nuevas preferencias
    for genre in preferences.genres:
        db.add(UserGenre(user_id=user.id, genre=genre))
    db.commit()
    db.refresh(user)
    return user

def get_user_preferences(user: User, db: Session) -> list:
    return [g.genre for g in db.query(UserGenre).filter(UserGenre.user_id == user.id).all()]

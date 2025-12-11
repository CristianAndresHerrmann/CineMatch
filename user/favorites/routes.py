from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import User
from schemas.favorites import UserFavorites
from core.dependencies import get_db, get_current_user
from services.favorites_service import (
    get_user_favorites,
    add_favorite_movie,
    remove_favorite_movie
)

router = APIRouter()

@router.get("/me/favorites", response_model=UserFavorites)
def get_favorites(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    movie_ids = get_user_favorites(current_user, db)
    return UserFavorites(movie_ids=movie_ids)

@router.post("/me/favorites", response_model=UserFavorites)
def add_favorite(favorites: UserFavorites, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    add_favorite_movie(current_user, favorites, db)
    movie_ids = get_user_favorites(current_user, db)
    return UserFavorites(movie_ids=movie_ids)

@router.delete("/me/favorites", response_model=UserFavorites)
def remove_favorite(favorites: UserFavorites, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    remove_favorite_movie(current_user, favorites, db)
    movie_ids = get_user_favorites(current_user, db)
    return UserFavorites(movie_ids=movie_ids)

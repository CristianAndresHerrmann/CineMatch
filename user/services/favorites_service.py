from sqlalchemy.orm import Session
from db.models import User, UserFavorite
from schemas.favorites import UserFavorites
from fastapi import HTTPException

def get_user_favorites(user: User, db: Session) -> list:
    return [f.movie_id for f in db.query(UserFavorite).filter(UserFavorite.user_id == user.id).all()]

def add_favorite_movie(user: User, favorites: UserFavorites, db: Session):
    for movie_id in favorites.movie_ids:
        exists = db.query(UserFavorite).filter_by(user_id=user.id, movie_id=movie_id).first()
        if not exists:
            db.add(UserFavorite(user_id=user.id, movie_id=movie_id))
    db.commit()

def remove_favorite_movie(user: User, favorites: UserFavorites, db: Session):
    for movie_id in favorites.movie_ids:
        fav = db.query(UserFavorite).filter_by(user_id=user.id, movie_id=movie_id).first()
        if fav:
            db.delete(fav)
    db.commit()

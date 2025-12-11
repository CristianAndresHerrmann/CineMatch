import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User, UserFavorite, UserWatched
from auth.utils import hash_password
import uuid

# Películas de ejemplo (IDs que deben existir en el microservicio de catalog)
MOVIE_IDS = [1, 2, 3, 4, 5]

USERS = [
    {
        "id": uuid.uuid4(),
        "username": "alice",
        "email": "alice@email.com",
        "password": "alice1234",
        "favorites": [1, 2],
        "watched": [1, 3, 5]
    },
    {
        "id": uuid.uuid4(),
        "username": "bob",
        "email": "bob@email.com",
        "password": "bob1234",
        "favorites": [2, 3, 4],
        "watched": [2, 4]
    },
    {
        "id": uuid.uuid4(),
        "username": "carol",
        "email": "carol@email.com",
        "password": "carol1234",
        "favorites": [5],
        "watched": [1, 2, 3, 4, 5]
    }
]


def seed():
    db: Session = SessionLocal()
    try:
        db.query(UserWatched).delete()
        db.query(UserFavorite).delete()
        db.query(User).delete()
        db.commit()
        for u in USERS:
            user = User(
                id=u["id"],
                username=u["username"],
                email=u["email"],
                password_hash=hash_password(u["password"])
            )
            db.add(user)
            db.commit()
            for movie_id in u["favorites"]:
                db.add(UserFavorite(user_id=user.id, movie_id=movie_id))
            for movie_id in u["watched"]:
                db.add(UserWatched(user_id=user.id, movie_id=movie_id))
            db.commit()
        print("Usuarios, favoritos y películas vistas cargados correctamente.")
    finally:
        db.close()

if __name__ == "__main__":
    seed()

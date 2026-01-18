import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import User, UserFavorite, UserWatched, UserGenre
from auth.utils import hash_password
import uuid

# NOTA: Estos IDs deben corresponder a películas que existan en el catálogo
# El catálogo usa IDs en formato "tmdb:XXXXX" (strings)
# Pero en la base de datos de usuarios guardamos solo el número (integer)
# Por ejemplo: "tmdb:1090991" -> guardamos 1090991

USERS = [
    {
        "id": uuid.uuid4(),
        "username": "alice",
        "email": "alice@email.com",
        "password": "alice1234",
        "favorites": [1090991, 1091043],  # IDs reales del catálogo
        "watched": [1182487, 1193824, 1245562],
        "genres": ["Action", "Sci-Fi", "Adventure"]
    },
    {
        "id": uuid.uuid4(),
        "username": "bob",
        "email": "bob@email.com",
        "password": "bob1234",
        "favorites": [1299039, 1370217, 1374686],
        "watched": [1465549, 1468057],
        "genres": ["Comedy", "Drama", "Romance"]
    },
    {
        "id": uuid.uuid4(),
        "username": "carol",
        "email": "carol@email.com",
        "password": "carol1234",
        "favorites": [1505291],
        "watched": [1531018, 1531026, 1534291, 1538573, 1547221],
        "genres": ["Horror", "Thriller", "Mystery", "Sci-Fi"]
    }
]


def seed():
    db: Session = SessionLocal()
    try:
        # Limpiar datos existentes en orden correcto (por las foreign keys)
        db.query(UserGenre).delete()
        db.query(UserWatched).delete()
        db.query(UserFavorite).delete()
        db.query(User).delete()
        db.commit()
        
        print("🗑️  Datos anteriores eliminados")
        
        # Crear usuarios con sus datos relacionados
        for u in USERS:
            # Crear usuario
            user = User(
                id=u["id"],
                username=u["username"],
                email=u["email"],
                password_hash=hash_password(u["password"])
            )
            db.add(user)
            db.commit()
            
            # Agregar favoritos
            for movie_id in u["favorites"]:
                db.add(UserFavorite(user_id=user.id, movie_id=movie_id))
            
            # Agregar películas vistas
            for movie_id in u["watched"]:
                db.add(UserWatched(user_id=user.id, movie_id=movie_id))
            
            # Agregar preferencias de género
            for genre in u.get("genres", []):
                db.add(UserGenre(user_id=user.id, genre=genre))
            
            db.commit()
            
            print(f"✅ Usuario '{user.username}' creado con {len(u['favorites'])} favoritos, {len(u['watched'])} vistas, {len(u.get('genres', []))} géneros")
        
        print("\n🎉 Seed completado exitosamente!")
        print(f"📊 Total: {len(USERS)} usuarios creados")
        
    except Exception as e:
        print(f"❌ Error durante el seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()

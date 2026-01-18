from sqlalchemy.orm import Session
from db.models import User, UserWatched
from schemas.watched import UserWatched as UserWatchedSchema, EnrichedWatched, MovieInfo
from services.catalog_client import catalog_client
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def get_user_watched(user: User, db: Session) -> list:
    """Obtiene la lista de IDs de películas vistas por el usuario"""
    return [w.movie_id for w in db.query(UserWatched).filter(UserWatched.user_id == user.id).all()]

async def get_user_watched_enriched(user: User, db: Session) -> EnrichedWatched:
    """
    Obtiene la lista de películas vistas enriquecida con información completa.
    Consulta el microservicio de Catálogo para cada película.
    """
    movie_ids = get_user_watched(user, db)
    
    if not movie_ids:
        return EnrichedWatched(
            movie_ids=[],
            movies=[],
            total=0,
            enriched=0
        )
    
    # Obtener información completa de las películas del catálogo
    movies_data = await catalog_client.get_movies_batch(movie_ids)
    
    # Convertir a MovieInfo objects
    movies = []
    for movie_id in movie_ids:
        if movie_id in movies_data:
            movie_data = movies_data[movie_id]
            try:
                movies.append(MovieInfo(
                    id=str(movie_data.get("_id", "")),
                    titulo=movie_data.get("titulo", "Título no disponible"),
                    titulo_original=movie_data.get("titulo_original"),
                    sinopsis=movie_data.get("sinopsis"),
                    anio=movie_data.get("anio"),
                    director=movie_data.get("director"),
                    generos=movie_data.get("generos", []),
                    calificacion_promedio=movie_data.get("calificacion_promedio"),
                    url_portada=movie_data.get("url_portada"),
                    duracion_minutos=movie_data.get("duracion_minutos"),
                    idioma_original=movie_data.get("idioma_original"),
                    tmdb_id=movie_data.get("tmdb_id")
                ))
            except Exception as e:
                logger.error(f"Error al procesar película {movie_id}: {e}")
    
    return EnrichedWatched(
        movie_ids=movie_ids,
        movies=movies,
        total=len(movie_ids),
        enriched=len(movies)
    )

def add_watched_movie(user: User, watched: UserWatchedSchema, db: Session):
    """Agrega películas a la lista de vistas del usuario"""
    for movie_id in watched.movie_ids:
        exists = db.query(UserWatched).filter_by(user_id=user.id, movie_id=movie_id).first()
        if not exists:
            db.add(UserWatched(user_id=user.id, movie_id=movie_id))
    db.commit()

def remove_watched_movie(user: User, watched: UserWatchedSchema, db: Session):
    """Elimina películas de la lista de vistas del usuario"""
    for movie_id in watched.movie_ids:
        watched_item = db.query(UserWatched).filter_by(user_id=user.id, movie_id=movie_id).first()
        if watched_item:
            db.delete(watched_item)
    db.commit()

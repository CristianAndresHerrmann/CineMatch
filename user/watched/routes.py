from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import User
from schemas.watched import UserWatched, EnrichedWatched
from core.dependencies import get_db, get_current_user
from services.watched_service import (
    get_user_watched_enriched,
    add_watched_movie,
    remove_watched_movie
)

router = APIRouter()

@router.get("/me/watched", response_model=EnrichedWatched)
async def get_watched(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtiene la lista de películas vistas por el usuario autenticado con información completa.
    
    Consulta el microservicio de Catálogo para enriquecer cada película con:
    - Título, sinopsis, año, director
    - Géneros, calificación, portada
    - Duración, idioma original, TMDb ID
    
    Returns:
        EnrichedWatched: Lista enriquecida con información completa de películas
    """
    return await get_user_watched_enriched(current_user, db)

@router.post("/me/watched", response_model=EnrichedWatched)
async def add_watched(watched: UserWatched, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Agrega películas a la lista de vistas del usuario autenticado.
    
    Args:
        watched: Lista de IDs de películas a agregar
        
    Returns:
        EnrichedWatched: Lista actualizada con información completa de películas
    """
    add_watched_movie(current_user, watched, db)
    return await get_user_watched_enriched(current_user, db)

@router.delete("/me/watched", response_model=EnrichedWatched)
async def remove_watched(watched: UserWatched, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Elimina películas de la lista de vistas del usuario autenticado.
    
    Args:
        watched: Lista de IDs de películas a eliminar
        
    Returns:
        EnrichedWatched: Lista actualizada con información completa de películas
    """
    remove_watched_movie(current_user, watched, db)
    return await get_user_watched_enriched(current_user, db)

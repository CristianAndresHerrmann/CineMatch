from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import User
from schemas.favorites import UserFavorites, EnrichedFavorites
from core.dependencies import get_db, get_current_user
from services.favorites_service import (
    get_user_favorites_enriched,
    add_favorite_movie,
    remove_favorite_movie
)

router = APIRouter()

@router.get("/me/favorites", response_model=EnrichedFavorites)
async def get_favorites(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Obtiene la lista de películas favoritas del usuario autenticado con información completa.
    
    Consulta el microservicio de Catálogo para enriquecer cada película con:
    - Título, sinopsis, año, director
    - Géneros, calificación, portada
    - Duración, idioma original, TMDb ID
    
    Returns:
        EnrichedFavorites: Lista enriquecida con información completa de películas
    """
    return await get_user_favorites_enriched(current_user, db)

@router.post("/me/favorites", response_model=EnrichedFavorites)
async def add_favorite(favorites: UserFavorites, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Agrega películas a la lista de favoritos del usuario autenticado.
    
    Args:
        favorites: Lista de IDs de películas a agregar
        
    Returns:
        EnrichedFavorites: Lista actualizada con información completa de películas
    """
    add_favorite_movie(current_user, favorites, db)
    return await get_user_favorites_enriched(current_user, db)

@router.delete("/me/favorites", response_model=EnrichedFavorites)
async def remove_favorite(favorites: UserFavorites, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Elimina películas de la lista de favoritos del usuario autenticado.
    
    Args:
        favorites: Lista de IDs de películas a eliminar
        
    Returns:
        EnrichedFavorites: Lista actualizada con información completa de películas
    """
    remove_favorite_movie(current_user, favorites, db)
    return await get_user_favorites_enriched(current_user, db)

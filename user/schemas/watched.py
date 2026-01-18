from pydantic import BaseModel
from typing import List, Optional

class UserWatched(BaseModel):
    """Schema básico con solo IDs"""
    movie_ids: List[int]

class MovieInfo(BaseModel):
    """Información completa de una película del catálogo"""
    id: str  # MongoDB ObjectId
    titulo: str
    titulo_original: Optional[str] = None
    sinopsis: Optional[str] = None
    anio: Optional[int] = None
    director: Optional[str] = None
    generos: List[str] = []
    calificacion_promedio: Optional[float] = None
    url_portada: Optional[str] = None
    duracion_minutos: Optional[int] = None
    idioma_original: Optional[str] = None
    tmdb_id: Optional[int] = None

class EnrichedWatched(BaseModel):
    """Schema enriquecido con información completa de películas"""
    movie_ids: List[int]
    movies: List[MovieInfo] = []
    total: int
    enriched: int  # Cuántas películas se pudieron enriquecer

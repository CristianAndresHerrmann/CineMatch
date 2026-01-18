import httpx
from typing import Optional, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)

class CatalogClient:
    """Cliente HTTP para comunicarse con el microservicio de Catálogo"""
    
    def __init__(self, base_url: Optional[str] = None):
        # Usar variable de entorno o valor por defecto
        # En Docker: usar nombre del contenedor
        # En local: usar localhost
        if base_url is None:
            base_url = os.getenv("CATALOG_SERVICE_URL", "http://cinematch-catalog-service:3001")
        
        self.base_url = base_url
        self.timeout = 5.0  # 5 segundos de timeout
        logger.info(f"CatalogClient inicializado con URL: {self.base_url}")
    
    async def get_movie(self, movie_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtiene información completa de una película del catálogo.
        
        Args:
            movie_id: ID numérico de TMDb (se convertirá a formato "tmdb:XXXXX")
            
        Returns:
            Dict con información de la película o None si no se encuentra
        """
        try:
            # Convertir ID numérico a formato del catálogo: "tmdb:XXXXX"
            catalog_id = f"tmdb:{movie_id}"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/movies/{catalog_id}")
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(f"Película {catalog_id} no encontrada en el catálogo")
                    return None
                else:
                    logger.error(f"Error al obtener película {catalog_id}: {response.status_code}")
                    return None
                    
        except httpx.TimeoutException:
            logger.error(f"Timeout al consultar película tmdb:{movie_id}")
            return None
        except Exception as e:
            logger.error(f"Error al consultar catálogo para película tmdb:{movie_id}: {e}")
            return None
    
    async def get_movies_batch(self, movie_ids: list[int]) -> Dict[int, Dict[str, Any]]:
        """
        Obtiene información de múltiples películas en paralelo.
        
        Args:
            movie_ids: Lista de IDs de películas
            
        Returns:
            Dict con movie_id como key y la info de la película como value
        """
        import asyncio
        
        tasks = [self.get_movie(movie_id) for movie_id in movie_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        movies = {}
        for movie_id, result in zip(movie_ids, results):
            if isinstance(result, dict) and result is not None:
                movies[movie_id] = result
            elif isinstance(result, Exception):
                logger.error(f"Error al obtener película {movie_id}: {result}")
        
        return movies
    
    async def get_genres(self) -> list[str]:
        """
        Obtiene la lista de géneros disponibles del catálogo.
        
        Returns:
            Lista de géneros disponibles
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(f"{self.base_url}/movies/genres")
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("data", [])
                else:
                    logger.error(f"Error al obtener géneros: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error al consultar géneros del catálogo: {e}")
            return []

# Instancia global del cliente
catalog_client = CatalogClient()

from pydantic import BaseModel
from typing import List

class UserFavorites(BaseModel):
    movie_ids: List[int]

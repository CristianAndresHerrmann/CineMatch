from pydantic import BaseModel, EmailStr, UUID4
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    from pydantic import Field
    password: str = Field(..., max_length=72, min_length=8, description="Password must be 8-72 characters")

class UserOut(UserBase):
    id: UUID4
    class Config:
        orm_mode = True

class UserPreferences(BaseModel):
    genres: List[str]

class UserFavorites(BaseModel):
    movie_ids: List[int]

class UserWatched(BaseModel):
    movie_ids: List[int]

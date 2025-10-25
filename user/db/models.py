import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(128), nullable=False)
    favorites = relationship("UserFavorite", back_populates="user", cascade="all, delete-orphan")
    watched = relationship("UserWatched", back_populates="user", cascade="all, delete-orphan")
    genres = relationship("UserGenre", back_populates="user", cascade="all, delete-orphan")

class UserFavorite(Base):
    __tablename__ = "user_favorites"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, primary_key=True)
    user = relationship("User", back_populates="favorites")
    __table_args__ = (UniqueConstraint('user_id', 'movie_id', name='_user_favorite_uc'),)

class UserWatched(Base):
    __tablename__ = "user_watched"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, primary_key=True)
    user = relationship("User", back_populates="watched")
    __table_args__ = (UniqueConstraint('user_id', 'movie_id', name='_user_watched_uc'),)

class UserGenre(Base):
    __tablename__ = "user_genres"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    genre = Column(String(32), primary_key=True)
    user = relationship("User", back_populates="genres")
    __table_args__ = (UniqueConstraint('user_id', 'genre', name='_user_genre_uc'),)

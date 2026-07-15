from sqlalchemy import Column, Integer, String, DateTime,Boolean,Text,Float
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True,unique=True)
    
    email = Column(String, unique=True, index=True, nullable=False)

    password_hash = Column(String, nullable=False)

    name = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())

    profile_image = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text, nullable=False)

    poster_url = Column(String, nullable=True)

    trailer_url = Column(String, nullable=True)

    release_year = Column(Integer)

    language = Column(String)

    runtime = Column(Integer)

    imdb_rating = Column(Float)

    created_at = Column(
        DateTime,
        server_default=func.now()
    )
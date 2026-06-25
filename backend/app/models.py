from sqlalchemy import Column, Integer, String, DateTime,Boolean
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


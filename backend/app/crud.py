from sqlalchemy.orm import Session

from . import models
from . import schemas
from .auth.security import hash_password
from .auth.security import verify_password

def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = hash_password(user.password)

    db_user = models.User(
        email=user.email,
        name=user.name,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def authenticate_user(
    db: Session,
    email: str,
    password: str
):
    user = (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.password_hash
    ):
        return None

    return user

def get_user_by_email(
    db: Session,
    email: str
):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )
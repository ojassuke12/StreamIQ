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

def create_movie(
    db: Session,
    movie: schemas.MovieCreate
):
    """
    Creates a new movie in the database.
    """

    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        poster_url=movie.poster_url,
        trailer_url=movie.trailer_url,
        release_year=movie.release_year,
        language=movie.language,
        runtime=movie.runtime,
        imdb_rating=movie.imdb_rating
    )

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie

def get_movies(
    db: Session
):
    """
    Returns all movies from the database.
    """

    return db.query(models.Movie).all()

def get_movie(
    db: Session,
    movie_id: int
):
    """
    Returns a single movie by its ID.
    """

    return (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id)
        .first()
    )

def update_movie(
    db: Session,
    movie_id: int,
    movie: schemas.MovieCreate
):
    """
    Updates an existing movie.
    """

    db_movie = (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id)
        .first()
    )

    if not db_movie:
        return None

    db_movie.title = movie.title
    db_movie.description = movie.description
    db_movie.poster_url = movie.poster_url
    db_movie.trailer_url = movie.trailer_url
    db_movie.release_year = movie.release_year
    db_movie.language = movie.language
    db_movie.runtime = movie.runtime
    db_movie.imdb_rating = movie.imdb_rating

    db.commit()
    db.refresh(db_movie)

    return db_movie

def delete_movie(
    db: Session,
    movie_id: int
):
    """
    Deletes a movie by its ID.
    """

    db_movie = (
        db.query(models.Movie)
        .filter(models.Movie.id == movie_id)
        .first()
    )

    if not db_movie:
        return None

    db.delete(db_movie)
    db.commit()

    return db_movie
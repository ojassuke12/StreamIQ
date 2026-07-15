from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from .auth.security import create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .auth.security import verify_access_token
from fastapi import HTTPException
from .database import engine

from . import crud, schemas,models
from .database import get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")

    user = crud.get_user_by_email(
        db,
        email
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.get("/")
def home():
    return {"message": "Welcome to StreamIQ"}


@app.post("/register", response_model=schemas.UserResponse)
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = crud.authenticate_user(
    db,
    form_data.username,
    form_data.password
)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user: models.User = Depends(get_current_user)
):
    return current_user

@app.post("/movies", response_model=schemas.MovieResponse)
def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db)
):
    return crud.create_movie(
        db,
        movie
    )

@app.get("/movies", response_model=list[schemas.MovieResponse])
def get_movies(
    db: Session = Depends(get_db)
):
    return crud.get_movies(db)

@app.get("/movies/{movie_id}", response_model=schemas.MovieResponse)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    movie = crud.get_movie(
        db,
        movie_id
    )

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie

@app.put("/movies/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(
    movie_id: int,
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db)
):
    updated_movie = crud.update_movie(
        db,
        movie_id,
        movie
    )

    if updated_movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return updated_movie

@app.delete("/movies/{movie_id}", response_model=schemas.MovieResponse)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):
    deleted_movie = crud.delete_movie(
        db,
        movie_id
    )

    if deleted_movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return deleted_movie
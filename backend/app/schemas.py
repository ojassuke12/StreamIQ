from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    name: str

    class Config:
       from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class MovieCreate(BaseModel):
    title: str
    description: str
    poster_url: str | None = None
    trailer_url: str | None = None
    release_year: int
    language: str
    runtime: int
    imdb_rating: float

class MovieResponse(MovieCreate):
    id: int

    class Config:
        from_attributes = True
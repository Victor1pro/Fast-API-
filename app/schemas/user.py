from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, Annotated
from datetime import datetime


# Base Model for Client (Request)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

# Base Model for Server (Response)
class PostResponse(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserResponse

    # Automatically changes response data to Dictionary
    model_config = ConfigDict(from_attributes=True)


class PostVote(PostBase):
    post: PostResponse
    votes: int

    # Automatically changes response data to Dictionary
    model_config = ConfigDict(from_attributes=True)

# User 
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# User Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


# User Vote
class Votes(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le = 1)]


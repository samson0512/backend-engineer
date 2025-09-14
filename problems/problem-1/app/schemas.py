from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# User schemas
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Project schemas
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int

    class Config:
        orm_mode = True

# Task schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    owner_id: Optional[int]
    project_id: Optional[int]

    class Config:
        orm_mode = True
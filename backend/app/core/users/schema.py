from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Annotated
from .models import UserRole

class UserBase(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.GESTOR

class ShowUser(UserBase):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)
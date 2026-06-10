from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator

from app.models.app_model import UserRole

class UserBase(BaseModel):
    """Base User Schema with common attributes"""
    email: EmailStr
    role: Optional[str]
    username: Optional[str] = Field(None, min_length=2, max_length=50, description="First name of the user")

class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8)

    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        return v

class UserUpdate(BaseModel):
    """Schema for updating user information"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=2, max_length=50)

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str
    password: str

    # email required check
    @validator('email')
    def email_required(cls, v):
        """Validate email for required"""
        if not v:
            raise ValueError('Email is required')
        return v

    @validator('password')
    def password_required(cls, v):
        """Validate password for required"""
        if not v:
            raise ValueError('Password is required')
        return v

class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    # class Config:
    #     orm_mode = True


class CreateNode(BaseModel):
    nodename: str
    pid: int
    ppath:str|None
    
class NodeContext(BaseModel):
    id: int
    pid: int

class ChgPermission(BaseModel):
    nid: int
    perm: int

class CreateGrp(BaseModel):
    grpname: str
    grpuserids: List[int]
    grpdesc: str

class CompleteUpload(BaseModel):
    file_id: int
    content_type: str
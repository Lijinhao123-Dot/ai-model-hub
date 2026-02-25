"""Pydantic 模型"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from uuid import UUID


# ============ 用户相关 ============
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: UUID
    avatar: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============ 模型相关 ============
class ModelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    category: str
    tags: List[str] = []
    framework: Optional[str] = None
    version: str = "1.0.0"


class ModelCreate(ModelBase):
    file_url: Optional[str] = None
    file_size: int = 0
    file_format: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_docs: Optional[str] = None


class ModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    framework: Optional[str] = None
    version: Optional[str] = None
    file_url: Optional[str] = None
    file_size: Optional[int] = None
    file_format: Optional[str] = None
    api_endpoint: Optional[str] = None
    api_docs: Optional[str] = None


class ModelResponse(ModelBase):
    id: UUID
    file_url: Optional[str] = None
    file_size: int = 0
    file_format: Optional[str] = None
    downloads: int = 0
    likes_count: int = 0
    comments_count: int = 0
    views: int = 0
    api_endpoint: Optional[str] = None
    api_docs: Optional[str] = None
    author_id: UUID
    author: Optional[UserResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ModelListResponse(BaseModel):
    items: List[ModelResponse]
    total: int
    page: int
    page_size: int


# ============ 评论相关 ============
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    rating: int = Field(5, ge=1, le=5)


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: UUID
    model_id: UUID
    user_id: UUID
    user: Optional[UserResponse] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============ 点赞相关 ============
class LikeResponse(BaseModel):
    id: UUID
    model_id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ============ 分类相关 ============
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon: Optional[str] = None


class CategoryResponse(CategoryBase):
    id: UUID
    sort_order: int = 0
    model_count: int = 0

    class Config:
        from_attributes = True


# ============ 通用响应 ============
class Message(BaseModel):
    message: str
    detail: Optional[str] = None

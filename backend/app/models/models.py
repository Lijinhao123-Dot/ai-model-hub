"""数据模型"""
from sqlalchemy import Column, String, Text, Integer, BigInteger, ForeignKey, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    models = relationship("Model", back_populates="author")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")


class Model(Base):
    """AI 模型"""
    __tablename__ = "models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False, index=True)  # nlp, cv, audio, multimodal
    tags = Column(ARRAY(String), default=list)
    framework = Column(String(100), nullable=True)  # pytorch, tensorflow, onnx
    version = Column(String(50), default="1.0.0")

    # 文件信息
    file_url = Column(String(1000), nullable=True)
    file_size = Column(BigInteger, default=0)
    file_format = Column(String(50), nullable=True)  # .pt, .bin, .onnx

    # 统计
    downloads = Column(Integer, default=0)
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    views = Column(Integer, default=0)

    # API 信息
    api_endpoint = Column(String(500), nullable=True)
    api_docs = Column(Text, nullable=True)

    # 作者
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # 时间
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    author = relationship("User", back_populates="models")
    comments = relationship("Comment", back_populates="model", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="model", cascade="all, delete-orphan")


class Comment(Base):
    """评论"""
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer, default=5)  # 1-5 星评分
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    model = relationship("Model", back_populates="comments")
    user = relationship("User", back_populates="comments")


class Like(Base):
    """点赞"""
    __tablename__ = "likes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id = Column(UUID(as_uuid=True), ForeignKey("models.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    model = relationship("Model", back_populates="likes")
    user = relationship("User", back_populates="likes")


class Category(Base):
    """分类"""
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), nullable=True)
    sort_order = Column(Integer, default=0)

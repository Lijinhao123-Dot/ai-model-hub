"""互动 API 路由（评论、点赞）"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.models import Model, Comment, Like, User
from app.schemas.schemas import CommentCreate, CommentResponse, LikeResponse, Message
from app.services.auth import get_current_active_user, User as AuthUser

router = APIRouter(tags=["互动"])


# ============ 评论相关 ============
@router.get("/models/{model_id}/comments", response_model=list[CommentResponse])
async def list_comments(
    model_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """获取模型评论列表"""
    result = await db.execute(
        select(Comment)
        .where(Comment.model_id == model_id)
        .order_by(Comment.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    comments = result.scalars().all()
    return comments


@router.post("/models/{model_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    model_id: str,
    comment_data: CommentCreate,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """发表评论"""
    # 检查模型是否存在
    result = await db.execute(select(Model).where(Model.id == model_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="模型不存在")

    comment = Comment(
        model_id=model_id,
        user_id=current_user.id,
        **comment_data.model_dump()
    )
    db.add(comment)

    # 更新评论计数
    await db.execute(
        Model.__table__.update()
        .where(Model.id == model_id)
        .values(comments_count=Model.comments_count + 1)
    )

    await db.commit()
    await db.refresh(comment)

    return comment


@router.delete("/comments/{comment_id}", response_model=Message)
async def delete_comment(
    comment_id: str,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除评论"""
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(status_code=404, detail="评论不存在")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此评论")

    model_id = comment.model_id
    await db.delete(comment)

    # 更新评论计数
    await db.execute(
        Model.__table__.update()
        .where(Model.id == model_id)
        .values(comments_count=Model.comments_count - 1)
    )

    await db.commit()

    return Message(message="删除成功")


# ============ 点赞相关 ============
@router.post("/models/{model_id}/like", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
async def like_model(
    model_id: str,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """点赞模型"""
    # 检查模型是否存在
    result = await db.execute(select(Model).where(Model.id == model_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="模型不存在")

    # 检查是否已点赞
    result = await db.execute(
        select(Like).where(
            Like.model_id == model_id,
            Like.user_id == current_user.id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="已点赞")

    like = Like(model_id=model_id, user_id=current_user.id)
    db.add(like)

    # 更新点赞计数
    await db.execute(
        Model.__table__.update()
        .where(Model.id == model_id)
        .values(likes_count=Model.likes_count + 1)
    )

    await db.commit()
    await db.refresh(like)

    return like


@router.delete("/models/{model_id}/like", response_model=Message)
async def unlike_model(
    model_id: str,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """取消点赞"""
    result = await db.execute(
        select(Like).where(
            Like.model_id == model_id,
            Like.user_id == current_user.id
        )
    )
    like = result.scalar_one_or_none()

    if not like:
        raise HTTPException(status_code=404, detail="未点赞")

    await db.delete(like)

    # 更新点赞计数
    await db.execute(
        Model.__table__.update()
        .where(Model.id == model_id)
        .values(likes_count=Model.likes_count - 1)
    )

    await db.commit()

    return Message(message="取消点赞成功")


@router.get("/models/{model_id}/like/status")
async def check_like_status(
    model_id: str,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """检查是否已点赞"""
    result = await db.execute(
        select(Like).where(
            Like.model_id == model_id,
            Like.user_id == current_user.id
        )
    )
    liked = result.scalar_one_or_none() is not None

    return {"liked": liked}

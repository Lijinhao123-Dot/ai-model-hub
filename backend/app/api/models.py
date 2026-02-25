"""模型 API 路由"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from typing import Optional
from app.database import get_db
from app.models.models import Model, User
from app.schemas.schemas import (
    ModelCreate, ModelUpdate, ModelResponse, ModelListResponse, Message
)
from app.services.auth import get_current_active_user, User as AuthUser

router = APIRouter(prefix="/models", tags=["模型"])


@router.get("", response_model=ModelListResponse)
async def list_models(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: str = Query("latest", regex="^(latest|popular|downloads)$"),
    db: AsyncSession = Depends(get_db)
):
    """获取模型列表"""
    query = select(Model).where(Model.id.isnot(None))

    # 分类筛选
    if category:
        query = query.where(Model.category == category)

    # 搜索
    if search:
        query = query.where(
            or_(
                Model.name.ilike(f"%{search}%"),
                Model.description.ilike(f"%{search}%")
            )
        )

    # 排序
    if sort == "latest":
        query = query.order_by(Model.created_at.desc())
    elif sort == "popular":
        query = query.order_by(Model.likes_count.desc())
    elif sort == "downloads":
        query = query.order_by(Model.downloads.desc())

    # 总数
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar()

    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    models = result.scalars().all()

    return ModelListResponse(
        items=models,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{model_id}", response_model=ModelResponse)
async def get_model(model_id: str, db: AsyncSession = Depends(get_db)):
    """获取模型详情"""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    # 增加浏览量
    model.views += 1
    await db.commit()

    return model


@router.post("", response_model=ModelResponse, status_code=status.HTTP_201_CREATED)
async def create_model(
    model_data: ModelCreate,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """创建模型"""
    model = Model(
        **model_data.model_dump(),
        author_id=current_user.id
    )
    db.add(model)
    await db.commit()
    await db.refresh(model)

    return model


@router.put("/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: str,
    model_data: ModelUpdate,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """更新模型"""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    if model.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权修改此模型")

    # 更新字段
    for key, value in model_data.model_dump(exclude_unset=True).items():
        setattr(model, key, value)

    await db.commit()
    await db.refresh(model)

    return model


@router.delete("/{model_id}", response_model=Message)
async def delete_model(
    model_id: str,
    current_user: AuthUser = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """删除模型"""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    if model.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权删除此模型")

    await db.delete(model)
    await db.commit()

    return Message(message="删除成功")


@router.post("/{model_id}/download")
async def download_model(
    model_id: str,
    db: AsyncSession = Depends(get_db)
):
    """下载模型（返回下载链接，增加下载计数）"""
    result = await db.execute(select(Model).where(Model.id == model_id))
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    if not model.file_url:
        raise HTTPException(status_code=400, detail="该模型暂无下载文件")

    # 增加下载计数
    model.downloads += 1
    await db.commit()

    return {
        "download_url": model.file_url,
        "file_size": model.file_size,
        "file_format": model.file_format
    }

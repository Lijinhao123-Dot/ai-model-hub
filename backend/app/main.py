"""AI Model Hub - 主应用（简化版）"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Model Hub",
    description="AI 模型展示平台 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI Model Hub API", "status": "running", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


# 模拟数据 - 模型列表
MOCK_MODELS = [
    {
        "id": "1",
        "name": "GPT-4-Turbo",
        "description": "最先进的语言模型，支持128K上下文",
        "category": "nlp",
        "tags": ["LLM", "ChatGPT", "Transformer"],
        "framework": "pytorch",
        "downloads": 125000,
        "likes_count": 8900,
        "version": "1.0.0"
    },
    {
        "id": "2", 
        "name": "Stable Diffusion XL",
        "description": "高质量图像生成模型",
        "category": "cv",
        "tags": ["Image Generation", "Diffusion"],
        "framework": "pytorch",
        "downloads": 98000,
        "likes_count": 7200,
        "version": "1.0.0"
    },
    {
        "id": "3",
        "name": "Whisper Large V3",
        "description": "OpenAI 多语言语音识别模型",
        "category": "audio",
        "tags": ["ASR", "Speech", "Multilingual"],
        "framework": "pytorch",
        "downloads": 45000,
        "likes_count": 3200,
        "version": "3.0.0"
    },
    {
        "id": "4",
        "name": "CLIP",
        "description": "OpenAI 图文多模态模型",
        "category": "multimodal",
        "tags": ["Vision", "NLP", "Zero-shot"],
        "framework": "pytorch",
        "downloads": 78000,
        "likes_count": 5600,
        "version": "1.0.0"
    }
]


@app.get("/api/models")
async def list_models(page: int = 1, page_size: int = 20, category: str = None, search: str = None):
    """获取模型列表"""
    models = MOCK_MODELS
    if category:
        models = [m for m in models if m["category"] == category]
    if search:
        models = [m for m in models if search.lower() in m["name"].lower()]
    return {"items": models, "total": len(models), "page": page, "page_size": page_size}


@app.get("/api/models/{model_id}")
async def get_model(model_id: str):
    """获取模型详情"""
    for m in MOCK_MODELS:
        if m["id"] == model_id:
            return m
    return {"error": "Model not found"}


@app.post("/api/models/{model_id}/like")
async def like_model(model_id: str):
    """点赞模型"""
    return {"message": "Liked", "model_id": model_id}


@app.get("/api/models/{model_id}/comments")
async def get_comments(model_id: str):
    """获取评论"""
    return [
        {"id": "1", "user": "User1", "content": "很棒的模型！", "rating": 5},
        {"id": "2", "user": "User2", "content": "效果很好", "rating": 4}
    ]

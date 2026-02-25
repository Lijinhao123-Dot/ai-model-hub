# AI Model Hub - AI 模型展示平台

> 全栈动态网站，支持用户注册、模型下载、API展示、评论点赞

## 🏗️ 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vite | 响应式 UI |
| 后端 | FastAPI (Python) | 高性能 API |
| 数据库 | PostgreSQL (Supabase) | 免费 500MB |
| 认证 | Supabase Auth | 邮箱/OAuth 登录 |
| 存储 | Supabase Storage | 模型文件托管 |
| 部署 | Vercel + Railway | 免费部署 |

## 📁 项目结构

```
ai-model-hub/
├── frontend/           # Vue 3 前端
│   ├── src/
│   │   ├── views/      # 页面
│   │   ├── components/ # 组件
│   │   ├── api/        # API 调用
│   │   └── stores/     # 状态管理
│   └── package.json
├── backend/            # FastAPI 后端
│   ├── app/
│   │   ├── api/        # API 路由
│   │   ├── models/     # 数据模型
│   │   ├── schemas/    # Pydantic 模型
│   │   └── services/   # 业务逻辑
│   └── requirements.txt
└── docs/               # 文档
```

## 🚀 功能模块

### 用户系统
- [x] 邮箱注册/登录
- [x] OAuth (GitHub/Google)
- [x] 个人资料管理
- [x] 收藏夹

### 模型管理
- [x] 模型上传
- [x] 分类/标签
- [x] 搜索/筛选
- [x] 版本管理

### 互动功能
- [x] 评论系统
- [x] 点赞/收藏
- [x] 评分系统

### API 展示
- [x] API 文档
- [x] 在线测试
- [x] SDK 下载

## 🔧 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 📊 数据库设计

### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uuid | 主键 |
| email | varchar | 邮箱 |
| username | varchar | 用户名 |
| avatar | varchar | 头像 |
| created_at | timestamp | 创建时间 |

### 模型表 (models)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uuid | 主键 |
| name | varchar | 模型名称 |
| description | text | 描述 |
| category | varchar | 分类 |
| tags | array | 标签 |
| file_url | varchar | 下载链接 |
| file_size | bigint | 文件大小 |
| downloads | integer | 下载次数 |
| likes | integer | 点赞数 |
| author_id | uuid | 作者 ID |
| created_at | timestamp | 创建时间 |

### 评论表 (comments)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uuid | 主键 |
| model_id | uuid | 模型 ID |
| user_id | uuid | 用户 ID |
| content | text | 评论内容 |
| created_at | timestamp | 创建时间 |

### 点赞表 (likes)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | uuid | 主键 |
| model_id | uuid | 模型 ID |
| user_id | uuid | 用户 ID |
| created_at | timestamp | 创建时间 |

## 🌐 API 接口

### 认证
- POST /api/auth/register
- POST /api/auth/login
- POST /api/auth/logout

### 模型
- GET /api/models - 模型列表
- GET /api/models/{id} - 模型详情
- POST /api/models - 创建模型
- PUT /api/models/{id} - 更新模型
- DELETE /api/models/{id} - 删除模型
- GET /api/models/{id}/download - 下载模型

### 互动
- GET /api/models/{id}/comments - 评论列表
- POST /api/models/{id}/comments - 发表评论
- POST /api/models/{id}/like - 点赞
- DELETE /api/models/{id}/like - 取消点赞

## 📝 开发进度

- [ ] 数据库搭建
- [ ] 后端 API 开发
- [ ] 前端页面开发
- [ ] 用户系统集成
- [ ] 文件上传功能
- [ ] 部署上线

---

*创建时间: 2026-02-25*

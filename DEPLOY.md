# AI Model Hub - 部署指南

## 🚀 部署架构（免费方案）

| 服务 | 平台 | 费用 |
|------|------|------|
| 数据库 | Supabase | 免费 500MB |
| 后端 API | Render | 免费 |
| 前端 | Vercel | 免费 |
| 代码托管 | GitHub | 免费 |

---

## 📋 第一步：创建 GitHub 仓库

1. 打开 https://github.com/new
2. 仓库名：`ai-model-hub`
3. 选择 **Private** 或 **Public**
4. 点击 **Create repository**
5. 在本地执行：

```bash
cd C:\Users\16671\.openclaw\workspace\projects\ai-model-hub
git remote add origin https://github.com/你的用户名/ai-model-hub.git
git branch -M main
git push -u origin main
```

---

## 📋 第二步：创建 Supabase 数据库

1. 打开 https://supabase.com
2. 点击 **Start your project** 注册/登录
3. 创建新组织（Organization）
4. 创建新项目：
   - Name: `ai-model-hub`
   - Database Password: 记住这个密码
   - Region: 选择 **Singapore** (离中国最近)
5. 等待项目创建完成（约2分钟）
6. 进入 **Settings** → **Database**
7. 复制 **Connection string** (URI格式)：
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```

8. 进入 **Settings** → **API**
   - 复制 **Project URL**
   - 复制 **anon public key**

---

## 📋 第三步：部署后端到 Render

1. 打开 https://render.com
2. 点击 **Get Started** 用 GitHub 登录
3. 授权 Render 访问你的 GitHub
4. 点击 **New** → **Web Service**
5. 连接你的 `ai-model-hub` 仓库
6. 配置：
   | 项目 | 值 |
   |------|------|
   | Name | `ai-model-hub-api` |
   | Root Directory | `backend` |
   | Runtime | `Python 3` |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
   | Instance Type | `Free` |

7. 添加环境变量（Advanced → Add Environment Variable）：

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | Supabase 的连接字符串 |
   | `SECRET_KEY` | 随便生成一个长字符串 |
   | `SUPABASE_URL` | Supabase Project URL |
   | `SUPABASE_KEY` | Supabase anon key |

8. 点击 **Deploy Web Service**
9. 等待部署完成（约5分钟）
10. 获得 API 地址：`https://ai-model-hub-api.onrender.com`

---

## 📋 第四步：部署前端到 Vercel

1. 打开 https://vercel.com
2. 点击 **Sign Up** 用 GitHub 登录
3. 授权 Vercel 访问你的 GitHub
4. 点击 **Add New** → **Project**
5. 导入 `ai-model-hub` 仓库
6. 配置：
   | 项目 | 值 |
   |------|------|
   | Framework Preset | `Vite` |
   | Root Directory | `frontend` |
   | Build Command | `npm run build` |
   | Output Directory | `dist` |

7. 添加环境变量：

   | Key | Value |
   |-----|-------|
   | `VITE_API_URL` | `https://ai-model-hub-api.onrender.com` |

8. 点击 **Deploy**
9. 等待部署完成（约2分钟）
10. 获得网站地址：`https://ai-model-hub.vercel.app`

---

## ✅ 部署完成后

### 测试 API
访问：`https://ai-model-hub-api.onrender.com/docs`

### 测试网站
访问：`https://ai-model-hub.vercel.app`

---

## 🔧 更新前端 API 地址

部署后需要修改前端的 API 地址：

```bash
# 编辑 frontend/src/api/index.js
# 将 baseURL 改为你的 Render 地址
baseURL: 'https://ai-model-hub-api.onrender.com/api'
```

或者使用环境变量，已在 Vercel 中配置。

---

## 📌 注意事项

1. **Render 免费版限制**：
   - 15分钟无请求会休眠
   - 每月 750 小时运行时间
   - 首次访问可能需要等待30秒唤醒

2. **Supabase 免费版限制**：
   - 500MB 数据库存储
   - 1GB 文件存储
   - 50,000 月活用户

3. **Vercel 免费版限制**：
   - 100GB 带宽/月
   - 无限制部署

---

## 🎉 完成！

你的 AI Model Hub 已上线：
- **网站**: https://ai-model-hub.vercel.app
- **API**: https://ai-model-hub-api.onrender.com/docs

---

*如有问题，随时问我！*

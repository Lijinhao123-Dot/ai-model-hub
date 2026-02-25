<template>
  <div class="model-detail" v-loading="loading">
    <template v-if="model">
      <!-- 基本信息 -->
      <el-card class="info-card">
        <div class="header">
          <div>
            <h1>{{ model.name }}</h1>
            <div class="meta">
              <el-tag :type="getCategoryType(model.category)">{{ model.category }}</el-tag>
              <span class="author">作者: {{ model.author?.username || '未知' }}</span>
              <span>发布于: {{ formatDate(model.created_at) }}</span>
            </div>
          </div>
          <div class="actions">
            <el-button type="primary" @click="handleDownload">
              <el-icon><Download /></el-icon> 下载
            </el-button>
            <el-button :type="liked ? 'danger' : 'default'" @click="handleLike">
              <el-icon><Star /></el-icon> {{ liked ? '已点赞' : '点赞' }} ({{ model.likes_count }})
            </el-button>
          </div>
        </div>

        <el-divider />

        <div class="description">
          <h3>模型描述</h3>
          <p>{{ model.description || '暂无描述' }}</p>
        </div>

        <div class="tags">
          <el-tag v-for="tag in model.tags" :key="tag" type="info">{{ tag }}</el-tag>
        </div>

        <el-descriptions :column="3" border class="details">
          <el-descriptions-item label="框架">{{ model.framework || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="版本">{{ model.version }}</el-descriptions-item>
          <el-descriptions-item label="格式">{{ model.file_format || '未知' }}</el-descriptions-item>
          <el-descriptions-item label="下载次数">{{ model.downloads }}</el-descriptions-item>
          <el-descriptions-item label="浏览次数">{{ model.views }}</el-descriptions-item>
          <el-descriptions-item label="文件大小">{{ formatSize(model.file_size) }}</el-descriptions-item>
        </el-descriptions>
      </el-card>

      <!-- API 文档 -->
      <el-card class="api-card" v-if="model.api_endpoint">
        <h3>API 接口</h3>
        <p><strong>Endpoint:</strong> <code>{{ model.api_endpoint }}</code></p>
        <pre class="code-block">{{ model.api_docs || '暂无 API 文档' }}</pre>
      </el-card>

      <!-- 评论区 -->
      <el-card class="comments-card">
        <h3>评论 ({{ model.comments_count }})</h3>

        <!-- 发表评论 -->
        <div class="comment-form" v-if="userStore.isLoggedIn">
          <el-rate v-model="newComment.rating" />
          <el-input v-model="newComment.content" type="textarea" :rows="3" placeholder="写下你的评论..." />
          <el-button type="primary" @click="submitComment">发表评论</el-button>
        </div>
        <el-alert v-else type="info" :closable="false">
          <router-link to="/login">登录</router-link> 后参与评论
        </el-alert>

        <!-- 评论列表 -->
        <div class="comment-list">
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <el-avatar :size="40">{{ comment.user?.username?.charAt(0) }}</el-avatar>
            <div class="comment-content">
              <div class="comment-header">
                <span class="username">{{ comment.user?.username }}</span>
                <el-rate :model-value="comment.rating" disabled />
                <span class="time">{{ formatDate(comment.created_at) }}</span>
              </div>
              <p>{{ comment.content }}</p>
            </div>
          </div>
        </div>
      </el-card>
    </template>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { modelAPI, interactionAPI } from '@/api'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const userStore = useUserStore()
const loading = ref(true)
const model = ref(null)
const comments = ref([])
const liked = ref(false)

const newComment = reactive({
  content: '',
  rating: 5
})

const loadModel = async () => {
  try {
    model.value = await modelAPI.get(route.params.id)
    if (userStore.isLoggedIn) {
      const res = await interactionAPI.checkLike(route.params.id)
      liked.value = res.liked
    }
  } catch {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const loadComments = async () => {
  try {
    const res = await interactionAPI.listComments(route.params.id)
    comments.value = res
  } catch {}
}

const handleDownload = async () => {
  try {
    const res = await modelAPI.download(route.params.id)
    window.open(res.download_url, '_blank')
  } catch {
    ElMessage.error('下载失败')
  }
}

const handleLike = async () => {
  if (!userStore.isLoggedIn) return ElMessage.warning('请先登录')
  try {
    if (liked.value) {
      await interactionAPI.unlike(route.params.id)
      model.value.likes_count--
    } else {
      await interactionAPI.like(route.params.id)
      model.value.likes_count++
    }
    liked.value = !liked.value
  } catch {}
}

const submitComment = async () => {
  if (!newComment.content.trim()) return
  try {
    const comment = await interactionAPI.createComment(route.params.id, newComment)
    comments.value.unshift(comment)
    model.value.comments_count++
    newComment.content = ''
    ElMessage.success('评论成功')
  } catch {}
}

const formatDate = (date) => new Date(date).toLocaleDateString('zh-CN')
const formatSize = (size) => size > 1073741824 ? (size/1073741824).toFixed(2)+'GB' : (size/1048576).toFixed(2)+'MB'
const getCategoryType = (cat) => ({ nlp: 'primary', cv: 'success', audio: 'warning' }[cat] || '')

onMounted(() => {
  loadModel()
  loadComments()
})
</script>

<style lang="scss" scoped>
.model-detail {
  max-width: 900px;
  margin: 0 auto;

  .info-card {
    margin-bottom: 24px;

    .header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;

      h1 { margin: 0 0 8px; }
      .meta { color: #666; font-size: 14px; display: flex; gap: 16px; align-items: center; }
    }

    .description { margin-bottom: 16px; }
    .tags { display: flex; gap: 8px; margin-bottom: 16px; }
    .details { margin-top: 16px; }
  }

  .api-card {
    margin-bottom: 24px;
    .code-block { background: #f5f5f5; padding: 16px; border-radius: 8px; overflow-x: auto; }
  }

  .comments-card {
    .comment-form {
      margin-bottom: 24px;
      .el-rate { margin-bottom: 12px; }
      .el-textarea { margin-bottom: 12px; }
    }

    .comment-list {
      .comment-item {
        display: flex; gap: 12px; padding: 16px 0; border-bottom: 1px solid #eee;
        .comment-content { flex: 1;
          .comment-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px;
            .username { font-weight: bold; }
            .time { color: #999; font-size: 12px; margin-left: auto; }
          }
        }
      }
    }
  }
}
</style>

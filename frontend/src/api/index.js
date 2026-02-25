import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    const message = error.response?.data?.detail || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

// ============ 认证 API ============
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
  updateMe: (data) => api.put('/auth/me', null, { params: data }),
  logout: () => api.post('/auth/logout')
}

// ============ 模型 API ============
export const modelAPI = {
  list: (params) => api.get('/models', { params }),
  get: (id) => api.get(`/models/${id}`),
  create: (data) => api.post('/models', data),
  update: (id, data) => api.put(`/models/${id}`, data),
  delete: (id) => api.delete(`/models/${id}`),
  download: (id) => api.post(`/models/${id}/download`)
}

// ============ 互动 API ============
export const interactionAPI = {
  // 评论
  listComments: (modelId, params) => api.get(`/models/${modelId}/comments`, { params }),
  createComment: (modelId, data) => api.post(`/models/${modelId}/comments`, data),
  deleteComment: (commentId) => api.delete(`/comments/${commentId}`),

  // 点赞
  like: (modelId) => api.post(`/models/${modelId}/like`),
  unlike: (modelId) => api.delete(`/models/${modelId}/like`),
  checkLike: (modelId) => api.get(`/models/${modelId}/like/status`)
}

export default api

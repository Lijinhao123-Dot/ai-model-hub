<template>
  <div class="profile-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>个人中心</span>
          <el-button type="primary" @click="editing = !editing">{{ editing ? '取消' : '编辑' }}</el-button>
        </div>
      </template>
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" :disabled="!editing" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="userStore.user?.email" disabled />
        </el-form-item>
        <el-form-item label="头像">
          <el-input v-model="form.avatar" :disabled="!editing" placeholder="头像URL" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.bio" type="textarea" :rows="3" :disabled="!editing" />
        </el-form-item>
        <el-form-item v-if="editing">
          <el-button type="primary" @click="handleSave" :loading="loading">保存</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="my-models">
      <template #header>我的模型</template>
      <el-empty v-if="!models.length" description="暂无上传的模型" />
      <div v-else class="model-list">
        <div v-for="model in models" :key="model.id" class="model-item">
          <div>
            <h4>{{ model.name }}</h4>
            <p>{{ model.description }}</p>
          </div>
          <div class="stats">
            <span><el-icon><Download /></el-icon> {{ model.downloads }}</span>
            <span><el-icon><Star /></el-icon> {{ model.likes_count }}</span>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { authAPI, modelAPI } from '@/api'

const userStore = useUserStore()
const editing = ref(false)
const loading = ref(false)
const models = ref([])

const form = reactive({
  username: userStore.user?.username || '',
  avatar: userStore.user?.avatar || '',
  bio: userStore.user?.bio || ''
})

const handleSave = async () => {
  loading.value = true
  try {
    await authAPI.updateMe(form)
    await userStore.fetchUser()
    editing.value = false
    ElMessage.success('保存成功')
  } catch {
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const res = await modelAPI.list({ page: 1, page_size: 10 })
    models.value = res.items.filter(m => m.author_id === userStore.user?.id)
  } catch {}
})
</script>

<style lang="scss" scoped>
.profile-page {
  max-width: 800px; margin: 0 auto;
  .card-header { display: flex; justify-content: space-between; align-items: center; }
  .my-models { margin-top: 24px;
    .model-list { .model-item { display: flex; justify-content: space-between; padding: 16px; border-bottom: 1px solid #eee;
      h4 { margin: 0 0 8px; }
      p { color: #666; font-size: 14px; margin: 0; }
      .stats { display: flex; gap: 16px; color: #999; align-items: center; }
    }}
  }
}
</style>

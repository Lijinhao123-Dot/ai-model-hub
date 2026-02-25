<template>
  <div class="models-page">
    <!-- 筛选栏 -->
    <el-card class="filter-card">
      <el-form :inline="true">
        <el-form-item label="搜索">
          <el-input v-model="filters.search" placeholder="搜索模型..." clearable @keyup.enter="loadModels" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filters.category" placeholder="全部分类" clearable>
            <el-option label="NLP" value="nlp" />
            <el-option label="CV" value="cv" />
            <el-option label="语音" value="audio" />
            <el-option label="多模态" value="multimodal" />
          </el-select>
        </el-form-item>
        <el-form-item label="排序">
          <el-select v-model="filters.sort">
            <el-option label="最新" value="latest" />
            <el-option label="最热" value="popular" />
            <el-option label="下载最多" value="downloads" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadModels">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 模型列表 -->
    <div class="model-grid" v-loading="loading">
      <ModelCard v-for="model in models" :key="model.id" :model="model" />
    </div>

    <!-- 分页 -->
    <el-pagination
      v-model:current-page="pagination.page"
      :page-size="pagination.pageSize"
      :total="pagination.total"
      layout="prev, pager, next"
      @current-change="loadModels"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { modelAPI } from '@/api'
import ModelCard from '@/components/ModelCard.vue'

const route = useRoute()
const loading = ref(false)
const models = ref([])

const filters = reactive({
  search: route.query.search || '',
  category: route.query.category || '',
  sort: 'latest'
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const loadModels = async () => {
  loading.value = true
  try {
    const res = await modelAPI.list({
      page: pagination.page,
      page_size: pagination.pageSize,
      ...filters
    })
    models.value = res.items
    pagination.total = res.total
  } catch {
    // 模拟数据
    models.value = [
      { id: '1', name: 'GPT-4-Turbo', description: '最先进的语言模型', category: 'nlp', downloads: 125000, likes_count: 8900, tags: ['LLM'] },
      { id: '2', name: 'Stable Diffusion XL', description: '高质量图像生成', category: 'cv', downloads: 98000, likes_count: 7200, tags: ['Diffusion'] },
      { id: '3', name: 'Whisper Large', description: '多语言语音识别', category: 'audio', downloads: 45000, likes_count: 3200, tags: ['ASR'] },
      { id: '4', name: 'CLIP', description: '图文多模态模型', category: 'multimodal', downloads: 78000, likes_count: 5600, tags: ['Vision', 'NLP'] }
    ]
    pagination.total = 4
  } finally {
    loading.value = false
  }
}

onMounted(loadModels)
</script>

<style lang="scss" scoped>
.models-page {
  max-width: 1200px;
  margin: 0 auto;

  .filter-card {
    margin-bottom: 24px;
  }

  .model-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
    min-height: 400px;
  }

  .el-pagination {
    justify-content: center;
  }
}
</style>

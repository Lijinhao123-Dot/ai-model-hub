<template>
  <div class="home">
    <!-- Hero 区域 -->
    <section class="hero">
      <h1>发现、分享 AI 模型</h1>
      <p>一站式 AI 模型展示与下载平台，汇聚全球优秀开源模型</p>
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索模型..."
          size="large"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button type="primary" @click="handleSearch">
              <el-icon><Search /></el-icon>
            </el-button>
          </template>
        </el-input>
      </div>
    </section>

    <!-- 分类导航 -->
    <section class="categories">
      <h2>热门分类</h2>
      <div class="category-grid">
        <div
          v-for="cat in categories"
          :key="cat.slug"
          class="category-card"
          @click="$router.push(`/models?category=${cat.slug}`)"
        >
          <el-icon :size="32"><component :is="cat.icon" /></el-icon>
          <h3>{{ cat.name }}</h3>
          <p>{{ cat.count }} 个模型</p>
        </div>
      </div>
    </section>

    <!-- 热门模型 -->
    <section class="hot-models">
      <div class="section-header">
        <h2>热门模型</h2>
        <el-button text @click="$router.push('/models')">
          查看全部 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <div class="model-grid">
        <ModelCard
          v-for="model in hotModels"
          :key="model.id"
          :model="model"
        />
      </div>
    </section>

    <!-- 最新模型 -->
    <section class="latest-models">
      <div class="section-header">
        <h2>最新上传</h2>
        <el-button text @click="$router.push('/models?sort=latest')">
          查看全部 <el-icon><ArrowRight /></el-icon>
        </el-button>
      </div>
      <div class="model-grid">
        <ModelCard
          v-for="model in latestModels"
          :key="model.id"
          :model="model"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { modelAPI } from '@/api'
import ModelCard from '@/components/ModelCard.vue'

const router = useRouter()
const searchQuery = ref('')
const hotModels = ref([])
const latestModels = ref([])

const categories = [
  { name: '自然语言处理', slug: 'nlp', icon: 'ChatDotRound', count: 128 },
  { name: '计算机视觉', slug: 'cv', icon: 'View', count: 256 },
  { name: '语音识别', slug: 'audio', icon: 'Headset', count: 64 },
  { name: '多模态', slug: 'multimodal', icon: 'PictureFilled', count: 32 },
  { name: '推荐系统', slug: 'recommendation', icon: 'Star', count: 48 },
  { name: '强化学习', slug: 'rl', icon: 'TrendCharts', count: 24 }
]

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/models?search=${encodeURIComponent(searchQuery.value)}`)
  }
}

onMounted(async () => {
  try {
    const [hot, latest] = await Promise.all([
      modelAPI.list({ sort: 'popular', page_size: 4 }),
      modelAPI.list({ sort: 'latest', page_size: 4 })
    ])
    hotModels.value = hot.items
    latestModels.value = latest.items
  } catch (e) {
    // 使用模拟数据
    hotModels.value = mockModels
    latestModels.value = mockModels
  }
})

// 模拟数据
const mockModels = [
  {
    id: '1',
    name: 'GPT-4-Turbo',
    description: '最先进的语言模型，支持128K上下文',
    category: 'nlp',
    tags: ['LLM', 'ChatGPT'],
    downloads: 125000,
    likes_count: 8900,
    framework: 'pytorch'
  },
  {
    id: '2',
    name: 'Stable Diffusion XL',
    description: '高质量图像生成模型',
    category: 'cv',
    tags: ['Image Generation', 'Diffusion'],
    downloads: 98000,
    likes_count: 7200,
    framework: 'pytorch'
  }
]
</script>

<style lang="scss" scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, var(--el-color-primary-light-7), var(--el-color-primary-light-9));
  border-radius: 16px;
  margin-bottom: 40px;

  h1 {
    font-size: 48px;
    margin-bottom: 16px;
    color: var(--el-color-primary-dark);
  }

  p {
    font-size: 18px;
    color: #666;
    margin-bottom: 32px;
  }

  .search-box {
    max-width: 600px;
    margin: 0 auto;
  }
}

.categories {
  margin-bottom: 40px;

  h2 {
    margin-bottom: 24px;
  }

  .category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 16px;
  }

  .category-card {
    background: #fff;
    padding: 24px;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;

    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }

    .el-icon {
      color: var(--el-color-primary);
      margin-bottom: 12px;
    }

    h3 {
      font-size: 16px;
      margin-bottom: 8px;
    }

    p {
      font-size: 14px;
      color: #999;
    }
  }
}

.hot-models, .latest-models {
  margin-bottom: 40px;

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
  }

  .model-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }
}
</style>

<template>
  <el-card class="model-card" shadow="hover" @click="$router.push(`/models/${model.id}`)">
    <div class="model-header">
      <h3>{{ model.name }}</h3>
      <el-tag :type="getCategoryType(model.category)" size="small">
        {{ getCategoryName(model.category) }}
      </el-tag>
    </div>

    <p class="description">{{ model.description || '暂无描述' }}</p>

    <div class="tags">
      <el-tag
        v-for="tag in model.tags?.slice(0, 3)"
        :key="tag"
        size="small"
        type="info"
        effect="plain"
      >
        {{ tag }}
      </el-tag>
    </div>

    <div class="stats">
      <span>
        <el-icon><Download /></el-icon>
        {{ formatNumber(model.downloads) }}
      </span>
      <span>
        <el-icon><Star /></el-icon>
        {{ formatNumber(model.likes_count) }}
      </span>
      <span v-if="model.framework">
        <el-icon><Cpu /></el-icon>
        {{ model.framework }}
      </span>
    </div>
  </el-card>
</template>

<script setup>
defineProps({
  model: {
    type: Object,
    required: true
  }
})

const categoryMap = {
  nlp: { name: 'NLP', type: 'primary' },
  cv: { name: 'CV', type: 'success' },
  audio: { name: '语音', type: 'warning' },
  multimodal: { name: '多模态', type: 'danger' },
  recommendation: { name: '推荐', type: 'info' },
  rl: { name: 'RL', type: '' }
}

const getCategoryName = (cat) => categoryMap[cat]?.name || cat
const getCategoryType = (cat) => categoryMap[cat]?.type || ''

const formatNumber = (num) => {
  if (!num) return '0'
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
  return num.toString()
}
</script>

<style lang="scss" scoped>
.model-card {
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
  }

  .model-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 12px;

    h3 {
      margin: 0;
      font-size: 18px;
    }
  }

  .description {
    color: #666;
    font-size: 14px;
    line-height: 1.6;
    margin-bottom: 12px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
  }

  .stats {
    display: flex;
    gap: 16px;
    font-size: 13px;
    color: #999;

    span {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }
}
</style>

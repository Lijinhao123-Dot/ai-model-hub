<template>
  <div class="upload-page">
    <el-card>
      <h2>上传模型</h2>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="模型名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请输入模型描述" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="选择分类">
            <el-option label="自然语言处理 (NLP)" value="nlp" />
            <el-option label="计算机视觉 (CV)" value="cv" />
            <el-option label="语音识别" value="audio" />
            <el-option label="多模态" value="multimodal" />
            <el-option label="推荐系统" value="recommendation" />
            <el-option label="强化学习" value="rl" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="form.tags" multiple filterable allow-create placeholder="输入标签">
            <el-option label="PyTorch" value="pytorch" />
            <el-option label="TensorFlow" value="tensorflow" />
            <el-option label="ONNX" value="onnx" />
            <el-option label="LLM" value="llm" />
            <el-option label="Diffusion" value="diffusion" />
          </el-select>
        </el-form-item>
        <el-form-item label="框架">
          <el-input v-model="form.framework" placeholder="如: PyTorch, TensorFlow" />
        </el-form-item>
        <el-form-item label="版本">
          <el-input v-model="form.version" placeholder="如: 1.0.0" />
        </el-form-item>
        <el-form-item label="文件链接">
          <el-input v-model="form.file_url" placeholder="模型文件下载链接" />
        </el-form-item>
        <el-form-item label="文件格式">
          <el-select v-model="form.file_format" placeholder="选择格式">
            <el-option label=".pt (PyTorch)" value=".pt" />
            <el-option label=".bin" value=".bin" />
            <el-option label=".onnx" value=".onnx" />
            <el-option label=".h5 (Keras)" value=".h5" />
            <el-option label=".pth" value=".pth" />
          </el-select>
        </el-form-item>
        <el-form-item label="API 端点">
          <el-input v-model="form.api_endpoint" placeholder="API 地址（可选）" />
        </el-form-item>
        <el-form-item label="API 文档">
          <el-input v-model="form.api_docs" type="textarea" :rows="4" placeholder="API 使用文档（可选）" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="loading">提交</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { modelAPI } from '@/api'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  name: '', description: '', category: '', tags: [],
  framework: '', version: '1.0.0', file_url: '', file_format: '',
  api_endpoint: '', api_docs: ''
})

const rules = {
  name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }]
}

const handleSubmit = async () => {
  await formRef.value.validate()
  loading.value = true
  try {
    await modelAPI.create(form)
    ElMessage.success('上传成功')
    router.push('/models')
  } catch {
    ElMessage.error('上传失败')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.upload-page {
  max-width: 800px; margin: 0 auto;
  h2 { margin-bottom: 24px; }
}
</style>

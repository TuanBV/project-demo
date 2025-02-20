<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const news = ref(null)

const fetchNewsDetail = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/news/${route.params.id}/`)
    news.value = response.data
  } catch (error) {
    console.error('Lỗi khi lấy chi tiết tin tức:', error)
  }
}

onMounted(fetchNewsDetail)
</script>

<template>
  <div v-if="news">
    <h1>{{ news.title }}</h1>
    <p>{{ news.content }}</p>
    <router-link to="/">Quay lại</router-link>
  </div>
</template>

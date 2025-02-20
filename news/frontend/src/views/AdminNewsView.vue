<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newsList = ref([])
const title = ref('')
const content = ref('')
const image = ref(null)

const fetchNews = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/news/')
  newsList.value = response.data
}

const createNews = async () => {
  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  await axios.post('http://127.0.0.1:8000/api/news/create/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

  fetchNews()
}

const deleteNews = async (id) => {
  await axios.delete(`http://127.0.0.1:8000/api/news/delete/${id}/`)
  fetchNews()
}

onMounted(fetchNews)
</script>

<template>
  <div>
    <h1>Quản lý tin tức</h1>
    <input v-model="title" placeholder="Tiêu đề" />
    <textarea v-model="content" placeholder="Nội dung"></textarea>
    <input type="file" @change="(e) => (image = e.target.files[0])" />
    <button @click="createNews">Thêm tin</button>

    <ul>
      <li v-for="news in newsList" :key="news.id">
        <img
          v-if="news.image"
          :src="'http://127.0.0.1:8000' + news.image"
          alt="Ảnh tin tức"
          width="100"
        />
        {{ news.title }} - <button @click="deleteNews(news.id)">Xóa</button>
      </li>
    </ul>
  </div>
</template>

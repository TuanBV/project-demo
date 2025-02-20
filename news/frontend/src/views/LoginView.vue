<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const store = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')

const handleLogin = async () => {
  await store.login(username.value, password.value)
  router.push('/')
}
</script>

<template>
  <div>
    <h1>Đăng nhập</h1>
    <input v-model="username" placeholder="Tên đăng nhập" />
    <input v-model="password" type="password" placeholder="Mật khẩu" />
    <button @click="handleLogin">Đăng nhập</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { extractErrorMessage } from '../api/errors'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const submitting = ref(false)

async function onSubmit() {
  errorMessage.value = ''
  submitting.value = true
  try {
    await authStore.login({ email: email.value, password: password.value })
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/dashboard/cvs'
    await router.push(redirect)
  } catch (error) {
    errorMessage.value = extractErrorMessage(error)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="flex flex-center bg-grey-2" style="min-height: 100vh">
    <q-card class="q-pa-lg" style="width: 100%; max-width: 400px">
      <q-card-section>
        <div class="text-h5 text-weight-bold">Đăng nhập</div>
        <div class="text-caption text-grey-7">Quản lý và chia sẻ CV của bạn</div>
      </q-card-section>

      <q-card-section>
        <q-form class="q-gutter-md" @submit.prevent="onSubmit">
          <q-input
            v-model="email"
            type="email"
            label="Email"
            data-testid="login-email"
            :rules="[(val) => !!val || 'Email là bắt buộc']"
            lazy-rules
          />
          <q-input
            v-model="password"
            type="password"
            label="Mật khẩu"
            data-testid="login-password"
            :rules="[(val) => !!val || 'Mật khẩu là bắt buộc']"
            lazy-rules
          />

          <div v-if="errorMessage" class="text-negative text-caption" data-testid="login-error">
            {{ errorMessage }}
          </div>

          <q-btn
            type="submit"
            color="primary"
            label="Đăng nhập"
            class="full-width"
            :loading="submitting"
            data-testid="login-submit"
          />
        </q-form>
      </q-card-section>

      <q-card-section class="text-center text-caption">
        Chưa có tài khoản?
        <router-link to="/register">Đăng ký</router-link>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { extractErrorMessage, extractFieldErrors } from '../api/errors'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const displayName = ref('')
const errorMessage = ref('')
const submitting = ref(false)

async function onSubmit() {
  errorMessage.value = ''
  submitting.value = true
  try {
    await authStore.register({ email: email.value, password: password.value, displayName: displayName.value })
    await router.push('/dashboard/cvs')
  } catch (error) {
    const fieldErrors = extractFieldErrors(error)
    errorMessage.value = fieldErrors.length > 0 ? fieldErrors.map((f) => f.message).join(', ') : extractErrorMessage(error)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="flex flex-center bg-grey-2" style="min-height: 100vh">
    <q-card class="q-pa-lg" style="width: 100%; max-width: 400px">
      <q-card-section>
        <div class="text-h5 text-weight-bold">Tạo tài khoản</div>
        <div class="text-caption text-grey-7">Bắt đầu quản lý CV của bạn</div>
      </q-card-section>

      <q-card-section>
        <q-form class="q-gutter-md" @submit.prevent="onSubmit">
          <q-input
            v-model="displayName"
            label="Họ và tên"
            data-testid="register-display-name"
            :rules="[(val) => !!val || 'Vui lòng nhập họ tên']"
            lazy-rules
          />
          <q-input
            v-model="email"
            type="email"
            label="Email"
            data-testid="register-email"
            :rules="[(val) => !!val || 'Email là bắt buộc']"
            lazy-rules
          />
          <q-input
            v-model="password"
            type="password"
            label="Mật khẩu"
            hint="Tối thiểu 8 ký tự"
            data-testid="register-password"
            :rules="[(val) => (val && val.length >= 8) || 'Mật khẩu cần ít nhất 8 ký tự']"
            lazy-rules
          />

          <div v-if="errorMessage" class="text-negative text-caption" data-testid="register-error">
            {{ errorMessage }}
          </div>

          <q-btn
            type="submit"
            color="primary"
            label="Đăng ký"
            class="full-width"
            :loading="submitting"
            data-testid="register-submit"
          />
        </q-form>
      </q-card-section>

      <q-card-section class="text-center text-caption">
        Đã có tài khoản?
        <router-link to="/login">Đăng nhập</router-link>
      </q-card-section>
    </q-card>
  </div>
</template>

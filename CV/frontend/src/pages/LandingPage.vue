<script setup lang="ts"></script>

<template>
  <div class="flex flex-center" style="min-height: 100vh">
    <div class="text-center q-pa-xl" style="max-width: 640px">
      <div class="text-h3 text-weight-bold text-primary">CV Platform</div>
      <p class="text-h6 text-grey-8 q-mt-md">
        Lưu trữ, quản lý và chia sẻ CV của bạn qua một đường link chuyên nghiệp -
        không cần bắt nhà tuyển dụng tải file.
      </p>
      <div class="q-mt-lg">
        <q-btn color="primary" size="lg" label="Bắt đầu miễn phí" to="/register" class="q-mr-sm" />
        <q-btn flat color="primary" size="lg" label="Đăng nhập" to="/login" />
      </div>
    </div>
  </div>
</template>

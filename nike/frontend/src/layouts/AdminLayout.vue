<script setup>
import AdminSliderBar from 'components/admin/navbar/AdminSlideBar.vue'
</script>
<template>
  <div class="grid h-dvh w-dvw grid-cols-7 bg-gray-200 text-gray-500">
    <!-- SideBar -->
    <AdminSliderBar />
    <!-- View Content -->
    <div class="col-span-6 bg-white p-5">
      <router-view></router-view>
    </div>
  </div>
</template>

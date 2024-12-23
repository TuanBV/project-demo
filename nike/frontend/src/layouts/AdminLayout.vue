<script setup>
// import NavBar from 'components/navbar/NavBar.vue'
// import FooterView from 'components/footer/FooterView.vue'
// import AlertView from 'components/alert/AlertView.vue'
import AdminSliderBar from 'components/navbar/AdminSlideBar.vue'
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

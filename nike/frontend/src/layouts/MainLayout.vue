<script setup>
import NavBar from 'components/navbar/NavBar.vue'
import FooterView from 'components/footer/FooterView.vue'
import AlertView from 'components/alert/AlertView.vue'
</script>
<template>
  <AlertView />

  <nav-bar></nav-bar>
  <!-- bg-[#EFEFEF] -->
  <div class="min-h-[100vh] w-full pt-[70px]">
    <router-view></router-view>
  </div>
  <footer-view></footer-view>
</template>

<script setup>
import NavBar from 'components/user/navbar/NavBar.vue'
import FooterView from 'components/user/footer/FooterView.vue'
import AlertView from 'components/common/alert/AlertView.vue'
</script>
<template>
  <AlertView />

  <nav-bar></nav-bar>
  <!-- bg-[#EFEFEF] -->
  <div class="w-full pt-[70px]">
    <router-view></router-view>
  </div>
  <footer-view></footer-view>
</template>

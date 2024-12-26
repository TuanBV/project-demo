<script setup>
import { ref } from 'vue'
const socialMedia = ref([
  {
    name: 'Facebook',
    link: 'https://www.facebook.com/',
    icon: 'src/assets/facebook.svg'
  },
  {
    name: 'Instagram',
    link: 'https://www.instgram.com/',
    icon: 'src/assets/instagram.svg'
  },
  {
    name: 'Tiktok',
    link: 'https://www.tiktok.com/',
    icon: 'src/assets/tiktok.svg'
  },
  {
    name: 'Twitter',
    link: 'https://www.twitter.com/',
    icon: 'src/assets/twitter.svg'
  }
])
</script>
<template>
  <li v-for="(item, index) in socialMedia" :key="index">
    <slot :item="item"></slot>
  </li>
</template>

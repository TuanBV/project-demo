<script setup>
import { computed } from 'vue'
import { useAppStore } from 'stores/app-store'

const appStore = useAppStore()

const socialMedia = computed(() => appStore.info)
</script>
<template>
  <li v-for="(item, index) in socialMedia" :key="index">
    <slot v-if="index.includes('_link')" :item="item"></slot>
  </li>
</template>

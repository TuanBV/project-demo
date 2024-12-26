<script setup>
import { storeToRefs } from 'pinia'
import { useAppStore } from './stores/app-store'
import LoadingView from 'components/common/loading/LoadingView.vue'

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const { isLoading } = storeToRefs(useAppStore())
// ==> 1.2) actions
// ==> 1.3) Others
// 2) ======= VARIABLE REF ========
// 3) ======= METHOD/FUNCTION ========
// 4) ======= VUE JS LIFECYCLE ========
</script>
<template>
  <router-view></router-view>
  <loading-view v-if="isLoading">
    <template #loading></template>
  </loading-view>
</template>

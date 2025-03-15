<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAppStore } from 'stores/app-store'
import settingService from 'service/setting.service'
import LoadingView from 'components/common/loading/LoadingView.vue'
import ToastUtil from 'utility/toast'
// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const appStore = useAppStore()
const { isLoading } = storeToRefs(useAppStore())
// ==> 1.2) actions
// ==> 1.3) Others
// 2) ======= VARIABLE REF ========
// 3) ======= METHOD/FUNCTION ========
// 4) ======= VUE JS LIFECYCLE ========
// Get info
const getInfo = async () => {
  const res = await settingService.getNewSetting()
  if (res) {
    appStore.setInfo(res)
    return
  }
  ToastUtil.error('Get info failed')
}
onMounted(async () => {
  await getInfo()
})
</script>
<template>
  <router-view></router-view>
  <loading-view v-if="isLoading">
    <template #loading></template>
  </loading-view>
</template>

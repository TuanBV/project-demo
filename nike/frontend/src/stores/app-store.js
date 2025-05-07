import { defineStore } from 'pinia'

export const useAppStore = defineStore('appStore', {
  state: () => ({
    loading: false,
    info: {},
  }),
  getters: {
    isLoading: state => state.loading,
  },
  actions: {
    setLoading(boolFlg) {
      this.loading = boolFlg
    },
    setInfo(info) {
      this.info = info
    },
  },
})

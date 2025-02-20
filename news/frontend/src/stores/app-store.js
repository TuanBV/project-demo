import { defineStore } from 'pinia'

export const useAppStore = defineStore('appStore', {
  state: () => ({
    loading: false
  }),
  getters: {
    isLoading: (state) => state.loading
  },
  actions: {
    setLoading(boolFlg) {
      this.loading = boolFlg
    }
  }
})

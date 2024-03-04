import { defineStore } from 'pinia';

export const useAppStore = defineStore('appStore', {
  state: () => ({
    loading: false,
    currentRouterName: '',
  }),
  getters: {
    isLoading: (state) => state.loading,
  },
  actions: {
    setLoading(boolFlg) {
      this.loading = boolFlg;
    },
    setCurrentRouterName(routeName) {
      this.currentRouterName = routeName;
    },
  },
});

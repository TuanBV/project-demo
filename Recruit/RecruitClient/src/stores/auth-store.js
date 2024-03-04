import { defineStore } from 'pinia';

export const useAuthStore = defineStore('authStore', {
  state: () => ({
    user: {},
  }),
  getters: {
    isLoggedIn: (state) => state.user?.email,
  },
  actions: {
    signIn(userData) {
      this.user = userData;
    },
    signOut() {
      this.user = {};
    },
  },
});

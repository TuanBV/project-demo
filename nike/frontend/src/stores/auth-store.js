import { defineStore } from 'pinia'

export const useAuthStore = defineStore('authStore', {
  state: () => ({
    user: {}
  }),
  getters: {
    isLoggedIn: (state) => state.user?.email,
    getRole: (state) => state.user?.role
  },
  actions: {
    signIn(userData) {
      this.user = userData
    },
    signOut() {
      this.user = {}
    }
  }
})

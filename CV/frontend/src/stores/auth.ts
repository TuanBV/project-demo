import { defineStore } from 'pinia'
import { authApi, type LoginPayload, type RegisterPayload, type UserResponse } from '../api/auth'

interface AuthState {
  accessToken: string | null
  user: UserResponse | null
  /** True once the initial silent-refresh attempt on app boot has settled. */
  sessionChecked: boolean
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    accessToken: null,
    user: null,
    sessionChecked: false,
  }),

  getters: {
    isAuthenticated: (state) => state.accessToken !== null && state.user !== null,
  },

  actions: {
    async register(payload: RegisterPayload) {
      const result = await authApi.register(payload)
      this.applySession(result.accessToken, result.user)
    },

    async login(payload: LoginPayload) {
      const result = await authApi.login(payload)
      this.applySession(result.accessToken, result.user)
    },

    async logout() {
      try {
        await authApi.logout()
      } finally {
        this.clearSession()
      }
    },

    /**
     * Tries to turn the HttpOnly refresh cookie into a fresh access token.
     * Never throws - callers (app bootstrap, the axios 401 interceptor) only
     * care whether it succeeded.
     */
    async tryRestoreSession(): Promise<boolean> {
      try {
        const result = await authApi.refresh()
        this.applySession(result.accessToken, result.user)
        return true
      } catch {
        this.clearSession()
        return false
      } finally {
        this.sessionChecked = true
      }
    },

    applySession(accessToken: string, user: UserResponse) {
      this.accessToken = accessToken
      this.user = user
    },

    clearSession() {
      this.accessToken = null
      this.user = null
    },
  },
})

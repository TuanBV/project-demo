import axios, { AxiosError, type InternalAxiosRequestConfig } from 'axios'
import { useAuthStore } from '../stores/auth'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8082',
  withCredentials: true,
})

apiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.accessToken) {
    config.headers.set('Authorization', `Bearer ${authStore.accessToken}`)
  }
  return config
})

declare module 'axios' {
  export interface InternalAxiosRequestConfig {
    _retriedAfterRefresh?: boolean
  }
}

// A 401 on any authenticated call almost always means the short-lived access
// token expired. Attempt exactly one silent refresh (via the HttpOnly cookie)
// and replay the original request before giving up and logging the user out.
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig | undefined
    const isAuthEndpoint = originalRequest?.url?.includes('/api/v1/auth/')

    if (error.response?.status !== 401 || !originalRequest || originalRequest._retriedAfterRefresh || isAuthEndpoint) {
      throw error
    }

    const authStore = useAuthStore()
    originalRequest._retriedAfterRefresh = true
    const refreshed = await authStore.tryRestoreSession()
    if (!refreshed) {
      authStore.clearSession()
      throw error
    }
    return apiClient(originalRequest)
  },
)

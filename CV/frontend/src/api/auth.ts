import { apiClient } from './client'

export interface UserResponse {
  id: string
  email: string
  displayName: string
  status: string
}

export interface AccessTokenResponse {
  accessToken: string
  expiresInSeconds: number
  user: UserResponse
}

export interface RegisterPayload {
  email: string
  password: string
  displayName: string
}

export interface LoginPayload {
  email: string
  password: string
}

export const authApi = {
  register: (payload: RegisterPayload) =>
    apiClient.post<AccessTokenResponse>('/api/v1/auth/register', payload).then((r) => r.data),

  login: (payload: LoginPayload) =>
    apiClient.post<AccessTokenResponse>('/api/v1/auth/login', payload).then((r) => r.data),

  refresh: () => apiClient.post<AccessTokenResponse>('/api/v1/auth/refresh').then((r) => r.data),

  logout: () => apiClient.post<void>('/api/v1/auth/logout'),

  me: () => apiClient.get<UserResponse>('/api/v1/me').then((r) => r.data),

  forgotPassword: (email: string) => apiClient.post<void>('/api/v1/auth/forgot-password', { email }),

  resetPassword: (token: string, newPassword: string) =>
    apiClient.post<void>('/api/v1/auth/reset-password', { token, newPassword }),

  changePassword: (currentPassword: string, newPassword: string) =>
    apiClient.post<void>('/api/v1/me/change-password', { currentPassword, newPassword }),
}

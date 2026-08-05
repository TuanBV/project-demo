import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '../auth'
import { authApi } from '../../api/auth'

vi.mock('../../api/auth', () => ({
  authApi: {
    login: vi.fn(),
    register: vi.fn(),
    refresh: vi.fn(),
    logout: vi.fn(),
    me: vi.fn(),
  },
}))

const sampleUser = { id: '1', email: 'user@example.com', displayName: 'User', status: 'ACTIVE' }

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('is not authenticated before any session exists', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
  })

  it('becomes authenticated after a successful login', async () => {
    vi.mocked(authApi.login).mockResolvedValueOnce({ accessToken: 'tok', expiresInSeconds: 900, user: sampleUser })

    const store = useAuthStore()
    await store.login({ email: 'user@example.com', password: 'password123' })

    expect(store.isAuthenticated).toBe(true)
    expect(store.user?.email).toBe('user@example.com')
  })

  it('clears the session when the refresh cookie is invalid or missing', async () => {
    vi.mocked(authApi.refresh).mockRejectedValueOnce(new Error('no refresh cookie'))

    const store = useAuthStore()
    const restored = await store.tryRestoreSession()

    expect(restored).toBe(false)
    expect(store.isAuthenticated).toBe(false)
    expect(store.sessionChecked).toBe(true)
  })

  it('clears local session state on logout even if the server call fails', async () => {
    vi.mocked(authApi.login).mockResolvedValueOnce({ accessToken: 'tok', expiresInSeconds: 900, user: sampleUser })
    vi.mocked(authApi.logout).mockRejectedValueOnce(new Error('network error'))

    const store = useAuthStore()
    await store.login({ email: 'user@example.com', password: 'password123' })

    await expect(store.logout()).rejects.toThrow()
    expect(store.isAuthenticated).toBe(false)
  })
})

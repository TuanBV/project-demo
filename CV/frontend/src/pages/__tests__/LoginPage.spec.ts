import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import { Quasar } from 'quasar'
import LoginPage from '../LoginPage.vue'
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

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/login', component: LoginPage },
      { path: '/register', component: { template: '<div data-testid="register" />' } },
      { path: '/dashboard/cvs', component: { template: '<div data-testid="dashboard" />' } },
    ],
  })
}

describe('LoginPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('shows the backend error message when credentials are rejected', async () => {
    vi.mocked(authApi.login).mockRejectedValueOnce({
      isAxiosError: true,
      response: {
        data: { code: 'INVALID_CREDENTIALS', message: 'Email or password is incorrect', fieldErrors: [], traceId: 'x' },
      },
    })

    const router = createTestRouter()
    await router.push('/login')
    await router.isReady()

    const wrapper = mount(LoginPage, { global: { plugins: [[Quasar, {}], router] } })

    await wrapper.find('[data-testid="login-email"]').setValue('user@example.com')
    await wrapper.find('[data-testid="login-password"]').setValue('wrong-password')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.find('[data-testid="login-error"]').text()).toContain('Email or password is incorrect')
  })

  it('redirects to the dashboard after a successful login', async () => {
    vi.mocked(authApi.login).mockResolvedValueOnce({
      accessToken: 'token-123',
      expiresInSeconds: 900,
      user: { id: '1', email: 'user@example.com', displayName: 'User', status: 'ACTIVE' },
    })

    const router = createTestRouter()
    await router.push('/login')
    await router.isReady()

    const wrapper = mount(LoginPage, { global: { plugins: [[Quasar, {}], router] } })

    await wrapper.find('[data-testid="login-email"]').setValue('user@example.com')
    await wrapper.find('[data-testid="login-password"]').setValue('correct-password')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(router.currentRoute.value.path).toBe('/dashboard/cvs')
  })
})

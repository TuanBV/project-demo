import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import { Quasar } from 'quasar'
import RegisterPage from '../RegisterPage.vue'
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
      { path: '/register', component: RegisterPage },
      { path: '/login', component: { template: '<div data-testid="login" />' } },
      { path: '/dashboard/cvs', component: { template: '<div data-testid="dashboard" />' } },
    ],
  })
}

describe('RegisterPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('shows the duplicate-email error returned by the backend', async () => {
    vi.mocked(authApi.register).mockRejectedValueOnce({
      isAxiosError: true,
      response: {
        data: { code: 'EMAIL_ALREADY_REGISTERED', message: 'An account with this email already exists', fieldErrors: [], traceId: 'x' },
      },
    })

    const router = createTestRouter()
    await router.push('/register')
    await router.isReady()

    const wrapper = mount(RegisterPage, { global: { plugins: [[Quasar, {}], router] } })

    await wrapper.find('[data-testid="register-display-name"]').setValue('Jane Doe')
    await wrapper.find('[data-testid="register-email"]').setValue('jane@example.com')
    await wrapper.find('[data-testid="register-password"]').setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(wrapper.find('[data-testid="register-error"]').text()).toContain('already exists')
  })

  it('redirects to the dashboard after a successful registration', async () => {
    vi.mocked(authApi.register).mockResolvedValueOnce({
      accessToken: 'token-123',
      expiresInSeconds: 900,
      user: { id: '1', email: 'jane@example.com', displayName: 'Jane Doe', status: 'ACTIVE' },
    })

    const router = createTestRouter()
    await router.push('/register')
    await router.isReady()

    const wrapper = mount(RegisterPage, { global: { plugins: [[Quasar, {}], router] } })

    await wrapper.find('[data-testid="register-display-name"]').setValue('Jane Doe')
    await wrapper.find('[data-testid="register-email"]').setValue('jane@example.com')
    await wrapper.find('[data-testid="register-password"]').setValue('password123')
    await wrapper.find('form').trigger('submit.prevent')
    await flushPromises()

    expect(router.currentRoute.value.path).toBe('/dashboard/cvs')
  })
})

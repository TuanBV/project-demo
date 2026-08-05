import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises, DOMWrapper } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import { Quasar, Notify, Dialog } from 'quasar'
import DashboardCvsPage from '../DashboardCvsPage.vue'
import { resumesApi } from '../../api/resumes'

vi.mock('../../api/resumes', () => ({
  resumesApi: {
    list: vi.fn(),
    create: vi.fn(),
    get: vi.fn(),
    update: vi.fn(),
    remove: vi.fn(),
    restore: vi.fn(),
    duplicate: vi.fn(),
  },
}))

vi.mock('../../api/auth', () => ({
  authApi: {
    login: vi.fn(),
    register: vi.fn(),
    refresh: vi.fn(),
    logout: vi.fn().mockResolvedValue(undefined),
    me: vi.fn(),
  },
}))

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/dashboard/cvs', component: DashboardCvsPage },
      { path: '/dashboard/cvs/:id/edit', component: { template: '<div/>' } },
      { path: '/login', component: { template: '<div/>' } },
    ],
  })
}

const sampleResume = {
  id: 'r1',
  publicId: 'p1',
  name: 'My CV',
  slug: 'my-cv',
  resumeType: 'PDF' as const,
  status: 'DRAFT' as const,
  visibility: 'PRIVATE' as const,
  allowDownload: false,
  searchEngineIndexable: false,
  isDefault: false,
  activeVersionId: null,
  viewCount: 0,
  publishedAt: null,
  publicUrl: null,
  unlistedShareToken: null,
  createdAt: '2026-08-05T00:00:00Z',
  updatedAt: '2026-08-05T00:00:00Z',
  deletedAt: null,
  restorableUntil: null,
}

async function mountDashboard() {
  const router = createTestRouter()
  await router.push('/dashboard/cvs')
  await router.isReady()
  return mount(DashboardCvsPage, {
    global: { plugins: [[Quasar, { plugins: { Notify, Dialog } }], createPinia(), router] },
  })
}

describe('DashboardCvsPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('renders resumes returned by the API', async () => {
    vi.mocked(resumesApi.list).mockResolvedValueOnce([sampleResume])

    const wrapper = await mountDashboard()
    await flushPromises()

    expect(resumesApi.list).toHaveBeenCalledWith(false)
    const cards = wrapper.findAll('[data-testid="resume-card"]')
    expect(cards).toHaveLength(1)
    expect(cards[0].text()).toContain('My CV')
  })

  it('shows an empty state when there are no resumes', async () => {
    vi.mocked(resumesApi.list).mockResolvedValueOnce([])

    const wrapper = await mountDashboard()
    await flushPromises()

    expect(wrapper.text()).toContain('Chưa có CV nào')
  })

  it('creates a resume and reloads the list', async () => {
    vi.mocked(resumesApi.list).mockResolvedValueOnce([]).mockResolvedValueOnce([sampleResume])
    vi.mocked(resumesApi.create).mockResolvedValueOnce(sampleResume)

    const wrapper = await mountDashboard()
    await flushPromises()

    await wrapper.find('[data-testid="create-resume-button"]').trigger('click')
    await flushPromises()
    // QDialog teleports its content to document.body, outside `wrapper`'s subtree.
    const body = new DOMWrapper(document.body)
    await body.find('[data-testid="new-resume-name"]').setValue('My CV')
    await body.find('[data-testid="confirm-create-resume"]').trigger('click')
    await flushPromises()

    expect(resumesApi.create).toHaveBeenCalledWith('My CV', 'PDF')
    expect(resumesApi.list).toHaveBeenCalledTimes(2)
  })
})

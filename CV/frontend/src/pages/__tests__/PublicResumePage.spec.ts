import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import { Quasar, Notify, Dialog } from 'quasar'
import PublicResumePage from '../PublicResumePage.vue'
import { publicResumeApi } from '../../api/public'

vi.mock('qrcode', () => ({
  default: { toDataURL: vi.fn().mockResolvedValue('data:image/png;base64,fake') },
}))

vi.mock('../../api/public', () => ({
  publicResumeApi: {
    get: vi.fn(),
    fileBlob: vi.fn(),
    fileUrl: vi.fn(),
    recordView: vi.fn().mockResolvedValue(undefined),
  },
}))

const publicResume = {
  publicId: 'p1',
  name: 'My CV',
  slug: 'my-cv',
  resumeType: 'PDF' as const,
  allowDownload: false,
  searchEngineIndexable: true,
  canonicalUrl: 'http://localhost:5174/cv/p1/my-cv',
  sections: [],
}

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [{ path: '/cv/:publicId/:slug', component: PublicResumePage }],
  })
}

async function mountPublicPage(path = '/cv/p1/my-cv') {
  const router = createTestRouter()
  await router.push(path)
  await router.isReady()
  return mount(PublicResumePage, {
    global: { plugins: [[Quasar, { plugins: { Notify, Dialog } }], createPinia(), router] },
  })
}

describe('PublicResumePage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('renders the CV name and PDF viewer when the resume is found', async () => {
    vi.mocked(publicResumeApi.get).mockResolvedValueOnce(publicResume)
    vi.mocked(publicResumeApi.fileBlob).mockResolvedValueOnce(new Blob(['%PDF-1.4'], { type: 'application/pdf' }))

    const wrapper = await mountPublicPage()
    await flushPromises()

    expect(wrapper.find('[data-testid="public-resume-name"]').text()).toBe('My CV')
    expect(wrapper.find('[data-testid="pdf-viewer"]').exists()).toBe(true)
  })

  it('records a view once the resume loads successfully', async () => {
    vi.mocked(publicResumeApi.get).mockResolvedValueOnce(publicResume)
    vi.mocked(publicResumeApi.fileBlob).mockResolvedValueOnce(new Blob(['%PDF-1.4'], { type: 'application/pdf' }))

    await mountPublicPage()
    await flushPromises()

    expect(publicResumeApi.recordView).toHaveBeenCalledWith('p1', 'my-cv')
  })

  it('shows a not-found message when the backend returns 404', async () => {
    vi.mocked(publicResumeApi.get).mockRejectedValueOnce({ isAxiosError: true, response: { status: 404 } })

    const wrapper = await mountPublicPage()
    await flushPromises()

    expect(wrapper.text()).toContain('Không tìm thấy')
    expect(publicResumeApi.recordView).not.toHaveBeenCalled()
  })

  it('shows a link-gone message when the backend returns 410', async () => {
    vi.mocked(publicResumeApi.get).mockRejectedValueOnce({ isAxiosError: true, response: { status: 410 } })

    const wrapper = await mountPublicPage()
    await flushPromises()

    expect(wrapper.find('[data-testid="link-gone-message"]').exists()).toBe(true)
  })

  it('hides the download button when the owner has not allowed downloads', async () => {
    vi.mocked(publicResumeApi.get).mockResolvedValueOnce({ ...publicResume, allowDownload: false })
    vi.mocked(publicResumeApi.fileBlob).mockResolvedValueOnce(new Blob(['%PDF-1.4'], { type: 'application/pdf' }))

    const wrapper = await mountPublicPage()
    await flushPromises()

    expect(wrapper.find('[data-testid="download-button"]').exists()).toBe(false)
  })

  it('shows the download button when the owner has allowed downloads', async () => {
    vi.mocked(publicResumeApi.get).mockResolvedValueOnce({ ...publicResume, allowDownload: true })
    vi.mocked(publicResumeApi.fileBlob).mockResolvedValueOnce(new Blob(['%PDF-1.4'], { type: 'application/pdf' }))

    const wrapper = await mountPublicPage()
    await flushPromises()

    expect(wrapper.find('[data-testid="download-button"]').exists()).toBe(true)
  })
})

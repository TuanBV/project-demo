import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createMemoryHistory } from 'vue-router'
import { Quasar, Notify, Dialog, QSelect } from 'quasar'
import ResumeEditPage from '../ResumeEditPage.vue'
import { resumesApi } from '../../api/resumes'

vi.mock('qrcode', () => ({
  default: { toDataURL: vi.fn().mockResolvedValue('data:image/png;base64,fake') },
}))

vi.mock('../../api/resumes', () => ({
  resumesApi: {
    get: vi.fn(),
    listVersions: vi.fn(),
    update: vi.fn(),
    uploadPdfVersion: vi.fn(),
    activateVersion: vi.fn(),
    deleteVersion: vi.fn(),
    previewFileBlob: vi.fn(),
    publish: vi.fn(),
    unpublish: vi.fn(),
    regenerateLink: vi.fn(),
    analyticsSummary: vi.fn(),
  },
}))

const emptySummary = { totalViews: 0, views7d: 0, views30d: 0, lastViewedAt: null }

const pdfResume = {
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
  activeVersionId: 'v1',
  viewCount: 0,
  publishedAt: null,
  publicUrl: null,
  unlistedShareToken: null,
  createdAt: '2026-08-05T00:00:00Z',
  updatedAt: '2026-08-05T00:00:00Z',
  deletedAt: null,
  restorableUntil: null,
}

const version1 = {
  id: 'v1',
  versionNumber: 1,
  sourceType: 'PDF' as const,
  active: true,
  originalFilename: 'resume.pdf',
  sizeBytes: 2048,
  contentType: 'application/pdf',
  checksum: 'abc',
  createdAt: '2026-08-05T00:00:00Z',
}

function createTestRouter() {
  return createRouter({
    history: createMemoryHistory(),
    routes: [
      { path: '/dashboard/cvs', component: { template: '<div/>' } },
      { path: '/dashboard/cvs/:id/edit', component: ResumeEditPage },
    ],
  })
}

async function mountEditPage() {
  const router = createTestRouter()
  await router.push('/dashboard/cvs/r1/edit')
  await router.isReady()
  return mount(ResumeEditPage, {
    global: { plugins: [[Quasar, { plugins: { Notify, Dialog } }], createPinia(), router] },
  })
}

describe('ResumeEditPage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
    vi.mocked(resumesApi.analyticsSummary).mockResolvedValue(emptySummary)
  })

  it('loads the resume and its versions', async () => {
    vi.mocked(resumesApi.get).mockResolvedValueOnce(pdfResume)
    vi.mocked(resumesApi.listVersions).mockResolvedValueOnce([version1])

    const wrapper = await mountEditPage()
    await flushPromises()

    expect(resumesApi.get).toHaveBeenCalledWith('r1')
    expect(wrapper.find('[data-testid="resume-name-input"]').element as HTMLInputElement).toHaveProperty('value', 'My CV')
    expect(wrapper.find('[data-testid="version-list"]').text()).toContain('resume.pdf')
    expect(wrapper.find('[data-testid="version-list"]').text()).toContain('Đang dùng')
  })

  it('saves a renamed resume', async () => {
    vi.mocked(resumesApi.get).mockResolvedValueOnce(pdfResume)
    vi.mocked(resumesApi.listVersions).mockResolvedValueOnce([version1])
    vi.mocked(resumesApi.update).mockResolvedValueOnce({ ...pdfResume, name: 'Renamed CV' })

    const wrapper = await mountEditPage()
    await flushPromises()

    await wrapper.find('[data-testid="resume-name-input"]').setValue('Renamed CV')
    await wrapper.find('[data-testid="save-resume-name"]').trigger('click')
    await flushPromises()

    expect(resumesApi.update).toHaveBeenCalledWith('r1', { name: 'Renamed CV' })
  })

  it('disables the upload button until a file is chosen', async () => {
    vi.mocked(resumesApi.get).mockResolvedValueOnce(pdfResume)
    vi.mocked(resumesApi.listVersions).mockResolvedValueOnce([version1])

    const wrapper = await mountEditPage()
    await flushPromises()

    const uploadButton = wrapper.find('[data-testid="upload-pdf-button"]')
    expect(uploadButton.attributes('disabled')).toBeDefined()
    expect(resumesApi.uploadPdfVersion).not.toHaveBeenCalled()
  })

  it('disables deleting the active version', async () => {
    vi.mocked(resumesApi.get).mockResolvedValueOnce(pdfResume)
    vi.mocked(resumesApi.listVersions).mockResolvedValueOnce([version1])

    const wrapper = await mountEditPage()
    await flushPromises()

    const deleteButtons = wrapper.findAll('[data-testid="version-list"] button')
    const activeDeleteButton = deleteButtons.find((b) => b.attributes('disabled') !== undefined)
    expect(activeDeleteButton).toBeTruthy()
  })

  it('shows a publish button for a draft resume and calls publish on click', async () => {
    vi.mocked(resumesApi.get).mockResolvedValueOnce(pdfResume)
    vi.mocked(resumesApi.listVersions).mockResolvedValueOnce([version1])
    vi.mocked(resumesApi.publish).mockResolvedValueOnce({ ...pdfResume, status: 'PUBLISHED', publishedAt: '2026-08-05T00:00:00Z' })

    const wrapper = await mountEditPage()
    await flushPromises()

    expect(wrapper.find('[data-testid="unpublish-button"]').exists()).toBe(false)
    await wrapper.find('[data-testid="publish-button"]').trigger('click')
    await flushPromises()

    expect(resumesApi.publish).toHaveBeenCalledWith('r1')
    expect(wrapper.find('[data-testid="unpublish-button"]').exists()).toBe(true)
  })

  it('shows the public link and QR trigger once published and public', async () => {
    const publishedPublic = {
      ...pdfResume,
      status: 'PUBLISHED' as const,
      visibility: 'PUBLIC' as const,
      publicUrl: 'http://localhost:5174/cv/p1/my-cv',
    }
    vi.mocked(resumesApi.get).mockResolvedValueOnce(publishedPublic)
    vi.mocked(resumesApi.listVersions).mockResolvedValueOnce([version1])

    const wrapper = await mountEditPage()
    await flushPromises()

    expect(wrapper.find('[data-testid="public-link-text"]').text()).toContain('/cv/p1/my-cv')
  })

  it('reveals the unlisted share token exactly once, right after switching visibility', async () => {
    vi.mocked(resumesApi.get).mockResolvedValueOnce(pdfResume)
    vi.mocked(resumesApi.listVersions).mockResolvedValueOnce([version1])
    vi.mocked(resumesApi.update).mockResolvedValueOnce({
      ...pdfResume,
      visibility: 'UNLISTED',
      unlistedShareToken: 'raw-token-abc',
    })

    const wrapper = await mountEditPage()
    await flushPromises()

    await wrapper.findComponent(QSelect).setValue('UNLISTED')
    await flushPromises()

    expect(resumesApi.update).toHaveBeenCalledWith('r1', { visibility: 'UNLISTED' })
    expect(document.body.textContent).toContain('raw-token-abc')
  })
})

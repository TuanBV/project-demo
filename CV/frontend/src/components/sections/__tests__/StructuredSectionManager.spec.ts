import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises, DOMWrapper } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { Quasar, Notify, Dialog } from 'quasar'
import StructuredSectionManager from '../StructuredSectionManager.vue'
import { sectionsApi } from '../../../api/sections'

vi.mock('../../../api/sections', () => ({
  sectionsApi: {
    list: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
    remove: vi.fn(),
    reorder: vi.fn(),
    preview: vi.fn(),
  },
}))

const summarySection = {
  id: 's1',
  sectionType: 'SUMMARY' as const,
  title: 'Giới thiệu bản thân',
  position: 0,
  visible: true,
  content: { text: 'Hello' },
}

function mountManager() {
  return mount(StructuredSectionManager, {
    props: { resumeId: 'r1' },
    global: { plugins: [[Quasar, { plugins: { Notify, Dialog } }], createPinia()] },
  })
}

describe('StructuredSectionManager', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('shows an empty-state hint when there are no sections yet', async () => {
    vi.mocked(sectionsApi.list).mockResolvedValueOnce([])

    const wrapper = mountManager()
    await flushPromises()

    expect(wrapper.text()).toContain('Chưa có mục nào')
  })

  it('renders existing sections', async () => {
    vi.mocked(sectionsApi.list).mockResolvedValueOnce([summarySection])

    const wrapper = mountManager()
    await flushPromises()

    expect(wrapper.find('[data-testid="section-list"]').text()).toContain('Giới thiệu bản thân')
  })

  it('disables adding a section type that already exists, one per type', async () => {
    const allTypes = ['PERSONAL_INFO', 'SUMMARY', 'SKILLS', 'EXPERIENCE', 'PROJECTS', 'EDUCATION', 'LANGUAGES', 'CERTIFICATIONS', 'LINKS', 'ADDITIONAL']
    const allSections = allTypes.map((t, i) => ({ ...summarySection, id: `s${i}`, sectionType: t, title: t }))
    vi.mocked(sectionsApi.list).mockResolvedValueOnce(allSections as never)

    const wrapper = mountManager()
    await flushPromises()

    expect(wrapper.find('[data-testid="add-section-button"]').attributes('disabled')).toBeDefined()
  })

  it('creates a new section via the add dialog', async () => {
    vi.mocked(sectionsApi.list).mockResolvedValueOnce([]).mockResolvedValueOnce([summarySection])
    vi.mocked(sectionsApi.create).mockResolvedValueOnce(summarySection)

    const wrapper = mountManager()
    await flushPromises()

    await wrapper.find('[data-testid="add-section-button"]').trigger('click')
    await flushPromises()

    const body = new DOMWrapper(document.body)
    const dialogAddButton = body.findAll('button').find((b) => b.text() === 'Thêm')
    await dialogAddButton!.trigger('click')
    await flushPromises()

    expect(sectionsApi.create).toHaveBeenCalled()
    expect(sectionsApi.list).toHaveBeenCalledTimes(2)
  })

  it('saves edited content for a section', async () => {
    vi.mocked(sectionsApi.list).mockResolvedValue([summarySection])
    vi.mocked(sectionsApi.update).mockResolvedValueOnce({ ...summarySection, content: { text: 'Updated' } })

    const wrapper = mountManager()
    await flushPromises()

    // Expand the section to reveal its form + Save button.
    await wrapper.find('[data-testid="section-list"] .q-item').trigger('click')
    await flushPromises()

    const saveButton = wrapper.findAll('button').find((b) => b.text() === 'Lưu')
    await saveButton!.trigger('click')
    await flushPromises()

    expect(sectionsApi.update).toHaveBeenCalledWith('r1', 's1', { content: expect.objectContaining({ text: 'Hello' }) })
  })

  it('removes a section after confirming the delete dialog', async () => {
    vi.mocked(sectionsApi.list).mockResolvedValueOnce([summarySection]).mockResolvedValueOnce([])
    vi.mocked(sectionsApi.remove).mockResolvedValueOnce(undefined as never)

    const wrapper = mountManager()
    await flushPromises()

    const deleteButton = wrapper.findAll('button').find((b) => b.find('.q-icon').exists() && b.classes().some((c) => c.includes('negative')))
    await deleteButton!.trigger('click')
    await flushPromises()

    const body = new DOMWrapper(document.body)
    const confirmButton = body.findAll('button').find((b) => b.text() === 'OK')
    await confirmButton!.trigger('click')
    await flushPromises()

    expect(sectionsApi.remove).toHaveBeenCalledWith('r1', 's1')
  })
})

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { Quasar } from 'quasar'
import StructuredResumeView from '../StructuredResumeView.vue'
import type { SnapshotSection } from '../../../api/sections'

function mountView(sections: SnapshotSection[]) {
  return mount(StructuredResumeView, {
    props: { sections },
    global: { plugins: [Quasar] },
  })
}

describe('StructuredResumeView', () => {
  it('renders personal info without showing a masked (null) phone', () => {
    const sections: SnapshotSection[] = [
      {
        type: 'PERSONAL_INFO',
        title: 'Info',
        position: 0,
        content: { fullName: 'Jane Doe', headline: 'Engineer', email: 'jane@example.com', phone: null, location: 'Hanoi', website: null },
      },
    ]

    const wrapper = mountView(sections)

    expect(wrapper.text()).toContain('Jane Doe')
    expect(wrapper.text()).toContain('Engineer')
    expect(wrapper.text()).toContain('jane@example.com')
    // A masked (null) field must never render as the literal string "null".
    expect(wrapper.text()).not.toContain('null')
  })

  it('renders a summary section', () => {
    const sections: SnapshotSection[] = [
      { type: 'SUMMARY', title: 'Giới thiệu', position: 0, content: { text: 'Experienced engineer.' } },
    ]

    const wrapper = mountView(sections)

    expect(wrapper.text()).toContain('Experienced engineer.')
  })

  it('renders skills as chips with their level', () => {
    const sections: SnapshotSection[] = [
      { type: 'SKILLS', title: 'Skills', position: 0, content: { skills: [{ name: 'Java', level: 'EXPERT' }] } },
    ]

    const wrapper = mountView(sections)

    expect(wrapper.text()).toContain('Java')
    expect(wrapper.text()).toContain('EXPERT')
  })

  it('renders experience items with company, title and dates', () => {
    const sections: SnapshotSection[] = [
      {
        type: 'EXPERIENCE',
        title: 'Experience',
        position: 0,
        content: {
          items: [
            { company: 'Acme', title: 'Engineer', startDate: '2020-01', endDate: null, current: true, location: 'Remote', description: 'Built things' },
          ],
        },
      },
    ]

    const wrapper = mountView(sections)

    expect(wrapper.text()).toContain('Acme')
    expect(wrapper.text()).toContain('Engineer')
    expect(wrapper.text()).toContain('Hiện tại')
    expect(wrapper.text()).toContain('Built things')
  })

  it('renders nothing extra when there are no sections', () => {
    const wrapper = mountView([])

    expect(wrapper.findAll('.structured-section')).toHaveLength(0)
  })
})

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { Quasar } from 'quasar'
import RepeatableItemList from '../RepeatableItemList.vue'

const itemFields = [
  { key: 'name', label: 'Name' },
  { key: 'level', label: 'Level', type: 'select' as const, options: ['BEGINNER', 'EXPERT'] },
]

function mountList(modelValue: Record<string, unknown>[]) {
  return mount(RepeatableItemList, {
    props: { itemFields, emptyItem: { name: '', level: '' }, modelValue },
    global: { plugins: [Quasar] },
  })
}

describe('RepeatableItemList', () => {
  it('emits a new item appended when "Thêm mục" is clicked', async () => {
    const wrapper = mountList([{ name: 'Java', level: 'EXPERT' }])

    await wrapper.find('[data-testid="add-item-button"]').trigger('click')

    const emitted = wrapper.emitted('update:modelValue')
    expect(emitted).toBeTruthy()
    expect(emitted![0][0]).toEqual([{ name: 'Java', level: 'EXPERT' }, { name: '', level: '' }]);
  })

  it('emits the list without the removed item when delete is clicked', async () => {
    const wrapper = mountList([{ name: 'Java', level: 'EXPERT' }, { name: 'Go', level: 'BEGINNER' }])

    const items = wrapper.findAll('[data-testid="repeatable-item"]')
    await items[0].find('button').trigger('click')

    const emitted = wrapper.emitted('update:modelValue')
    expect(emitted![0][0]).toEqual([{ name: 'Go', level: 'BEGINNER' }])
  })

  it('renders one card per item', () => {
    const wrapper = mountList([{ name: 'Java', level: 'EXPERT' }, { name: 'Go', level: 'BEGINNER' }])

    expect(wrapper.findAll('[data-testid="repeatable-item"]')).toHaveLength(2)
  })
})

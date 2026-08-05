<script setup lang="ts">
import type { FieldDef } from '../../config/sectionFields'
import type { SectionContent } from '../../api/sections'

const props = defineProps<{
  itemFields: FieldDef[]
  emptyItem: SectionContent
  modelValue: SectionContent[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: SectionContent[]]
}>()

function setItemField(index: number, key: string, value: unknown) {
  const items = props.modelValue.map((item, i) => (i === index ? { ...item, [key]: value } : item))
  emit('update:modelValue', items)
}

function addItem() {
  emit('update:modelValue', [...props.modelValue, { ...props.emptyItem }])
}

function removeItem(index: number) {
  emit('update:modelValue', props.modelValue.filter((_, i) => i !== index))
}

function tagsToText(value: unknown): string {
  return Array.isArray(value) ? value.join(', ') : ''
}

function textToTags(text: string): string[] {
  return text.split(',').map((s) => s.trim()).filter((s) => s.length > 0)
}
</script>

<template>
  <div class="q-gutter-md">
    <q-card v-for="(item, index) in modelValue" :key="index" bordered flat class="q-pa-sm" data-testid="repeatable-item">
      <q-card-section class="q-gutter-sm">
        <template v-for="field in itemFields" :key="field.key">
          <q-checkbox
            v-if="field.type === 'checkbox'"
            :model-value="Boolean(item[field.key])"
            :label="field.label"
            @update:model-value="(v) => setItemField(index, field.key, v)"
          />
          <q-select
            v-else-if="field.type === 'select'"
            :model-value="item[field.key] ?? ''"
            :options="field.options ?? []"
            :label="field.label"
            @update:model-value="(v) => setItemField(index, field.key, v)"
          />
          <q-input
            v-else-if="field.type === 'tags'"
            :model-value="tagsToText(item[field.key])"
            :label="field.label"
            @update:model-value="(v) => setItemField(index, field.key, textToTags(String(v ?? '')))"
          />
          <q-input
            v-else-if="field.type === 'textarea'"
            :model-value="item[field.key] ?? ''"
            :label="field.label"
            type="textarea"
            autogrow
            @update:model-value="(v) => setItemField(index, field.key, v)"
          />
          <q-input
            v-else
            :model-value="item[field.key] ?? ''"
            :label="field.label"
            @update:model-value="(v) => setItemField(index, field.key, v)"
          />
        </template>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat dense icon="delete" color="negative" label="Xóa mục" @click="removeItem(index)" />
      </q-card-actions>
    </q-card>

    <q-btn flat dense icon="add" label="Thêm mục" data-testid="add-item-button" @click="addItem" />
  </div>
</template>

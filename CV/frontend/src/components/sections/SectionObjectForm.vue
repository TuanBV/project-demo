<script setup lang="ts">
import type { FieldDef } from '../../config/sectionFields'
import type { SectionContent } from '../../api/sections'

const props = defineProps<{
  fields: FieldDef[]
  modelValue: SectionContent
}>()

const emit = defineEmits<{
  'update:modelValue': [value: SectionContent]
}>()

function setField(key: string, value: unknown) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}
</script>

<template>
  <div class="q-gutter-md">
    <template v-for="field in fields" :key="field.key">
      <q-checkbox
        v-if="field.type === 'checkbox'"
        :model-value="Boolean(modelValue[field.key])"
        :label="field.label"
        :data-testid="`field-${field.key}`"
        @update:model-value="(v) => setField(field.key, v)"
      />
      <q-input
        v-else-if="field.type === 'textarea'"
        :model-value="modelValue[field.key] ?? ''"
        :label="field.label"
        type="textarea"
        autogrow
        :data-testid="`field-${field.key}`"
        @update:model-value="(v) => setField(field.key, v)"
      />
      <q-input
        v-else
        :model-value="modelValue[field.key] ?? ''"
        :label="field.label"
        :data-testid="`field-${field.key}`"
        @update:model-value="(v) => setField(field.key, v)"
      />
    </template>
  </div>
</template>

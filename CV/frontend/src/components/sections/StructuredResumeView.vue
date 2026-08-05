<script setup lang="ts">
import type { SnapshotSection } from '../../api/sections'

defineProps<{
  sections: SnapshotSection[]
}>()

function joinNonEmpty(parts: (string | null | undefined)[], sep = ' · ') {
  return parts.filter((p) => p && p.trim().length > 0).join(sep)
}
</script>

<template>
  <div class="structured-resume">
    <div v-for="section in sections" :key="section.type" class="structured-section">
      <template v-if="section.type === 'PERSONAL_INFO'">
        <div class="text-h4 text-weight-bold">{{ section.content.fullName }}</div>
        <div class="text-subtitle1 text-grey-8">{{ section.content.headline }}</div>
        <div class="text-caption text-grey-7 q-mt-xs">
          {{ joinNonEmpty([section.content.email, section.content.phone, section.content.location, section.content.website]) }}
        </div>
      </template>

      <template v-else-if="section.type === 'SUMMARY'">
        <div class="text-h6 q-mb-xs">{{ section.title }}</div>
        <p class="section-text">{{ section.content.text }}</p>
      </template>

      <template v-else-if="section.type === 'ADDITIONAL'">
        <div class="text-h6 q-mb-xs">{{ section.title }}</div>
        <p class="section-text">{{ section.content.text }}</p>
      </template>

      <template v-else-if="section.type === 'SKILLS'">
        <div class="text-h6 q-mb-xs">{{ section.title }}</div>
        <div class="row q-gutter-xs">
          <q-chip v-for="(skill, i) in section.content.skills" :key="i" dense outline>
            {{ skill.name }}<span v-if="skill.level" class="text-grey-7">&nbsp;({{ skill.level }})</span>
          </q-chip>
        </div>
      </template>

      <template v-else-if="section.type === 'LANGUAGES'">
        <div class="text-h6 q-mb-xs">{{ section.title }}</div>
        <div class="row q-gutter-md">
          <div v-for="(lang, i) in section.content.items" :key="i">
            {{ lang.name }}<span v-if="lang.proficiency" class="text-grey-7"> ({{ lang.proficiency }})</span>
          </div>
        </div>
      </template>

      <template v-else-if="section.type === 'LINKS'">
        <div class="text-h6 q-mb-xs">{{ section.title }}</div>
        <div class="row q-gutter-md">
          <a v-for="(link, i) in section.content.items" :key="i" :href="link.url" target="_blank" rel="noopener">
            {{ link.label || link.url }}
          </a>
        </div>
      </template>

      <template v-else-if="section.type === 'EXPERIENCE'">
        <div class="text-h6 q-mb-sm">{{ section.title }}</div>
        <div v-for="(item, i) in section.content.items" :key="i" class="q-mb-md">
          <div class="text-subtitle2 text-weight-medium">{{ item.title }} · {{ item.company }}</div>
          <div class="text-caption text-grey-7">
            {{ item.startDate }} - {{ item.current ? 'Hiện tại' : item.endDate }}
            <span v-if="item.location"> · {{ item.location }}</span>
          </div>
          <p class="section-text">{{ item.description }}</p>
        </div>
      </template>

      <template v-else-if="section.type === 'EDUCATION'">
        <div class="text-h6 q-mb-sm">{{ section.title }}</div>
        <div v-for="(item, i) in section.content.items" :key="i" class="q-mb-md">
          <div class="text-subtitle2 text-weight-medium">{{ item.degree }} · {{ item.school }}</div>
          <div class="text-caption text-grey-7">
            {{ item.fieldOfStudy }}<span v-if="item.startDate"> · {{ item.startDate }} - {{ item.endDate }}</span>
          </div>
          <p class="section-text">{{ item.description }}</p>
        </div>
      </template>

      <template v-else-if="section.type === 'PROJECTS'">
        <div class="text-h6 q-mb-sm">{{ section.title }}</div>
        <div v-for="(item, i) in section.content.items" :key="i" class="q-mb-md">
          <div class="text-subtitle2 text-weight-medium">
            <a v-if="item.url" :href="item.url" target="_blank" rel="noopener">{{ item.name }}</a>
            <span v-else>{{ item.name }}</span>
          </div>
          <div v-if="item.technologies?.length" class="text-caption text-grey-7">{{ item.technologies.join(', ') }}</div>
          <p class="section-text">{{ item.description }}</p>
        </div>
      </template>

      <template v-else-if="section.type === 'CERTIFICATIONS'">
        <div class="text-h6 q-mb-sm">{{ section.title }}</div>
        <div v-for="(item, i) in section.content.items" :key="i" class="q-mb-sm">
          <span class="text-weight-medium">{{ item.name }}</span>
          <span v-if="item.issuer" class="text-grey-7"> · {{ item.issuer }}</span>
          <span v-if="item.issueDate" class="text-caption text-grey-7"> · {{ item.issueDate }}</span>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.structured-resume {
  max-width: 100%;
}

.structured-section {
  margin-bottom: 24px;
}

.section-text {
  white-space: pre-wrap;
  margin: 4px 0 0;
}

@media print {
  .structured-section {
    break-inside: avoid;
  }
}
</style>

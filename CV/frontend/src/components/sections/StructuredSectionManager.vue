<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useQuasar } from 'quasar'
import { sectionsApi, type ResumeSectionResponse, type SectionContent, type SectionType, type SnapshotSection } from '../../api/sections'
import { SECTION_FIELD_CONFIG, SECTION_LABELS, emptyContentFor, type ListSectionConfig, type ObjectSectionConfig } from '../../config/sectionFields'
import { extractErrorMessage } from '../../api/errors'
import SectionObjectForm from './SectionObjectForm.vue'
import RepeatableItemList from './RepeatableItemList.vue'
import StructuredResumeView from './StructuredResumeView.vue'

const props = defineProps<{
  resumeId: string
}>()

const $q = useQuasar()
const sections = ref<ResumeSectionResponse[]>([])
const drafts = ref<Record<string, Record<string, unknown>>>({})
const loading = ref(false)
const savingId = ref<string | null>(null)

const showAddDialog = ref(false)
const newSectionType = ref<SectionType | null>(null)
const newSectionTitle = ref('')
const creating = ref(false)

const showPreviewDialog = ref(false)
const previewSections = ref<SnapshotSection[]>([])
const previewLoading = ref(false)

const allSectionTypes = Object.keys(SECTION_LABELS) as SectionType[]
const availableSectionTypes = computed(() =>
  allSectionTypes.filter((t) => !sections.value.some((s) => s.sectionType === t)),
)

async function load() {
  loading.value = true
  try {
    sections.value = await sectionsApi.list(props.resumeId)
    drafts.value = Object.fromEntries(sections.value.map((s) => [s.id, { ...s.content }]))
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    loading.value = false
  }
}

onMounted(load)

function isListSection(type: SectionType): boolean {
  return SECTION_FIELD_CONFIG[type].kind === 'list'
}

function objectFields(type: SectionType) {
  return (SECTION_FIELD_CONFIG[type] as ObjectSectionConfig).fields
}

function listConfig(type: SectionType): ListSectionConfig {
  return SECTION_FIELD_CONFIG[type] as ListSectionConfig
}

function listValueFor(section: ResumeSectionResponse): SectionContent[] {
  const draft = drafts.value[section.id]
  const key = listConfig(section.sectionType).listKey
  const value = draft?.[key]
  return Array.isArray(value) ? (value as SectionContent[]) : []
}

function setListValue(section: ResumeSectionResponse, items: SectionContent[]) {
  const key = listConfig(section.sectionType).listKey
  drafts.value[section.id] = { ...drafts.value[section.id], [key]: items }
}

function openAddDialog() {
  newSectionType.value = availableSectionTypes.value[0] ?? null
  newSectionTitle.value = newSectionType.value ? SECTION_LABELS[newSectionType.value] : ''
  showAddDialog.value = true
}

async function confirmAdd() {
  if (!newSectionType.value) return
  creating.value = true
  try {
    await sectionsApi.create(props.resumeId, newSectionType.value, newSectionTitle.value.trim(), emptyContentFor(newSectionType.value))
    showAddDialog.value = false
    await load()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    creating.value = false
  }
}

async function saveSection(section: ResumeSectionResponse) {
  savingId.value = section.id
  try {
    await sectionsApi.update(props.resumeId, section.id, { content: drafts.value[section.id] })
    $q.notify({ type: 'positive', message: `Đã lưu "${section.title}"` })
    await load()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
    // Draft is left untouched on failure - nothing is lost.
  } finally {
    savingId.value = null
  }
}

async function toggleVisible(section: ResumeSectionResponse, visible: boolean) {
  try {
    await sectionsApi.update(props.resumeId, section.id, { visible })
    await load()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

async function removeSection(section: ResumeSectionResponse) {
  $q.dialog({
    title: 'Xóa mục',
    message: `Xóa mục "${section.title}"?`,
    cancel: true,
  }).onOk(async () => {
    try {
      await sectionsApi.remove(props.resumeId, section.id)
      await load()
    } catch (error) {
      $q.notify({ type: 'negative', message: extractErrorMessage(error) })
    }
  })
}

async function moveSection(index: number, direction: -1 | 1) {
  const targetIndex = index + direction
  if (targetIndex < 0 || targetIndex >= sections.value.length) return
  const ids = sections.value.map((s) => s.id)
  const tmp = ids[index]
  ids[index] = ids[targetIndex]
  ids[targetIndex] = tmp
  try {
    await sectionsApi.reorder(props.resumeId, ids)
    await load()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

async function openPreview() {
  previewLoading.value = true
  showPreviewDialog.value = true
  try {
    previewSections.value = await sectionsApi.preview(props.resumeId)
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    previewLoading.value = false
  }
}
</script>

<template>
  <div>
    <div class="row items-center q-mb-md">
      <div class="text-subtitle1">Các mục trong CV</div>
      <q-space />
      <q-btn flat dense label="Xem trước" icon="visibility" data-testid="section-preview-button" @click="openPreview" />
      <q-btn
        color="primary"
        icon="add"
        label="Thêm mục"
        :disable="availableSectionTypes.length === 0"
        data-testid="add-section-button"
        @click="openAddDialog"
      />
    </div>

    <q-inner-loading :showing="loading" />

    <div v-if="!loading && sections.length === 0" class="text-grey-7">
      Chưa có mục nào. Nhấn "Thêm mục" để bắt đầu (vd: Thông tin cá nhân, Kỹ năng, Kinh nghiệm).
    </div>

    <q-list bordered separator data-testid="section-list">
      <q-expansion-item v-for="(section, index) in sections" :key="section.id" :label="section.title" :caption="SECTION_LABELS[section.sectionType]">
        <template #header>
          <q-item-section>
            <q-item-label>{{ section.title }}</q-item-label>
            <q-item-label caption>{{ SECTION_LABELS[section.sectionType] }}</q-item-label>
          </q-item-section>
          <q-item-section side>
            <div class="row items-center q-gutter-xs" @click.stop>
              <q-btn flat dense round icon="arrow_upward" :disable="index === 0" @click="moveSection(index, -1)" />
              <q-btn flat dense round icon="arrow_downward" :disable="index === sections.length - 1" @click="moveSection(index, 1)" />
              <q-toggle :model-value="section.visible" @update:model-value="(v) => toggleVisible(section, v)" />
              <q-btn flat dense round icon="delete" color="negative" @click="removeSection(section)" />
            </div>
          </q-item-section>
        </template>

        <q-card>
          <q-card-section>
            <SectionObjectForm
              v-if="!isListSection(section.sectionType)"
              v-model="drafts[section.id]"
              :fields="objectFields(section.sectionType)"
            />
            <RepeatableItemList
              v-else
              :model-value="listValueFor(section)"
              :item-fields="listConfig(section.sectionType).itemFields"
              :empty-item="listConfig(section.sectionType).emptyItem"
              @update:model-value="(items) => setListValue(section, items)"
            />
          </q-card-section>
          <q-card-actions align="right">
            <q-btn color="primary" label="Lưu" :loading="savingId === section.id" @click="saveSection(section)" />
          </q-card-actions>
        </q-card>
      </q-expansion-item>
    </q-list>

    <q-dialog v-model="showAddDialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Thêm mục mới</div>
        </q-card-section>
        <q-card-section class="q-gutter-md">
          <q-select
            v-model="newSectionType"
            :options="availableSectionTypes"
            :option-label="(t) => SECTION_LABELS[t as SectionType]"
            label="Loại mục"
            emit-value
            map-options
            @update:model-value="(t) => (newSectionTitle = SECTION_LABELS[t as SectionType])"
          />
          <q-input v-model="newSectionTitle" label="Tiêu đề hiển thị" />
        </q-card-section>
        <q-card-actions align="right">
          <q-btn flat label="Hủy" v-close-popup />
          <q-btn color="primary" label="Thêm" :loading="creating" @click="confirmAdd" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="showPreviewDialog" full-width full-height>
      <q-card>
        <q-card-section class="row items-center">
          <div class="text-h6">Xem trước CV công khai</div>
          <q-space />
          <q-btn flat round icon="close" v-close-popup />
        </q-card-section>
        <q-separator />
        <q-card-section style="max-width: 800px; margin: 0 auto">
          <q-inner-loading :showing="previewLoading" />
          <StructuredResumeView :sections="previewSections" />
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

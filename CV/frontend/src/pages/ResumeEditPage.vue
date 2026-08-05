<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import QRCode from 'qrcode'
import {
  resumesApi,
  type ResumeResponse,
  type ResumeVersionResponse,
  type ResumeVisibility,
  type AnalyticsSummaryResponse,
} from '../api/resumes'
import { extractErrorMessage } from '../api/errors'
import StructuredSectionManager from '../components/sections/StructuredSectionManager.vue'

const route = useRoute()
const router = useRouter()
const $q = useQuasar()

const resumeId = computed(() => route.params.id as string)
const resume = ref<ResumeResponse | null>(null)
const versions = ref<ResumeVersionResponse[]>([])
const analytics = ref<AnalyticsSummaryResponse | null>(null)
const loading = ref(false)

const nameDraft = ref('')
const savingName = ref(false)

const selectedFile = ref<File | null>(null)
const uploading = ref(false)

const visibilityDraft = ref<ResumeVisibility>('PRIVATE')
const savingVisibility = ref(false)
const publishing = ref(false)
const regenerating = ref(false)

const revealedShareLink = ref<string | null>(null)
const revealedShareQr = ref<string | null>(null)
const showShareDialog = ref(false)

async function load() {
  loading.value = true
  try {
    resume.value = await resumesApi.get(resumeId.value)
    nameDraft.value = resume.value.name
    visibilityDraft.value = resume.value.visibility
    if (resume.value.resumeType === 'PDF') {
      versions.value = await resumesApi.listVersions(resumeId.value)
    }
    analytics.value = await resumesApi.analyticsSummary(resumeId.value)
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
    await router.push('/dashboard/cvs')
  } finally {
    loading.value = false
  }
}

onMounted(load)

async function revealShareLink(rawLink: string) {
  revealedShareLink.value = rawLink
  revealedShareQr.value = await QRCode.toDataURL(rawLink, { width: 220 })
  showShareDialog.value = true
}

function publicUrlFor(r: ResumeResponse, rawToken: string) {
  // The backend only ever tells us the token, never a ready-made unlisted
  // URL - it has no way to know the frontend's own base URL. Same shape as
  // `publicUrl` for PUBLIC resumes: `${baseUrl}/cv/{publicId}/{slugOrToken}`.
  return `${window.location.origin}/cv/${r.publicId}/${rawToken}`
}

async function saveName() {
  if (!resume.value || !nameDraft.value.trim() || nameDraft.value === resume.value.name) return
  savingName.value = true
  try {
    resume.value = await resumesApi.update(resumeId.value, { name: nameDraft.value.trim() })
    $q.notify({ type: 'positive', message: 'Đã lưu tên CV' })
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    savingName.value = false
  }
}

async function onVisibilityChange(newVisibility: ResumeVisibility) {
  if (!resume.value || newVisibility === resume.value.visibility) return
  savingVisibility.value = true
  try {
    const updated = await resumesApi.update(resumeId.value, { visibility: newVisibility })
    resume.value = updated
    if (updated.unlistedShareToken) {
      await revealShareLink(publicUrlFor(updated, updated.unlistedShareToken))
    }
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
    if (resume.value) visibilityDraft.value = resume.value.visibility
  } finally {
    savingVisibility.value = false
  }
}

watch(visibilityDraft, (value) => onVisibilityChange(value))

async function onToggleAllowDownload(value: boolean) {
  if (!resume.value) return
  try {
    resume.value = await resumesApi.update(resumeId.value, { allowDownload: value })
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

async function onPublish() {
  publishing.value = true
  try {
    resume.value = await resumesApi.publish(resumeId.value)
    $q.notify({ type: 'positive', message: 'Đã xuất bản CV' })
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    publishing.value = false
  }
}

async function onUnpublish() {
  publishing.value = true
  try {
    resume.value = await resumesApi.unpublish(resumeId.value)
    $q.notify({ type: 'positive', message: 'Đã gỡ xuất bản' })
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    publishing.value = false
  }
}

async function onRegenerateLink() {
  regenerating.value = true
  try {
    const updated = await resumesApi.regenerateLink(resumeId.value)
    resume.value = updated
    if (updated.unlistedShareToken) {
      await revealShareLink(publicUrlFor(updated, updated.unlistedShareToken))
    }
    $q.notify({ type: 'positive', message: 'Link cũ đã bị vô hiệu hóa' })
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    regenerating.value = false
  }
}

async function copyLink(link: string) {
  await navigator.clipboard.writeText(link)
  $q.notify({ type: 'positive', message: 'Đã copy link' })
}

async function showPublicLinkQr() {
  if (!resume.value?.publicUrl) return
  await revealShareLink(resume.value.publicUrl)
}

function onFileSelected(file: File | null) {
  selectedFile.value = file
}

async function uploadVersion() {
  if (!selectedFile.value) return
  uploading.value = true
  try {
    await resumesApi.uploadPdfVersion(resumeId.value, selectedFile.value)
    selectedFile.value = null
    $q.notify({ type: 'positive', message: 'Đã upload phiên bản mới' })
    await load()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    uploading.value = false
  }
}

async function activateVersion(version: ResumeVersionResponse) {
  try {
    resume.value = await resumesApi.activateVersion(resumeId.value, version.id)
    await load()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

async function deleteVersion(version: ResumeVersionResponse) {
  $q.dialog({
    title: 'Xóa phiên bản',
    message: `Xóa phiên bản #${version.versionNumber}?`,
    cancel: true,
  }).onOk(async () => {
    try {
      await resumesApi.deleteVersion(resumeId.value, version.id)
      await load()
    } catch (error) {
      $q.notify({ type: 'negative', message: extractErrorMessage(error) })
    }
  })
}

async function previewActiveFile() {
  try {
    const blob = await resumesApi.previewFileBlob(resumeId.value)
    const url = URL.createObjectURL(blob)
    window.open(url, '_blank')
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

function formatSize(bytes: number | null) {
  if (bytes === null) return ''
  return `${(bytes / 1024).toFixed(0)} KB`
}

function formatDate(iso: string | null) {
  return iso ? new Date(iso).toLocaleString('vi-VN') : '-'
}
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary">
      <q-toolbar>
        <q-btn flat dense round icon="arrow_back" to="/dashboard/cvs" />
        <q-toolbar-title>Quản lý CV</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-lg" style="max-width: 720px; margin: 0 auto">
        <q-inner-loading :showing="loading" />

        <template v-if="resume">
          <q-card class="q-mb-md">
            <q-card-section>
              <div class="row q-gutter-sm items-end">
                <q-input v-model="nameDraft" label="Tên CV" class="col" data-testid="resume-name-input" @keyup.enter="saveName" />
                <q-btn color="primary" label="Lưu" :loading="savingName" data-testid="save-resume-name" @click="saveName" />
              </div>
              <div class="text-caption text-grey-7 q-mt-sm">
                Loại: {{ resume.resumeType === 'PDF' ? 'CV file PDF' : 'CV dạng web' }} ·
                Trạng thái: {{ resume.status }}
              </div>
            </q-card-section>
          </q-card>

          <q-card class="q-mb-md">
            <q-card-section>
              <div class="text-subtitle1 q-mb-sm">Chia sẻ & Xuất bản</div>

              <div class="row q-gutter-md items-center">
                <q-select
                  v-model="visibilityDraft"
                  :options="['PRIVATE', 'UNLISTED', 'PUBLIC']"
                  label="Chế độ hiển thị"
                  style="min-width: 200px"
                  :loading="savingVisibility"
                  data-testid="visibility-select"
                />
                <q-toggle
                  :model-value="resume.allowDownload"
                  label="Cho phép tải PDF"
                  data-testid="allow-download-toggle"
                  @update:model-value="onToggleAllowDownload"
                />
              </div>

              <div class="q-mt-md">
                <q-btn
                  v-if="resume.status !== 'PUBLISHED'"
                  color="primary"
                  label="Xuất bản"
                  :loading="publishing"
                  data-testid="publish-button"
                  @click="onPublish"
                />
                <q-btn
                  v-else
                  color="negative"
                  flat
                  label="Gỡ xuất bản"
                  :loading="publishing"
                  data-testid="unpublish-button"
                  @click="onUnpublish"
                />
              </div>

              <q-banner v-if="resume.status === 'PUBLISHED' && resume.visibility === 'PUBLIC' && resume.publicUrl" class="bg-grey-2 q-mt-md">
                <div class="text-caption text-grey-8">Public link:</div>
                <div class="row items-center q-gutter-sm">
                  <div class="text-body2 ellipsis" data-testid="public-link-text">{{ resume.publicUrl }}</div>
                  <q-btn flat dense round icon="content_copy" @click="copyLink(resume.publicUrl!)" />
                  <q-btn flat dense round icon="qr_code_2" data-testid="show-qr-button" @click="showPublicLinkQr" />
                </div>
              </q-banner>

              <q-banner v-else-if="resume.status === 'PUBLISHED' && resume.visibility === 'UNLISTED'" class="bg-grey-2 q-mt-md">
                Link không công khai đã được hiển thị khi bạn chuyển sang "UNLISTED" hoặc tạo lại link lần gần nhất.
                Nếu đã làm mất, hãy tạo lại (link cũ sẽ mất hiệu lực ngay).
                <div class="q-mt-sm">
                  <q-btn flat dense label="Tạo lại link" :loading="regenerating" data-testid="regenerate-link-button" @click="onRegenerateLink" />
                </div>
              </q-banner>

              <div v-if="resume.status !== 'PUBLISHED'" class="text-caption text-grey-7 q-mt-md">
                Xuất bản để có link chia sẻ. CV ở chế độ "PRIVATE" sẽ không hiển thị công khai dù đã xuất bản.
              </div>
            </q-card-section>

            <q-separator />

            <q-card-section v-if="analytics">
              <div class="text-subtitle2 q-mb-sm">Lượt xem</div>
              <div class="row q-gutter-lg">
                <div><div class="text-h6">{{ analytics.totalViews }}</div><div class="text-caption text-grey-7">Tổng</div></div>
                <div><div class="text-h6">{{ analytics.views7d }}</div><div class="text-caption text-grey-7">7 ngày</div></div>
                <div><div class="text-h6">{{ analytics.views30d }}</div><div class="text-caption text-grey-7">30 ngày</div></div>
                <div><div class="text-body2">{{ formatDate(analytics.lastViewedAt) }}</div><div class="text-caption text-grey-7">Lần cuối</div></div>
              </div>
            </q-card-section>
          </q-card>

          <q-card v-if="resume.resumeType === 'PDF'">
            <q-card-section>
              <div class="text-subtitle1 q-mb-sm">Upload phiên bản mới</div>
              <div class="row q-gutter-sm items-center">
                <q-file
                  v-model="selectedFile"
                  label="Chọn file PDF"
                  accept="application/pdf"
                  class="col"
                  data-testid="pdf-file-input"
                  @update:model-value="onFileSelected"
                />
                <q-btn
                  color="primary"
                  label="Upload"
                  :loading="uploading"
                  :disable="!selectedFile"
                  data-testid="upload-pdf-button"
                  @click="uploadVersion"
                />
              </div>
              <div class="text-caption text-grey-6 q-mt-xs">Chỉ nhận file .pdf, tối đa 10MB.</div>
            </q-card-section>

            <q-separator />

            <q-card-section>
              <div class="row items-center q-mb-sm">
                <div class="text-subtitle1">Các phiên bản</div>
                <q-space />
                <q-btn
                  v-if="resume.activeVersionId"
                  flat
                  dense
                  color="primary"
                  label="Xem trước"
                  data-testid="preview-active-file"
                  @click="previewActiveFile"
                />
              </div>

              <div v-if="versions.length === 0" class="text-grey-7">Chưa có phiên bản nào.</div>

              <q-list bordered separator data-testid="version-list">
                <q-item v-for="version in versions" :key="version.id">
                  <q-item-section>
                    <q-item-label>
                      Phiên bản #{{ version.versionNumber }}
                      <q-badge v-if="version.active" color="positive" class="q-ml-sm">Đang dùng</q-badge>
                    </q-item-label>
                    <q-item-label caption>
                      {{ version.originalFilename }} · {{ formatSize(version.sizeBytes) }} · {{ formatDate(version.createdAt) }}
                    </q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-btn
                      v-if="!version.active"
                      flat
                      dense
                      label="Đặt làm active"
                      @click="activateVersion(version)"
                    />
                    <q-btn
                      flat
                      dense
                      round
                      icon="delete"
                      color="negative"
                      :disable="version.active"
                      @click="deleteVersion(version)"
                    />
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card-section>
          </q-card>

          <q-card v-else>
            <q-card-section>
              <StructuredSectionManager :resume-id="resumeId" />
            </q-card-section>
          </q-card>
        </template>

        <q-dialog v-model="showShareDialog">
          <q-card style="min-width: 320px" class="text-center q-pa-md">
            <q-card-section>
              <div class="text-subtitle1">Link chia sẻ</div>
              <div class="text-caption text-grey-7 q-mb-sm" data-testid="share-link-text">{{ revealedShareLink }}</div>
              <img v-if="revealedShareQr" :src="revealedShareQr" alt="QR code" width="220" height="220" />
            </q-card-section>
            <q-card-actions align="center">
              <q-btn flat label="Copy link" @click="copyLink(revealedShareLink!)" />
              <q-btn flat label="Đóng" v-close-popup />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

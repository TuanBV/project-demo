<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { isAxiosError } from 'axios'
import QRCode from 'qrcode'
import { publicResumeApi, type PublicResumeResponse } from '../api/public'
import StructuredResumeView from '../components/sections/StructuredResumeView.vue'

const route = useRoute()
const $q = useQuasar()

const publicId = computed(() => route.params.publicId as string)
const slugOrToken = computed(() => route.params.slug as string)

const loading = ref(true)
const resume = ref<PublicResumeResponse | null>(null)
const notFound = ref(false)
const gone = ref(false)
const fileBlobUrl = ref<string | null>(null)
const qrDataUrl = ref<string | null>(null)

async function load() {
  loading.value = true
  notFound.value = false
  gone.value = false
  try {
    resume.value = await publicResumeApi.get(publicId.value, slugOrToken.value)
    document.title = `${resume.value.name} · CV Platform`

    if (resume.value.resumeType === 'PDF') {
      const blob = await publicResumeApi.fileBlob(publicId.value, slugOrToken.value)
      fileBlobUrl.value = URL.createObjectURL(blob)
    }

    qrDataUrl.value = await QRCode.toDataURL(resume.value.canonicalUrl, { width: 200 })

    // Fire-and-forget: never blocks rendering, never surfaces an error to the visitor.
    publicResumeApi.recordView(publicId.value, slugOrToken.value)
  } catch (error) {
    if (isAxiosError(error) && error.response?.status === 404) {
      notFound.value = true
    } else if (isAxiosError(error) && error.response?.status === 410) {
      gone.value = true
    } else {
      gone.value = true
    }
  } finally {
    loading.value = false
  }
}

onMounted(load)

onBeforeUnmount(() => {
  if (fileBlobUrl.value) URL.revokeObjectURL(fileBlobUrl.value)
})

async function copyLink() {
  if (!resume.value) return
  await navigator.clipboard.writeText(resume.value.canonicalUrl)
  $q.notify({ type: 'positive', message: 'Đã copy link' })
}

async function downloadFile() {
  if (!resume.value) return
  const blob = await publicResumeApi.fileBlob(publicId.value, slugOrToken.value, true)
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${resume.value.name}.pdf`
  link.click()
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="flex flex-center" style="min-height: 100vh">
    <q-inner-loading :showing="loading" />

    <div v-if="notFound" class="text-center q-pa-xl">
      <div class="text-h5 text-grey-7">Không tìm thấy CV này</div>
      <p class="text-grey-6">Đường link có thể không đúng.</p>
    </div>

    <div v-else-if="gone" class="text-center q-pa-xl" data-testid="link-gone-message">
      <div class="text-h5 text-grey-7">Link đã hết hiệu lực</div>
      <p class="text-grey-6">CV này hiện không còn được chia sẻ công khai.</p>
    </div>

    <div v-else-if="resume" class="q-pa-md" style="width: 100%; max-width: 900px">
      <div class="row items-center q-mb-md no-print">
        <div class="text-h5" data-testid="public-resume-name">{{ resume.name }}</div>
        <q-space />
        <q-btn flat dense icon="content_copy" label="Copy link" @click="copyLink" />
        <q-btn v-if="resume.allowDownload" flat dense icon="download" label="Tải PDF" data-testid="download-button" @click="downloadFile" />
        <img v-if="qrDataUrl" :src="qrDataUrl" alt="QR code" width="64" height="64" />
      </div>

      <q-card v-if="resume.resumeType === 'PDF'" flat bordered>
        <iframe
          v-if="fileBlobUrl"
          :src="fileBlobUrl"
          data-testid="pdf-viewer"
          style="width: 100%; height: 85vh; border: none"
          title="CV PDF"
        />
      </q-card>

      <q-card v-else flat bordered class="q-pa-lg" data-testid="structured-resume-view">
        <StructuredResumeView :sections="resume.sections" />
      </q-card>
    </div>
  </div>
</template>

<style scoped>
@media print {
  .no-print {
    display: none;
  }
}
</style>

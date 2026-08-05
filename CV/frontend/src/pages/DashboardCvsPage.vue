<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useAuthStore } from '../stores/auth'
import { resumesApi, type ResumeResponse, type ResumeType } from '../api/resumes'
import { extractErrorMessage } from '../api/errors'

const router = useRouter()
const authStore = useAuthStore()
const $q = useQuasar()

const resumes = ref<ResumeResponse[]>([])
const loading = ref(false)
const includeDeleted = ref(false)

const showCreateDialog = ref(false)
const newName = ref('')
const newType = ref<ResumeType>('PDF')
const creating = ref(false)

async function loadResumes() {
  loading.value = true
  try {
    resumes.value = await resumesApi.list(includeDeleted.value)
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    loading.value = false
  }
}

onMounted(loadResumes)

async function onLogout() {
  await authStore.logout()
  await router.push('/login')
}

function openCreateDialog() {
  newName.value = ''
  newType.value = 'PDF'
  showCreateDialog.value = true
}

async function onCreate() {
  if (!newName.value.trim()) return
  creating.value = true
  try {
    await resumesApi.create(newName.value.trim(), newType.value)
    showCreateDialog.value = false
    await loadResumes()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  } finally {
    creating.value = false
  }
}

function openResume(resume: ResumeResponse) {
  router.push(`/dashboard/cvs/${resume.id}/edit`)
}

async function onDuplicate(resume: ResumeResponse) {
  try {
    await resumesApi.duplicate(resume.id)
    $q.notify({ type: 'positive', message: 'Đã tạo bản sao' })
    await loadResumes()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

async function onSetDefault(resume: ResumeResponse) {
  try {
    await resumesApi.update(resume.id, { isDefault: true })
    await loadResumes()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

async function onDelete(resume: ResumeResponse) {
  $q.dialog({
    title: 'Xóa CV',
    message: `Xóa "${resume.name}"? Bạn có thể khôi phục trong 30 ngày.`,
    cancel: true,
  }).onOk(async () => {
    try {
      await resumesApi.remove(resume.id)
      await loadResumes()
    } catch (error) {
      $q.notify({ type: 'negative', message: extractErrorMessage(error) })
    }
  })
}

async function onRestore(resume: ResumeResponse) {
  try {
    await resumesApi.restore(resume.id)
    $q.notify({ type: 'positive', message: 'Đã khôi phục' })
    await loadResumes()
  } catch (error) {
    $q.notify({ type: 'negative', message: extractErrorMessage(error) })
  }
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('vi-VN')
}
</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary">
      <q-toolbar>
        <q-toolbar-title>CV Platform</q-toolbar-title>
        <div class="q-mr-sm">{{ authStore.user?.displayName }}</div>
        <q-btn flat dense label="Đăng xuất" data-testid="logout-button" @click="onLogout" />
      </q-toolbar>
    </q-header>

    <q-page-container>
      <q-page class="q-pa-lg">
        <div class="row items-center q-mb-md">
          <div class="text-h5">CV của bạn</div>
          <q-space />
          <q-toggle v-model="includeDeleted" label="Xem thùng rác" @update:model-value="loadResumes" />
          <q-btn color="primary" icon="add" label="Tạo CV mới" data-testid="create-resume-button" @click="openCreateDialog" />
        </div>

        <q-inner-loading :showing="loading" />

        <div v-if="!loading && resumes.length === 0" class="text-grey-7">
          Chưa có CV nào. Nhấn "Tạo CV mới" để bắt đầu.
        </div>

        <div class="row q-col-gutter-md">
          <div v-for="resume in resumes" :key="resume.id" class="col-12 col-sm-6 col-md-4">
            <q-card data-testid="resume-card" :class="{ 'bg-grey-2': resume.deletedAt }">
              <q-card-section>
                <div class="row items-center no-wrap">
                  <div class="text-subtitle1 text-weight-medium ellipsis">{{ resume.name }}</div>
                  <q-space />
                  <q-badge v-if="resume.isDefault" color="secondary">Mặc định</q-badge>
                </div>
                <div class="text-caption text-grey-7">
                  {{ resume.resumeType === 'PDF' ? 'CV file PDF' : 'CV dạng web' }} ·
                  {{ resume.status }} · {{ resume.visibility }}
                </div>
                <div class="text-caption text-grey-6">Cập nhật: {{ formatDate(resume.updatedAt) }}</div>
                <div class="text-caption text-grey-6">Lượt xem: {{ resume.viewCount }}</div>
              </q-card-section>

              <q-card-actions v-if="!resume.deletedAt" align="right">
                <q-btn flat dense label="Nhân bản" @click="onDuplicate(resume)" />
                <q-btn v-if="!resume.isDefault" flat dense label="Đặt mặc định" @click="onSetDefault(resume)" />
                <q-btn flat dense color="primary" label="Quản lý" @click="openResume(resume)" />
                <q-btn flat dense round icon="delete" color="negative" @click="onDelete(resume)" />
              </q-card-actions>
              <q-card-actions v-else align="right">
                <div class="text-caption text-grey-7 q-mr-auto self-center">Đã xóa</div>
                <q-btn flat dense label="Khôi phục" @click="onRestore(resume)" />
              </q-card-actions>
            </q-card>
          </div>
        </div>

        <q-dialog v-model="showCreateDialog">
          <q-card style="min-width: 350px">
            <q-card-section>
              <div class="text-h6">Tạo CV mới</div>
            </q-card-section>
            <q-card-section class="q-gutter-md">
              <q-input v-model="newName" label="Tên CV" data-testid="new-resume-name" autofocus />
              <q-select
                v-model="newType"
                :options="['PDF', 'STRUCTURED']"
                label="Loại CV"
                data-testid="new-resume-type"
              />
            </q-card-section>
            <q-card-actions align="right">
              <q-btn flat label="Hủy" v-close-popup />
              <q-btn
                color="primary"
                label="Tạo"
                :loading="creating"
                :disable="!newName.trim()"
                data-testid="confirm-create-resume"
                @click="onCreate"
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

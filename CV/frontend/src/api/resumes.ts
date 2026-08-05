import { apiClient } from './client'

export type ResumeType = 'PDF' | 'STRUCTURED'
export type ResumeVisibility = 'PRIVATE' | 'UNLISTED' | 'PUBLIC'

export interface ResumeResponse {
  id: string
  publicId: string
  name: string
  slug: string
  resumeType: ResumeType
  status: 'DRAFT' | 'PUBLISHED' | 'ARCHIVED'
  visibility: ResumeVisibility
  allowDownload: boolean
  searchEngineIndexable: boolean
  isDefault: boolean
  activeVersionId: string | null
  viewCount: number
  publishedAt: string | null
  /** Only meaningful when visibility is PUBLIC and status is PUBLISHED. */
  publicUrl: string | null
  /**
   * The raw unlisted share token - present ONLY in the response right after
   * switching visibility to UNLISTED or calling regenerateLink(). The
   * backend never stores or re-derives the raw value, so the caller must
   * capture and show it immediately.
   */
  unlistedShareToken: string | null
  createdAt: string
  updatedAt: string
  deletedAt: string | null
  restorableUntil: string | null
}

export interface ResumeVersionResponse {
  id: string
  versionNumber: number
  sourceType: 'PDF' | 'STRUCTURED_SNAPSHOT'
  active: boolean
  originalFilename: string | null
  sizeBytes: number | null
  contentType: string | null
  checksum: string | null
  createdAt: string
}

export interface AnalyticsSummaryResponse {
  totalViews: number
  views7d: number
  views30d: number
  lastViewedAt: string | null
}

export interface UpdateResumePayload {
  name?: string
  isDefault?: boolean
  visibility?: ResumeVisibility
  allowDownload?: boolean
  searchEngineIndexable?: boolean
}

export const resumesApi = {
  list: (includeDeleted = false) =>
    apiClient.get<ResumeResponse[]>('/api/v1/resumes', { params: { includeDeleted } }).then((r) => r.data),

  get: (resumeId: string) => apiClient.get<ResumeResponse>(`/api/v1/resumes/${resumeId}`).then((r) => r.data),

  create: (name: string, resumeType: ResumeType) =>
    apiClient.post<ResumeResponse>('/api/v1/resumes', { name, resumeType }).then((r) => r.data),

  update: (resumeId: string, payload: UpdateResumePayload) =>
    apiClient.patch<ResumeResponse>(`/api/v1/resumes/${resumeId}`, payload).then((r) => r.data),

  remove: (resumeId: string) => apiClient.delete<void>(`/api/v1/resumes/${resumeId}`),

  restore: (resumeId: string) => apiClient.post<ResumeResponse>(`/api/v1/resumes/${resumeId}/restore`).then((r) => r.data),

  duplicate: (resumeId: string) => apiClient.post<ResumeResponse>(`/api/v1/resumes/${resumeId}/duplicate`).then((r) => r.data),

  publish: (resumeId: string) => apiClient.post<ResumeResponse>(`/api/v1/resumes/${resumeId}/publish`).then((r) => r.data),

  unpublish: (resumeId: string) => apiClient.post<ResumeResponse>(`/api/v1/resumes/${resumeId}/unpublish`).then((r) => r.data),

  regenerateLink: (resumeId: string) =>
    apiClient.post<ResumeResponse>(`/api/v1/resumes/${resumeId}/regenerate-link`).then((r) => r.data),

  listVersions: (resumeId: string) =>
    apiClient.get<ResumeVersionResponse[]>(`/api/v1/resumes/${resumeId}/versions`).then((r) => r.data),

  uploadPdfVersion: (resumeId: string, file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient
      .post<ResumeVersionResponse>(`/api/v1/resumes/${resumeId}/versions/pdf`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then((r) => r.data)
  },

  activateVersion: (resumeId: string, versionId: string) =>
    apiClient.post<ResumeResponse>(`/api/v1/resumes/${resumeId}/versions/${versionId}/activate`).then((r) => r.data),

  deleteVersion: (resumeId: string, versionId: string) =>
    apiClient.delete<void>(`/api/v1/resumes/${resumeId}/versions/${versionId}`),

  previewFileUrl: (resumeId: string) => `/api/v1/resumes/${resumeId}/preview/file`,

  previewFileBlob: (resumeId: string) =>
    apiClient.get(`/api/v1/resumes/${resumeId}/preview/file`, { responseType: 'blob' }).then((r) => r.data as Blob),

  analyticsSummary: (resumeId: string) =>
    apiClient.get<AnalyticsSummaryResponse>(`/api/v1/resumes/${resumeId}/analytics/summary`).then((r) => r.data),
}

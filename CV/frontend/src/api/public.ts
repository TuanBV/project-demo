import { apiClient } from './client'
import type { SnapshotSection } from './sections'

export interface PublicResumeResponse {
  publicId: string
  name: string
  slug: string
  resumeType: 'PDF' | 'STRUCTURED'
  allowDownload: boolean
  searchEngineIndexable: boolean
  canonicalUrl: string
  /** Only populated for STRUCTURED resumes. */
  sections: SnapshotSection[]
}

export const publicResumeApi = {
  get: (publicId: string, slugOrToken: string) =>
    apiClient.get<PublicResumeResponse>(`/api/v1/public/resumes/${publicId}/${slugOrToken}`).then((r) => r.data),

  fileBlob: (publicId: string, slugOrToken: string, download = false) =>
    apiClient
      .get(`/api/v1/public/resumes/${publicId}/${slugOrToken}/file`, { params: { download }, responseType: 'blob' })
      .then((r) => r.data as Blob),

  fileUrl: (publicId: string, slugOrToken: string, download = false) => {
    const base = (apiClient.defaults.baseURL ?? '').replace(/\/$/, '')
    return `${base}/api/v1/public/resumes/${publicId}/${slugOrToken}/file${download ? '?download=true' : ''}`
  },

  recordView: (publicId: string, slugOrToken: string) =>
    apiClient.post<void>(`/api/v1/public/resumes/${publicId}/${slugOrToken}/view`).catch(() => {
      // Never let analytics failures break the public page for a visitor.
    }),
}

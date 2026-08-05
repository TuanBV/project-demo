import { apiClient } from './client'

export type SectionType =
  | 'PERSONAL_INFO'
  | 'SUMMARY'
  | 'SKILLS'
  | 'EXPERIENCE'
  | 'PROJECTS'
  | 'EDUCATION'
  | 'LANGUAGES'
  | 'CERTIFICATIONS'
  | 'LINKS'
  | 'ADDITIONAL'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type SectionContent = Record<string, any>

export interface ResumeSectionResponse {
  id: string
  sectionType: SectionType
  title: string
  position: number
  visible: boolean
  content: SectionContent
}

export interface SnapshotSection {
  type: SectionType
  title: string
  position: number
  content: SectionContent
}

export const sectionsApi = {
  list: (resumeId: string) =>
    apiClient.get<ResumeSectionResponse[]>(`/api/v1/resumes/${resumeId}/sections`).then((r) => r.data),

  create: (resumeId: string, sectionType: SectionType, title: string, content: SectionContent) =>
    apiClient
      .post<ResumeSectionResponse>(`/api/v1/resumes/${resumeId}/sections`, { sectionType, title, content })
      .then((r) => r.data),

  update: (resumeId: string, sectionId: string, payload: { title?: string; content?: SectionContent; visible?: boolean }) =>
    apiClient.patch<ResumeSectionResponse>(`/api/v1/resumes/${resumeId}/sections/${sectionId}`, payload).then((r) => r.data),

  remove: (resumeId: string, sectionId: string) =>
    apiClient.delete<void>(`/api/v1/resumes/${resumeId}/sections/${sectionId}`),

  reorder: (resumeId: string, sectionIds: string[]) =>
    apiClient
      .put<ResumeSectionResponse[]>(`/api/v1/resumes/${resumeId}/sections/order`, { sectionIds })
      .then((r) => r.data),

  preview: (resumeId: string) =>
    apiClient.get<SnapshotSection[]>(`/api/v1/resumes/${resumeId}/sections/preview`).then((r) => r.data),
}

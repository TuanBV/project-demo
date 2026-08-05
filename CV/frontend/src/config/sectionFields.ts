import type { SectionType } from '../api/sections'

export interface FieldDef {
  key: string
  label: string
  type?: 'text' | 'textarea' | 'checkbox' | 'select' | 'tags'
  options?: string[]
}

export interface ObjectSectionConfig {
  kind: 'object'
  fields: FieldDef[]
}

export interface ListSectionConfig {
  kind: 'list'
  listKey: string
  itemFields: FieldDef[]
  emptyItem: SectionContentRecord
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type SectionContentRecord = Record<string, any>

export type SectionFieldConfig = ObjectSectionConfig | ListSectionConfig

export const SECTION_LABELS: Record<SectionType, string> = {
  PERSONAL_INFO: 'Thông tin cá nhân',
  SUMMARY: 'Giới thiệu bản thân',
  SKILLS: 'Kỹ năng',
  EXPERIENCE: 'Kinh nghiệm làm việc',
  PROJECTS: 'Dự án',
  EDUCATION: 'Học vấn',
  LANGUAGES: 'Ngoại ngữ',
  CERTIFICATIONS: 'Chứng chỉ',
  LINKS: 'Liên kết',
  ADDITIONAL: 'Thông tin thêm',
}

const PROFICIENCY_OPTIONS = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT', 'NATIVE']

export const SECTION_FIELD_CONFIG: Record<SectionType, SectionFieldConfig> = {
  PERSONAL_INFO: {
    kind: 'object',
    fields: [
      { key: 'fullName', label: 'Họ và tên' },
      { key: 'headline', label: 'Chức danh' },
      { key: 'email', label: 'Email' },
      { key: 'hideEmail', label: 'Ẩn email trên trang công khai', type: 'checkbox' },
      { key: 'phone', label: 'Số điện thoại' },
      { key: 'hidePhone', label: 'Ẩn số điện thoại trên trang công khai', type: 'checkbox' },
      { key: 'location', label: 'Địa chỉ' },
      { key: 'hideLocation', label: 'Ẩn địa chỉ trên trang công khai', type: 'checkbox' },
      { key: 'website', label: 'Website' },
    ],
  },
  SUMMARY: {
    kind: 'object',
    fields: [{ key: 'text', label: 'Giới thiệu', type: 'textarea' }],
  },
  ADDITIONAL: {
    kind: 'object',
    fields: [{ key: 'text', label: 'Nội dung', type: 'textarea' }],
  },
  SKILLS: {
    kind: 'list',
    listKey: 'skills',
    itemFields: [
      { key: 'name', label: 'Kỹ năng' },
      { key: 'level', label: 'Mức độ', type: 'select', options: PROFICIENCY_OPTIONS },
    ],
    emptyItem: { name: '', level: '' },
  },
  EXPERIENCE: {
    kind: 'list',
    listKey: 'items',
    itemFields: [
      { key: 'company', label: 'Công ty' },
      { key: 'title', label: 'Vị trí' },
      { key: 'startDate', label: 'Bắt đầu (vd: 2022-01)' },
      { key: 'endDate', label: 'Kết thúc (để trống nếu đang làm)' },
      { key: 'current', label: 'Đang làm việc tại đây', type: 'checkbox' },
      { key: 'location', label: 'Địa điểm' },
      { key: 'description', label: 'Mô tả', type: 'textarea' },
    ],
    emptyItem: { company: '', title: '', startDate: '', endDate: '', current: false, location: '', description: '' },
  },
  PROJECTS: {
    kind: 'list',
    listKey: 'items',
    itemFields: [
      { key: 'name', label: 'Tên dự án' },
      { key: 'description', label: 'Mô tả', type: 'textarea' },
      { key: 'url', label: 'Đường dẫn' },
      { key: 'technologies', label: 'Công nghệ (phân tách bởi dấu phẩy)', type: 'tags' },
      { key: 'startDate', label: 'Bắt đầu' },
      { key: 'endDate', label: 'Kết thúc' },
    ],
    emptyItem: { name: '', description: '', url: '', technologies: [], startDate: '', endDate: '' },
  },
  EDUCATION: {
    kind: 'list',
    listKey: 'items',
    itemFields: [
      { key: 'school', label: 'Trường' },
      { key: 'degree', label: 'Bằng cấp' },
      { key: 'fieldOfStudy', label: 'Chuyên ngành' },
      { key: 'startDate', label: 'Bắt đầu' },
      { key: 'endDate', label: 'Kết thúc' },
      { key: 'description', label: 'Mô tả', type: 'textarea' },
    ],
    emptyItem: { school: '', degree: '', fieldOfStudy: '', startDate: '', endDate: '', description: '' },
  },
  LANGUAGES: {
    kind: 'list',
    listKey: 'items',
    itemFields: [
      { key: 'name', label: 'Ngôn ngữ' },
      { key: 'proficiency', label: 'Trình độ', type: 'select', options: PROFICIENCY_OPTIONS },
    ],
    emptyItem: { name: '', proficiency: '' },
  },
  CERTIFICATIONS: {
    kind: 'list',
    listKey: 'items',
    itemFields: [
      { key: 'name', label: 'Tên chứng chỉ' },
      { key: 'issuer', label: 'Đơn vị cấp' },
      { key: 'issueDate', label: 'Ngày cấp' },
      { key: 'credentialUrl', label: 'Đường dẫn xác thực' },
    ],
    emptyItem: { name: '', issuer: '', issueDate: '', credentialUrl: '' },
  },
  LINKS: {
    kind: 'list',
    listKey: 'items',
    itemFields: [
      { key: 'label', label: 'Tên hiển thị' },
      { key: 'url', label: 'Đường dẫn' },
    ],
    emptyItem: { label: '', url: '' },
  },
}

export function emptyContentFor(type: SectionType): SectionContentRecord {
  const config = SECTION_FIELD_CONFIG[type]
  if (config.kind === 'object') {
    const content: SectionContentRecord = {}
    config.fields.forEach((f) => {
      content[f.key] = f.type === 'checkbox' ? false : ''
    })
    return content
  }
  return { [config.listKey]: [] }
}

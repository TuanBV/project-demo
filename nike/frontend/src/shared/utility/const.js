const STATUS_CODE = {
  SUCCESS: 0,
  INVALID_REQUEST: 'ERRAPI401',
  ERROR: 'ERRAPI400',
  NOT_FOUND: 'ERRAPI404',
  SYSTEM_ERROR: 'ERRAPI999',
  NO_CONTENT: 'ERRAPI204',
  SEND_MAIL_FAILED: 'ERRAPI500',
  INVALID_PERMISSION: 'ERRAPI403',
  INVALID_TOKEN: 'ERRAPI998',
  APP_VERSION_ERROR: 'ERRAPI503',
}

// Pagination default
const PAGINATION_DEFAULT = {
  LIMIT: 20,
  OFFSET: 1,
  MAX_PAGE: 6,
}

// Pagination default
const SELECT_OPTION = {
  CANDIDATE: 'candidates',
  OFFICE: 'offices',
  ROOM: 'meeting_rooms',
  INTERVIEW: 'interview_details',
}

const FORMAT_DATE = 'YYYY/MM/DD'
const FORMAT_DATE_IN_SERVER = 'YYYY-MM-DD'

const PERPAGE_OPTIONS = [20, 50, 100]

// PDF max size
const MAX_SIZE_PDF = 10 * 1024 * 1024

// Max length of post
const MAX_POST = 2000

// Meeting room
const MEETING_ROOM = {
  BIG_ROOM: 1,
  SMALL_ROOM: 2,
}

// role of user
const POSITION_ID = {
  INTERN: 1,
  STAFF: 2,
  LEADER: 3,
  MANAGER: 4,
  COLLABORATORS: 5,
  ADMIN: 6,
}

// Type valid
const FILE_TYPE_VALID = ['pdf', 'doc', 'docx']

// Name column search
const COLUMN_SEARCH = [
  'fullname',
  'email',
  'time_interview',
  'telephone_no',
  'birthday',
  'start_join_date',
  'name',
  'title',
]

const EVALUATE = {
  NOT_INTERVIEW_YET: 0,
  PASS: 1,
  FAILED: 2,
  NOT_TEST: 8,
  NOT_INTERVIEW: 9,
}

const OFFICES = {
  HANOI: 1,
  HUE: 2,
}

const ROLE_EDIT_INTERVIEW = {
  USER: 1,
  ADMIN: 2,
}

const TYPE_KBN = {
  TEST: 0,
  FIRST_INTERVIEW: 1,
  SECOND_INTERVIEW: 2,
}

const EVALUATE_TYPE = {
  ELIMINATE: 0,
  SAVE: 1,
  ACCEPT: 2,
}

const POSITION_TYPE = {
  NOT_INTERNSHIP: 0,
  INTERNSHIP: 1,
}

const CONFIRM_TEST = {
  NO_TEST: 0,
  TEST: 1,
}

const TYPE_INTERVIEW = {
  OFFLINE: 1,
  ONLINE: 2,
}

const TYPE_CALENDAR = {
  CREATE: 0,
  UPDATE: 1,
}

const TYPE_ACTION = {
  VIEW: 0,
  CREATE: 1,
}

const StatusPost = Object.freeze({
  ADD: 0,
  SAVE: 1,
})

export {
  STATUS_CODE,
  PAGINATION_DEFAULT,
  SELECT_OPTION,
  FORMAT_DATE,
  FORMAT_DATE_IN_SERVER,
  PERPAGE_OPTIONS,
  MAX_SIZE_PDF,
  MAX_POST,
  TYPE_INTERVIEW,
  MEETING_ROOM,
  POSITION_ID,
  FILE_TYPE_VALID,
  COLUMN_SEARCH,
  EVALUATE,
  OFFICES,
  ROLE_EDIT_INTERVIEW,
  TYPE_KBN,
  EVALUATE_TYPE,
  POSITION_TYPE,
  CONFIRM_TEST,
  TYPE_CALENDAR,
  StatusPost,
  TYPE_ACTION,
}

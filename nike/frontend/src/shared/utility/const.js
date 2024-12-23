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
};

// Pagination default
const PAGINATION_DEFAULT = {
  LIMIT: 20,
  OFFSET: 1,
  MAX_PAGE: 6,
};

// Pagination default
const SELECT_OPTION = {
  CANDIDATE: 'candidates',
  OFFICE: 'offices',
  ROOM: 'meeting_rooms',
  INTERVIEW: 'interview_details',
};

const FORMAT_DATE = 'YYYY/MM/DD';
const FORMAT_DATE_IN_SERVER = 'YYYY-MM-DD';

const PERPAGE_OPTIONS = [20, 50, 100];

// Candidate status
const CANDIDATE_STATUS = [
  {
    id: 0,
    name: 'Nhận CV',
  },
  {
    id: 1,
    name: 'Loại CV',
  },
  {
    id: 2,
    name: 'Duyệt CV',
  },
  {
    id: 3,
    name: 'Mời Test',
  },
  {
    id: 4,
    name: 'Làm bài test',
  },
  {
    id: 5,
    name: 'Test OK',
  },
  {
    id: 6,
    name: 'Trượt bài test',
  },
  {
    id: 7,
    name: 'Mời PV vòng 1',
  },
  {
    id: 8,
    name: 'PV vòng 1',
  },
  {
    id: 9,
    name: 'Qua vòng 1',
  },
  {
    id: 10,
    name: 'Trượt vòng 1',
  },
  {
    id: 11,
    name: 'Mời PV vòng 2',
  },
  {
    id: 12,
    name: 'PV vòng 2',
  },
  {
    id: 13,
    name: 'Qua vòng 2',
  },
  {
    id: 14,
    name: 'Trượt vòng 2',
  },
  {
    id: 15,
    name: 'Đã gửi offer',
  },
  {
    id: 16,
    name: 'Đã nhận offer',
  },
  {
    id: 17,
    name: 'Từ chối offer',
  },
  {
    id: 18,
    name: 'Đã gửi form',
  },
  {
    id: 19,
    name: 'All OK',
  },
  {
    id: 20,
    name: 'Không đến PV',
  },
  {
    id: 21,
    name: 'Đã cập nhật form',
  },
  {
    id: 22,
    name: 'HD đến văn phòng',
  },
  {
    id: 23,
    name: 'DS đen',
  },
  {
    id: 24,
    name: 'Không đến test',
  },
  {
    id: 25,
    name: 'Nhận offer nhưng không đến làm',
  },
  {
    id: 26,
    name: 'Nghỉ việc',
  },
];
// List status fail
const LIST_CANDIDATE_STATUS_FAIL = ['Loại CV', 'Không đến PV', 'Từ chối offer', 'Trượt vòng 2', 'Trượt vòng 1', 'Trượt bài test', 'Nghỉ việc', 'Nhận offer nhưng không đi làm', 'Không đến test'];

// PDF max size
const MAX_SIZE_PDF = 10 * 1024 * 1024;

// Type interview
const TYPE_INTERVIEW_FORM = [
  {
    id: 1,
    name: 'PV Offline',
  },
  {
    id: 2,
    name: 'PV Online',
  },
];

// Invite status
const INVITE_STATUS = [
  {
    id: 3,
    name: 'Mời Test',
  },
  {
    id: 7,
    name: 'Mời PV vòng 1',
  },
  {
    id: 11,
    name: 'Mời PV vòng 2',
  },
];

// Meeting room
const MEETING_ROOM = {
  BIG_ROOM: 1,
  SMALL_ROOM: 2,
};

// Interview evaluate
const INTERVIEW_EVALUATE = [
  {
    id: 0,
    name: 'Chưa PV',
  },
  {
    id: 1,
    name: 'Pass',
  },
  {
    id: 2,
    name: 'Trượt',
  },
];

// role of user
const POSITION_ID = {
  INTERN: 1,
  STAFF: 2,
  LEADER: 3,
  MANAGER: 4,
  COLLABORATORS: 5,
  ADMIN: 6,
};

// Type valid
const FILE_TYPE_VALID = ['pdf', 'doc', 'docx'];

// Name column search
const COLUMN_SEARCH = ['fullname', 'email', 'time_interview', 'telephone_no', 'birthday', 'start_join_date', 'name', 'title'];

// Gender
const GENDER = [
  {
    id: 0,
    name: 'Nam',
  },
  {
    id: 1,
    name: 'Nữ',
  },
  {
    id: 2,
    name: 'Không xác định',
  },
];

const EVALUATE = {
  NOT_INTERVIEW_YET: 0,
  PASS: 1,
  FAILED: 2,
  NOT_TEST: 8,
  NOT_INTERVIEW: 9,
};

const OFFICES = {
  HANOI: 1,
  HUE: 2,
};

const ROLE_EDIT_INTERVIEW = {
  USER: 1,
  ADMIN: 2,
};

const TYPE_KBN = {
  TEST: 0,
  FIRST_INTERVIEW: 1,
  SECOND_INTERVIEW: 2,
};

const EVALUATE_TYPE = {
  ELIMINATE: 0,
  SAVE: 1,
  ACCEPT: 2,
};

const POSITION_TYPE = {
  NOT_INTERNSHIP: 0,
  INTERNSHIP: 1,
};

const CONFIRM_TEST = {
  NO_TEST: 0,
  TEST: 1,
};

const TYPE_INTERVIEW = {
  OFFLINE: 1,
  ONLINE: 2,
};

const TYPE_CALENDAR = {
  CREATE: 0,
  UPDATE: 1,
};

const TYPE_ACTION = {
  VIEW: 0,
  CREATE: 1,
};

const EnumCandidateStatus = Object.freeze({
  RECEIVE_CV: 0,
  FAILED_CV: 1,
  ACCEPT_CV: 2,
  INVITE_TEST: 3,
  TEST: 4,
  TEST_OK: 5,
  FAILED_TEST: 6,
  INVITE_FIRST_INTERVIEW: 7,
  FIRST_INTERVIEW: 8,
  FIRST_INTERVIEW_PASS: 9,
  FIRST_INTERVIEW_FAILED: 10,
  INVITE_SECOND_INTERVIEW: 11,
  SECOND_INTERVIEW: 12,
  SECOND_INTERVIEW_PASS: 13,
  SECOND_INTERVIEW_FAILED: 14,
  SEND_OFFER: 15,
  ACCEPT_OFFER: 16,
  REFUSE_OFFER: 17,
  SEND_FORM: 18,
  ALL_OK: 19,
  NOT_INTERVIEW: 20,
  UPDATED_FORM: 21,
  TUTORIAL: 22,
  BLACK_LIST: 23,
  NOT_TEST: 24,
  NOT_START_WORKING: 25,
  QUIT_JOB: 26,
});

const EnumTeam = Object.freeze({
  C_SHARP: 1,
  PHP: 2,
  JAVA: 3,
  DESIGNER: 4,
  NODEJS: 5,
  PYTHON: 6,
  FRONTEND: 7,
  CPLUS: 8,
  FLUTTER: 9,
  REACTJS: 10,
  COMTOR: 11,
  QAQC: 12,
  CTV: 13,
  TESTER: 14,
  ADMIN: 15,
});

export {
  STATUS_CODE,
  PAGINATION_DEFAULT,
  SELECT_OPTION,
  FORMAT_DATE,
  FORMAT_DATE_IN_SERVER,
  PERPAGE_OPTIONS,
  CANDIDATE_STATUS,
  MAX_SIZE_PDF,
  TYPE_INTERVIEW_FORM,
  TYPE_INTERVIEW,
  INVITE_STATUS,
  LIST_CANDIDATE_STATUS_FAIL,
  MEETING_ROOM,
  INTERVIEW_EVALUATE,
  POSITION_ID,
  FILE_TYPE_VALID,
  GENDER,
  COLUMN_SEARCH,
  EVALUATE,
  OFFICES,
  ROLE_EDIT_INTERVIEW,
  TYPE_KBN,
  EVALUATE_TYPE,
  POSITION_TYPE,
  EnumCandidateStatus,
  CONFIRM_TEST,
  TYPE_CALENDAR,
  EnumTeam,
  TYPE_ACTION,
};

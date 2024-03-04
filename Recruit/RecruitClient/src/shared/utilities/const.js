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
];
// List status fail
const LIST_CANDIDATE_STATUS_FAIL = ['Loại CV', 'Không đến PV', 'Từ chối offer', 'Trượt vòng 2', 'Trượt vòng 1', 'Trượt bài test'];

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
const COLUMN_SEARCH = ['fullname', 'email', 'full_address', 'telephone_no', 'title', 'note', 'name'];

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
};

const OFFICES = {
  HANOI: 1,
  HUE: 2,
};

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
};

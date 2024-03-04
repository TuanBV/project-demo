<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Đánh giá ứng viên</h1>

    <!-- Search Advance -->
    <div class="tw-mt-3 tw-border tw-border-gray-300 tw-p-5 tw-rounded-md">
      <div class="tw-flex tw-flex-wrap">
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="position">Chức danh:</label>
          <select
            id="position"
            class="tw-rounded-md focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-min-w-[100px]"
            v-model="dataSearch.advance.position"
            @change="searchHandle"
          >
            <option value="">Tất cả</option>
            <option v-for="(position, index) in listPosition" :value="position.name" :key="index">
              {{ position.name }}
            </option>
          </select>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="position">Giới tính:</label>
          <select
            id="gender"
            class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-min-w-[100px] sp:tw-min-w-[160px] tw-rounded-md"
            v-model="dataSearch.advance.gender"
            @change="searchHandle"
          >
            <option value="">Tất cả</option>
            <option v-for="(item, index) in GENDER" :value="item.name" :key="index">
              {{ item.name }}
            </option>
          </select>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="team">Vị trí:</label>
          <select
            id="team"
            class="tw-rounded-md focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-w-[130px]"
            v-model="dataSearch.advance.team"
            @change="searchHandle"
          >
            <option value="">Tất cả</option>
            <option v-for="(team, index) in listTeam" :value="team.name" :key="index">
              {{ team.name }}
            </option>
          </select>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block">PV từ ngày:</label>
          <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px] tw-rounded-md"
            :class=" interviewDayFromFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
            <input
              type="text"
              class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
              @focusin="interviewDayFromFocus = true"
              @focusout="interviewDayFromFocus = false"
              v-model="dataSearch.advance.date_interview_from"
              @input="searchHandle"
            >
            <q-icon name="event" class="cursor-pointer" size="xs">
              <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyFrom">
                <q-date name="wedding" v-model="dataSearch.advance.date_interview_from"
                  @update:model-value="searchHandle, qDateProxyFrom.hide()">
                </q-date>
              </q-popup-proxy>
            </q-icon>
          </div>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block">PV đến ngày:</label>
          <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px] tw-rounded-md"
            :class=" interviewDayToFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
            <input
              type="text"
              class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
              @focusin="interviewDayToFocus = true"
              @focusout="interviewDayToFocus = false"
              v-model="dataSearch.advance.date_interview_to"
              @input="searchHandle"
            >
            <q-icon name="event" class="cursor-pointer" size="xs">
              <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyTo">
                <q-date name="wedding" v-model="dataSearch.advance.date_interview_to"
                  @update:model-value="searchHandle, qDateProxyTo.hide()">
                </q-date>
              </q-popup-proxy>
            </q-icon>
          </div>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1">
          <label class="tw-block">Địa điểm PV:</label>
          <select
            id="office"
            class="tw-rounded-md tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-w-[100px] focus:tw-outline-none
              focus:tw-border-sky-500"
            v-model="dataSearch.advance.office"
            @change="searchHandle"
          >
            <option value="">Tất cả</option>
            <option v-for="(office, index) in listOffice" :value="office.name" :key="index">
              {{ office.name }}
            </option>
          </select>
        </div>
      </div>
      <!-- Btn Search -->
      <div class="tw-mt-3">
        <button
          type="button"
          class="bg-green-7 text-white tw-py-[4px] tw-px-2 tw-rounded"
          @click.prevent="resetSearch"
        >
          Đặt lại
        </button>
      </div>
    </div>

    <!-- List of candidate -->
    <q-table
      class="tw-mt-8 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      loading-label="Đang tìm kiếm dữ liệu ..."
      hide-pagination
      :loading="loading"
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên có thể đánh giá</span>
        <q-form
          class="tw-inline-block sp:tw-ml-0 tw-ml-10 tw-translate-y-px"
        >
          <q-input
            dense
            debounce="300"
            input-class="tw-py-0"
            v-model="dataSearch.search_key"
            placeholder="Tìm kiếm"
            @update:model-value="searchHandle"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>
        </q-form>
      </template>
      <!-- No data slot -->
      <template v-slot:no-data="{ message }">
        <div class="full-width row flex-center q-gutter-sm tw-text-sm tw-mt-1">
          {{ message }}
        </div>
      </template>
      <!-- Column serial -->
      <template v-slot:body-cell-serial="props">
        <q-td :props="props" class="tw-w-[70px]">
          {{ props.pageIndex + 1 }}
        </q-td>
      </template>
      <!-- Column type interview -->
      <template v-slot:body-cell-type_interview="props">
        <q-td :props="props" class="md:tw-w-[100px]">
          <div
            class="tw-text-[12px] tw-bg-sky-600
            tw-text-white tw-p-1 tw-text-center tw-rounded-sm tw-font-semibold"
          >
            {{ props.row.type_interview }}
          </div>
        </q-td>
      </template>
      <!-- Column status -->
      <template v-slot:body-cell-status="props">
        <q-td :props="props" class="tw-w-[100px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-for="(item, index) in CANDIDATE_STATUS" :key="index">
            <p v-if="props.row.status == item.id">
              {{ item.name }}
            </p>
          </div>
        </q-td>
      </template>
      <!-- Column Action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              v-if="checkInterviewer(props)"
              class="tw-text-[12px] sp:tw-text-[10px] tw-mr-2"
              color="green-7"
              @click.prevent="openModalAssessment(props)"
            >
              Đánh giá
            </q-btn>
            <q-btn
              v-else
              class="tw-text-[12px] sp:tw-text-[10px] tw-mr-2"
              color="green-7"
              @click.prevent="openModalAssessment(props)"
            >
              Xem đánh giá
            </q-btn>
          </div>
          <div class="sp:tw-w-[170px] md:tw-inline-block tw-mr-2" v-if="user.position_id === POSITION_ID.ADMIN">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="green-7"
              @click.prevent="confirmPass(props)"
            >
              Pass
            </q-btn>
          </div>
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-if="user.position_id === POSITION_ID.ADMIN">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="red-7"
              @click.prevent="confirmEliminate(props)"
            >
              Trượt
            </q-btn>
          </div>
        </q-td>
      </template>
      <!-- Choose perpage -->
      <template v-slot:top-right>
        <div class="sp:tw-w-screen sp:tw-mt-3">
          <span class="tw-mr-8">Tổng số bản ghi: {{ totalRecord }}</span>
          <label for="per_page" class="tw-mr-2">Số bản ghi mỗi page:</label>
          <select
            id="per_page"
            @change="changePerPage"
            v-model="pagination.rowsPerPage"
            class="tw-outline-none"
          >
            <option v-for="option in PERPAGE_OPTIONS" :key="option.id" :value="option">{{ option }}</option>
          </select>
        </div>
      </template>
    </q-table>

    <!-- Pagination -->
    <div
      class="q-pt-sm flex tw-justify-center"
    >
      <q-pagination
        v-if="pagination.totalPage > 1"
        v-model="pagination.page"
        :max="pagination.totalPage"
        :max-pages="PAGINATION_DEFAULT.MAX_PAGE"
        color="grey"
        active-color="primary"
        boundary-links
        direction-links
      />
    </div>

    <q-dialog v-model="modalAssessment">
      <q-card style="width: 700px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Đánh giá ứng viên {{ dataCandidate.fullname }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: max-content">
          <template v-if="dataCandidate.employee.length > 0">
            <template v-for="(assessment, index) in dataCandidate.employee" :key="index">
              <template v-if="user.employee_code !== assessment.employee_code">
                <p class="tw-font-bold">{{ index + 1 }}, {{ assessment.fullname }}</p>
                <div class="tw-mt-5 tw-flex">
                  <div class="tw-w-[200px] tw-text-right tw-mr-8">
                    <label for="name">Nội dung đánh giá:</label>
                  </div>
                  <textarea class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white tw-w-[65%]
                    tw-rounded-md focus:tw-outline-none focus:tw-border-sky-500" rows="5"
                    v-model="assessment.comment" disabled></textarea>
                </div>
                <div class="tw-mt-5 tw-flex">
                  <div class="tw-w-[200px] tw-text-right tw-mr-8">
                    <label for="name">Kết quả:</label>
                  </div>
                  <select
                    id="evaluate"
                    v-model="assessment.evaluate"
                    class="tw-rounded-md tw-border tw-border-gray-300
                    tw-py-1 tw-pl-1 tw-w-[100px] focus:tw-outline-none
                    focus:tw-border-sky-500" disabled
                  >
                    <option v-for="evaluate in INTERVIEW_EVALUATE" :key="evaluate.id" :value="evaluate.id">
                      {{ evaluate.name }}
                    </option>
                  </select>
                </div>
              </template>
              <template v-else>
                <p class="tw-font-bold">{{ index + 1 }}, {{ assessment.fullname }}</p>
                <div class="tw-mt-5 tw-flex">
                  <div class="tw-w-[200px] tw-text-right tw-mr-8">
                    <label for="name">Nội dung đánh giá:</label>
                  </div>
                  <textarea class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white tw-w-[65%]
                    tw-rounded-md focus:tw-outline-none focus:tw-border-sky-500" rows="5"
                    v-model="assessment.comment"></textarea>
                </div>
                <div class="tw-mt-5 tw-flex">
                  <div class="tw-w-[200px] tw-text-right tw-mr-8">
                    <label for="name">Kết quả:</label>
                  </div>
                  <select
                    id="evaluate"
                    v-model="assessment.evaluate"
                    class="tw-rounded-md tw-border tw-border-gray-300
                    tw-py-1 tw-pl-1 tw-w-[100px] focus:tw-outline-none
                    focus:tw-border-sky-500"
                  >
                    <option v-for="evaluate in INTERVIEW_EVALUATE" :key="evaluate.id" :value="evaluate.id">
                      {{ evaluate.name }}
                    </option>
                  </select>
                </div>
              </template>
            </template>
          </template>
        </q-card-section>

        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <template v-for="(assessment, index) in dataCandidate.employee" :key="index">
            <q-btn class="tw-w-[100px] tw-bg-[#ff9800] tw-text-white"
            @click.prevent="openModalConfirmAssessment()" label="Lưu" v-if="user.employee_code === assessment.employee_code"/>
          </template>
        </q-card-actions>

      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import candidateAssessmentService from 'services/candidate-assessment.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';
import meetingRoomService from 'services/meeting-room.service';
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems } from 'utilities/common';
import { MESSAGE } from 'utilities/message';
import { useAuthStore } from 'stores/auth-store';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, INTERVIEW_EVALUATE, POSITION_ID,
  GENDER, EVALUATE,
} from 'utilities/const';
import { cloneDeep } from 'lodash';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters

const { user } = useAuthStore();

// ==> 1.2) actions
// ==> 1.3) Others

const { confirmPopup, countRecord } = useMixin();

// 2) ======= VARIABLE REF ========

const interviewDayFromFocus = ref(false);
const interviewDayToFocus = ref(false);
const modalAssessment = ref(false);
const loading = ref(true);
const idEliminate = ref(null);
const flagEvaluate = ref({
  PASS: true,
  FAILED: false,
});

const dataSearch = reactive({
  search_key: '',
  advance: {
    date_interview_from: '',
    date_interview_to: '',
    team: '',
    position: '',
    office: '',
    gender: '',
  },
});

const dataCandidate = reactive({
  id: null,
  fullname: '',
  employee: [],
});

const columns = [
  {
    name: 'serial',
    align: 'left',
    label: 'STT',
    field: 'serial',
    sortable: true,
  },
  {
    name: 'fullname',
    align: 'left',
    label: 'Họ tên',
    field: 'fullname',
    sortable: true,
  },
  {
    name: 'gender',
    align: 'left',
    label: 'Giới tính',
    field: 'gender',
  },
  {
    name: 'team',
    align: 'left',
    label: 'Vị trí',
    field: 'team',
    sortable: true,
  },
  {
    name: 'position',
    align: 'left',
    label: 'Chức danh',
    field: 'position',
    sortable: true,
  },
  {
    name: 'email',
    align: 'left',
    label: 'Email',
    field: 'email',
    sortable: false,
  },
  {
    name: 'telephone_no',
    align: 'left',
    label: 'Số điện thoại',
    field: 'telephone_no',
    sortable: false,
  },
  {
    name: 'time_interview',
    align: 'left',
    label: 'Thời gian PV',
    field: 'time_interview',
    sortable: false,
  },
  {
    name: 'office',
    align: 'left',
    label: 'Địa điểm PV',
    field: 'office',
    sortable: true,
  },
  {
    name: 'meeting_room',
    align: 'left',
    label: 'Phòng họp',
    field: 'meeting_room',
    sortable: false,
  },
  {
    name: 'status',
    align: 'left',
    label: 'Trạng thái',
    field: 'status',
    sortable: true,
  },
  {
    name: 'action',
    align: 'center',
    label: 'Hành động',
    field: 'action',
    sortable: false,
  },
];

const listTeam = ref([]);

const listPosition = ref([]);

const listOffice = ref([]);

const listMeetingRoom = ref([]);

const rows = ref([]);

const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});

const totalRecord = ref(rows.value.length);
const records = ref([]);
const qDateProxyTo = ref();
const qDateProxyFrom = ref();

// 3) ======= METHOD/FUNCTION ========

// Open modal assessment
const openModalAssessment = (data) => {
  modalAssessment.value = true;
  dataCandidate.id = data.row.id;
  dataCandidate.fullname = data.row.fullname;
  dataCandidate.employee = data.row.employee;
};

// Update paginate
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

// Change page
const changePerPage = () => {
  updatePaginate(rows.value.length);
};

// Search data
const searchHandle = () => {
  rows.value = searchItems(dataSearch, records.value);
  totalRecord.value = rows.value.length;
  updatePaginate(totalRecord.value);
};

// Reset search data
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.position = '';
  dataSearch.advance.team = '';
  dataSearch.advance.date_interview_from = '';
  dataSearch.advance.date_interview_to = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

// Get list candidate
const getListCandidate = async (flagLoading = true) => {
  const data = await candidateAssessmentService.getList(flagLoading);
  if (data) {
    data.item.forEach((candidate) => {
      candidate.time_interview = `${candidate.date !== null ? candidate.date : ''} ${candidate.time !== null ? candidate.time : ''}`;
    });
    totalRecord.value = data.item.length;
    updatePaginate(totalRecord.value);
    records.value = cloneDeep(data.item);
    rows.value = cloneDeep(data.item);
    searchHandle();
  }
};

// Get list position
const getListPosition = async () => {
  const data = await positionService.getList();
  if (data) {
    listPosition.value = cloneDeep(data);
  }
};

// Get list team
const getListTeam = async () => {
  const data = await teamService.getList();
  if (data) {
    listTeam.value = cloneDeep(data);
  }
};

// Get list office
const getListOffice = async () => {
  const data = await officeService.getList();
  if (data) {
    listOffice.value = cloneDeep(data.list_office);
    listOffice.value.forEach((item) => {
      if (item.id === user.office_id) {
        dataSearch.advance.office = item.name;
      }
    });
  }
};

// Get list office
const getListMeetingRoom = async () => {
  const data = await meetingRoomService.getList();
  if (data) {
    listMeetingRoom.value = cloneDeep(data.item);
  }
};

// Reopen modal assessment
const reopenModalAsessment = () => {
  modalAssessment.value = true;
};

// Assessment candidate
const assessment = async () => {
  let dataAssessment = {};
  dataCandidate.employee.forEach((element) => {
    if (user.employee_code === element.employee_code) {
      dataAssessment = {
        comment: element.comment,
        evaluate: element.evaluate,
        id: element.id,
      };
    }
  });
  const data = await candidateAssessmentService.assessment(dataCandidate.id, dataAssessment);
  if (data) {
    let flagRemoveData = true;
    if (dataAssessment.evaluate !== EVALUATE.NOT_INTERVIEW_YET) {
      dataCandidate.employee.forEach((element) => {
        if ((element.comment === '' || element.comment === null) && element.evaluate === INTERVIEW_EVALUATE[0].id) {
          flagRemoveData = false;
        }
      });

      if (flagRemoveData) {
        // Remove candidate from list data
        rows.value = rows.value.filter((row) => row.id !== dataCandidate.id);
        records.value = records.value.filter((row) => row.id !== dataCandidate.id);
        // Update paginate and total record
        updatePaginate(rows.value.length);
        totalRecord.value = rows.value.length;
        // Update count record of menu
        countRecord();
      }
    }
  }
};

// Open modal confirm assessment
const openModalConfirmAssessment = () => {
  modalAssessment.value = false;

  confirmPopup(MESSAGE.ASSESSMENT.ADD.CONFIRM_TITLE, MESSAGE.ASSESSMENT.ADD.CONFIRM_QUESTION, assessment, reopenModalAsessment);
};

// Admin eavluate
const adminEvaluate = async (status) => {
  const data = await candidateAssessmentService.admin_evaluate(idEliminate.value, status);

  // Response code is SUCCESS
  if (data) {
    // Remove candidate from list data
    rows.value = rows.value.filter((row) => row.id !== idEliminate.value);
    records.value = records.value.filter((row) => row.id !== idEliminate.value);

    // Update paginate and total record
    updatePaginate(rows.value.length);
    totalRecord.value = rows.value.length;
    // Update count record of menu
    countRecord();
  }
};

// Eliminate candidate
const eliminateCandidate = async () => {
  adminEvaluate(flagEvaluate.value.FAILED);
};

// Open modal confirm eliminate candidate
const confirmEliminate = (data) => {
  idEliminate.value = data.row.id;

  confirmPopup(MESSAGE.CONTACT.DELETE.CONFIRM_TITLE, MESSAGE.CONTACT.DELETE.CONFIRM_QUESTION, eliminateCandidate);
};

// Eliminate candidate
const passCandidate = async () => {
  adminEvaluate(flagEvaluate.value.PASS);
};

// Open modal confirm eliminate candidate
const confirmPass = (data) => {
  idEliminate.value = data.row.id;

  confirmPopup(MESSAGE.ASSESSMENT.PASS.CONFIRM_TITLE, MESSAGE.ASSESSMENT.PASS.CONFIRM_QUESTION, passCandidate);
};

// Check interviewer
const checkInterviewer = (data) => {
  let isInterviewer = false;
  data.row.employee.forEach((empl) => {
    if (empl.employee_code === user.employee_code) {
      isInterviewer = true;
    }
  });

  return isInterviewer;
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  await Promise.all([
    getListOffice(),
    getListMeetingRoom(),
    getListPosition(),
    getListTeam(),
  ]);

  await getListCandidate(false);
  loading.value = false;
});

</script>

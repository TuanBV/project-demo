<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Quản lí lịch phỏng vấn</h1>
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
              id="date_interview_from"
              type="text"
              class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
              v-model="dataSearch.advance.date_interview_from"
              @focusin="interviewDayFromFocus = true"
              @focusout="interviewDayFromFocus = false"
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
              id="date_interview_to"
              type="text"
              class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
              v-model="dataSearch.advance.date_interview_to"
              @focusin="interviewDayToFocus = true"
              @focusout="interviewDayToFocus = false"
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

    <!-- List of interview schedule -->
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
        <span class="q-table__title tw-inline-block">Danh sách ứng viên cần tạo lịch phỏng vấn</span>
        <div
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
        </div>
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
      <!-- Column name -->
      <template v-slot:body-cell-fullname="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <p class="tw-text-sky-600 tw-cursor-pointer hover:tw-underline
            hover:tw-underline-offset-1"
            v-if="checkPdfFile(props)" @click.prevent="openModalCv(props)">
            {{ props.row.fullname }}
          </p>
            <p class="tw-text-sky-600 tw-cursor-pointer hover:tw-underline
              hover:tw-underline-offset-1" v-else
              @click.prevent="dowloadCv(props.row.cv_file_path)">
            {{ props.row.fullname }}
          </p>
        </q-td>
      </template>
      <!-- Column type interview -->
      <template v-slot:body-cell-interview_form="props">
        <q-td :props="props" class="tw-w-[100px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-for="(item, index) in TYPE_INTERVIEW_FORM" :key="index">
            <p v-if="props.row.interview_form == item.id" class="tw-border tw-bg-blue-500 tw-text-white tw-font-bold tw-p-1 tw-rounded-md">
              {{ item.name }}
            </p>
          </div>
        </q-td>
      </template>
      <!-- Column type interviewer -->
      <template v-slot:body-cell-employee="props">
        <q-td :props="props" class="tw-w-[100px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-for="(item, index) in props.row.employee" :key="index">
            <p>{{ item.fullname }}<template v-if="index + 1 < props.row.employee.length">,</template></p>
          </div>
        </q-td>
      </template>
      <!-- Column status -->
      <template v-slot:body-cell-status="props">
        <q-td :props="props" class="tw-w-[100px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <p>
              {{ props.row.status }}
            </p>
          </div>
        </q-td>
      </template>
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <div class="tw-w-[170px] md:tw-inline-block" v-if="props.row.meeting_room === null">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="green-7"
              @click.prevent="openModalInterview(props)"
            >
              <q-icon name="add_box" class="tw-mr-2"/>
              Thêm
            </q-btn>
          </div>
          <div class="tw-w-[200px]" v-else>
            <q-btn
              class="tw-text-[12px] tw-mr-2 tw-w-[120px]"
              color="green-7"
              @click.prevent="openModalUpdateInterview(props)"
            >
              <q-icon name="edit" class="tw-mr-2"/>
              Cập nhật
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

    <q-dialog v-model="cvModal">
      <q-card style="width: 900px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Xem CV của ứng viên {{ dataCv.candidate }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: 650px">
          <iframe title="cv" :src="dataCv.cv_file" height="100%" width="100%"></iframe>
        </q-card-section>
      </q-card>
    </q-dialog>

    <q-dialog v-model="interviewModal">
      <q-card style="width: 500px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Thêm lịch phỏng vấn</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: max-content">
          <div
            class="tw-rounded tw-p-3 tw-mt-4"
          >
            <div class="tw-flex">
              <div class="tw-flex-1 w-32">
                <div class="sp:tw-w-[45%]">
                  <label class="tw-block" for="name">Họ tên</label>
                  <input type="text" id="address"
                    class="tw-border
                      tw-border-gray-300 tw-rounded-md
                      tw-py-[3px] tw-pl-2 tw-w-[200px]"
                      disabled
                    v-model="dataInterview.fullname"
                  >
                </div>
                <div class="tw-mt-3 tw-w-[200px]">
                  <label class="tw-block" for="date_interview">Ngày phỏng vấn: <span class="text-red">*</span></label>
                  <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px]
                    tw-rounded-md" :class=" interviewDateFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
                    <input
                      type="text"
                      id="date_interview"
                      class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
                      v-model="dataInterview.date_interview"
                      placeholder="Nhập ngày phỏng vấn"
                      @focusin="interviewDateFocus = true"
                      @focusout="interviewDateFocus = false"
                    >
                    <q-icon name="event" class="cursor-pointer" size="xs">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyInterview">
                        <q-date name="wedding" v-model="dataInterview.date_interview" @update:model-value="qDateProxyInterview.hide()">
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </div>
                  <span v-if="(errors.date_interview)" class="text-red tw-text-xs">*{{ errors.date_interview }}</span>
                </div>
                <div div class="tw-mt-3 sp:tw-w-[45%]">
                  <label class="tw-block" for="position">Địa điểm phỏng vấn:</label>
                  <input type="text" id="address"
                    class="focus:tw-outline-none focus:tw-border-sky-500 tw-border
                      tw-border-gray-300 tw-rounded-md
                      tw-py-[3px] tw-pl-2 tw-w-[200px]" disabled
                    v-model="dataInterview.office"
                  >
                </div>
              </div>
              <div class="tw-flex-1 w-32">
                <div div class="sp:tw-w-[45%]">
                  <label class="tw-block" for="position">Vị trí:</label>
                  <input type="text" id="address"
                    class="focus:tw-outline-none focus:tw-border-sky-500 tw-border
                      tw-border-gray-300 tw-rounded-md
                      tw-py-[3px] tw-pl-2 tw-w-[200px]" disabled
                    v-model="dataInterview.position"
                  >
                </div>
                <div class="tw-mt-3 sp:tw-w-[45%]">
                  <label class="tw-block" for="address">Thời gian: <span class="text-red">*</span></label>
                  <div class="focus:tw-outline-none focus:tw-border-sky-500 tw-border
                      tw-border-gray-300 tw-rounded-md tw-pl-2 tw-w-[200px]"
                      :class=" interviewTimeFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
                    <input
                      type="text"
                      id="birthday"
                      class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
                      v-model="dataInterview.time_interview"
                      placeholder="Nhập thời gian phỏng vấn"
                      @focusin="interviewTimeFocus = true"
                      @focusout="interviewTimeFocus = false"
                      @change="convertTime"
                      maxlength="5"
                    >
                    <q-icon name="schedule" class="cursor-pointer" size="xs">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-time name="wedding" v-model="dataInterview.time_interview" format24h>
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                          </div>
                        </q-time>
                      </q-popup-proxy>
                    </q-icon>
                  </div>
                  <span v-if="(errors.time_interview)" class="text-red tw-text-xs">*{{ errors.time_interview }}</span>
                </div>
                <div class="tw-mt-3 sp:tw-w-[45%]">
                  <label class="tw-block" for="address">Phòng họp: <span class="text-red">*</span></label>
                  <select
                    class="focus:tw-outline-none focus:tw-border-sky-500 tw-border
                    tw-border-gray-300 tw-rounded-md tw-py-[3px] tw-pl-2 tw-w-[200px]"
                    v-model="dataInterview.meeting_room_id"
                  >
                    <option v-for="(room, index) in listMeetingRoom" :key="index" :value="room.id">
                      {{ room.name }}
                    </option>
                  </select>
                <span v-if="(errors.meeting_room)" class="text-red tw-text-xs">*{{ errors.meeting_room }}</span>
                </div>
              </div>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3 tw-mr-[20px]">
              <label class="tw-block" for="typeInterview">Loại phỏng vấn: <strong>{{ dataInterview.interview_form }}</strong></label>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3 tw-mr-[20px]">
              <label class="tw-block" for="note">Người phỏng vấn: <span class="text-red">*</span></label>
              <q-select
                filled
                class="tw-rounded-md focus:tw-outline-none focus:tw-border-sky-500
                  tw-py-1 tw-w-full"
                v-model="dataInterview.employee"
                :options="listLeader"
                option-label="fullname"
                stack-label
                multiple
              >
                <template v-slot:selected-item="scope">
                  <q-chip
                    removable
                    @remove="scope.removeAtIndex(scope.index)"
                    :tabindex="scope.tabindex"
                    dense
                    color="white"
                    text-color="primary"
                    class="q-my-none q-ml-xs q-mr-none"
                  >
                    {{ scope.opt.fullname }}
                  </q-chip>
                </template>
              </q-select>
              <span v-if="(errors.employee)" class="text-red tw-text-xs">*{{ errors.employee }}</span>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3 tw-mr-[20px] tw-flex" v-if="flagModalUpdate">
              <input type="checkbox" id="comeTest" v-model="dataInterview.flag_not_interview">
              <label for="typeInterview" class="tw-pl-2">Ứng viên không đến phỏng vấn</label>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn color="green-7" class="tw-w-[100px] tw-text-white" @click.prevent="openModalConfirmSchedule()" v-if="!flagModalUpdate" label="Thêm"/>
          <q-btn color="green-7" class="tw-w-[100px] tw-text-white" @click.prevent="openModalConfirmUpdateInterview()" v-if="flagModalUpdate" label="Cập nhật"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import interviewScheduleService from 'services/interview-schedule.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';
import meetingRoomService from 'services/meeting-room.service';
import usersService from 'services/user.service';
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems } from 'utilities/common';
import { useAuthStore } from 'stores/auth-store';
import { MESSAGE } from 'utilities/message';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, TYPE_INTERVIEW_FORM, CANDIDATE_STATUS,
  MEETING_ROOM, GENDER,
} from 'utilities/const';
import { cloneDeep } from 'lodash';
import useValidate from 'composables/validate';
import addInterviewSchema from '../../validations/schemas/candidate/interview.js';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others

const { confirmPopup, countRecord } = useMixin();
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF ========

const interviewDayFromFocus = ref(false);
const interviewDayToFocus = ref(false);
const interviewTimeFocus = ref(false);
const flagModalUpdate = ref(false);
const cvModal = ref(false);
const interviewModal = ref(false);
const interviewDateFocus = ref(false);
const loading = ref(true);
const dataCv = reactive({
  id: '',
  candidate: '',
  cv_file: '',
});
const valueNotTest = ref({
  notTest: true,
  test: false,
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

const dataInterview = reactive({
  id: null,
  fullname: '',
  team: null,
  date_interview: '',
  time_interview: '',
  office: null,
  meeting_room_id: MEETING_ROOM.BIG_ROOM,
  interview_form: null,
  employee: [],
  flag_not_interview: valueNotTest.value.test,
  room_name: '',
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
    name: 'time_interview',
    align: 'left',
    label: 'Thời gian PV',
    field: 'time_interview',
    sortable: true,
  },
  {
    name: 'office',
    align: 'left',
    label: 'Địa điểm PV',
    field: 'office',
    sortable: true,
  },
  {
    name: 'employee',
    align: 'left',
    label: 'Người PV',
    field: 'employee',
    sortable: false,
  },
  {
    name: 'meeting_room',
    align: 'left',
    label: 'Phòng họp',
    field: 'meeting_room',
    sortable: false,
  },
  {
    name: 'interview_form',
    align: 'left',
    label: 'Loại PV',
    field: 'interview_form',
    sortable: true,
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

const listLeader = ref([]);

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

const qDateProxyFrom = ref();
const qDateProxyTo = ref();
const qDateProxyInterview = ref();

// 3) ======= METHOD/FUNCTION ========

// Open modal show cv
const openModalCv = (data) => {
  cvModal.value = true;
  dataCv.candidate = data.row.fullname;
  dataCv.cv_file = `${data.row.cv_file_path}/`;
  dataCv.id = data.row.id;
};

// Open modal interview
const openModalInterview = (data) => {
  errors.value = {};
  flagModalUpdate.value = false;
  dataInterview.employee = [];
  interviewModal.value = true;
  dataInterview.id = data.row.id;
  dataInterview.fullname = data.row.fullname;
  dataInterview.position = data.row.position;
  dataInterview.date_interview = data.row.date;
  dataInterview.time_interview = data.row.time;
  dataInterview.office = data.row.office;
  dataInterview.meeting_room_id = data.row.meeting_room_id ? data.row.meeting_room_id : 1;
  dataInterview.flag_not_interview = false;
  dataInterview.room_name = data.row.meeting_room;
  TYPE_INTERVIEW_FORM.forEach((element) => {
    if (element.id === parseInt(data.row.interview_form, 10)) {
      dataInterview.interview_form = element.name;
    }
  });
};

// Reopen modal add schedule
const reopenAddScheduleModal = () => {
  interviewModal.value = true;
};

// Add schedule
const addSchedule = async () => {
  const interviewer = [];
  dataInterview.employee.forEach((empl) => {
    interviewer.push(empl.employee_code);
  });
  const dataSubmit = {
    employee: interviewer,
    date: dataInterview.date_interview,
    time: dataInterview.time_interview,
    meeting_room: dataInterview.meeting_room_id,
  };

  const dataResponse = await interviewScheduleService.add(dataInterview.id, dataSubmit);
  if (dataResponse) {
    rows.value.forEach((candidate) => {
      if (candidate.id === dataInterview.id) {
        candidate.employee = dataInterview.employee;
        candidate.meeting_room_id = dataInterview.meeting_room_id;
        listMeetingRoom.value.forEach((room) => {
          if (dataInterview.meeting_room_id === room.id) {
            candidate.meeting_room = room.name;
          }
        });
      }
    });

    // Update count record of menu
    countRecord();
  }
};

// Open modal confirm schedule
const openModalConfirmSchedule = () => {
  const dataSubmit = {
    employee: dataInterview.employee,
    date_interview: dataInterview.date_interview,
    time_interview: dataInterview.time_interview,
    meeting_room: dataInterview.meeting_room_id,
  };

  const isValid = validate(addInterviewSchema, dataSubmit);

  if (!isValid) {
    return;
  }

  interviewModal.value = false;

  confirmPopup(MESSAGE.INTERVIEW_SCHEDULE.ADD.CONFIRM_TITLE, MESSAGE.INTERVIEW_SCHEDULE.ADD.CONFIRM_QUESTION, addSchedule, reopenAddScheduleModal);
};

// Open modal update
const openModalUpdateInterview = (data) => {
  flagModalUpdate.value = true;
  dataInterview.employee = [];
  interviewModal.value = true;
  dataInterview.id = data.row.id;
  dataInterview.fullname = data.row.fullname;
  dataInterview.position = data.row.position;
  dataInterview.date_interview = data.row.date;
  dataInterview.time_interview = data.row.time;
  dataInterview.office = data.row.office;
  dataInterview.meeting_room_id = data.row.meeting_room_id ? data.row.meeting_room_id : 1;
  dataInterview.flag_not_interview = false;
  dataInterview.employee = data.row.employee;
  dataInterview.room_name = data.row.meeting_room;
  TYPE_INTERVIEW_FORM.forEach((element) => {
    if (element.id === parseInt(data.row.interview_form, 10)) {
      dataInterview.interview_form = element.name;
    }
  });
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
  dataSearch.advance.date_interview_from = '';
  dataSearch.advance.date_interview_to = '';
  dataSearch.advance.team = '';
  dataSearch.advance.position = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

// Edit schedule
const editSchedule = async () => {
  const interviewer = [];
  dataInterview.employee.forEach((empl) => {
    interviewer.push(empl.employee_code);
  });
  const dataSubmit = {
    employee: interviewer,
    date: dataInterview.date_interview,
    time: dataInterview.time_interview,
    meeting_room: dataInterview.meeting_room_id,
    flag_not_interview: dataInterview.flag_not_interview,
  };

  const dataResponse = await interviewScheduleService.edit(dataInterview.id, dataSubmit);

  if (dataResponse) {
    if (!dataInterview.flag_not_interview) {
      rows.value.forEach((candidate) => {
        if (candidate.id === dataInterview.id) {
          candidate.employee = dataInterview.employee;
          candidate.meeting_room_id = dataInterview.meeting_room_id;
          listMeetingRoom.value.forEach((room) => {
            if (dataInterview.meeting_room_id === room.id) {
              candidate.meeting_room = room.name;
            }
          });
        }
      });
    } else {
      // Remove candidate from list data
      rows.value = rows.value.filter((row) => row.id !== dataInterview.id);
      records.value = records.value.filter((row) => row.id !== dataInterview.id);

      // Update paginate and total record
      updatePaginate(rows.value.length);
      totalRecord.value = rows.value.length;
    }

    // Update count record of menu
    countRecord();
  }
};

// Open modal confirm update
const openModalConfirmUpdateInterview = () => {
  const dataSubmit = {
    employee: dataInterview.employee,
    date_interview: dataInterview.date_interview,
    time_interview: dataInterview.time_interview,
    meeting_room: dataInterview.meeting_room_id,
  };

  const isValid = validate(addInterviewSchema, dataSubmit);

  if (!isValid) {
    return;
  }

  interviewModal.value = false;

  confirmPopup(MESSAGE.INTERVIEW_SCHEDULE.ADD.CONFIRM_TITLE, MESSAGE.INTERVIEW_SCHEDULE.ADD.CONFIRM_QUESTION, editSchedule, reopenAddScheduleModal);
};

// Get list candidate
const getListCandidate = async (flagLoading = true) => {
  const data = await interviewScheduleService.getList(flagLoading);
  if (data) {
    data.item.forEach((candidate) => {
      candidate.time_interview = `${candidate.date !== null ? candidate.date : ''} ${candidate.time !== null ? candidate.time : ''}`;
      listMeetingRoom.value.forEach((room) => {
        if (candidate.meeting_room === room.id) {
          candidate.meeting_room = room.name;
        }
      });

      CANDIDATE_STATUS.forEach((itemStatus) => {
        if (itemStatus.id === candidate.status) {
          candidate.status = itemStatus.name;
        }
      });
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

// Get list leader
const getListInterviewer = async () => {
  const data = await usersService.getListInterviewer();
  if (data) {
    listLeader.value = cloneDeep(data.item);
  }
};

// Get list office
const getListMeetingRoom = async () => {
  const data = await meetingRoomService.getList();
  if (data) {
    listMeetingRoom.value = cloneDeep(data.item);
  }
};

// Check pdf file
const checkPdfFile = (data) => {
  const arrFileType = data.row.cv_file_path.split('.');
  const fileType = arrFileType[arrFileType.length - 1];
  return fileType === 'pdf';
};

// Dowload cv
const dowloadCv = (url) => {
  const iframeTag = document.createElement('a');
  iframeTag.href = url;
  iframeTag.click();
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  await Promise.all([
    getListPosition(),
    getListTeam(),
    getListOffice(),
    getListMeetingRoom(),
    getListInterviewer(),
  ]);

  await getListCandidate(false);

  loading.value = false;
});

</script>

<template>
  <div class="q-pa-md">
    <h1 class="tw-text-xl">Liên hệ ứng viên</h1>

    <!-- Search Advance -->
    <div class="tw-mt-3 tw-border tw-border-gray-300 tw-p-5 tw-rounded-md">
      <div class="tw-flex tw-flex-wrap">
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
        <label class="tw-block" for="position">Chức danh:</label>
        <select
          id="position"
          class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
            tw-py-1 tw-pl-1 tw-min-w-[100px] tw-rounded-md"
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
            class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-w-[130px] tw-rounded-md"
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
          <label class="tw-block" for="status">Trạng thái:</label>
          <select
            id="status"
            class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 sp:tw-min-w-[160px] tw-rounded-md"
            v-model="dataSearch.advance.status"
            @change="searchHandle"
          >
            <option value="">Tất cả</option>
            <option v-for="(status, index) in CANDIDATE_STATUS" :value="status.id" :key="index">
              {{ status.name }}
            </option>
          </select>
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

    <!-- List of candidates -->
    <q-table
      class="tw-mt-8 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      hide-pagination
      loading-label="Đang tìm kiếm dữ liệu ..."
      :loading="loading"
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
    >
    <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên cần liên hệ</span>
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
      <!-- No data -->
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
      <!-- Column fullname -->
      <template v-slot:body-cell-fullname="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <p class="tw-text-sky-600 tw-cursor-pointer hover:tw-underline
              hover:tw-underline-offset-1" v-if="checkPdfFile(props)"
              @click.prevent="openModalCv(props)">
            {{ props.row.fullname }}
          </p>
          <p class="tw-text-sky-600 tw-cursor-pointer hover:tw-underline
              hover:tw-underline-offset-1" v-else
              @click.prevent="dowloadCv(props.row.cv_file_path)">
            {{ props.row.fullname }}
          </p>
        </q-td>
      </template>
      <!-- Column status -->
      <template v-slot:body-cell-status="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <p>
              {{ props.row.status }}
            </p>
          </div>
        </q-td>
      </template>
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="tw-max-w-[350px]">
          <div class="tw-w-[200px] md:tw-inline-block">
            <q-btn
              class="sp:tw-text-[10px]"
              color="green-7"
              size="11px"
              @click.prevent="contact(props)"
            >
              <q-icon name="call" class="tw-mr-2"/>
              Liên hệ
            </q-btn>
            <q-btn
              class="tw-mx-2 sp:tw-text-[10px]"
              color="red-7"
              size="11px"
              @click.prevent="confirmEliminate(props)"
            >
              Loại
            </q-btn>
            <q-btn
              v-if="props.row.status === CANDIDATE_STATUS[9].id"
              class="sp:tw-text-[10px]"
              color="blue-7"
              size="11px"
              @click.prevent="confirmPassInterview(props)"
            >
              Qua vòng 2
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

    <q-dialog v-model="contactModal">
      <q-card style="width: 500px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Lưu thông tin liên hệ ứng viên {{ nameCandidate }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: max-content">
          <div
            class="tw-rounded tw-p-3 tw-mt-4"
          >
            <div class="tw-flex">
              <div class="tw-flex-1 w-32">
                <div class="tw-w-[200px]">
                  <label class="tw-block" for="birthday">Ngày phỏng vấn: <span class="text-red">*</span></label>
                  <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px]
                    tw-rounded-md" :class=" interviewDateFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
                    <input
                      type="text"
                      id="birthday"
                      class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
                      v-model="dataCandidate.date"
                      placeholder="Nhập ngày phỏng vấn"
                      @focusin="interviewDateFocus = true"
                      @focusout="interviewDateFocus = false"
                    >
                    <q-icon name="event" class="cursor-pointer" size="xs">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxy">
                        <q-date name="wedding" v-model="dataCandidate.date" @update:model-value="qDateProxy.hide()">
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </div>
                  <span v-if="(errors.date)" class="text-red tw-text-xs">*{{ errors.date }}</span>
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
                      v-model="dataCandidate.time"
                      placeholder="Nhập thời gian phỏng vấn"
                      @focusin="interviewTimeFocus = true"
                      @focusout="interviewTimeFocus = false"
                      @change="convertTime"
                      maxlength="5"
                    >
                    <q-icon name="schedule" class="cursor-pointer" size="xs">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                        <q-time name="wedding" v-model="dataCandidate.time" format24h>
                          <div class="row items-center justify-end">
                            <q-btn v-close-popup label="Close" color="primary" flat />
                          </div>
                        </q-time>
                      </q-popup-proxy>
                    </q-icon>
                  </div>
                </div>
                <span v-if="(errors.time)" class="text-red tw-text-xs">*{{ errors.time }}</span>
              </div>
              <div class="tw-flex-1 w-32">
                <div div class="sp:tw-w-[45%]">
                  <label class="tw-block" for="position">Địa điểm phỏng vấn:</label>
                  <select
                    id="position"
                    class="tw-rounded-md tw-border tw-border-gray-300
                      tw-py-1 tw-pl-1 tw-w-[200px] focus:tw-outline-none
                      focus:tw-border-sky-500"
                      v-model="dataCandidate.office_id"
                  >
                    <option value="1">Hà Nội</option>
                    <option value="2">Huế</option>
                  </select>
                </div>
              </div>
              <span v-if="(errors.office_id)" class="text-red tw-text-xs">*{{ errors.office_id }}</span>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3 tw-mr-[20px]">
              <label class="tw-block" for="typeInterview">Loại phỏng vấn:</label>

              <div class="tw-inline-block tw-mx-4 tw-mt-2">
                <input checked type="radio" id="interviewOff" class="tw-mr-2" name="type_interview" value="1"
                v-model="dataCandidate.interview_form">
                <label for="interviewOff">Phỏng vấn offline</label><br>
              </div>
              <div class="tw-inline-block tw-mt-2">
                <input type="radio" id="interviewOnl" class="tw-mx-2" name="type_interview" value="2"
                v-model="dataCandidate.interview_form" @change="clearLinkInterview">
                <label for="interviewOnl">Phỏng vấn online</label><br>
              </div>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3 tw-mr-[20px]" v-if="dataCandidate.interview_form == typeInterview.online">
              <label class="tw-block" for="note">Link PV: <span class="text-red">*</span></label>
              <input class="tw-outline-0 tw-py-1 tw-pl-2 tw-w-full
                tw-border tw-rounded-md tw-border-gray-300 focus:tw-outline-none
                focus:tw-border-sky-500"
                v-model="dataCandidate.link_interview" />
              <span v-if="(errors.link_interview)" class="text-red tw-text-xs">*{{ errors.link_interview }}</span>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3 tw-mr-[20px]">
              <label class="tw-block" for="note">Ghi chú:</label>
              <textarea class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white tw-w-[100%]
                tw-rounded-md focus:tw-outline-none focus:tw-border-sky-500"
                v-model="dataCandidate.note"></textarea>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" @click.prevent="confirmContactCandidate()" label="Lưu"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="cvModal">
      <q-card style="width: 900px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Xem CV của ứng viên {{ dataCv.candidate }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: 650px">
          <iframe title="cv" :src="dataCv.cv_file"
            height="100%" width="100%"></iframe>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import contactCandidateService from 'services/contact-candidate.service';
import candidateService from 'services/candidate.service';
import recommenderService from 'services/recommender.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';
import { useAuthStore } from 'stores/auth-store';
import {
  reactive, ref, onMounted,
} from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems, convertToTime } from 'utilities/common';
import { MESSAGE } from 'utilities/message';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, GENDER,
} from 'utilities/const';
import { cloneDeep } from 'lodash';
import useValidate from 'composables/validate';
import addContactSchema from '../../validations/schemas/candidate/contact-candidate.js';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others

const { confirmPopup, countRecord } = useMixin();
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF ========

const contactModal = ref(false);
const nameCandidate = ref('');
const interviewDateFocus = ref(false);
const interviewTimeFocus = ref(false);
const idEliminate = ref(null);
const cvModal = ref(false);
const typeInterview = ref({
  offline: '1',
  online: '2',
});
const dataCv = reactive({
  id: '',
  candidate: '',
  cv_file: '',
});
const records = ref([]);
const loading = ref(true);

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
    sortable: true,
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
    sortable: true,
  },
  {
    name: 'telephone_no',
    align: 'left',
    label: 'Số điện thoại',
    field: 'telephone_no',
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
    name: 'status',
    align: 'left',
    label: 'Trạng thái',
    field: 'status',
    sortable: true,
  },
  {
    name: 'note',
    align: 'left',
    label: 'Ghi chú',
    field: 'note',
    sortable: true,
  },
  {
    name: 'action',
    align: 'left',
    label: 'Hành động',
    field: 'action',
    sortable: true,
  },
];

const listPosition = ref([]);

const listTeam = ref([]);

const listRecommender = ref([]);

const listOffice = ref([]);

const listIdCandidate = ref([]);

const rows = ref([]);

const dataCandidate = reactive({
  candidate_id: null,
  office_id: null,
  date: '',
  time: '',
  interview_form: typeInterview.value.offline,
  note: '',
  link_interview: '',
});

const dataSearch = reactive({
  search_key: '',
  advance: {
    position: '',
    team: '',
    status: '',
    office: '',
    gender: '',
  },
});

const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});

const totalRecord = ref(0);

const qDateProxy = ref();

// 3) ======= METHOD/FUNCTION ========

// Clear link interview
const clearLinkInterview = () => {
  dataCandidate.link_interview = '';
  if ('link_interview' in errors.value) {
    delete errors.value.link_interview;
  }
};

// Open modal show cv
const openModalCv = (data) => {
  cvModal.value = true;
  dataCv.candidate = data.row.name;
  dataCv.cv_file = `${data.row.cv_file_path}/`;
  dataCv.id = data.row.id;
};

// Open modal contact to candidate
const contact = (data) => {
  errors.value = {};
  listOffice.value.forEach((office) => {
    if (office.name === data.row.office) {
      dataCandidate.office_id = office.id;
    }
  });
  dataCandidate.date = '';
  dataCandidate.time = '';
  dataCandidate.interview_form = typeInterview.value.offline;
  dataCandidate.note = data.row.note;

  contactModal.value = true;
  nameCandidate.value = data.row.fullname;
  dataCandidate.candidate_id = data.row.id;
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

// Get list candidate
const getListCandidate = async (flagLoading = true) => {
  const data = await contactCandidateService.getList(flagLoading);
  if (data) {
    data.item.forEach((itemCand) => {
      CANDIDATE_STATUS.forEach((itemStatus) => {
        if (itemStatus.id === itemCand.status) {
          itemCand.status = itemStatus.name;
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

// Get list recommender
const getListRecommender = async () => {
  const data = await recommenderService.getList();
  if (data) {
    listRecommender.value = cloneDeep(data.item);
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

// Reset data search
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.advance.position = '';
  dataSearch.advance.team = '';
  dataSearch.advance.status = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

// Contact candidate
const contactCandidate = async () => {
  const data = await contactCandidateService.add(dataCandidate);

  if (data) {
    // Remove candidate from list data
    rows.value = rows.value.filter((row) => row.id !== parseInt(dataCandidate.candidate_id, 10));
    records.value = records.value.filter((row) => row.id !== parseInt(dataCandidate.candidate_id, 10));

    // Update paginate and total record
    updatePaginate(rows.value.length);
    totalRecord.value = rows.value.length;

    // Update count record of menu
    countRecord();
  }
};

// Reopen contact modal
const reopenContactModal = () => {
  contactModal.value = true;
};

// Contact candidate
const confirmContactCandidate = () => {
  // Validate user
  const isValid = validate(addContactSchema, dataCandidate);
  if (!isValid) {
    return;
  }
  contactModal.value = false;

  confirmPopup(MESSAGE.CONTACT.ADD.CONFIRM_TITLE, MESSAGE.CONTACT.ADD.CONFIRM_QUESTION, contactCandidate, reopenContactModal);
};

// Update status candidate
const updateStatus = async (cvStatus, message) => {
  listIdCandidate.value.push(idEliminate.value);

  const dataUpdate = {
    list_id: listIdCandidate.value,
    status: cvStatus,
  };

  const data = await candidateService.editStatus(dataUpdate, message);
  listIdCandidate.value = [];

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
const eliminateCandidate = () => {
  updateStatus(CANDIDATE_STATUS[1].id, MESSAGE.CONTACT.DELETE.SUCCESS);
};

// Open modal confirm eliminate candidate
const confirmEliminate = (data) => {
  idEliminate.value = data.row.id;

  confirmPopup(MESSAGE.CONTACT.DELETE.CONFIRM_TITLE, MESSAGE.CONTACT.DELETE.CONFIRM_QUESTION, eliminateCandidate);
};

// Convert time
const convertTime = () => {
  dataCandidate.time = convertToTime(dataCandidate.time);
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

const passInterview = async () => {
  listIdCandidate.value.push(dataCv.id);

  const dataUpdate = {
    list_id: listIdCandidate.value,
    status: CANDIDATE_STATUS[13].id,
  };

  const data = await candidateService.editStatus(dataUpdate, MESSAGE.CONTACT.PASS.SUCCESS);
  listIdCandidate.value = [];

  // Update status SUCCESS
  if (data) {
    // Remove candidate from list data
    rows.value = rows.value.filter((row) => row.id !== dataCv.id);
    records.value = records.value.filter((row) => row.id !== dataCv.id);

    // Update paginate and total record
    updatePaginate(rows.value.length);
    totalRecord.value = rows.value.length;
    // Update count record of menu
    countRecord();
  }
};

// Accept cv
const confirmPassInterview = (data) => {
  dataCv.candidate = data.row.name;
  dataCv.cv_file = data.row.cv_file_path;
  dataCv.id = data.row.id;
  confirmPopup(MESSAGE.CONTACT.PASS.CONFIRM_TITLE, MESSAGE.CONTACT.PASS.CONFIRM_QUESTION, passInterview);
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  await Promise.all([
    getListOffice(),
    getListRecommender(),
    getListPosition(),
    getListTeam(),
    getListCandidate(),
  ]);

  await getListCandidate(false);

  loading.value = false;
});

</script>

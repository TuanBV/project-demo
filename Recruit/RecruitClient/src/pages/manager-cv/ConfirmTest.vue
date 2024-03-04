<template>
  <div class="q-pa-md">
    <h1 class="tw-text-xl">Phê duyệt bài test ứng viên</h1>

    <!-- Search Advance -->
    <div class="tw-mt-3 tw-border tw-border-gray-300 tw-p-5 tw-rounded-md">
      <div class="tw-flex tw-flex-wrap">
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="technique">Vị trí:</label>
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
          <label class="tw-block" for="technique">Điểm test:</label>
          <div class="tw-inline tw-border tw-border-gray-300 tw-border-r-0 tw-p-[5px] bg-gray-200 tw-rounded-l-md">
            >=
          </div>
          <input
            id="score"
            type="tel"
            class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-[3px] tw-pl-2 tw-w-[70px] tw-rounded-r-md"
            min="1"
            maxlength="2"
            onkeypress="return event.charCode >= 48 && event.charCode <= 57"
            v-model="dataSearch.advance.score"
            @input="searchHandle"
          >
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

    <!-- Send mail -->
    <div class="tw-mt-5">
      <q-btn
        class="sp:tw-text-[10px] tw-pl-"
        color="green-7"
        size="12px"
        @click.prevent="confirmSaveScoreAll"
        :disable="rows.length === 0"
      >
        <q-icon name="save_as" class="tw-mr-2"/>
        Lưu điểm
      </q-btn>
      <q-btn
        class="sp:tw-text-[10px] tw-mx-3"
        color="green-7"
        size="12px"
        @click.prevent="confirmCandidate"
        :disable="rows.length === 0"
      >
        Duyệt
      </q-btn>
      <q-btn
        class="sp:tw-text-[10px]"
        color="red-7"
        size="12px"
        @click.prevent="confirmEliminateAll"
        :disable="rows.length === 0"
      >
        Loại
      </q-btn>
    </div>

    <!-- List of candidates -->
    <q-table
      class="tw-mt-5 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      loading-label="Đang tìm kiếm dữ liệu ..."
      hide-pagination
      :loading="loading"
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      selection="multiple"
      v-model:selected="candidateSelected"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách bài test ứng viên</span>
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
      <!-- Column score -->
      <template v-slot:body-cell-score="props">
        <q-td :props="props" class="tw-w-[150px]">
          <input type="tel" class="tw-w-[70px] tw-border tw-border-gray-500 focus:tw-outline-none
            focus:tw-border-sky-500 tw-rounded-sm tw-px-1" v-model="props.row.score"
            min="1"
            maxlength="2"
            onkeypress="return event.charCode >= 48 && event.charCode <= 57" />
        </q-td>
      </template>
      <!-- Column checkbox not test -->
      <template v-slot:body-cell-not_test="props">
        <q-td :props="props" class="tw-w-[100px]">
          <q-checkbox v-model="idsNotTest" :val="props.row.id" color="grey-8" />
        </q-td>
      </template>
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[240px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="sp:tw-text-[10px]"
              color="red-7"
              size="12px"
              @click.prevent="confirmEliminate(props)"
            >
              Loại
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
      <template v-slot:bottom>
        <span v-if="candidateSelected.length > 0">{{ candidateSelected.length }} bản ghi được chọn</span>
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

  </div>
</template>

<script setup>
import confirmTestService from 'services/confirm-test.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems } from 'utilities/common';
import { MESSAGE, WARNING } from 'utilities/message';
import { useAuthStore } from 'stores/auth-store';
import { PAGINATION_DEFAULT, PERPAGE_OPTIONS, GENDER } from 'utilities/const';
import { cloneDeep } from 'lodash';
import ToastUtil from 'utilities/toast';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others

const { confirmPopup, countRecord } = useMixin();

// 2) ======= VARIABLE REF ========

const columns = ref([
  {
    name: 'serial',
    align: 'left',
    label: 'STT',
    field: 'serial',
    sortable: true,
  },
  {
    name: 'checkbox',
    align: 'left',
    label: '',
    field: 'checkbox',
    sortable: false,
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
    name: 'score',
    align: 'center',
    label: 'Điểm test',
    field: 'score',
    sortable: false,
  },
  {
    name: 'not_test',
    align: 'center',
    label: 'Không đến test',
    field: 'not_test',
    sortable: false,
  },
  {
    name: 'action',
    align: 'center',
    label: 'Hành động',
    field: 'action',
    sortable: false,
  },
]);

const rows = ref([]);

const listTeam = ref([]);
const listOffice = ref([]);

const dataSearch = reactive({
  search_key: '',
  advance: {
    team: '',
    score: '',
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

const candidateSelected = ref([]);
const idsNotTest = ref([]);
const idEliminate = ref(null);
const totalRecord = ref(rows.value.length);
const records = ref([]);
const loading = ref(true);

// 3) ======= METHOD/FUNCTION ========

// Save all test score
const saveScoreAll = async () => {
  const candidateScores = [];
  let flagStopConfirm = false;
  candidateSelected.value.forEach((candidate) => {
    if (candidate.score === null) {
      flagStopConfirm = true;
      return;
    }
    candidateScores.push({
      id: candidate.id,
      score: candidate.score,
      interview_id: candidate.interview_id,
    });
  });

  if (flagStopConfirm) {
    ToastUtil.warning(WARNING.CANDIDATE_NOT_HAVE_SCORE);
    return;
  }

  await confirmTestService.saveScore(candidateScores);
  candidateSelected.value = [];
};

// Open modal confirm save all test score
const confirmSaveScoreAll = () => {
  if (candidateSelected.value.length > 0) {
    confirmPopup(MESSAGE.CONFIRM.SAVE_SCORE.CONFIRM_TITLE, MESSAGE.CONFIRM.SAVE_SCORE.CONFIRM_QUESTION, saveScoreAll);
  } else {
    ToastUtil.warning(WARNING.NOT_SELECTED);
  }
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
  candidateSelected.value = [];
  idsNotTest.value = [];
  rows.value = searchItems(dataSearch, records.value);
  totalRecord.value = rows.value.length;
  updatePaginate(totalRecord.value);
};

// Reset searc data
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.advance.team = '';
  dataSearch.advance.score = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

// Get list candidate
const getListCandidate = async (flagLoading = true) => {
  const data = await confirmTestService.getList(flagLoading);
  if (data) {
    totalRecord.value = data.item.length;
    updatePaginate(totalRecord.value);
    records.value = cloneDeep(data.item);
    rows.value = cloneDeep(data.item);
    searchHandle();
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

// Eliminate candidate
const eliminate = async () => {
  const flagTest = idsNotTest.value.includes(idEliminate.value);
  const data = await confirmTestService.eliminate(idEliminate.value, flagTest);

  // Update status SUCCESS
  if (data) {
    // Remove candidate from list data
    rows.value = rows.value.filter((row) => row.id !== idEliminate.value);
    records.value = records.value.filter((row) => row.id !== idEliminate.value);

    // Update paginate and total record
    updatePaginate(rows.value.length);
    totalRecord.value = rows.value.length;
    idEliminate.value = null;
    // Update count record of menu
    countRecord();
  }
};

// Open modal confirm eliminate
const confirmEliminate = (data) => {
  idEliminate.value = data.row.id;

  confirmPopup(MESSAGE.CONFIRM.DELETE.CONFIRM_TITLE, MESSAGE.CONFIRM.DELETE.CONFIRM_QUESTION, eliminate);
};

// Eliminate all candidate
const eliminateAll = async () => {
  const candidateEliminate = [];
  const idRemove = [];
  candidateSelected.value.forEach((candidate) => {
    candidateEliminate.push({
      id: candidate.id,
      flag_not_test: idsNotTest.value.includes(candidate.id),
    });
    idRemove.push(candidate.id);
  });

  const sent = await confirmTestService.eliminateAll(candidateEliminate);
  if (sent) {
    // Delete candidate in rows, records
    rows.value = rows.value.filter((row) => !idRemove.includes(row.id));
    records.value = records.value.filter((row) => !idRemove.includes(row.id));
    totalRecord.value = rows.value.length;
    updatePaginate(totalRecord.value);
    // Update count record of menu
    countRecord();
  }
};

// Open modal confirm eliminate all candidate
const confirmEliminateAll = () => {
  if (candidateSelected.value.length > 0) {
    confirmPopup(MESSAGE.CONFIRM.DELETE_ALL.CONFIRM_TITLE, MESSAGE.CONFIRM.DELETE_ALL.CONFIRM_QUESTION, eliminateAll);
  } else {
    ToastUtil.warning(WARNING.NOT_SELECTED);
  }
};

// Edit status all candidate
const editStatusCandidate = async () => {
  const candidateList = [];
  let flagStopConfirm = false;
  candidateSelected.value.forEach((candidate) => {
    if (candidate.score === null) {
      flagStopConfirm = true;
      return;
    }
    candidateList.push(candidate.id);
  });

  if (flagStopConfirm) {
    ToastUtil.warning(WARNING.CANDIDATE_NOT_HAVE_SCORE);
    return;
  }

  const sent = await confirmTestService.confirmTest(candidateList);
  if (sent) {
    // Delete candidate in rows, records
    rows.value = rows.value.filter((row) => !candidateList.includes(row.id));
    records.value = records.value.filter((row) => !candidateList.includes(row.id));
    totalRecord.value = rows.value.length;
    updatePaginate(totalRecord.value);
    // Update count record of menu
    countRecord();
    candidateSelected.value = [];
  }
};

// Open modal confirm accept all candidate
const confirmCandidate = () => {
  if (candidateSelected.value.length > 0) {
    confirmPopup(MESSAGE.CONFIRM.EDIT_STATUS.CONFIRM_TITLE, MESSAGE.CONFIRM.EDIT_STATUS.CONFIRM_QUESTION, editStatusCandidate);
  } else {
    ToastUtil.warning(WARNING.NOT_SELECTED);
  }
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  await Promise.all([
    getListOffice(),
    getListTeam(),
  ]);

  await getListCandidate(false);

  loading.value = false;
});

</script>

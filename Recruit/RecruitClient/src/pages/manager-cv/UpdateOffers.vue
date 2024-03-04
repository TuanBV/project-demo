<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Cập nhật trạng thái offer</h1>

    <!-- Search Advance -->
    <div class="tw-mt-3 tw-border tw-border-gray-300 tw-p-5 tw-rounded-md">
      <div class="tw-flex tw-flex-wrap">
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="position">Chức danh:</label>
          <select
            id="position"
            class="tw-rounded-md focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-min-w-[100px]"
            v-model="dataSearch.advance.position_id"
            @change="searchHandle"
          >
            <option value="">Tất cả</option>
            <option v-for="(position, index) in listPosition" :value="position.id" :key="index">
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
              tw-py-1 tw-pl-1 tw-min-w-[100px]"
            v-model="dataSearch.advance.team_id"
            @change="searchHandle"
          >
            <option value="">Tất cả</option>
            <option v-for="(team, index) in listTeam" :value="team.id" :key="index">
              {{ team.name }}
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

    <!-- List of candidate -->
    <q-table
      class="tw-mt-5 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      loading-label="Đang tìm kiếm dữ liệu ..."
      hide-pagination
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      :loading="loading"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên đã gửi offer</span>
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
        <q-td :props="props" class="md:tw-w-[150px]">
          {{ props.pageIndex + 1 }}
        </q-td>
      </template>
      <!-- Column fullname -->
      <template v-slot:body-cell-fullname="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <p class="tw-text-sky-600 tw-cursor-pointer hover:tw-underline
            hover:tw-underline-offset-1" @click.prevent="openModalCv(props.row)">{{ props.row.fullname }}</p>
        </q-td>
      </template>
      <!-- Action field -->
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
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="tw-w-[160px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="green-7"
              @click.prevent="openModalOffer(props)"
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

    <q-dialog v-model="modalOffer">
      <q-card style="width: 25%; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Đổi trạng thái offer của ứng viên {{ dataOffer.name }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="height: max-content">
          <div class="sp:tw-mt-1 tw-text-center">
            <div class="tw-w-[125px] tw-text-right tw-inline-block tw-mr-8">
              <label class="tw-font-bold" for="name">Chuyển trạng thái:<span class="text-red">*</span></label>
            </div>
            <select
              id="status"
              class="tw-rounded-md tw-border tw-border-gray-300
                tw-py-[3px] tw-pl-2 tw-w-[60%] tw-inline
                focus:tw-outline-none focus:tw-border-sky-500"
              placeholder="Nhập tiêu đề"
              v-model="dataOffer.status"
            >
              <option value="">Tất cả</option>
              <option :value="CANDIDATE_STATUS[16].id">{{ CANDIDATE_STATUS[16].name }}</option>
              <option :value="CANDIDATE_STATUS[17].id">{{ CANDIDATE_STATUS[17].name }}</option>
            </select>
          </div>
        </q-card-section>
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn color="green-7" class="tw-w-[100px] tw-text-white" @click.prevent="openModalConfirmStatus()" label="Cập nhập"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="cvModal">
      <q-card style="width: 900px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Xem CV của ứng viên {{ cv.name }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: 650px">
          <iframe title="cv" :src="cv.link"
            height="100%" width="100%"></iframe>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems } from 'utilities/common';
import { MESSAGE } from 'utilities/message';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, GENDER,
} from 'utilities/const';
import { cloneDeep } from 'lodash';
import { useAuthStore } from 'stores/auth-store';
import candidateService from 'services/candidate.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others

const { confirmPopup, countRecord } = useMixin();

// 2) ======= VARIABLE REF ========
const loading = ref(true);
const modalOffer = ref(false);
const cvModal = ref(false);
const cv = reactive({
  name: '',
  link: '',
});

const dataSearch = reactive({
  search_key: '',
  advance: {
    position_id: '',
    team_id: '',
    office: '',
    gender: '',
  },
});

const dataOffer = reactive({
  list_id: null,
  name: '',
  status: '',
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

const rows = ref([]);

const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});

const totalRecord = ref(rows.value.length);
let records = [];

// 3) ======= METHOD/FUNCTION ========

// Update paginate
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

// Change page
const changePerPage = () => {
  updatePaginate(rows.value.length);
};

// Open modal offer
const openModalOffer = (data) => {
  modalOffer.value = true;
  dataOffer.list_id = [data.row.id];
  dataOffer.name = data.row.name;
  dataOffer.status = '';
};

// Update status
const updateStatus = async () => {
  const edited = await candidateService.editStatus(dataOffer, MESSAGE.CANDIDATE.UPDATE_OFFER.SUCCESS);
  if (edited) {
    // Delete candidate in rows, records
    rows.value = rows.value.filter((row) => !dataOffer.list_id.includes(row.id));
    records = records.filter((row) => !dataOffer.list_id.includes(row.id));
    totalRecord.value = rows.value.length;
    updatePaginate(totalRecord.value);
    // Update count record of menu
    countRecord();
  }
};

// Reopen modal offer
const reopenModalOffer = () => {
  modalOffer.value = true;
};

// Open modal confirm status offer
const openModalConfirmStatus = () => {
  modalOffer.value = false;

  confirmPopup(MESSAGE.OFFER.UPDATE.CONFIRM_TITLE, MESSAGE.OFFER.UPDATE.CONFIRM_QUESTION, updateStatus, reopenModalOffer);
};

// Search data
const searchHandle = () => {
  rows.value = searchItems(dataSearch, records);
  totalRecord.value = rows.value.length;
  updatePaginate(totalRecord.value);
};

// Reset search data
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.advance.position_id = '';
  dataSearch.advance.team_id = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

// Open modal show cv
const openModalCv = (row) => {
  cvModal.value = true;
  cv.name = row.name;
  cv.link = `${row.cv_file_path}/`;
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  const [dataOffices, positions, teams] = await Promise.all([
    officeService.getList(),
    positionService.getList(),
    teamService.getList(),
  ]);
  loading.value = false;

  if (dataOffices) {
    listOffice.value = cloneDeep(dataOffices.list_office);
    listOffice.value.forEach((item) => {
      if (item.id === user.office_id) {
        dataSearch.advance.office = item.name;
      }
    });
  }

  const candidates = await candidateService.getOfferCandidates(false);

  if (candidates) {
    totalRecord.value = candidates.length;
    updatePaginate(totalRecord.value);
    records = cloneDeep(candidates);
    rows.value = cloneDeep(candidates);
    searchHandle();
  }

  if (positions) {
    listPosition.value = positions;
  }

  if (teams) {
    listTeam.value = teams;
  }
});

</script>

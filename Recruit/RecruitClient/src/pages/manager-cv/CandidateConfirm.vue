<template>
  <div class="q-pa-md">
    <!-- Search Advance -->
    <div class="tw-mt-3 tw-border tw-border-gray-300 tw-p-5 tw-rounded-md">
      <div class="tw-flex tw-flex-wrap">
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="level">Chức danh:</label>
          <select
            id="position"
            class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-min-w-[100px] tw-rounded-md"
            v-model="dataSearch.advance.position"
            @change="searchHandler()"
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
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option v-for="(item, index) in GENDER" :value="item.name" :key="index">
              {{ item.name }}
            </option>
          </select>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="technique">Vị trí:</label>
          <select
            id="team"
            class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-min-w-[100px] tw-rounded-md"
            v-model="dataSearch.advance.team"
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option v-for="(team, index) in listTeam" :value="team.name" :key="index">
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
            @change="searchHandler()"
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
          @click="resetSearch()"
        >
          Đặt lại
        </button>
      </div>
    </div>

    <!-- List of candidates -->
    <q-table
      class="tw-mt-5 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      loading-label="Đang tìm kiếm dữ liệu ..."
      :loading="loading"
      hide-pagination
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên cần duyệt thông tin</span>
        <q-form
          class="tw-inline-block sp:tw-ml-0 tw-ml-10 tw-translate-y-px"
        >
          <q-input
            dense
            debounce="300"
            input-class="tw-py-0"
            v-model="dataSearch.search_key"
            placeholder="Tìm kiếm"
            @update:model-value="searchHandler"
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
      <!-- Search data ... -->
      <template v-slot:loadingLabel="{ message }">
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
      <!-- Column test point -->
      <template v-slot:body-cell-test_point="props">
        <q-td :props="props" class="tw-w-[150px]">
          <input type="text" class="tw-w-[70px] tw-border tw-border-gray-500 focus:tw-outline-none
            focus:tw-border-sky-500 tw-rounded-sm">
        </q-td>
      </template>
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[240px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="sp:tw-text-[10px]"
              color="green-7"
              size="12px"
              @click.prevent="viewCandidates(props.row.id)"
            >
              <q-icon name="visibility" class="tw-mr-2"/>Xem
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

    <q-dialog v-model="dialog">
      <q-card class="tw-min-w-[480px]">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Thông tin ứng viên{{ dataMail.name }}</div>
          <q-space />
        </q-card-section>

        <q-card-section>
          <div class="tw-divide-y tw-divide-slate-300 tw-mt-[-10px]">
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Họ tên:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.fullname }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Ngày sinh:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.birthday }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Vị trí:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.team }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Chức danh:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.position }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Số CCCD:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.identification_number }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Nơi cấp:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.place_issued_identification }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Ngày cấp:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.date_issued_identification }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">TK ngân hàng:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.bank_account }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Chi nhánh:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.bank_branch }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Biển số xe:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.vehicle_number }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Số điện thoại:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.telephone_no }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Email:</label>
              </div>
              <div class="tw-w-[200px] hidden-text">{{ candidate.email }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Ngày dự kiến đi làm:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidate.start_join_date }}</div>
            </div>
          </div>
        </q-card-section>

        <q-card-section align="center" class="row tw-justify-center tw-items-center q-pb-lg">
          <q-btn label="Duyệt" @click="dialog=false, confirmPopup(
            MESSAGE.CANDIDATE.CONFIRM.CONFIRM_TITLE, MESSAGE.CANDIDATE.CONFIRM.CONFIRM_QUESTION + `<b>${candidate.fullname}</b>?`, confirmCandidate, onClose
          )" text-color="white" color="green" class="tw-mr-3"/>
        </q-card-section>
      </q-card>
    </q-dialog>

  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import candidateConfirmService from 'services/candidate-confirm.service';
import positionService from 'services/position.service';
import officeService from 'services/office.service';
import teamService from 'services/team.service';
import toast from 'utilities/toast';
import { MESSAGE } from 'src/shared/utilities/message';
import useMixin from 'mixins/common.js';
import { PAGINATION_DEFAULT, PERPAGE_OPTIONS, GENDER } from 'utilities/const';
import { cloneDeep } from 'lodash';
import { searchItems } from 'utilities/common';
import { useAuthStore } from 'stores/auth-store';

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
    name: 'action',
    align: 'center',
    label: 'Hành động',
    field: 'action',
    sortable: false,
  },
]);

const candidate = reactive({
  id: '',
  fullname: '',
  team: '',
  position: '',
  email: '',
  telephone_no: '',
  birthday: '',
  school: '',
  place_issued_identification: '',
  identification_number: '',
  date_issued_identification: '',
  start_join_date: '',
  class: '',
  bank_account: '',
  bank_branch: '',
  vehicle_number: '',
  faculty: '',
});

const rows = ref([]);

const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});

const allSelected = ref(false);
const idsSelected = ref([]);
const dialog = ref(false);

const dataMail = reactive({
  id: null,
  title: '',
  body: '',
  candidate_id: null,
  name: '',
});

const totalRecord = ref(rows.value.length);
const records = ref([]);

const dataSearch = reactive({
  advance: {
    position: '',
    team: '',
    office: '',
    gender: '',
  },
  search_key: '',
});
const listTeam = ref([]);
const listPosition = ref([]);
const listOffice = ref([]);
const loading = ref(true);

// 3) ======= METHOD/FUNCTION ========
// Open modal edit mail
const onClose = () => {
  dialog.value = true;
};

// Update paginate
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

// Search data
const searchHandler = async () => {
  const listCandidates = await candidateConfirmService.getList(false);
  idsSelected.value = [];

  if (listCandidates) {
    records.value = cloneDeep(listCandidates.item);
    rows.value = searchItems(dataSearch, records.value);
    totalRecord.value = listCandidates.item.length;
    updatePaginate(totalRecord.value);
  }
};

// Reset search data
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.advance.position = '';
  dataSearch.advance.team = '';
  dataSearch.advance.office = '';
  dataSearch.advance.gender = '';
  searchHandler();
};

// Confirm candidate
const confirmCandidate = async () => {
  const isConfirmCandidate = await candidateConfirmService.edit(candidate.id);
  if (isConfirmCandidate) {
    // Update count record of menu
    countRecord();
    toast.success(MESSAGE.CANDIDATE.CONFIRM.SUCCESS);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.CANDIDATE.CONFIRM.ERROR);
};

// Change page
const changePerPage = () => {
  updatePaginate(rows.value.length);
};

// View candidate
const viewCandidates = async (idCandidate) => {
  const infoCandidate = await candidateConfirmService.getConfirmCandidate(idCandidate);
  if (infoCandidate) {
    candidate.id = infoCandidate.id;
    candidate.fullname = infoCandidate.fullname;
    candidate.team = infoCandidate.team;
    candidate.position = infoCandidate.position;
    candidate.email = infoCandidate.email;
    candidate.telephone_no = infoCandidate.telephone_no;
    candidate.birthday = infoCandidate.birthday;
    candidate.school = infoCandidate.school;
    candidate.place_issued_identification = infoCandidate.place_issued_identification;
    candidate.identification_number = infoCandidate.identification_number;
    candidate.date_issued_identification = infoCandidate.date_issued_identification;
    candidate.school = infoCandidate.school;
    candidate.start_join_date = infoCandidate.start_join_date;
    candidate.class = infoCandidate.class;
    candidate.bank_account = infoCandidate.bank_account;
    candidate.bank_branch = infoCandidate.bank_branch;
    candidate.vehicle_number = infoCandidate.vehicle_number;
    candidate.faculty = infoCandidate.faculty;
    dialog.value = true;
  }
};

// 4) ======= VUE JS LIFECYCLE ========
onMounted(async () => {
  const [listPositions, listTeams, dataOffices] = await Promise.all([
    positionService.getList(),
    teamService.getList(),
    officeService.getList(),
  ]);
  // Get position
  listPosition.value = listPositions;
  listTeam.value = listTeams;
  listOffice.value = dataOffices.list_office;
  allSelected.value = false;
  listOffice.value.forEach((item) => {
    if (item.id === user.office_id) {
      dataSearch.advance.office = item.name;
    }
  });
  await searchHandler();

  loading.value = false;
});

</script>

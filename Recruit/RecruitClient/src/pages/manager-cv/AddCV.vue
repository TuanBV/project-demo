<template>
  <div class="q-pa-md">
    <h1 class="tw-text-xl">Nhập thông tin CV</h1>
    <q-btn color="green-7" class="tw-mt-4 sp:tw-text-xs" icon="add" label="Thêm CV ứng viên" @click="openModalAdd" />

    <!-- Search Advance -->
    <div class="tw-mt-3 tw-border tw-border-gray-300 tw-p-5 tw-rounded-md">
      <div class="tw-flex tw-flex-wrap">
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="position">Chức danh:</label>
          <select
            id="position"
            class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-min-w-[100px] sp:tw-min-w-[160px] tw-rounded-md"
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
      loading-label="Đang tìm kiếm dữ liệu ..."
      hide-pagination
      :loading="loading"
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên đã nhập</span>
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
      <!-- Column status -->
      <template v-slot:body-cell-status="props">
        <q-td :props="props" class="md:tw-w-[240px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <p>
              {{ props.row.status }}
            </p>
          </div>
        </q-td>
      </template>
      <!-- Column previous status -->
      <template v-slot:body-cell-previous_status="props">
        <q-td :props="props" class="md:tw-w-[240px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <p>
              {{ props.row.previous_status }}
            </p>
          </div>
        </q-td>
      </template>
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[240px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-if="checkPdfFile(props)">
            <q-btn
              class="sp:tw-text-[10px]"
              color="green-7"
              size="12px"
              @click.prevent="openModalCv(props)"
            >
              <q-icon name="visibility" class="tw-mr-2"/>
              Xem CV
            </q-btn>
          </div>
          <div class="tw-w-[230px] md:tw-inline-block" v-else>
            <q-btn
              class="sp:tw-text-[10px] tw-mr-2"
              color="blue-7"
              size="11px"
              @click.prevent="dowloadCv(props.row.cv_file_path)"
            >
              <q-icon name="file_download" class="tw-mr-2"/>
              Tải CV
            </q-btn>
            <q-btn
              class="sp:tw-text-[10px] tw-mr-2"
              color="green-7"
              size="11px"
              @click.prevent="confirmDocCv(props)"
            >
              Duyệt
            </q-btn>
            <q-btn
              class="sp:tw-text-[10px]"
              color="orange-7"
              size="11px"
              @click.prevent="eliminateDocCv(props)"
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
      <q-card style="width: 900px; max-width: 80vw; height: 800px">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Duyệt CV ứng viên {{ dataCv.candidate }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: 650px">
          <iframe title="cv" :src="dataCv.cv_file"
            height="100%" width="100%"></iframe>
        </q-card-section>

        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" @click.prevent="confirmEliminate()" label="Loại"/>
          <q-btn color="positive" class="tw-w-[100px] tw-text-white" @click.prevent="confirmAcceptCv()" label="Duyệt"/>
        </q-card-actions>

      </q-card>
    </q-dialog>

    <q-dialog v-model="addModal">
      <q-card style="width: 100%; max-width: 650px;  height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Nhập thông tin CV</div>
          <q-space />
        </q-card-section>

        <q-card-section class="q-pt-none">
          <div
            class="tw-rounded tw-p-3 tw-mt-4"
          >
            <div class="tw-grid tw-grid-cols-2">
              <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                <label class="tw-block" for="name">Họ tên: <span class="text-red">*</span></label>
                <input
                  type="text"
                  id="name"
                  class="tw-rounded-md tw-border tw-border-gray-300
                    tw-py-[3px] tw-pl-2 sp:tw-w-[160px] tw-w-[280px]
                    focus:tw-outline-none focus:tw-border-sky-500"
                  placeholder="Nhập đầy đủ họ tên"
                  v-model="dataCandidate.fullname"
                >
                <span v-if="(errors.fullname)" class="text-red tw-text-xs">*{{ errors.fullname }}</span>
              </div>
              <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                <label class="tw-block" for="email">Email: <span class="text-red">*</span></label>
                <input
                  type="text"
                  id="email"
                  v-model="dataCandidate.email"
                  class="tw-border tw-border-gray-300 tw-rounded-md
                    tw-py-[3px] tw-pl-2 sp:tw-w-[160px] tw-w-[280px] focus:tw-outline-none
                    focus:tw-border-sky-500"
                    placeholder="Nhập email"
                >
                <span v-if="(errors.email)" class="text-red tw-text-xs">*{{ errors.email }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3  sp:tw-w-[45%]">
                <label class="tw-block" for="telephone">Số điện thoại: <span class="text-red">*</span></label>
                <input
                  type="text"
                  id="telephone"
                  class="tw-border tw-border-gray-300 tw-rounded-md
                    tw-py-[3px] tw-pl-2 sp:tw-w-[160px] tw-w-[280px] focus:tw-outline-none
                    focus:tw-border-sky-500"
                    v-model="dataCandidate.telephone_no"
                    placeholder="Nhập SĐT"
                    maxlength="11"
                >
                <span v-if="(errors.telephone_no)" class="text-red tw-text-xs">*{{ errors.telephone_no }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3  sp:tw-w-[45%]">
                <label class="tw-block" for="cv">Chọn CV: <span class="text-red">*</span></label>
                <input type="file" name="cv" id="cv" class="tw-border-gray-300
                  sp:tw-w-[160px] tw-w-[280px] focus:tw-outline-none focus:tw-border-sky-500"
                  accept="application/pdf, .docx, .doc"
                  @change="uploadFile"
                >
                <span v-if="errors['cv_file/file']" class="text-red tw-text-xs">*{{ errors['cv_file/file']}}</span>
                <span v-if="textCvFile !== ''" class="text-red tw-text-xs">*{{ textCvFile }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%] tw-w-[280px]">
                <label class="tw-block" for="birthday">Ngày sinh: <span class="text-red">*</span></label>
                <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px]
                  tw-rounded-md" :class=" birthdayFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
                  <input
                    type="text"
                    id="birthday"
                    class="tw-outline-0 tw-py-[3px] tw-w-[90%]"
                    v-model="dataCandidate.birthday"
                    placeholder="Nhập ngày sinh (năm tháng ngày)"
                    @focusin="birthdayFocus = true"
                    @focusout="birthdayFocus = false"
                  >
                  <q-icon name="event" class="cursor-pointer" size="xs">
                    <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxy">
                      <q-date name="wedding" v-model="dataCandidate.birthday" @update:model-value="qDateProxy.hide()">
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </div>
                <span v-if="(errors.birthday)" class="text-red tw-text-xs">*{{ errors.birthday }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%]">
                <label class="tw-block" for="address">Địa chỉ: <span class="text-red">*</span></label>
                <input
                  type="text"
                  id="address"
                  class="focus:tw-outline-none focus:tw-border-sky-500 tw-border
                    tw-border-gray-300 tw-rounded-md
                    tw-py-[3px] tw-pl-2 sp:tw-w-[160px] tw-w-[280px]"
                  v-model="dataCandidate.full_address"
                  placeholder="Nhập địa chỉ"
                >
                <span v-if="(errors.full_address)" class="text-red tw-text-xs">*{{ errors.full_address }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%]">
                <label class="tw-block" for="position">Chức danh:</label>
                <select
                  id="position"
                  class="tw-rounded-md tw-border tw-border-gray-300
                    tw-py-1 tw-pl-1 sp:tw-min-w-[160px] tw-w-[280px] focus:tw-outline-none
                    focus:tw-border-sky-500"
                    v-model="dataCandidate.position_id"
                >
                  <option value=""></option>
                  <option v-for="(position, index) in listPosition" :value="position.id" :key="index">
                    {{ position.name }}
                  </option>
                </select>
                <br>
                <span v-if="(errors.position_id)" class="text-red tw-text-xs">*{{ errors.position_id }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%]">
                <label class="tw-block" for="team">Vị trí:</label>
                <select
                  id="team"
                  class="tw-border tw-border-gray-300 focus:tw-outline-none focus:tw-border-sky-500
                    tw-py-1 tw-pl-1 tw-min-w-[160px] tw-w-[280px] tw-rounded-md"
                    v-model="dataCandidate.team_id"
                >
                  <option value=""></option>
                  <option v-for="(team, index) in listTeam" :value="team.id" :key="index">
                    {{ team.name }}
                  </option>
                </select>
                <br>
                <span v-if="(errors.team_id)" class="text-red tw-text-xs">*{{ errors.team_id }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%]">
                <label class="tw-block" for="recommender">Nguồn giới thiệu:</label>
                <select
                  id="recommender"
                  class="focus:tw-outline-none focus:tw-border-sky-500
                    tw-rounded-md tw-border tw-border-gray-300
                    tw-py-1 tw-pl-1 tw-min-w-[160px] tw-w-[280px]"
                  v-model="dataCandidate.recommender_id"
                >
                  <option value=""></option>
                  <option v-for="(recommenrder, index) in listRecommender" :value="recommenrder.id" :key="index">
                    {{ recommenrder.fullname }}
                  </option>
                </select>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%]">
                <label class="tw-block" for="recommender">Địa điểm:</label>
                <select
                  id="recommender"
                  class="focus:tw-outline-none focus:tw-border-sky-500
                    tw-rounded-md tw-border tw-border-gray-300
                    tw-py-1 tw-pl-1 tw-min-w-[160px] tw-w-[280px]"
                  v-model="dataCandidate.office_id"
                >
                  <option value=""></option>
                  <option v-for="(office, index) in listOffice" :value="office.id" :key="index">
                    {{ office.name }}
                  </option>
                </select>
                <span v-if="(errors.office_id)" class="text-red tw-text-xs">*{{ errors.office_id }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%]">
                <label class="tw-block" for="gender">Giới tính:</label>
                <select
                  id="gender"
                  class="focus:tw-outline-none focus:tw-border-sky-500
                    tw-rounded-md tw-border tw-border-gray-300
                    tw-py-1 tw-pl-1 tw-min-w-[160px] tw-w-[280px]"
                  v-model="dataCandidate.gender"
                >
                  <option value=""></option>
                  <option v-for="(item, index) in GENDER" :value="item.id" :key="index">
                    {{ item.name }}
                  </option>
                </select>
                <br>
                <span v-if="(errors.gender)" class="text-red tw-text-xs">*{{ errors.gender }}</span>
              </div>
              <div class="sp:tw-mt-1 tw-mt-3 sp:tw-w-[45%]">
                <label class="tw-block" for="experience">Năm kinh nghiệm: <span class="text-red">*</span></label>
                <input
                  type="text"
                  id="experience"
                  class="tw-rounded-md tw-border tw-border-gray-300
                    tw-py-[3px] tw-pl-2 sp:tw-w-[160px] tw-w-[280px]
                    focus:tw-outline-none focus:tw-border-sky-500"
                  placeholder="Nhập năm kinh nghiệm"
                  v-model="dataCandidate.number_experiences"
                  maxlength="4"
                >
                <span v-if="(errors.number_experiences)" class="text-red tw-text-xs">*{{ errors.number_experiences }}</span>
              </div>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" @click.prevent="confirmCloseModalAddCv" />
          <q-btn color="green-7" class="tw-w-[100px] tw-text-white" @click.prevent="confirmAddCv" label="Thêm"/>
          <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" @click.prevent="resetAdd" label="Nhập lại"/>
        </q-card-actions>

      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import candidateService from 'services/candidate.service';
import recommenderService from 'services/recommender.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';
import addCvService from 'services/add-cv.service';
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems, setDataFile } from 'utilities/common';
import { useAuthStore } from 'stores/auth-store';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, MAX_SIZE_PDF,
  FILE_TYPE_VALID, GENDER,
} from 'utilities/const';
import { cloneDeep, isEqual, remove } from 'lodash';
import { MESSAGE } from 'utilities/message';
import useValidate from 'composables/validate';
import addCvSchema from '../../validations/schemas/candidate/candidate.js';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others

const { confirmPopup, countRecord } = useMixin();
const { errors, validate } = useValidate();

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
    name: 'recommender',
    align: 'left',
    label: 'Người giới thiệu',
    field: 'recommender',
    sortable: false,
  },
  {
    name: 'status',
    align: 'left',
    label: 'Trạng thái ứng viên',
    field: 'status',
    sortable: false,
  },
  {
    name: 'previous_status',
    align: 'left',
    label: 'Trạng thái trước đây',
    field: 'previous_status',
    sortable: false,
  },
  {
    name: 'application_date',
    align: 'left',
    label: 'Ngày Apply',
    field: 'application_date',
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

const dataCandidate = reactive({
  fullname: '',
  telephone_no: '',
  position_id: '',
  team_id: '',
  recommender_id: '',
  cv_file: {
    file: '',
    file_ext: '',
    file_size: '',
  },
  full_address: '',
  birthday: '',
  email: '',
  office_id: '',
  gender: '',
  number_experiences: '0',
});

const baseDataCandidate = reactive(cloneDeep(dataCandidate));

const dataCv = reactive({
  id: '',
  candidate: '',
  cv_file: '',
});

const listPosition = ref([]);

const listTeam = ref([]);

const listRecommender = ref([]);

const listOffice = ref([]);

const listIdCandidate = ref([]);

const dataSearch = reactive({
  search_key: '',
  advance: {
    position: '',
    team: '',
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

const cvModal = ref(false);
const addModal = ref(false);
const birthdayFocus = ref(false);
const totalRecord = ref(0);
const records = ref([]);
const flagCvFile = ref(false);
const textCvFile = ref('');
const loading = ref(true);
const qDateProxy = ref();

// 3) ======= METHOD/FUNCTION ========

// Open modal show cv
const openModalCv = (data) => {
  cvModal.value = true;
  dataCv.id = data.row.id;
  dataCv.candidate = data.row.fullname;
  dataCv.cv_file = `${data.row.cv_file_path}/`;
};

// Reopen modal cv
const reopenModalCv = () => {
  cvModal.value = true;
};

// Reset add data
const resetAdd = () => {
  errors.value = {};
  dataCandidate.fullname = '';
  dataCandidate.birthday = '';
  dataCandidate.cv_file = {
    file: '',
    file_ext: '',
    file_size: '',
  };
  dataCandidate.email = '';
  dataCandidate.full_address = '';
  dataCandidate.position_id = '';
  dataCandidate.telephone_no = '';
  dataCandidate.team_id = '';
  dataCandidate.recommender_id = '';
  dataCandidate.office_id = '';
  dataCandidate.gender = '';
  dataCandidate.number_experiences = '0';

  const element = document.querySelector('#cv');
  if (element) {
    element.value = '';
  }
};

// Open modal add cv
const openModalAdd = () => {
  addModal.value = true;
  resetAdd();
};

// Close modal add cv
const closeModalAddCv = () => {
  cvModal.value = false;
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
  dataSearch.advance.position = '';
  dataSearch.advance.team = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

// Get list candidate
const getListCandidate = async (flagLoading = true) => {
  const data = await addCvService.getList(flagLoading);
  if (data) {
    data.item.forEach((candidate) => {
      CANDIDATE_STATUS.forEach((itemStatus) => {
        if (itemStatus.id === candidate.status) {
          candidate.status = itemStatus.name;
        }
        if (itemStatus.id === candidate.previous_status) {
          candidate.previous_status = itemStatus.name;
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

// Check size and ext
const checkSizeAndExt = (fileSize, fileExt) => {
  // File size greater than 5mb or not pdf type
  // will return an error
  if ((fileSize !== '' && fileSize > MAX_SIZE_PDF)
  || (fileExt !== '' && !FILE_TYPE_VALID.includes(fileExt))) {
    flagCvFile.value = false;
    textCvFile.value = MESSAGE.FILE_NOT_VALID;
  }
};

// Validate upload file function
const checkFile = (input) => {
  const file = input.files[0];
  flagCvFile.value = true;
  textCvFile.value = '';
  const fileSize = file.size.toString();
  const arrFileExt = file.name.toString().split('.');
  const fileExt = arrFileExt[arrFileExt.length - 1].toString();

  checkSizeAndExt(fileSize, fileExt);
};

// Set data cv file
const setDataCv = (input, e) => {
  const newInput = input;
  const dataFile = setDataFile(newInput.files[0], e.target.result);

  dataCandidate.cv_file.file_size = dataFile.size;
  dataCandidate.cv_file.file_ext = dataFile.ext;
  dataCandidate.cv_file.file = dataFile.name;
};

// Read file
const handleReadFile = (input) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    setDataCv(input, e);
  };
  reader.readAsDataURL(input.files[0]);
};

// Upload cv
const uploadFile = (event) => {
  const input = event.target;
  // Have upload file
  if (input.files[0]) {
    checkFile(input);
    // Flag check file are true will read file
    if (flagCvFile.value) {
      handleReadFile(input);
    } else {
      input.value = null;
    }
  }
};

// Add cv
const addCv = async () => {
  const candidate = await addCvService.add(dataCandidate);

  if (candidate) {
    listTeam.value.forEach((item) => {
      if (candidate.team_id === item.id) {
        candidate.team = item.name;
      }
    });

    listPosition.value.forEach((item) => {
      if (candidate.position_id === item.id) {
        candidate.position = item.name;
      }
    });

    listRecommender.value.forEach((item) => {
      if (candidate.recommender_id === item.id) {
        candidate.recommender = item.fullname;
      }
    });

    CANDIDATE_STATUS.forEach((itemStatus) => {
      if (itemStatus.id === candidate.status) {
        candidate.status = itemStatus.name;
      }
      if (itemStatus.id === candidate.previous_status) {
        candidate.previous_status = itemStatus.name;
      }
    });

    delete candidate.team_id;
    delete candidate.position_id;
    delete candidate.recommender_id;

    const candidateNew = cloneDeep(candidate);
    remove(records.value, (e) => e.id === candidateNew.id);

    // Add cv to records
    records.value.unshift(candidateNew);
    searchHandle();
    // Update count record of menu
    countRecord();
    resetAdd();
  } else {
    addModal.value = true;
  }
};

// Reopen add modal
const reopenAddModal = () => {
  addModal.value = true;
};

// Open modal confirm add
const confirmAddCv = () => {
  // Validate data
  const isValid = validate(addCvSchema, dataCandidate);
  if (!isValid) {
    return;
  }
  addModal.value = false;

  confirmPopup(MESSAGE.ADD_CV.ADD.CONFIRM_TITLE, MESSAGE.ADD_CV.ADD.CONFIRM_QUESTION, addCv, reopenAddModal);
};

// Update status cv
const updateCvStatus = async (cvStatus, message) => {
  listIdCandidate.value.push(dataCv.id);

  const dataUpdate = {
    list_id: listIdCandidate.value,
    status: cvStatus,
  };

  const data = await candidateService.editStatus(dataUpdate, message);
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

// Eliminate cv
const eliminateCv = () => {
  updateCvStatus(CANDIDATE_STATUS[1].id, MESSAGE.ADD_CV.DELETE.SUCCESS);
};

// Accept cv
const acceptCv = () => {
  updateCvStatus(CANDIDATE_STATUS[2].id, MESSAGE.ADD_CV.ACCEPT.SUCCESS);
};

// Open modal confirm eliminate
const confirmEliminate = () => {
  cvModal.value = false;

  confirmPopup(MESSAGE.ADD_CV.DELETE.CONFIRM_TITLE, MESSAGE.ADD_CV.DELETE.CONFIRM_QUESTION, eliminateCv, reopenModalCv);
};

// Open modal confirm accept
const confirmAcceptCv = () => {
  cvModal.value = false;

  confirmPopup(MESSAGE.ADD_CV.ACCEPT.CONFIRM_TITLE, MESSAGE.ADD_CV.ACCEPT.CONFIRM_QUESTION, acceptCv, reopenModalCv);
};

// Close modal add cv
const confirmCloseModalAddCv = () => {
  addModal.value = false;
  if (!isEqual(baseDataCandidate, dataCandidate)) {
    confirmPopup(MESSAGE.ADD_CV.ADD.CONFIRM_CLOSE_TITLE, MESSAGE.ADD_CV.ADD.CONFIRM_CLOSE, closeModalAddCv, reopenAddModal);
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

// Confirm candidate have cv is doc file
const confirmDocCv = (data) => {
  dataCv.id = data.row.id;
  dataCv.candidate = data.row.fullname;
  dataCv.cv_file = data.row.cv_file_path;

  confirmPopup(MESSAGE.ADD_CV.ACCEPT.CONFIRM_TITLE, MESSAGE.ADD_CV.ACCEPT.CONFIRM_QUESTION, acceptCv);
};

// Eliminate candidate have cv is doc file
const eliminateDocCv = (data) => {
  dataCv.id = data.row.id;
  dataCv.candidate = data.row.fullname;
  dataCv.cv_file = data.row.cv_file_path;

  confirmPopup(MESSAGE.ADD_CV.DELETE.CONFIRM_TITLE, MESSAGE.ADD_CV.DELETE.CONFIRM_QUESTION, eliminateCv);
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  await Promise.all([
    getListOffice(),
    getListRecommender(),
    getListPosition(),
    getListTeam(),
  ]);

  await getListCandidate(false);
  loading.value = false;
});

</script>

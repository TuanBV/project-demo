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
        <div class="tw-mr-4 sp:tw-mt-1">
          <label class="tw-block">Địa điểm làm việc:</label>
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
        <div class="tw-mr-4 sp:tw-mt-1">
          <label class="tw-block">Giới tính:</label>
          <select
            id="office"
            class="tw-rounded-md tw-border tw-border-gray-300
              tw-py-1 tw-pl-1 tw-w-[100px] focus:tw-outline-none
              focus:tw-border-sky-500"
            v-model="dataSearch.advance.gender_text"
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option value="Nam">Nam</option>
            <option value="Nữ">Nữ</option>
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

    <div class="q-pa-md">
        <!-- Button add -->
      <q-btn icon="add" label="Thêm user" color="green-7" @click="flagEdit=false, flagDelete=false, resetDataUser()" />

      <!-- Dialog -->
      <q-dialog v-model="dialog">
        <q-card style="width: 100%; max-width: 650px;  height: max-content">
          <q-card-section class="row items-center tw-bg-[#17a2b8!important]">
            <div class="tw-text-[18px] text-white" v-if="flagEdit">Sửa Thông Tin User</div>
            <div class="tw-text-[18px] text-white" v-else>Thêm User</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <div class="tw-rounded tw-p-3">
              <!-- Employee code -->
              <div class="tw-grid tw-grid-cols-2">
                <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                  <label class="tw-leading-loose">Mã nhân viên <span class="text-red">(*)</span></label>
                  <input type="text" v-model="user.employee_code"
                    :disabled="flagEdit"
                    maxlength="6"
                    :class="[flagEdit ? 'tw-bg-gray-300 tw-text-black disabled:tw-opacity-[100!important]' : '']"
                    class="tw-px-4 tw-py-2 tw-border focus:tw-border-sky-500 tw-w-full tw-h-[36px]
                    tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600" placeholder="VN0021">
                  <span v-if="(errors.employee_code)" class="text-red tw-text-xs">*{{ errors.employee_code }}</span>
                </div>
              </div>
            <!-- Fullname and Email -->
              <div class="tw-grid tw-grid-cols-2">
                <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                  <label class="tw-leading-loose">Họ tên <span class="text-red">(*)</span></label>
                  <input type="text" v-model="user.fullname" maxlength="50"
                    class="tw-px-4 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-w-full tw-h-[36px]
                    tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600" placeholder="Nhập họ tên">
                  <span v-if="(errors.fullname)" class="text-red tw-text-xs">*{{ errors.fullname }}</span>
                </div>
                <div class="sp:tw-mt-1 sp:tw-w-[45%] tw-ml-4">
                  <label class="tw-leading-loose">Email <span class="text-red">(*)</span></label>
                  <input type="text" v-model="user.email" maxlength="256"
                    class="tw-px-4 tw-py-2 tw-border focus:tw-border-sky-500 tw-w-full tw-h-[36px]
                    tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600" placeholder="Nhập email">
                  <span v-if="(errors.email)" class="text-red tw-text-xs">*{{ errors.email }}</span>
                </div>
              </div>
              <!-- Position and Office -->
              <div class="tw-grid tw-grid-cols-2">
                <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                  <label class="tw-leading-loose">Chức danh <span class="text-red">(*)</span></label>
                  <div class="relative focus-within:text-gray-600 text-gray-400">
                    <select v-model="user.position_id"
                      class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-h-[36px]
                      tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600"
                    >
                    <option value=""></option>
                    <option v-for="(position, index) in listPosition" :value="position.id" :key="index">
                      {{ position.name }}
                    </option>
                    </select>
                    <span v-if="(errors.position_id)" class="text-red tw-text-xs">*{{ errors.position_id }}</span>
                  </div>
                </div>
                <div class="sp:tw-mt-1 sp:tw-w-[45%] tw-ml-4">
                  <label class="tw-leading-loose">Văn phòng làm việc <span class="text-red">(*)</span></label>
                  <div class="relative focus-within:text-gray-600 text-gray-400">
                    <select name="" id="" v-model="user.office_id"
                      class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-h-[36px]
                      tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600"
                    >
                    <option value=""></option>
                    <option v-for="(office, index) in listOffice" :value="office.id" :key="index">
                      {{ office.name }}
                    </option>
                    </select>
                    <span v-if="(errors.office_id)" class="text-red tw-text-xs">*{{ errors.office_id }}</span>
                  </div>
                </div>
              </div>
              <!-- Birthday and Register_date -->
              <div class="tw-grid tw-grid-cols-2">
                <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                  <label class="tw-leading-loose">Ngày sinh <span class="text-red">(*)</span></label>
                  <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px] tw-rounded-md">
                    <input
                      type="text" maxlength="10"
                      class="tw-outline-0 tw-py-[3px] tw-w-[90%] tw-rounded-md tw-leading-[30px]"
                      placeholder="Nhập ngày sinh"
                      v-model="user.birthday"
                    >
                    <q-icon name="event" class="cursor-pointer" size="xs">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyBirth">
                        <q-date name="wedding" v-model="user.birthday" @update:model-value="qDateProxyBirth.hide()">
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </div>
                  <span v-if="(errors.birthday)" class="text-red tw-text-xs">*{{ errors.birthday }}</span>
                </div>
                <div class="sp:tw-mt-1 sp:tw-w-[45%] tw-ml-4">
                  <label class="tw-leading-loose">Ngày vào cty</label>
                  <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px] tw-rounded-md">
                    <input
                      type="text" maxlength="10"
                      class="tw-outline-0 tw-py-[3px] tw-w-[90%] tw-rounded-md tw-leading-[30px]"
                      placeholder="Nhập ngày vào công ty"
                      v-model="user.registered_date"
                    >
                    <q-icon name="event" class="cursor-pointer" size="xs">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyRegisted">
                        <q-date name="wedding" v-model="user.registered_date"
                          @update:model-value="qDateProxyRegisted.hide()">
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </div>
                  <span v-if="(errors.registered_date)" class="text-red tw-text-xs">*{{ errors.registered_date }}</span>
                </div>
              </div>

              <!-- Identification number and Place issued identification -->
              <div class="tw-grid tw-grid-cols-2">
                <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                  <label class="tw-leading-loose">Số CMT/CCCD <span class="text-red">(*)</span></label>
                  <input type="text" v-model="user.identification_number" maxlength="12"
                    class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-h-[36px]
                    tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600" placeholder="Nhập số CMT/CCCD">
                  <span v-if="(errors.identification_number)" class="text-red tw-text-xs">*{{ errors.identification_number }}</span>
                </div>
                <div class="sp:tw-mt-1 sp:tw-w-[45%] tw-ml-4">
                  <label class="tw-leading-loose">Nơi cấp CMT/CCCD <span class="text-red">(*)</span></label>
                  <input type="text" v-model="user.place_issued_identification"
                    class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-h-[36px]
                    tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600"
                    placeholder="Nhập nơi cấp CMT/CCCD">
                  <span v-if="(errors.place_issued_identification)" class="text-red tw-text-xs">*{{ errors.place_issued_identification }}</span>
                </div>
              </div>
              <!-- Date issued identification and Telephone_no -->
              <div class="tw-grid tw-grid-cols-2">
                <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                  <label class="tw-leading-loose">Ngày cấp CMT/CCCD <span class="text-red">(*)</span></label>
                  <div class="tw-border tw-border-gray-300 tw-pl-2 tw-pr-2 tw-bg-white sp:tw-min-w-[160px] tw-rounded-md tw-h-[36px] tw-leading-[28px]">
                    <input
                      type="text" maxlength="10"
                      class="tw-outline-0 tw-py-[3px] tw-w-[90%] tw-rounded-md"
                      v-model="user.date_issued_identification"
                      placeholder="Nhập ngày cấp CMT/CCCD"
                    >
                    <q-icon name="event" class="cursor-pointer" size="xs" style="float: right;padding-top: 6px;">
                      <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyIdentity">
                        <q-date name="wedding" v-model="user.date_issued_identification"
                            @update:model-value="qDateProxyIdentity.hide()">
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </div>
                  <span v-if="(errors.date_issued_identification)" class="text-red tw-text-xs">*{{ errors.date_issued_identification }}</span>
                </div>
                <div class="sp:tw-mt-1 sp:tw-w-[45%] tw-ml-4">
                  <label class="tw-leading-loose">Số điện thoại <span class="text-red">(*)</span></label>
                  <input type="text" v-model="user.telephone_no" maxlength="11"
                    class="tw-px-2 tw-py-2 tw-border focus:tw-border-sky-500 tw-w-full tw-h-[36px]
                    tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600" placeholder="Nhập số điện thoại">
                  <span v-if="(errors.telephone_no)" class="text-red tw-text-xs tw-block">*{{ errors.telephone_no }}</span>
                </div>
              </div>
              <!--Gender and Full address -->
              <div class="tw-grid tw-grid-cols-2">
                <div class="sp:tw-mt-1 sp:tw-w-[45%]">
                  <label class="tw-leading-loose">Giới tính <span class="text-red">(*)</span></label>
                  <div class="relative focus-within:text-gray-600 text-gray-400">
                    <select v-model="user.gender"
                      class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-h-[36px]
                      tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600"
                    >
                    <option value=""></option>
                    <option value="0">Nam</option>
                    <option value="1">Nữ</option>
                    <option value="2">Khác</option>
                    </select>
                    <span v-if="(errors.gender)" class="text-red tw-text-xs">*{{ errors.gender }}</span>
                  </div>
                </div>
                <div class="sp:tw-mt-1 sp:tw-w-[45%] tw-ml-4">
                  <label class="tw-leading-loose">Địa chỉ liên hệ <span class="text-red">(*)</span></label>
                  <input type="text" v-model="user.full_address"
                    class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-h-[36px]
                    tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600"
                    placeholder="Nhập địa chỉ liên hệ">
                  <span v-if="(errors.full_address)" class="text-red tw-text-xs">*{{ errors.full_address }}</span>
                </div>
              </div>
              <!-- Password -->
              <div class="tw-grid tw-mt-3" v-if="!flagEdit">
                <div class="sp:tw-mt-1 tw-text-gray-500">
                  **** Mật khẩu mặc định : Test123@
                </div>
              </div>
          </div>
          </q-card-section>

          <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
            <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
            <q-btn class="tw-bg-[#28a745] tw-w-[100px] tw-text-white" v-if="!flagEdit" @click="validateUser()" label="Thêm"/>
            <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" v-if="flagEdit" @click="validateEditUser()" label="Cập nhật"/>
          </q-card-actions>

        </q-card>
      </q-dialog>
    </div>
    <!-- List of candidates -->
    <q-table
      title="Danh sách users"
      binary-state-sort
      class="tw-mt-8 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      loading-label="Đang tìm kiếm dữ liệu ..."
      :loading="loading"
      v-model:pagination="pagination"
      no-data-label="Không có dữ liệu"
      :rows="rows"
      :columns="columns"
      hide-pagination
    >
      <!-- Column serial -->
      <template v-slot:body-cell-serial="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          {{ props.pageIndex + 1 }}
        </q-td>
      </template>
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <q-form class="tw-flex">
          <span class="q-table__title tw-inline-block tw-mr-2">Danh sách users</span>
          <q-input
            dense
            debounce="300"
            input-class="tw-py-0 tw-w-[320px]"
            v-model="dataSearch.search_key"
            @update:model-value="searchHandler()"
            placeholder="Tìm kiếm (Họ tên, email, số điện thoại, quê quán)"
          >
            <template v-slot:append>
              <q-btn @click="searchHandler()" type="submit" dense unelevated round icon="search" />
            </template>
          </q-input>
        </q-form>
      </template>

      <!-- Choose per-page -->
      <template v-slot:top-right>
        <div class="sp:tw-w-screen sp:tw-mt-3">
          <span class="tw-mr-8">Tổng số bản ghi: {{ totalRecord }}</span>
          <label for="per_page" class="tw-mr-2">Số bản ghi mỗi page:</label>
          <select
            id="per_page"
            @change="getRecommenderList"
            v-model="pagination.rowsPerPage"
            class="tw-outline-none"
          >
            <option v-for="option in PERPAGE_OPTIONS" :key="option.id" :value="option">{{ option }}</option>
          </select>
        </div>
      </template>
      <!-- Search data ... -->
      <template v-slot:loadingLabel="{ message }">
        <div class="full-width row flex-center q-gutter-sm tw-text-sm tw-mt-1">
          {{ message }}
        </div>
      </template>
      <!-- Field name -->
      <template v-slot:body-cell-name="props">
        <q-td :props="props">
          <p class="tooltip tw-w-[180px] tw-text-ellipsis tw-overflow-hidden">
            {{ props.row.name }}
            <span class="tooltiptext">{{ props.row.name }}</span>
          </p>
        </q-td>
      </template>
      <!-- Field email -->
      <template v-slot:body-cell-email="props">
        <q-td :props="props">
          <p class="tooltip tw-w-[180px] tw-text-ellipsis tw-overflow-hidden">
            {{ props.row.email }}
            <span class="tooltiptext">{{ props.row.email }}</span>
          </p>
        </q-td>
      </template>
      <!-- Field email -->
      <template v-slot:body-cell-full_address="props">
        <q-td :props="props">
          <p class="tooltip tw-w-[180px] tw-text-ellipsis tw-overflow-hidden">
            {{ props.row.full_address }}
            <span class="tooltiptext">{{ props.row.full_address }}</span>
          </p>
        </q-td>
      </template>
      <template v-slot:body-cell-action="props">
        <q-td :props="props">
          <div>
            <q-btn color="green-7" @click="viewUser(props.row.employee_code)" size="12px"><q-icon name="visibility"></q-icon>Xem</q-btn>
            <q-btn color="red" @click="flagDelete=true, flagEdit=false, user.employee_code = props.row.employee_code,
              confirmPopup(
                MESSAGE.USER.DELETE.CONFIRM_TITLE, MESSAGE.USER.DELETE.CONFIRM_QUESTION + `<b>${props.row.fullname}</b>`, deleteUser
              )"
              size="12px" class="tw-ml-[5px]"><q-icon name="delete"></q-icon>Xóa</q-btn>
          </div>
        </q-td>
      </template>
      <template v-slot:no-data="{ message }">
        <div class="full-width row flex-center q-gutter-sm tw-text-sm tw-mt-1">
          {{ message }}
        </div>
      </template>
      <template v-slot:bottom></template>
    </q-table>
    <!-- Pagination -->
    <div
      class="q-pt-sm flex tw-justify-center"
    >
      <q-pagination
        v-if="pagination.totalPage > 1"
        v-model="pagination.page"
        :max="pagination.totalPage"
        color="grey"
        active-color="primary"
        boundary-numbers
      />
    </div>

  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { cloneDeep } from 'lodash';
import dayjs from 'utilities/day';
import { PAGINATION_DEFAULT, FORMAT_DATE, PERPAGE_OPTIONS } from 'utilities/const';
import { MESSAGE, ERROR } from 'utilities/message';
import toast from 'utilities/toast';
import { searchItems } from 'utilities/common';
import { useAuthStore } from 'stores/auth-store';
import userService from 'services/user.service';
import positionService from 'services/position.service';
import officeService from 'services/office.service';
import useValidate from '../../composables/validate.js';
import useMixin from '../../mixins/common.js';
import userSchema from '../../validations/schemas/user/user.js';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const userStore = useAuthStore().user;
// ==> 1.2) actions
// ==> 1.3) Others
const { confirmPopup } = useMixin();
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF, REACTIVE ========
const dialog = ref(false);
const flagEdit = ref(false);
const flagDelete = ref(false);
const rows = ref([]);
const totalRecord = ref(0);
const user = reactive({
  employee_code: '',
  fullname: '',
  email: '',
  telephone_no: '',
  position_id: 0,
  office_id: 0,
  date_issued_identification: '',
  identification_number: '',
  place_issued_identification: '',
  registered_date: '',
  full_address: '',
  birthday: '',
  gender: '',
});
const userAdd = reactive({
  employee_code: '',
  fullname: '',
  email: '',
  telephone_no: '',
  position: '',
  office: '',
});
const columns = ref([
  {
    name: 'serial',
    align: 'left',
    label: 'STT',
    field: 'serial',
    sortable: true,
  },
  {
    name: 'employee_code',
    align: 'left',
    label: 'Mã nhân viên',
    field: 'employee_code',
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
    field: 'gender_text',
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
    name: 'full_address',
    align: 'left',
    label: 'Quê quán ',
    field: 'full_address',
    sortable: true,
  },
  {
    name: 'office',
    align: 'left',
    label: 'Địa điểm làm việc',
    field: 'office',
    sortable: true,
  },
  {
    name: 'action',
    align: 'center',
    label: 'Hành động',
    field: 'action',
  },
]);
const records = ref([]);
const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: 1,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});
const dataSearch = reactive({
  search_key: '',
  column: '',
  advance: {
    position: '',
    office: '',
    gender_text: '',
  },
});
const listPosition = ref([]);
const listOffice = ref([]);
const loading = ref(true);

const qDateProxyBirth = ref();
const qDateProxyIdentity = ref();
const qDateProxyRegisted = ref();

// 3) ======= FUNCTION ========

// Function update pagination
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

// Reset data user
const resetDataUser = () => {
  // Show card
  errors.value = {};
  dialog.value = true;
  flagEdit.value = false;
  // Set value for user
  user.employee_code = '';
  user.fullname = '';
  user.gender = '';
  user.email = '';
  user.telephone_no = '';
  user.birthday = '';
  user.registered_date = '';
  user.date_issued_identification = '';
  user.identification_number = '';
  user.place_issued_identification = '';
  user.office_id = '';
  user.position_id = '';
  user.full_address = '';
};

// Get list user
const searchHandler = () => {
  rows.value = searchItems(dataSearch, records.value);
  totalRecord.value = rows.value.length;
  updatePaginate(rows.value.length);
};

// Reset search data
const resetSearch = () => {
  dataSearch.advance.position = '';
  dataSearch.advance.office = '';
  dataSearch.advance.gender_text = '';
  dataSearch.search_key = '';
  searchHandler();
};

// Close model
const onClose = () => {
  if (!flagDelete.value) {
    dialog.value = true;
  }
};

// Add user
const addUser = async () => {
  const isAddUser = await userService.add(user);
  if (isAddUser) {
    userAdd.employee_code = user.employee_code;
    userAdd.email = user.email;
    userAdd.fullname = user.fullname;
    userAdd.full_address = user.full_address;
    userAdd.telephone_no = user.telephone_no;
    userAdd.fullname = user.fullname;
    // Get office of user
    listOffice.value.forEach((office) => {
      if (office.id === Number(user.office_id)) {
        userAdd.office = office.name;
      }
    });
    // Get position of user
    listPosition.value.forEach((position) => {
      if (position.id === Number(user.position_id)) {
        userAdd.position = position.name;
      }
    });
    // Add user to records, rows
    const dataClone = cloneDeep(userAdd);
    records.value.unshift(dataClone);
    rows.value.unshift(dataClone);
    toast.success(MESSAGE.USER.ADD.SUCCESS);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.USER.ADD.ERROR);
};

// Call api edit user
const editUser = async () => {
  const isEditUser = await userService.edit(user);
  if (isEditUser) {
    // Update data to records
    records.value.forEach((row, index) => {
      if (row.employee_code === user.employee_code) {
        records.value[index].fullname = user.fullname;
        records.value[index].email = user.email;
        records.value[index].full_address = user.full_address;
        records.value[index].telephone_no = user.telephone_no;
        records.value[index].gender = user.gender;
        records.value[index].gender_text = '';
        if (parseInt(user.gender, 10) === 0) {
          records.value[index].gender_text = 'Nam';
        } else if (parseInt(user.gender, 10) === 1) {
          records.value[index].gender_text = 'Nữ';
        }
        listOffice.value.forEach((office) => {
          if (office.id === Number(user.office_id)) {
            records.value[index].office = office.name;
          }
        });
        listPosition.value.forEach((position) => {
          if (position.id === Number(user.position_id)) {
            records.value[index].position = position.name;
          }
        });
      }
    });
    // Update data to rows
    rows.value.forEach((row, index) => {
      if (row.employee_code === user.employee_code) {
        rows.value[index].fullname = user.fullname;
        rows.value[index].email = user.email;
        rows.value[index].full_address = user.full_address;
        rows.value[index].telephone_no = user.telephone_no;
        rows.value[index].gender = user.gender;
        rows.value[index].gender_text = '';
        if (parseInt(user.gender, 10) === 0) {
          rows.value[index].gender_text = 'Nam';
        } else if (parseInt(user.gender, 10) === 1) {
          rows.value[index].gender_text = 'Nữ';
        }
        listOffice.value.forEach((office) => {
          if (office.id === Number(user.office_id)) {
            rows.value[index].office = office.name;
          }
        });
        listPosition.value.forEach((position) => {
          if (position.id === Number(user.position_id)) {
            rows.value[index].position = position.name;
          }
        });
      }
    });
    toast.success(MESSAGE.USER.UPDATE.SUCCESS);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.USER.UPDATE.ERROR);
};

// Validate edit user
const validateEditUser = () => {
  if (!user.registered_date) {
    delete user.registered_date;
  }
  // Validate user
  const isValid = validate(userSchema, user);
  if (!user.registered_date) {
    user.registered_date = null;
  }
  if (!isValid) {
    return;
  }
  dialog.value = false;
  confirmPopup(
    MESSAGE.USER.UPDATE.CONFIRM_TITLE,
    `${MESSAGE.USER.UPDATE.CONFIRM_QUESTION}<b>${user.fullname}</b>`,
    editUser,
    onClose,
  );
};

// Validate user
const validateUser = () => {
  // Validate user
  errors.value = {};
  let isCheckEmployeeCode = false;
  rows.value.forEach((row) => {
    if (row.employee_code === user.employee_code) {
      isCheckEmployeeCode = true;
    }
  });
  if (!user.registered_date) {
    delete user.registered_date;
  }
  const isValid = validate(userSchema, user);
  if (!user.registered_date) {
    user.registered_date = null;
  }
  if (!isValid || errors.value.employee_code) {
    if (isCheckEmployeeCode) {
      errors.value.employee_code = ERROR.EMPLOYEE_CODE.EXISTS;
    }
    return;
  }
  dialog.value = false;
  confirmPopup(MESSAGE.USER.ADD.CONFIRM_TITLE, MESSAGE.USER.ADD.CONFIRM_QUESTION, addUser, onClose);
};

// View info user
const viewUser = async (employeeCode) => {
  errors.value = {};
  flagEdit.value = true;
  flagDelete.value = false;
  // Call api get info of user
  const infoUser = await userService.get(employeeCode);
  // Set value for user
  if (infoUser) {
    user.gender = infoUser.gender;
    user.employee_code = employeeCode;
    user.fullname = infoUser.fullname;
    user.email = infoUser.email;
    user.telephone_no = infoUser.telephone_no;
    user.birthday = dayjs(infoUser.birthday).format(FORMAT_DATE);
    user.registered_date = infoUser.registered_date ? dayjs(infoUser.registered_date).format(FORMAT_DATE) : '';
    user.date_issued_identification = dayjs(infoUser.date_issued_identification).format(FORMAT_DATE);
    user.identification_number = infoUser.identification_number;
    user.place_issued_identification = infoUser.place_issued_identification;
    user.office_id = infoUser.office_id;
    user.position_id = infoUser.position_id;
    user.full_address = infoUser.full_address;
    // Show card
    dialog.value = true;
  }
};

// Delete user
const deleteUser = async () => {
  // Call api delete user
  const delUser = await userService.delete(user.employee_code);
  if (delUser) {
    records.value = records.value.filter((row) => row.employee_code !== user.employee_code);
    user.employee_code = '';
    toast.success(MESSAGE.USER.DELETE.SUCCESS);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.USER.DELETE.ERROR);
};

// 4) ======= VUE JS LIFECYCLE ========
onMounted(async () => {
  const [listPositions, listOffices] = await Promise.all([
    positionService.getList(),
    officeService.getList(),
    userService.getList(),
  ]);
  // Get position
  listPosition.value = listPositions;
  listOffice.value = listOffices.list_office;
  listOffice.value.forEach((item) => {
    if (item.id === userStore.office_id) {
      dataSearch.advance.office = item.name;
    }
  });

  const listUser = await userService.getList(false);

  if (listUser) {
    records.value = cloneDeep(listUser.list_user);
    rows.value = searchItems(dataSearch, records.value);
    totalRecord.value = rows.value.length;
    updatePaginate(rows.value.length);
  }
  loading.value = false;
});

</script>

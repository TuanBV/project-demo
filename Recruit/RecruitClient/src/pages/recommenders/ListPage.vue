<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Người giới thiệu</h1>
    <q-btn color="green-7" @click="showAddDialogRecommender" class="tw-mt-4 sp:tw-text-xs" icon="add" label="Thêm người giới thiệu" />
    <!-- Dialog add recommender -->
    <q-dialog v-model="dialogAddOrEditRecommender" @hide="handleClearRecommenderAndErrors">
      <q-card class="tw-mt-[-120px]">
        <q-card-section class="row tw-align-center tw-bg-[#17a2b8]">
          <span class="tw-text-sm tw-text-white tw-text-[18px]">
            {{ recommenderId ? 'Cập nhật người giới thiệu' : 'Thêm người giới thiệu' }}
          </span>
        </q-card-section>
        <q-form @submit="addRecommender">
          <q-card-section class="row items-center">
            <div class="tw-flex tw-flex-col tw-justify-center tw-sm:tw-py-12">
              <div class="tw-relative tw-sm:tw-max-w-xl tw-sm:tw-mx-auto">
                <div class="tw-relative tw-bg-white tw-md:tw-mx-0 tw-sm:tw-p-10">
                  <div class="tw-max-w-md">
                    <div class="tw-divide-gray-200">
                      <div class="tw-text-base tw-leading-6 tw-text-gray-700 tw-sm:tw-text-lg tw-sm:tw-leading-7">
                        <div class="tw-flex tw-items-center tw-space-x-4 sp:tw-space-x-0 sp:tw-block">
                          <div class="tw-flex tw-flex-col tw-w-[250px]">
                            <label class="tw-leading-loose">Họ tên<span class="text-red">*</span></label>
                            <input
                              type="text"
                              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-full tw-border-gray-300 tw-rounded-md
                                tw-outline-0 tw-text-gray-600"
                              placeholder="Nhập đầy đủ họ tên"
                              v-model.trim="recommender.fullname"
                              :class="!errors.fullname && errors.email ? 'tw-mb-4' : ''"
                              @focusin="onFocusInput($event, true)"
                              @focusout="onFocusInput"
                            >
                            <span v-if="errors.fullname" class="text-red tw-text-xs">*{{ errors.fullname }}</span>
                          </div>
                          <div class="tw-flex tw-flex-col tw-w-[250px]">
                            <label class="tw-leading-loose">Email<span class="text-red">*</span></label>
                            <input
                              type="text"
                              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-full tw-border-gray-300 tw-rounded-md
                                tw-outline-0 tw-text-gray-600"
                              placeholder="Nhập địa chỉ mail"
                              v-model.trim="recommender.email"
                              :class="!errors.email && errors.fullname ? 'tw-mb-4' : ''"
                              @focusin="onFocusInput($event, true)"
                              @focusout="onFocusInput"
                            >
                            <span v-if="errors.email" class="text-red tw-text-xs">*{{ errors.email }}</span>
                          </div>
                        </div>
                        <div class="tw-flex tw-items-center tw-space-x-4 sp:tw-space-x-0 sp:tw-block">
                          <div class="tw-flex tw-flex-col tw-w-[250px]">
                            <label class="tw-leading-loose">Số điện thoại<span class="text-red">*</span></label>
                            <input
                              type="text"
                              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-full
                                tw-border-gray-300 tw-rounded-md
                                tw-outline-0 tw-text-gray-600"
                              placeholder="Nhập số điện thoại"
                              v-model.trim="recommender.telephone_no"
                              :class="!errors.telephone_no && errors.birthday ? 'tw-mb-4' : ''"
                              @focusin="onFocusInput($event, true)"
                              @focusout="onFocusInput"
                              maxlength="11"
                            >
                            <span v-if="errors.telephone_no" class="text-red tw-text-xs">
                              *{{ errors.telephone_no }}
                            </span>
                          </div>
                          <div class="tw-flex tw-flex-col tw-w-[250px]">
                            <label class="tw-block tw-leading-loose">Ngày sinh<span class="text-red">*</span></label>
                            <div
                              :class="!errors.birthday && errors.telephone_no ? 'tw-mb-4' : ''"
                              class="tw-pr-4 tw-pl-2 tw-py-[5px] tw-border tw-border-gray-300 tw-rounded-md
                                tw-focus:tw-outline-none tw-text-gray-600"
                            >
                              <input
                                id="birthday"
                                type="text"
                                class="tw-outline-0 tw-w-[90%]"
                                placeholder="Nhập ngày sinh"
                                v-model.trim="recommender.birthday"
                                @focusin="onFocusInput($event, true)"
                                @focusout="onFocusInput"
                              >
                              <q-icon name="event" class="cursor-pointer" size="xs">
                                <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                  <q-date :mask="FORMAT_DATE" v-model="recommender.birthday">
                                    <div class="row items-center justify-end">
                                      <q-btn v-close-popup label="Close" color="primary" flat />
                                    </div>
                                  </q-date>
                                </q-popup-proxy>
                              </q-icon>
                            </div>
                            <span v-if="errors.birthday" class="text-red tw-text-xs">*{{ errors.birthday }}</span>
                          </div>
                        </div>
                        <div class="tw-flex tw-flex-col">
                          <label class="tw-leading-loose">Địa chỉ liên hệ<span class="text-red">*</span></label>
                          <input
                            type="text"
                            class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-full
                              tw-border-gray-300 tw-rounded-md
                              tw-outline-0 tw-text-gray-600"
                            placeholder="Nhập địa chỉ liên hệ"
                            v-model.trim="recommender.full_address"
                            @focusin="onFocusInput($event, true)"
                            @focusout="onFocusInput"
                          >
                          <span v-if="errors.full_address" class="text-red tw-text-xs">
                            *{{ errors.full_address }}
                          </span>
                        </div>
                        <div class="tw-flex tw-flex-col">
                          <label class="tw-leading-loose">Nơi cấp CMT/CCCD<span class="text-red">*</span></label>
                          <input
                            type="text"
                            class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-full
                              tw-border-gray-300 tw-rounded-md
                              tw-outline-0 tw-text-gray-600"
                            placeholder="Nhập nơi cấp CMT/CCCD"
                            v-model.trim="recommender.place_issued_identification"
                            @focusin="onFocusInput($event, true)"
                            @focusout="onFocusInput"
                          >
                          <span v-if="errors.place_issued_identification" class="text-red tw-text-xs">
                            *{{ errors.place_issued_identification }}
                          </span>
                        </div>
                        <div class="tw-flex tw-flex-col">
                          <label class="tw-leading-loose">Số CMT/CCCD<span class="text-red">*</span></label>
                          <input
                            type="text"
                            class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-full
                              tw-border-gray-300 tw-rounded-md
                              tw-outline-0 tw-text-gray-600"
                            placeholder="Nhập số CMT/CCCD"
                            v-model.trim="recommender.identification_number"
                            @focusin="onFocusInput($event, true)"
                            @focusout="onFocusInput"
                            maxlength="12"
                          >
                          <span
                            v-if="errors.identification_number"
                            class="text-red tw-text-xs"
                          >*{{ errors.identification_number }}</span>
                        </div>
                        <div class="tw-flex tw-flex-col">
                          <label class="tw-block tw-leading-loose focus:tw-hidden">
                            Ngày cấp CMT/CCCD<span class="text-red">*</span>
                          </label>
                          <div
                            class="tw-pr-4 tw-pl-2 tw-py-[5px] tw-border tw-border-gray-300 tw-rounded-md
                              tw-focus:tw-outline-none tw-text-gray-600"
                          >
                            <input
                              id="date_issued_identification"
                              type="text"
                              class="tw-outline-0 tw-w-[95%]"
                              placeholder="Nhập ngày cấp CMT/CCCD"
                              v-model.trim="recommender.date_issued_identification"
                              @focusin="onFocusInput($event, true)"
                              @focusout="onFocusInput"
                            >
                            <q-icon name="event" class="cursor-pointer" size="xs">
                              <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                                <q-date :mask="FORMAT_DATE" v-model="recommender.date_issued_identification">
                                  <div class="row items-center justify-end">
                                    <q-btn v-close-popup label="Close" color="primary" flat />
                                  </div>
                                </q-date>
                              </q-popup-proxy>
                            </q-icon>
                          </div>
                          <span v-if="errors.date_issued_identification" class="text-red tw-text-xs">
                            *{{ errors.date_issued_identification }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </q-card-section>
          <!-- Notice v-close-popup -->
          <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
            <q-btn type="button" color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
            <q-btn
              class="bg-green-7 tw-w-[100px] tw-text-white"
              v-if="!recommenderId"
              label="Thêm"
              type="submit"
            />
            <q-btn
              v-else
              type="submit"
              class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white"
              @click="updateRecommender"
              label="Cập nhật"
            />
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
    <!-- List of recommender -->
    <q-table
      class="tw-mt-8 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      hide-pagination
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách người giới thiệu</span>
        <q-form
          class="tw-inline-block sp:tw-ml-0 tw-ml-10 tw-translate-y-px"
        >
          <q-input
            dense
            debounce="300"
            input-class="tw-py-0"
            v-model="dataSearch.search_key"
            placeholder="Tìm kiếm"
            @update:model-value="handleSearch"
          >
            <template v-slot:append>
              <q-btn @click="handleSearch" type="submit" dense unelevated round icon="search" />
            </template>
          </q-input>
        </q-form>
      </template>
      <!-- Choose perpage -->
      <template v-slot:top-right>
        <div class="sp:tw-w-screen sp:tw-mt-3">
          <span class="tw-mr-8 sp:tw-block">Tổng số bản ghi: {{ totalRecord }}</span>
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
      <!-- No data slot -->
      <template v-slot:no-data="{ message }">
        <div class="full-width row flex-center q-gutter-sm tw-text-sm tw-mt-1">
          {{ message }}
        </div>
      </template>
      <!-- Action field -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[240px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="green-7"
              icon="visibility"
              @click="viewRecommender(props.row)"
            >
              Xem
            </q-btn>
            <q-btn
              color="red"
              icon="delete"
              @click="showConfirmDialogDeleteRecommender(props.row)"
              class="tw-ml-3 tw-text-[12px] sp:tw-text-[10px]"
            >
              Xóa
            </q-btn>
          </div>
        </q-td>
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
import {
  onMounted,
  reactive,
  ref,
} from 'vue';
import recommenderService from 'services/recommender.service';
import { PAGINATION_DEFAULT, FORMAT_DATE, PERPAGE_OPTIONS } from 'utilities/const';
import dayjs from 'utilities/day';
import { searchItems } from 'utilities/common';
import { MESSAGE } from 'utilities/message';
import useMixin from 'mixins/common.js';
import useValidate from 'composables/validate';
import recommenderSchema from 'schemas/recommender';
import { cloneDeep } from 'lodash';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
// ==> 1.2) actions
// ==> 1.3) Others
const { confirmPopup } = useMixin();
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF ========
const dataSearch = reactive({
  search_key: '',
});
const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});
const recommender = reactive({
  fullname: '',
  email: '',
  telephone_no: '',
  birthday: '',
  full_address: '',
  place_issued_identification: '',
  identification_number: '',
  date_issued_identification: '',
});
const recommenderId = ref(0);
const columns = [
  {
    name: 'fullname',
    align: 'left',
    label: 'Họ tên',
    field: 'fullname',
    sortable: true,
  },
  {
    name: 'telephone_no',
    align: 'center',
    label: 'Số điện thoại',
    field: 'telephone_no',
    sortable: true,
  },
  {
    name: 'email',
    align: 'center',
    label: 'Email',
    field: 'email',
    sortable: true,
  },
  {
    name: 'birthday',
    align: 'center',
    label: 'Ngày sinh',
    field: 'birthday',
    sortable: true,
  },
  {
    name: 'full_address',
    align: 'center',
    label: 'Địa chỉ',
    field: 'full_address',
    sortable: true,
  },
  {
    name: 'identification_number',
    align: 'center',
    label: 'Số CCCD',
    field: 'identification_number',
    sortable: true,
  },
  {
    name: 'action',
    align: 'center',
    label: 'Hành động',
    field: 'action',
  },
];
const rows = ref([]);
const totalRecord = ref(0);
const dialogAddOrEditRecommender = ref(false);
const idInputsDate = ['birthday', 'date_issued_identification'];
let clearRecommender = true;
let records = [];

// 3) ======= METHOD/FUNCTION ========

/**
 * Handle clear recommender data and errors
 *
 * @return void
 */
const handleClearRecommenderAndErrors = () => {
  if (clearRecommender) {
    // Clear recommender variable
    recommender.fullname = '';
    recommender.email = '';
    recommender.telephone_no = '';
    recommender.birthday = '';
    recommender.full_address = '';
    recommender.place_issued_identification = '';
    recommender.identification_number = '';
    recommender.date_issued_identification = '';
    // Clear errors
    errors.value = {};
  }
};

/**
 * Handle update paginate
 *
 * @param int totalItem
 * @return void
 */
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

/**
 * Handle change per page
 *
 * @return void
 */
const changePerPage = () => {
  updatePaginate(rows.value.length);
};

/**
 * Handle search data
 *
 * @return void
 */
const handleSearch = () => {
  rows.value = searchItems(dataSearch, records);
  totalRecord.value = rows.value.length;
  updatePaginate(totalRecord.value);
};

/**
 * Handle get recommender list
 *
 * @return void
 */
const getRecommenderList = async () => {
  const data = await recommenderService.getList();
  if (data) {
    totalRecord.value = data.item.length;
    updatePaginate(totalRecord.value);
    data.item.map((item) => {
      item.birthday = dayjs(item.birthday).format(FORMAT_DATE);
      item.date_issued_identification = dayjs(item.date_issued_identification).format(FORMAT_DATE);
      return item;
    });
    records = cloneDeep(data.item);
    rows.value = cloneDeep(data.item);
  }
};

/**
 * Handle show dialog edit recommender
 *
 * @param object row
 * @return void
 */
const viewRecommender = (row) => {
  clearRecommender = true;
  recommender.birthday = row.birthday;
  recommender.date_issued_identification = row.date_issued_identification;
  recommender.email = row.email;
  recommender.full_address = row.full_address;
  recommender.fullname = row.fullname;
  recommender.identification_number = row.identification_number;
  recommender.place_issued_identification = row.place_issued_identification;
  recommender.telephone_no = row.telephone_no;
  recommenderId.value = row.id;
  // Show dialog edit recommender
  dialogAddOrEditRecommender.value = true;
};

/**
 * Handle show dialog add recommender
 *
 * @return void
 */
const showAddDialogRecommender = () => {
  recommenderId.value = 0;
  dialogAddOrEditRecommender.value = true;
};

/**
 * Handle show dialog add recommender
 *
 * @return void
 */
const comfirmAddRecommender = async () => {
  const dataRecommender = await recommenderService.add(recommender);
  recommenderId.value = 0;
  // Clear variable recommender
  clearRecommender = true;
  handleClearRecommenderAndErrors();
  // Add recommender to records
  records.unshift(dataRecommender);
  handleSearch();
};

/**
 * Handle show dialog add or edit recommender
 *
 * @return void
 */
const showDialogRecommender = () => {
  clearRecommender = true;
  dialogAddOrEditRecommender.value = true;
};

/**
 * Handle data validation and show dialog confirm add recommender
 *
 * @return void
 */
const addRecommender = () => {
  const isValid = validate(recommenderSchema, recommender);
  if (!isValid) {
    return;
  }
  clearRecommender = false;
  // Hide dialog add recommender
  dialogAddOrEditRecommender.value = false;
  // Show confirm popup add recommender
  confirmPopup(
    MESSAGE.RECOMMENDER.ADD.CONFIRM_TITLE,
    MESSAGE.RECOMMENDER.ADD.CONFIRM_QUESTION,
    comfirmAddRecommender,
    showDialogRecommender,
  );
};

/**
 * Handle delete recommender
 *
 * @return void
 */
const comfirmDeleteRecommender = async () => {
  const deleted = await recommenderService.delete(recommenderId.value);

  if (deleted) {
    // Delete recommender in rows, records
    rows.value = rows.value.filter((row) => row.id !== recommenderId.value);
    records = records.filter((row) => row.id !== recommenderId.value);
    recommenderId.value = 0;

    // Update paginate and total record
    updatePaginate(rows.value.length);
    totalRecord.value = rows.value.length;
  }
};

/**
 * On cancel dialog delete recommender
 *
 * @return void
 */
const onCancelDialogDeleteRecommender = () => {
  recommenderId.value = 0;
};

/**
 * Handle show confirm dialog delete recommender
 *
 * @param object row
 * @return void
 */
const showConfirmDialogDeleteRecommender = (row) => {
  recommenderId.value = row.id;
  confirmPopup(
    MESSAGE.RECOMMENDER.DELETE.CONFIRM_TITLE,
    MESSAGE.RECOMMENDER.DELETE.CONFIRM_QUESTION.replace(':fullname', row.fullname),
    comfirmDeleteRecommender,
    onCancelDialogDeleteRecommender,
  );
};

/**
 * Handle update recommender data
 *
 * @return void
 */
const comfirmUpdateRecommender = async () => {
  const edited = await recommenderService.edit(recommenderId.value, recommender);
  if (edited) {
    // Update data to data table
    rows.value.forEach((row, index) => {
      if (row.id === recommenderId.value) {
        rows.value[index].fullname = recommender.fullname;
        rows.value[index].email = recommender.email;
        rows.value[index].telephone_no = recommender.telephone_no;
        rows.value[index].birthday = recommender.birthday;
        rows.value[index].full_address = recommender.full_address;
        rows.value[index].place_issued_identification = recommender.place_issued_identification;
        rows.value[index].identification_number = recommender.identification_number;
        rows.value[index].date_issued_identification = recommender.date_issued_identification;
      }
    });

    // Update data to records
    records.forEach((row, index) => {
      if (row.id === recommenderId.value) {
        records[index].fullname = recommender.fullname;
        records[index].email = recommender.email;
        records[index].telephone_no = recommender.telephone_no;
        records[index].birthday = recommender.birthday;
        records[index].full_address = recommender.full_address;
        records[index].place_issued_identification = recommender.place_issued_identification;
        records[index].identification_number = recommender.identification_number;
        records[index].date_issued_identification = recommender.date_issued_identification;
      }
    });
    recommenderId.value = 0;
    // Clear variable recommender
    clearRecommender = true;
    handleClearRecommenderAndErrors();
  }
};

/**
 * Handle data validation and show dialog confirm update recommender
 *
 * @return void
 */
const updateRecommender = () => {
  const isValid = validate(recommenderSchema, recommender);
  if (!isValid) {
    return;
  }

  // hide dialog edit recommender
  dialogAddOrEditRecommender.value = false;
  clearRecommender = false;
  confirmPopup(
    MESSAGE.RECOMMENDER.UPDATE.CONFIRM_TITLE,
    MESSAGE.RECOMMENDER.UPDATE.CONFIRM_QUESTION.replace(':fullname', recommender.fullname),
    comfirmUpdateRecommender,
    showDialogRecommender,
  );
};

/**
 * Add or remove class when focus in or forcus out
 *
 * @param EventHTML event element
 * @param bool focus in
 *
 * @return void
 */
const onFocusInput = (event, focusIn = false) => {
  let element = event.target;
  if (idInputsDate.includes(element.id)) {
    element = element.parentElement;
  }

  if (focusIn) {
    element.classList.add('tw-border-sky-500', 'tw-outline-none');
  } else { // focusOut
    element.classList.remove('tw-border-sky-500', 'tw-outline-none');
  }
};

// 4) ======= VUEJS LIFECYCLE ========
onMounted(async () => {
  await getRecommenderList();
});
</script>

<template>
  <div class="q-pa-md">
    <div class="q-pa-md">
        <!-- Button add -->
      <q-btn icon="add" label="Thêm param" color="green-7" @click="flagEdit=false, flagDelete=false, clearParam()" />

      <!-- Dialog -->
      <q-dialog v-model="dialog" :full-height="false">
        <q-card class="tw-mt-[-120px]">
          <q-card-section class="row tw-align-center tw-bg-[#17a2b8!important]">
            <span class="tw-text-sm tw-text-white tw-text-[18px]">Thêm param mới</span>
          </q-card-section>

          <q-card-section class="row items-center">
            <div class="tw-flex tw-flex-col tw-justify-center tw-sm:tw-py-12">
              <div class="tw-relative tw-sm:tw-max-w-xl tw-sm:tw-mx-auto">
                <div class="tw-relative tw-bg-white tw-md:tw-mx-0 tw-sm:tw-p-10">
                  <div class="tw-max-w-md">
                    <div class="tw-divide-gray-200 tw-w-[300px]">
                      <div class="tw-flex-col tw-items-center">
                        <div class="tw-flex tw-flex-col">
                          <label class="tw-pl-[5px]">Tên param</label>
                          <input type="text" v-model="parameter.name"
                            class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-h-[36px]
                            tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600"
                            placeholder="Ten_param">
                          <span v-if="(errors.name)" class="text-red tw-text-xs">*{{ errors.name }}</span>
                        </div>
                        <div class="tw-flex tw-flex-col tw-mt-3">
                          <label class="tw-pl-[5px]">Chọn loại thông tin</label>
                          <div
                            class="tw-min-h-[36px!important]"
                          >
                          <select v-model="parameter.table"
                            @change="parameter.column = ''"
                            class="tw-bg-gray-50 tw-border tw-border-sky-500 tw-text-gray-900 tw-text-sm tw-rounded-lg
                            focus:tw-border-sky-500 tw-block tw-w-full tw-p-2.5 focus:tw-outline-none"
                          >
                            <option value="candidates">Thông tin ứng viên</option>
                            <option value="offices">Thông tin văn phòng</option>
                            <option value="meeting_rooms">Thông tin phòng họp</option>
                            <option value="interview_details">Thông tin buổi phỏng vấn</option>
                          </select>
                          </div>
                        </div>
                        <span v-if="(errors.table)" class="text-red tw-text-xs">*{{ errors.table }}</span>
                        <div class="tw-flex tw-flex-col tw-mt-3" v-if="(parameter.table == SELECT_OPTION.CANDIDATE)">
                          <label class="tw-pl-[5px]">Ứng viên</label>
                          <div
                            class="tw-min-h-[36px!important]"
                          >
                          <select v-model="parameter.column"
                            class="tw-bg-gray-50 tw-border tw-border-sky-500 tw-text-gray-900 tw-text-sm tw-rounded-lg
                            focus:tw-border-sky-500 tw-block tw-w-full tw-p-2.5 focus:tw-outline-none"
                          >
                            <option value="fullname">Họ tên</option>
                            <option value="email">Email</option>
                            <option value="birthday">Ngày sinh</option>
                            <option value="full_address">Địa chỉ</option>
                            <option value="place_issued_identification">Nơi cấp CCCD</option>
                            <option value="identification_number">Số CCCD</option>
                            <option value="date_issued_identification">Ngày cấp</option>
                            <option value="telephone_no">Số điện thoại</option>
                            <option value="application_date">Ngày ứng tuyển</option>
                            <option value="position_id">Tên vị trí</option>
                            <option value="team_id">Tên team</option>
                          </select>
                          </div>
                        </div>
                        <div class="tw-flex tw-flex-col tw-mt-3" v-if="(parameter.table === SELECT_OPTION.OFFICE)">
                          <label class="tw-pl-[5px]">Văn phòng</label>
                          <div
                            class="tw-min-h-[36px!important]"
                          >
                          <select v-model="parameter.column"
                            class="tw-bg-gray-50 tw-border tw-border-sky-500 tw-text-gray-900 tw-text-sm tw-rounded-lg
                            focus:tw-border-sky-500 tw-block tw-w-full tw-p-2.5 focus:tw-outline-none"
                          >
                            <option value="name">Tên văn phòng</option>
                            <option value="full_address">Địa chỉ văn phòng</option>
                            <option value="telephone_no">Số điện thoại</option>
                            <option value="mail_admin">Mail nhân sự</option>
                          </select>
                          </div>
                        </div>
                        <div class="tw-flex tw-flex-col tw-mt-3" v-if="(parameter.table === SELECT_OPTION.ROOM)">
                          <label class="tw-pl-[5px]">Phòng họp</label>
                          <div
                            class="tw-min-h-[36px!important]"
                          >
                          <select v-model="parameter.column"
                            class="tw-bg-gray-50 tw-border tw-border-sky-500 tw-text-gray-900 tw-text-sm tw-rounded-lg
                            focus:tw-border-sky-500 tw-block tw-w-full tw-p-2.5 focus:tw-outline-none"
                          >
                            <option value="name">Tên phòng họp</option>
                          </select>
                          </div>
                        </div>
                        <div class="tw-flex tw-flex-col tw-mt-3" v-if="(parameter.table === SELECT_OPTION.INTERVIEW)">
                          <label class="tw-pl-[5px]">Buổi phỏng vấn</label>
                          <div
                            class="tw-min-h-[36px!important]"
                          >
                          <select v-model="parameter.column"
                            class="tw-bg-gray-50 tw-border tw-border-sky-500 tw-text-gray-900 tw-text-sm tw-rounded-lg
                            focus:tw-border-sky-500 tw-block tw-w-full tw-p-2.5 focus:tw-outline-none"
                          >
                            <option value="employee_code">Nhân viên</option>
                            <option value="evaluate">Đánh giá</option>
                            <option value="comment">Nhận xét</option>
                          </select>
                          </div>
                        </div>
                        <span v-if="(errors.column && parameter.table)" class="text-red tw-text-xs">*{{ errors.column }}</span>
                        <div class="tw-flex tw-flex-col tw-mt-3">
                          <label class="tw-pl-[5px]">Ghi chú</label>
                          <textarea v-model="parameter.note"
                            class="tw-pr-4 tw-pl-2 tw-py-2 tw-border focus:tw-ring-gray-500 focus:tw-border-sky-500 tw-max-h-[150px] tw-min-h-[150px]
                            tw-w-full tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600">
                          </textarea>
                          <span v-if="(errors.note)" class="text-red tw-text-xs">*{{ errors.note }}</span>
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
            <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
            <q-btn class="tw-bg-[#28a745] tw-w-[100px] tw-text-white" v-if="!flagEdit" @click="validateParam()" label="Thêm"/>
            <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" v-if="flagEdit" @click="flagDelete=false, validateEditParam()" label="Cập nhật"/>
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>

    <!-- List of candidates -->
    <q-table
      title="Danh sách param"
      class="tw-mt-8 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      :loading="loading"
      loading-label="Đang tìm kiếm dữ liệu ..."
      hide-pagination
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách param</span>
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
      <template v-slot:body-cell-action="props">
        <q-td :props="props">
          <div>
            <q-btn color="green-7" @click.prevent="flagDelete = false, viewParam(props.row.id)" size="12px"><q-icon name="visibility"></q-icon>Xem</q-btn>
            <q-btn color="red" @click.prevent="flagDelete = true, parameter.id = props.row.id,
              confirmPopup(
                MESSAGE.PARAM.DELETE.CONFIRM_TITLE,
                `${MESSAGE.PARAM.DELETE.CONFIRM_QUESTION}<b>${parameter.name}</b>?`,
                deleteParam,
                onClose,
              )" size="12px" class="tw-ml-[5px]"><q-icon name="delete"></q-icon>Xóa</q-btn>
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
import { MESSAGE } from 'utilities/message';
import { searchItems } from 'utilities/common';
import toast from 'utilities/toast';
import paramService from 'services/parameter.service';
import useValidate from '../../composables/validate.js';
import useMixin from '../../mixins/common.js';
import { PAGINATION_DEFAULT, PERPAGE_OPTIONS, SELECT_OPTION } from '../../shared/utilities/const.js';
import parameterSchema from '../../validations/schemas/parameter/param.js';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
// ==> 1.2) actions
// ==> 1.3) Others
const { confirmPopup } = useMixin();
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF, REACTIVE ========
const dataSearch = reactive({
  search_key: '',
});
const dialog = ref(false);
const flagEdit = ref(false);
const flagDelete = ref(false);
const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: 1,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});
const parameter = reactive({
  id: 1,
  name: '',
  table: '',
  column: '',
  note: '',
  is_deleted: 0,
});
const columns = ref([
  {
    name: 'id',
    align: 'left',
    label: 'ID param',
    field: 'id',
    sortable: true,
  },
  {
    name: 'name',
    align: 'left',
    label: 'Tên param',
    field: 'name',
    sortable: true,
  },
  {
    name: 'note',
    align: 'left',
    label: 'Ghi chú',
    field: 'note',
  },
  {
    name: 'action',
    align: 'center',
    label: 'Hành động',
    field: 'action',
  },
]);
const rows = ref([]);
const records = ref([]);
const totalRecord = ref(0);
const loading = ref(true);

// 3) ======= FUNCTION ========
// Update pagination
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

// Get list param
const searchHandler = async () => {
  rows.value = searchItems(dataSearch, records.value);
  totalRecord.value = rows.value.length;
  updatePaginate(rows.value.length);
};

// Close model
const onClose = () => {
  if (!flagDelete.value) {
    dialog.value = true;
  }
};

// Add param new
const addParam = async () => {
  const addParameter = await paramService.add(parameter);
  if (addParameter) {
    toast.success(MESSAGE.PARAM.ADD.SUCCESS);
    const paramNew = cloneDeep(addParameter);
    // Add recommender to records
    records.value.push(paramNew);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.PARAM.ADD.ERROR);
};

// Validate when add param
const validateParam = () => {
  // Validate user
  const isValid = validate(parameterSchema, parameter);
  if (!isValid) {
    return;
  }
  dialog.value = false;
  confirmPopup(MESSAGE.PARAM.ADD.CONFIRM_TITLE, MESSAGE.PARAM.ADD.CONFIRM_QUESTION, addParam, onClose);
};

// Delete param
const deleteParam = async () => {
  const delParam = await paramService.delete(parameter.id);
  if (delParam) {
    records.value = records.value.filter((row) => row.id !== parameter.id);
    parameter.id = '';
    toast.success(MESSAGE.PARAM.DELETE.SUCCESS);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.PARAM.DELETE.ERROR);
};

// View info param
const viewParam = async (idParam) => {
  errors.value = {};
  const infoParam = await paramService.get(idParam);
  if (infoParam) {
    parameter.id = infoParam.id;
    parameter.name = infoParam.name;
    parameter.table = infoParam.table;
    parameter.column = infoParam.column;
    parameter.note = infoParam.note;
  }
  if (!flagDelete.value) {
    dialog.value = true;
    flagEdit.value = true;
  }
};

// Call api edit param
const updateParam = async () => {
  const editParam = await paramService.edit(parameter);
  if (editParam) {
    // Update data to records
    records.value.forEach((row, index) => {
      if (row.id === parameter.id) {
        records.value[index].name = parameter.name;
        records.value[index].note = parameter.note;
      }
    });
    toast.success(MESSAGE.PARAM.UPDATE.SUCCESS);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.PARAM.UPDATE.ERROR);
};

// Validate when edit param
const validateEditParam = () => {
  // Validate user
  const isValid = validate(parameterSchema, parameter);
  if (!isValid) {
    return;
  }
  dialog.value = false;
  confirmPopup(
    MESSAGE.PARAM.UPDATE.CONFIRM_TITLE,
    `${MESSAGE.PARAM.UPDATE.CONFIRM_QUESTION}<b>${parameter.name}</b>?`,
    updateParam,
    onClose,
  );
};

// Clear data when add param
const clearParam = async () => {
  // Reset parameter
  errors.value = {};
  parameter.id = '';
  parameter.name = '';
  parameter.column = '';
  parameter.table = '';
  parameter.note = '';
  dialog.value = true;
  flagEdit.value = false;
};

// 4) ======= VUEJS LIFECYCLE ========
onMounted(async () => {
  const listParams = await paramService.getList();
  if (listParams) {
    records.value = cloneDeep(listParams.list_param);
    rows.value = searchItems(dataSearch, records.value);
    totalRecord.value = rows.value.length;
    updatePaginate(rows.value.length);
  }
  loading.value = false;
});

</script>

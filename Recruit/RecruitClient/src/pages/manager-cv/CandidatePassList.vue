<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Danh sách ứng viên pass</h1>

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
              tw-py-1 tw-pl-1 tw-min-w-[100px]"
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

    <!-- Send mail -->
    <div class="tw-mt-5">
      <q-btn
        class="tw-mr-3"
        color="green-7"
        size="12px"
        @click.prevent="confirmCreateMail"
        :disable="rows.length === 0"
      >
        <q-icon name="add_box" class="tw-mr-2"/>
        Tạo mail
      </q-btn>
      <q-btn
        color="green-7"
        size="12px"
        @click.prevent="confirmSendMail"
        :disable="rows.length === 0"
      >
        Gửi mail
      </q-btn>
    </div>

    <!-- List of candidate -->
    <q-table
      class="tw-mt-5 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      loading-label="Đang tìm kiếm dữ liệu ..."
      :loading="loading"
      hide-pagination
      v-model:pagination="pagination"
      v-model:selected="candidateSelected"
      :rows="rows"
      :columns="columns"
      selection="multiple"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên cần gửi hướng dẫn</span>
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
      <!-- Address field -->
      <template v-slot:body-cell-full_address="props">
        <q-td :props="props" class="md:tw-max-w-[100px]">
          <div
            class="tw-text-[12px] tw-overflow-clip tw-max-w-[100px] tw-truncate"
          >
            {{ props.row.full_address }}
          </div>
        </q-td>
      </template>
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="green-7"
              v-if="props.row.id_template"
              @click.prevent="openModalMail(props)"
            >
              Xem trước mail
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

    <q-dialog v-model="modalMail">
      <q-card style="width: 1200px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Thông tin mail ứng viên {{ dataMail.name }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: max-content">
          <div class="sp:tw-mt-1 tw-flex sp:tw-block">
            <div class="tw-w-[10%] tw-inline-block sp:tw-w-full">
              <label class="tw-font-bold" for="name">Tiêu đề:</label>
            </div>
            <div class="tw-w-[90%] sp:tw-w-full tw-inline-block">
              <input
                type="text"
                id="title"
                class="tw-rounded-md tw-border tw-w-full tw-border-gray-300 tw-py-[3px] tw-pl-2 tw-inline
                  focus:tw-outline-none focus:tw-border-sky-500"
                placeholder="Nhập tiêu đề"
                v-model="dataMail.title"
              >
              <span v-if="(errors.title)" class="text-red tw-text-xs">*{{ errors.title }}</span>
            </div>
          </div>
          <div class="tw-mt-3">
            <div class="tw-w-[10%] tw-inline-block sp:tw-w-full">
              <label class="tw-font-bold" for="name">Người nhận:</label>
            </div>
            <input
              type="text"
              id="emailReciever"
              class="tw-rounded-md tw-border tw-border-gray-300 tw-bg-gray-300
                tw-py-[3px] tw-pl-2 tw-w-[50%] tw-inline sp:tw-w-[70%]" disabled
              placeholder="Email người nhận"
              v-model="dataMail.candidate_email"
            >
            <label for="cc" class="tw-ml-[50px] sp:tw-ml-3 tw-font-bold tw-cursor-pointer" @click.prevent="addEmailCc"
              :class="dataMail.list_email_cc.length >= limitEmailCc ? 'disabled' : ''">Thêm Cc</label>
          </div>
          <template v-for="(email, index) in dataMail.list_email_cc" :key="index">
            <div class="tw-mt-3">
              <div class="tw-w-[10%] tw-inline-block sp:tw-w-full">
                <label class="tw-font-bold" for="name">Người nhận Cc:</label>
              </div>
              <input
                type="email"
                id="name"
                class="tw-rounded-md tw-border tw-border-gray-300
                  tw-py-[3px] tw-pl-2 tw-w-[50%] tw-mr-5 sp:tw-w-[70%]
                  focus:tw-outline-none focus:tw-border-sky-500"
                v-model="dataMail.list_email_cc[index]"
                placeholder="emailcc@gmail.com"
              >
              <q-icon
                name="cancel"
                size="20px"
                class="tw-cursor-pointer"
                @click.prevent="removeEmailCc(index)"
              />
            </div>
          </template>
          <div class="tw-mt-5 tw-flex sp:tw-block">
            <div class="tw-w-[10%] sp:tw-w-full">
              <label class="tw-font-bold " for="name">Nội dung:</label>
            </div>
            <q-editor
              class="tw-rounded-[0.375rem] tw-w-[90%] sp:tw-w-full tw-min-h-[400px]"
              v-model="dataMail.body"
              :dense="$q.screen.lt.md"
              :definitions="{
                bold: {label: 'Bold', icon: null, tip: 'My bold tooltip'}
              }"
              :toolbar="[
                [
                  {
                    label: $q.lang.editor.align,
                    icon: $q.iconSet.editor.align,
                    fixedLabel: true,
                    list: 'only-icons',
                    options: ['left', 'center', 'right', 'justify']
                  },
                ],
                ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
                ['token', 'hr', 'link', 'custom_btn'],
                ['print', 'fullscreen'],
                [
                  {
                    label: $q.lang.editor.formatting,
                    icon: $q.iconSet.editor.formatting,
                    list: 'no-icons',
                    options: [
                      'p',
                      'h1',
                      'h2',
                      'h3',
                      'h4',
                      'h5',
                      'h6',
                      'code'
                    ]
                  },
                  {
                    label: $q.lang.editor.fontSize,
                    icon: $q.iconSet.editor.fontSize,
                    fixedLabel: true,
                    fixedIcon: true,
                    list: 'no-icons',
                    options: [
                      'size-1',
                      'size-2',
                      'size-3',
                      'size-4',
                      'size-5',
                      'size-6',
                      'size-7'
                    ]
                  },
                  {
                    label: $q.lang.editor.defaultFont,
                    icon: $q.iconSet.editor.font,
                    fixedIcon: true,
                    list: 'no-icons',
                    options: [
                      'default_font',
                      'arial',
                      'arial_black',
                      'comic_sans',
                      'courier_new',
                      'impact',
                      'lucida_grande',
                      'times_new_roman',
                      'verdana'
                    ]
                  },
                  'removeFormat'
                ],
                ['quote', 'unordered', 'ordered', 'outdent', 'indent'],

                ['undo', 'redo'],
                ['viewsource']
              ]"
              :fonts="{
                arial: 'Arial',
                arial_black: 'Arial Black',
                comic_sans: 'Comic Sans MS',
                courier_new: 'Courier New',
                impact: 'Impact',
                lucida_grande: 'Lucida Grande',
                times_new_roman: 'Times New Roman',
                verdana: 'Verdana'
              }"
            />
          </div>
        </q-card-section>
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn class="tw-w-[100px] tw-text-white tw-bg-[#ff9800]" @click.prevent="openModalConfirmSaveMail()" label="Lưu"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems } from 'utilities/common';
import { MESSAGE, WARNING, SUCCESS } from 'utilities/message';
import { PAGINATION_DEFAULT, PERPAGE_OPTIONS, GENDER } from 'utilities/const';
import { cloneDeep } from 'lodash';
import { useAuthStore } from 'stores/auth-store';
import ToastUtil from 'utilities/toast';
import teamService from 'services/team.service';
import positionService from 'services/position.service';
import candidatePassListService from 'services/candidate-pass-list.service';
import officeService from 'services/office.service';
import useValidate from '../../composables/validate.js';
import templateCandidatePassSchema from '../../validations/schemas/candidate/candidate_pass_list.js';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others

const { confirmPopup, countRecord } = useMixin();
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF ========

const modalMail = ref(false);
const idsSelected = ref([]);
const allSelected = ref(false);
const loading = ref(true);
const candidateSelected = ref([]);

const dataSearch = reactive({
  advance: {
    position: '',
    team: '',
    gender: '',
  },
  search_key: '',
});

const dataMail = reactive({
  id: null,
  title: '',
  body: '',
  candidate_id: null,
  candidate_email: '',
  list_email_cc: [],
});

const limitEmailCc = ref(3);

const columns = [
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
    name: 'birthday',
    align: 'left',
    label: 'Ngày sinh',
    field: 'birthday',
    sortable: false,
  },
  {
    name: 'full_address',
    align: 'left',
    label: 'Địa chỉ',
    field: 'full_address',
    sortable: false,
  },
  {
    name: 'start_join_date',
    align: 'left',
    label: 'Ngày đi làm dự kiến',
    field: 'start_join_date',
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
const records = ref([]);
const listIdCandidateSend = ref([]);
// 3) ======= METHOD/FUNCTION ========
// Update paginate
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

// Open modal edit mail
const openModalMail = (data) => {
  modalMail.value = true;
  dataMail.candidate_email = data.row.email;
  dataMail.list_email_cc = data.row.list_email_cc ? data.row.list_email_cc : [];
  dataMail.id = data.row.id_template;
  dataMail.title = data.row.title;
  dataMail.body = data.row.body;
  dataMail.candidate_id = data.row.id;
};

// Create mail
const createMail = async () => {
  const candidateChoose = [];
  candidateSelected.value.forEach((candidate) => {
    candidateChoose.push(candidate.id);
  });
  const resultMail = await candidatePassListService.addMail({ list_id_candidate: candidateChoose });
  resultMail.mails.forEach((mail) => {
    rows.value.forEach((row) => {
      if (row.id === mail.candidate_id) {
        row.title = mail.title;
        row.body = mail.body;
        row.id_template = mail.id;
        row.status = [];
      }
    });
    records.value.forEach((record) => {
      if (record.id === mail.candidate_id) {
        record.title = mail.title;
        record.body = mail.body;
        record.id_template = mail.id;
        record.status = mail.status;
        record.list_email_cc = [];
      }
    });
  });
  ToastUtil.success(SUCCESS.CREATE_FORM);
};

// Open modal confirm create mail
const confirmCreateMail = () => {
  let flagStopCreateMail = false;
  if (candidateSelected.value.length > 0) {
    candidateSelected.value.forEach((candidate) => {
      if (candidate.id_template) {
        flagStopCreateMail = true;
      }
    });
    if (flagStopCreateMail) {
      ToastUtil.warning(WARNING.SELECTED);
      return;
    }

    confirmPopup(MESSAGE.RESULT.CREATE_MAIL.CONFIRM_TITLE, MESSAGE.RESULT.CREATE_MAIL.CONFIRM_QUESTION, createMail);
    return;
  }
  ToastUtil.warning(WARNING.NOT_SELECTED);
};

// Send mail
const sendMail = async () => {
  const resultSend = await candidatePassListService.sendMail({ list_id_candidate: listIdCandidateSend.value });
  if (resultSend) {
    rows.value = rows.value.filter((row) => !listIdCandidateSend.value.includes(row.id));
    totalRecord.value = rows.value.length;
    updatePaginate(rows.value.length);
    candidateSelected.value = [];
    // Toast message success
    ToastUtil.success(SUCCESS.SEND_MAIL);
    // Update count record of menu
    countRecord();
  }
};

// Open modal confirm send mail
const confirmSendMail = () => {
  let flagStopSendMail = false;
  listIdCandidateSend.value = [];
  candidateSelected.value.forEach((candidate) => {
    listIdCandidateSend.value.push(candidate.id);
    if (!candidate.id_template) {
      flagStopSendMail = true;
    }
  });
  if (flagStopSendMail) {
    ToastUtil.warning(WARNING.CREATE_MAIL);
    return;
  }
  if (candidateSelected.value.length === 0) {
    ToastUtil.warning(WARNING.NOT_SELECTED);
    return;
  }

  confirmPopup(MESSAGE.RESULT.SEND_MAIL.CONFIRM_TITLE, MESSAGE.RESULT.SEND_MAIL.CONFIRM_QUESTION, sendMail);
};

// Save mail
const saveMail = async () => {
  const updateMail = await candidatePassListService.editMail(dataMail);
  if (updateMail) {
    rows.value.forEach((row) => {
      if (row.id === updateMail.candidate_id) {
        row.title = updateMail.title;
        row.body = updateMail.body;
        row.list_email_cc = updateMail.carbon_copy;
      }
    });
    records.value.forEach((record) => {
      if (record.id === updateMail.candidate_id) {
        record.title = updateMail.title;
        record.body = updateMail.body;
        record.list_email_cc = updateMail.carbon_copy;
      }
    });

    ToastUtil.success(MESSAGE.CANDIDATE.UPDATE.SUCCESS);

    return;
  }
  ToastUtil.errors(MESSAGE.CANDIDATE.UPDATE.ERROR);
};

// Reopen modal save mail
const reOpenModalSaveMail = () => {
  modalMail.value = true;
};

// Open modal confirm save mail offer
const openModalConfirmSaveMail = () => {
  errors.value = [];
  const isValid = validate(templateCandidatePassSchema, dataMail);
  if (!isValid) {
    return;
  }
  modalMail.value = false;
  confirmPopup(MESSAGE.RESULT.SAVE_MAIL.CONFIRM_TITLE, MESSAGE.RESULT.SAVE_MAIL.CONFIRM_QUESTION, saveMail, reOpenModalSaveMail);
};

// Add email Cc
const addEmailCc = () => {
  if (dataMail.list_email_cc.length < limitEmailCc.value) {
    dataMail.list_email_cc.push('');
  }
};

// Remove email Cc
const removeEmailCc = (index) => {
  dataMail.list_email_cc.splice(index, 1);
};

// Change page
const changePerPage = () => {
  updatePaginate(rows.value.length);
};

// Search data
const searchHandle = () => {
  idsSelected.value = [];
  allSelected.value = false;
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

// 4) ======= VUEJS LIFECYCLE ========
onMounted(async () => {
  const [dataOffices, listPositions, listTeams] = await Promise.all([
    officeService.getList(),
    positionService.getList(),
    teamService.getList(),
  ]);
  // Get position
  listPosition.value = listPositions;
  listTeam.value = listTeams;
  listOffice.value = dataOffices.list_office;
  listOffice.value.forEach((item) => {
    if (item.id === user.office_id) {
      dataSearch.advance.office = item.name;
    }
  });

  const listCandidates = await candidatePassListService.getList(false);

  if (listCandidates) {
    records.value = cloneDeep(listCandidates.item);
    rows.value = searchItems(dataSearch, records.value);
    searchHandle();
    totalRecord.value = rows.value.length;
    updatePaginate(rows.value.length);
  }
  loading.value = false;
});

</script>

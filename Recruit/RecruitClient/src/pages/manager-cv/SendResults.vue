<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Gửi kết quả</h1>

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

    <!-- Send mail -->
    <div class="tw-mt-5 tw-flex tw-items-center">
      <q-btn
        class="tw-mr-3 tw-h-fit"
        color="green-7"
        size="13px"
        @click="confirmCreateMail"
        :disable="rows.length === 0"
      >
        <q-icon name="add_box" class="tw-mr-2"/>
        Tạo mail
      </q-btn>
      <q-btn
        color="green-7 tw-h-fit"
        size="13px"
        @click="confirmSendMail"
        :disable="rows.length === 0"
      >
        Gửi mail
      </q-btn>
      <q-select
        outlined
        @update:model-value="changeList"
        v-model="showListOffer"
        :options="optionGetList"
        label="Tùy chọn lấy danh sách"
        emit-value
        map-options
        class="tw-w-[250px] tw-ml-auto"
      />
    </div>

    <!-- List of candidate -->
    <q-table
      selection="multiple"
      class="tw-mt-5 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      loading-label="Đang tìm kiếm dữ liệu ..."
      hide-pagination
      v-model:pagination="pagination"
      v-model:selected="candidatesSelected"
      :rows="rows"
      :columns="columns"
      :loading="loading"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">
          Danh sách ứng viên
        </span>
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
        <q-td :props="props" class="md:tw-w-[150px]">
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
      <!-- Column action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-if="props.row.mail_id">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="green-7"
              @click="openModalMail(props.row)"
            >
              Xem truớc mail
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
        <span v-if="candidatesSelected.length > 0">{{ candidatesSelected.length }} bản ghi được chọn</span>
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
      <q-card style="width: 950px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Thông tin mail ứng viên {{ dataMail.name }}</div>
          <q-space />
        </q-card-section>

        <q-form @submit="openModalConfirmSaveMail">
          <q-card-section style="width: 100%; height: max-content">
            <div class="sp:tw-mt-1 tw-flex">
              <div class="tw-w-[120px] tw-text-right tw-inline-block tw-mr-8">
                <label class="tw-font-bold" for="name">Tiêu đề:<span class="text-red">*</span></label>
              </div>
              <div class="tw-w-[56%]">
                <input
                  type="text"
                  id="title"
                  class="tw-rounded-md tw-border tw-border-gray-300
                    tw-py-[3px] tw-pl-2 tw-inline tw-w-full
                    focus:tw-outline-none focus:tw-border-sky-500"
                  placeholder="Nhập tiêu đề"
                  v-model="dataMail.title"
                >
                <span v-if="errors.title" class="text-red tw-text-xs tw-block">*{{ errors.title }}</span>
              </div>
            </div>
            <div class="tw-mt-3 tw-flex">
              <div class="tw-w-[120px] tw-text-right tw-inline-block tw-mr-8">
                <label class="tw-font-bold" for="name">Người nhận:<span class="text-red">*</span></label>
              </div>
              <div class="tw-w-[56%]">
                <input
                  type="text"
                  id="emailReciever"
                  class="tw-rounded-md tw-border tw-border-gray-300
                    tw-py-[3px] tw-pl-2 tw-w-[60%] tw-inline
                    focus:tw-outline-none focus:tw-border-sky-500"
                  placeholder="Email người nhận"
                  readonly
                  :value="dataMail.candidate_email"
                >
                <label for="cc" class="tw-ml-[50px] tw-font-bold tw-cursor-pointer" @click.prevent="addEmailCc"
                  :class="dataMail.carbon_copy.length >= limitEmailCc ? 'disabled' : ''">Thêm Cc</label>
                <span v-if="errors.candidate_email" class="text-red tw-text-xs tw-block">*{{ errors.candidate_email }}</span>
              </div>
            </div>
            <template v-for="(_, index) in dataMail.carbon_copy" :key="index">
              <div class="tw-mt-3 tw-flex">
                <div class="tw-w-[120px] tw-text-right tw-inline-block tw-mr-8">
                  <label class="tw-font-bold" for="name">Người nhận Cc:<span class="text-red">*</span></label>
                </div>
                <div class="tw-w-[56%]">
                  <input
                    type="text"
                    id="name"
                    class="tw-rounded-md tw-border tw-border-gray-300
                      tw-py-[3px] tw-pl-2 tw-w-[60%] tw-mr-5
                      focus:tw-outline-none focus:tw-border-sky-500"
                    v-model="dataMail.carbon_copy[index]"
                    placeholder="Email người nhận Cc"
                  >
                  <q-icon
                    name="cancel"
                    size="20px"
                    class="tw-cursor-pointer"
                    @click.prevent="removeEmailCc(index)"
                  />
                  <span v-if="errors[`receiver_cc${index}`]" class="text-red tw-text-xs tw-block">*{{ errors[`receiver_cc${index}`] }}</span>
                </div>
              </div>
            </template>
            <div class="tw-mt-5 tw-flex">
              <div class="tw-w-[120px] tw-text-right tw-mr-8">
                <label class="tw-font-bold " for="name">Nội dung:<span class="text-red">*</span></label>
              </div>
              <div>
                <q-editor
                  class="tw-rounded-[0.375rem] tw-w-[750px] tw-min-h-[400px]"
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
                <span v-if="errors.body" class="text-red tw-text-xs tw-block">*{{ errors.body }}</span>
              </div>
            </div>
            <div class="tw-mt-5 tw-flex">
              <div class="tw-w-[120px] tw-text-right tw-inline-block tw-mr-8">
                <label class="tw-font-bold" for="attach_file">File đính kèm:<span class="text-red">*</span></label>
              </div>
              <div class="tw-w-[56%]">
                <template v-if="(typeof dataMail.attach_file === 'string')">
                  <a
                    :href="dataMail.attach_file"
                    target="_blank"
                    class="tw-text-sky-600 tw-cursor-pointer hover:tw-underline hover:tw-underline-offset-1"
                  >{{ dataMail.attach_file_name }}</a>
                  <q-icon
                    name="cancel"
                    size="20px"
                    class="tw-cursor-pointer tw-ml-2"
                    @click="removeAttachFile"
                  />
                </template>
                <template v-else>
                  <input type="file" id="attach_file" class="tw-border-gray-300
                    sp:tw-w-[160px] tw-w-[280px] focus:tw-outline-none focus:tw-border-sky-500"
                    accept="application/pdf"
                    @change="chooseFile"
                  >
                  <span v-if="errors.attach_file" class="text-red tw-text-xs tw-block">*{{ errors.attach_file }}</span>
                </template>
              </div>
            </div>
          </q-card-section>
          <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
            <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup/>
            <q-btn type="submit" class="tw-w-[100px] tw-bg-[#ff9800] tw-text-white" label="Lưu"/>
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <!-- Modal preview mail -->
    <q-dialog v-model="modalPreviewMail" @hide="onCloseModalPreviewMail">
      <q-card style="width: 950px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">
            Thông tin mail gửi mời phỏng vấn cho các ứng viên
          </div>
          <q-space />
        </q-card-section>

        <q-card-section
          v-for="(mail, index) in mails"
          :key="mail.id"
          class="tw-w-full tw-text-gray-700"
          :class="index % 2 !== 0 ? 'tw-bg-[whitesmoke]' : ''"
        >
          <table class="tw-w-full">
            <tbody>
              <tr>
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Họ tên:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">{{ mail.fullname }}</td>
              </tr>
              <tr>
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Tiêu đề:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">{{ mail.title }}</td>
              </tr>
              <tr>
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Người nhận:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">{{ mail.email }}</td>
              </tr>
              <tr v-if="mail.carbon_copy && mail.carbon_copy.length > 0">
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Đồng kính gửi:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">
                  <template v-for="(item, index) in mail.carbon_copy" :key="index">
                    {{ item }}<template v-if="mail.carbon_copy.length > index + 1">, </template>
                  </template>
                </td>
              </tr>
              <tr>
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Nội dung:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2" v-html="mail.body"></td>
              </tr>
              <tr v-if="(typeof mail.attached_file === 'string')">
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">File đính kèm:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">
                  <a
                    :href="mail.attached_file"
                    target="_blank"
                    class="tw-text-sky-600 tw-cursor-pointer hover:tw-underline hover:tw-underline-offset-1"
                  >{{ mail.attached_file_name }}</a>
                </td>
              </tr>
            </tbody>
          </table>
        </q-card-section>
        <!-- Button bottom -->
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup/>
          <q-btn
            class="bg-green-7 tw-w-[100px] tw-text-white"
            @click="sendMail"
            label="Gửi mail"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { searchItems, setDataFile } from 'utilities/common';
import { MESSAGE } from 'utilities/message';
import { PAGINATION_DEFAULT, PERPAGE_OPTIONS, GENDER } from 'utilities/const';
import { cloneDeep } from 'lodash';
import { useAuthStore } from 'stores/auth-store';
import candidateService from 'services/candidate.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';
import mailService from 'services/mail.service';
import candidateMailSchema from 'schemas/mail/candidate-mail';
import useValidate from 'composables/validate';
import ToastUtil from 'utilities/toast';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others
const { errors, validate } = useValidate();

const { confirmPopup, countRecord } = useMixin();

// 2) ======= VARIABLE REF ========
const showListOffer = ref(0);
const modalMail = ref(false);
const modalPreviewMail = ref(false);
const candidatesSelected = ref([]);
const loading = ref(true);

const mails = ref([]);

const optionGetList = [
  {
    label: 'Tất cả',
    value: 0,
  },
  {
    label: 'Danh sách ứng viên đã trượt',
    value: 1,
  },
  {
    label: 'Danh sách offer ứng viên',
    value: 2,
  },
];

const dataSearch = reactive({
  search_key: '',
  advance: {
    position_id: '',
    team_id: '',
    office: '',
    gender: '',
  },
});

const dataMail = reactive({
  id: null,
  title: '',
  body: '',
  carbon_copy: [],
  attach_file: {
    file: '',
    file_name: '',
    file_size: '',
    file_ext: '',
  },
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

// Search data
const searchHandle = () => {
  rows.value = searchItems(dataSearch, records);
  totalRecord.value = rows.value.length;
  updatePaginate(totalRecord.value);
};

// Open modal edit mail
const openModalMail = (row) => {
  modalMail.value = true;
  dataMail.id = row.mail_id;
  dataMail.title = row.title;
  dataMail.body = row.body;
  dataMail.candidate_email = row.email;
  dataMail.carbon_copy = row.carbon_copy ? cloneDeep(row.carbon_copy) : [];
  if (row.attached_file) {
    dataMail.attach_file = row.attached_file;
    dataMail.attach_file_name = row.attached_file_name;
  } else {
    dataMail.attach_file = {
      file: '',
      file_name: '',
      file_size: '',
      file_ext: '',
    };
  }
};

// Reset search data
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.advance.position_id = '';
  dataSearch.advance.team_id = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

/**
 * Handle create mail
 */
const handleCreateMail = async () => {
  const candidatesId = [];
  candidatesSelected.value.forEach((candidate) => {
    candidatesId.push(candidate.id);
  });

  const newMails = await candidateService.createResultMails(candidatesId);
  if (newMails) {
    records.map((record) => {
      newMails.forEach((mail) => {
        if (record.id === mail.candidate_id) {
          record.title = mail.title;
          record.body = mail.body;
          record.mail_id = mail.id;
        }
      });
      return record;
    });

    rows.value.map((row) => {
      newMails.forEach((mail) => {
        if (row.id === mail.candidate_id) {
          row.title = mail.title;
          row.body = mail.body;
          row.mail_id = mail.id;
        }
      });
      return row;
    });
  }
  searchHandle();
};

// Open modal confirm create mail
const confirmCreateMail = () => {
  const mailsName = [];
  if (candidatesSelected.value.length > 0) {
    let createMail = true;
    candidatesSelected.value.forEach((candidate) => {
      if (!candidate.mail_id) {
        mailsName.push(`<b>${candidate.fullname}</b>`);
      } else {
        createMail = false;
      }
    });

    if (createMail) {
      confirmPopup(
        MESSAGE.MAIL.CREATE.CONFIRM_TITLE,
        MESSAGE.MAIL.CREATE.CONFIRM_QUESTION.replace(':candidates', mailsName.join(', ')),
        handleCreateMail,
      );
    } else {
      ToastUtil.warning(MESSAGE.MAIL.CREATE.NOT_ALLOW);
    }
  }
};

// Send mail
const sendMail = async () => {
  const candidateIds = [];
  mails.value.forEach((mail) => {
    candidateIds.push(mail.id);
  });
  modalPreviewMail.value = false;
  const sent = await candidateService.sendMails(candidateIds);
  if (sent) {
    // Delete candidate in rows, records
    rows.value = rows.value.filter((row) => !candidateIds.includes(row.id));
    records = records.filter((row) => !candidateIds.includes(row.id));
    totalRecord.value = rows.value.length;
    updatePaginate(totalRecord.value);
    // Update count record of menu
    countRecord();
    candidatesSelected.value = [];
  }
};

// Open modal confirm send mail
const confirmSendMail = () => {
  if (candidatesSelected.value.length > 0) {
    let allowSendMail = true;
    mails.value = [];
    candidatesSelected.value.forEach((candidate) => {
      if (candidate.mail_id) {
        mails.value.push(candidate);
      } else {
        allowSendMail = false;
      }
    });

    if (allowSendMail) {
      modalPreviewMail.value = true;
    } else {
      ToastUtil.warning(MESSAGE.MAIL.SEND.NOT_ALLOW);
    }
  }
};

/**
 * Close modal confirm update mail
 */
const closeModalConfirmUpdateMail = () => {
  modalMail.value = true;
};

/**
 * Handle update mail
 */
const handleUpdateMail = async () => {
  const mail = {
    title: dataMail.title,
    body: dataMail.body,
    carbon_copy: dataMail.carbon_copy,
  };

  if ((typeof dataMail.attach_file === 'object' && dataMail.attach_file.file) || typeof dataMail.attach_file === 'string') {
    mail.attach_file = dataMail.attach_file;
  }

  const newMail = await mailService.update(dataMail.id, mail);
  if (newMail) {
    rows.value.forEach((row, index) => {
      if (row.mail_id === dataMail.id) {
        rows.value[index].title = dataMail.title;
        rows.value[index].body = dataMail.body;
        rows.value[index].carbon_copy = dataMail.carbon_copy ?? [];
        if (newMail.attached_file) {
          rows.value[index].attached_file = newMail.attached_file;
          rows.value[index].attached_file_name = newMail.attached_file_name;
        } else {
          rows.value[index].attached_file = {
            file: '',
            file_name: '',
            file_size: '',
            file_ext: '',
          };
        }
      }
    });

    // Update data to records
    records.forEach((record, index) => {
      if (record.mail_id === dataMail.id) {
        records[index].title = dataMail.title;
        records[index].body = dataMail.body;
        records[index].carbon_copy = dataMail.carbon_copy ?? [];
        if (newMail.attached_file) {
          records[index].attached_file = newMail.attached_file;
          records[index].attached_file_name = newMail.attached_file_name;
        } else {
          records[index].attached_file = {
            file: '',
            file_name: '',
            file_size: '',
            file_ext: '',
          };
        }
      }
    });

    // Update count record of menu
    countRecord();
  }
};

/**
 * Extract text html to normal text
 * @param string text html
 * @example extractContent('<p>Hello word</p>') -> Hello word
 * @return string Normal text
 */
const extractContent = (string) => {
  const span = document.createElement('span');
  span.innerHTML = string;
  const content = span.textContent || span.innerText;
  span.remove();
  return content;
};

// Open modal confirm save mail offer
const openModalConfirmSaveMail = () => {
  const mail = {
    title: dataMail.title,
    candidate_email: dataMail.candidate_email,
    body: extractContent(dataMail.body),
  };
  dataMail.carbon_copy.forEach((email, index) => {
    mail[`receiver_cc${index}`] = email;
  });

  if (dataMail.attach_file.file) {
    mail.attach_file = dataMail.attach_file;
  }

  const isValid = validate(candidateMailSchema, mail);
  if (!isValid) {
    return;
  }
  modalMail.value = false;
  confirmPopup(MESSAGE.RESULT.SAVE_MAIL.CONFIRM_TITLE, MESSAGE.RESULT.SAVE_MAIL.CONFIRM_QUESTION, handleUpdateMail, closeModalConfirmUpdateMail);
};

// Add email Cc
const addEmailCc = () => {
  dataMail.carbon_copy.push('');
};

// Remove email Cc
const removeEmailCc = (index) => {
  dataMail.carbon_copy.splice(index, 1);
};

const onCloseModalPreviewMail = () => {
  mails.value = [];
};

// Handle change list of candidates
const changeList = async (listOption) => {
  candidatesSelected.value = [];
  mails.value = [];
  const candidates = await candidateService.getInterviewedCandidates(listOption);
  if (candidates) {
    totalRecord.value = candidates.length;
    updatePaginate(totalRecord.value);
    records = cloneDeep(candidates);
    rows.value = cloneDeep(candidates);
    searchHandle();
  }
};

// Handle choose attach file
const chooseFile = (e) => {
  const reader = new FileReader();
  const file = e.target.files[0];
  reader.onload = (event) => {
    const dataFile = setDataFile(file, event.target.result);
    dataMail.attach_file.file_size = dataFile.size;
    dataMail.attach_file.file_name = dataFile.filename;
    dataMail.attach_file.file_ext = dataFile.ext;
    dataMail.attach_file.file = dataFile.name;
  };
  reader.readAsDataURL(file);
};

// Handle remove attach file
const removeAttachFile = () => {
  dataMail.attach_file = {
    file: '',
    file_name: '',
    file_size: '',
    file_ext: '',
  };
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  const [dataOffices, candidates, positions, teams] = await Promise.all([
    officeService.getList(),
    candidateService.getInterviewedCandidates(),
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

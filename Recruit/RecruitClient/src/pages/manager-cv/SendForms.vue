<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Gửi link form</h1>

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
          @click="resetSearch"
        >
          Đặt lại
        </button>
      </div>
    </div>

    <!-- Send mail -->
    <div class="tw-mt-5">
      <q-btn
        class="tw-mr-3 tw-h-fit"
        color="green-7"
        size="13px"
        @click="confirmCreateMail"
        :disable="rows.length === 0"
      >
        <q-icon name="add_box" class="tw-mr-2"/>
        Tạo mail form
      </q-btn>
      <q-btn
        color="green-7"
        size="12px"
        @click="confirmSendMail"
      >
        Gửi link form
      </q-btn>
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
      selection="multiple"
      v-model:selected="candidatesSelected"
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên đã nhận offer</span>
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
            hover:tw-underline-offset-1" @click="openModalCv(props)">{{ props.row.fullname }}</p>
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
        <q-td :props="props" :class="props.row.mail_id ? 'md:tw-w-[350px]' : 'md:tw-w-[210px]'">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="tw-text-[11px]"
              color="green-7"
              @click="openModalWorking(props.row)"
            >
              <q-icon name="calendar_month" class="tw-mr-2"/>
              Ngày đi làm dự kiến
            </q-btn>
            <q-btn
              v-if="props.row.mail_id"
              class="tw-text-[12px] sp:tw-text-[10px] tw-ml-2"
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

    <q-dialog v-model="modalWorking" @hide="hideModalWorking">
      <q-card style="width: 35%; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Thêm ngày đi làm cho ứng viên {{ dataWorking.fullname }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="height: max-content">
          <div class="sp:tw-mt-1 tw-text-center">
            <div class="tw-w-[150px] tw-text-right tw-inline-block tw-mr-8">
              <label class="tw-font-bold" for="name">Ngày đi làm dự kiến:<span class="text-red">*</span></label>
            </div>
            <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white tw-w-[61%]
              tw-rounded-md tw-inline-block"
                :class="workingDayFocus ? 'tw-border-sky-500 tw-outline-none' : ''">
              <input
                type="text"
                id="birthday"
                class="tw-outline-0 tw-py-[3px] tw-w-[90%]"
                v-model="dataWorking.start_join_date"
                :placeholder="`Ngày đi làm dự kiến (${FORMAT_DATE.toLowerCase()})`"
                @focusin="workingDayFocus = true"
                @focusout="workingDayFocus = false"
              >
              <q-icon name="event" class="cursor-pointer" size="xs">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxy">
                  <q-date name="wedding" v-model="dataWorking.start_join_date" @update:model-value="qDateProxy.hide()">
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </div>
            <span v-if="(errors.start_join_date)"
              class="tw-ml-10 text-red tw-text-xs">*{{ errors.start_join_date }}</span>
          </div>
        </q-card-section>
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn color="green-7" class="tw-w-[100px] tw-text-white" @click="openModalConfirmWorking()" label="Cập nhật"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-dialog v-model="cvModal">
      <q-card style="width: 900px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Xem CV của ứng viên {{ nameCv }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: 650px">
          <iframe title="cv" :src="dataCv.cv_file" height="100%" width="100%"></iframe>
        </q-card-section>
      </q-card>
    </q-dialog>

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
            Thông tin mail gửi điền thông tin của các ứng viên
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
import { searchItems } from 'utilities/common';
import { MESSAGE, WARNING } from 'utilities/message';
import { useAuthStore } from 'stores/auth-store';
import {
  PAGINATION_DEFAULT,
  PERPAGE_OPTIONS,
  FORMAT_DATE,
  FORMAT_DATE_IN_SERVER,
  GENDER,
} from 'utilities/const';
import { cloneDeep } from 'lodash';
import dayjs from 'utilities/day';
import candidateService from 'services/candidate.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import ToastUtil from 'utilities/toast';
import useValidate from 'composables/validate';
import startJoinSchema from 'schemas/candidate/start-join-candidate';
import officeService from 'services/office.service';
import mailService from 'services/mail.service';
import candidateMailSchema from 'schemas/mail/candidate-mail';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others
const { errors, validate } = useValidate();
const { confirmPopup, countRecord } = useMixin();

// 2) ======= VARIABLE REF ========
const loading = ref(true);
const modalWorking = ref(false);
const cvModal = ref(false);
const nameCv = ref('');
const workingDayFocus = ref(false);
const dataSearch = reactive({
  search_key: '',
  advance: {
    position_id: '',
    team_id: '',
    office: '',
    gender: '',
  },
});
const dataWorking = reactive({
  id: null,
  name: '',
  start_join_date: '',
});
const dataCv = reactive({
  cv_file: '',
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
    name: 'start_join_date',
    align: 'left',
    label: 'Ngày đi làm dự kiến',
    field: 'start_join_date',
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
const candidatesSelected = ref([]);
const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});

const totalRecord = ref(0);
let records = [];
const modalMail = ref(false);
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

const qDateProxy = ref();
const mails = ref([]);
const modalPreviewMail = ref(false);

// 3) ======= METHOD/FUNCTION ========

// Open modal set working day
const openModalWorking = (row) => {
  modalWorking.value = true;
  dataWorking.start_join_date = row.start_join_date ? dayjs(row.start_join_date).format(FORMAT_DATE) : '';
  dataWorking.id = row.id;
  dataWorking.fullname = row.fullname;
};

// Update status
const updateWorking = async () => {
  const startJoinDate = dayjs(dataWorking.start_join_date).format(FORMAT_DATE_IN_SERVER);
  const updated = candidateService.editStartJoin(dataWorking.id, startJoinDate);
  if (updated) {
    // Update candidate in rows, records
    rows.value.map((row) => {
      if (dataWorking.id === row.id) {
        row.start_join_date = startJoinDate;
      }
      return row;
    });
    records.map((record) => {
      if (dataWorking.id === record.id) {
        record.start_join_date = startJoinDate;
      }
      return record;
    });
  }
};

// Reopen modal offer
const reopenModalOffer = () => {
  modalWorking.value = true;
};

// Open modal confirm working day offer
const openModalConfirmWorking = () => {
  const isValid = validate(startJoinSchema, { start_join_date: dataWorking.start_join_date });
  if (!isValid) {
    return;
  }
  modalWorking.value = false;
  confirmPopup(MESSAGE.FORM.UPDATE.CONFIRM_TITLE, MESSAGE.FORM.UPDATE.CONFIRM_QUESTION, updateWorking, reopenModalOffer);
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
const openModalCv = (data) => {
  cvModal.value = true;
  nameCv.value = data.row.name;
  dataCv.cv_file = `${data.row.cv_file_path}/`;
};

// Send mail
const sendMail = async () => {
  const candidatesId = [];
  mails.value.forEach((candidate) => {
    candidatesId.push(candidate.id);
  });
  modalPreviewMail.value = false;
  const sent = await candidateService.sendCandidatesForm(candidatesId);
  if (sent) {
    // Delete candidate in rows, records
    rows.value = rows.value.filter((row) => !candidatesId.includes(row.id));
    records = records.filter((row) => !candidatesId.includes(row.id));
    totalRecord.value = rows.value.length;
    updatePaginate(totalRecord.value);
    // Update count record of menu
    countRecord();
    candidatesSelected.value = [];
  }
};

// Open modal confirm send mail
const confirmSendMail = () => {
  let valid = true;
  candidatesSelected.value.forEach((candidate) => {
    if (!candidate.start_join_date || !candidate.mail_id) {
      valid = false;
    }
  });

  if (valid && candidatesSelected.value.length > 0) {
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
      ToastUtil.warning(MESSAGE.MAIL.SEND.SEND_FORM);
    }
  } else {
    ToastUtil.warning(WARNING.SEND_FORM);
  }
};

// Hide modal update start join date
const hideModalWorking = () => {
  errors.value = {};
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

/**
 * Handle create mail
 */
const handleCreateMail = async () => {
  const candidatesId = [];
  candidatesSelected.value.forEach((candidate) => {
    candidatesId.push(candidate.id);
  });

  const newMails = await candidateService.createFormMails(candidatesId);
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

const onCloseModalPreviewMail = () => {
  mails.value = [];
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

  const candidates = await candidateService.getAcceptOfferCandidates(false);

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

<template>
  <div class="q-pa-md">
    <h1 class="tw-text-xl">Mời phỏng vấn</h1>

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
          <label class="tw-block">PV từ ngày:</label>
          <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px] tw-rounded-md"
            :class=" interviewDayFromFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
            <input
              id="date_interview_from"
              type="text"
              class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
              @focusin="interviewDayFromFocus = true"
              @focusout="interviewDayFromFocus = false"
              v-model="dataSearch.advance.date_interview_from"
              @input="searchHandle"
            >
            <q-icon name="event" class="cursor-pointer" size="xs">
              <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyFrom">
                <q-date name="wedding" v-model="dataSearch.advance.date_interview_from"
                    @update:model-value="searchHandle, qDateProxyFrom.hide()">

                </q-date>
              </q-popup-proxy>
            </q-icon>
          </div>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block">PV đến ngày:</label>
          <div class="tw-border tw-border-gray-300 tw-pl-2 tw-bg-white sp:tw-min-w-[160px] tw-rounded-md"
            :class=" interviewDayToFocus ? 'tw-border-sky-500 tw-outline-none' : '' ">
            <input
              id="date_interview_to"
              type="text"
              class="tw-outline-0 tw-py-[3px] tw-w-[85%]"
              v-model="dataSearch.advance.date_interview_to"
              @focusin="interviewDayToFocus = true"
              @focusout="interviewDayToFocus = false"
              @input="searchHandle"
            >
            <q-icon name="event" class="cursor-pointer" size="xs">
              <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyTo">
                <q-date name="wedding" v-model="dataSearch.advance.date_interview_to"
                    @update:model-value="searchHandle, qDateProxyTo.hide()">

                </q-date>
              </q-popup-proxy>
            </q-icon>
          </div>
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
        color="green-7"
        size="12px"
        @click.prevent="confirmCreateMail"
        :disable="rows.length === 0"
      >
        <q-icon name="add_box" class="tw-mr-2"/>
        Tạo mail
      </q-btn>
      <q-btn
        class="tw-mx-3"
        color="green-7"
        size="12px"
        @click.prevent="confirmSendMail"
        :disable="rows.length === 0"
      >
        Gửi mail
      </q-btn>
      <div class="tw-inline tw-float-right">
        <label class="tw-inline tw-align-baseline tw-mr-4">Tùy chọn gửi mail:</label>
        <select
          class="focus:tw-outline-none focus:tw-border-sky-500 tw-border tw-border-gray-300
            tw-py-1 tw-pl-1 tw-min-w-[160px] tw-rounded-md" v-model="dataSearch.advance.status"
          @change="searchHandle"
        >
          <option value="">Tất cả</option>
          <option v-for="(status, index) in INVITE_STATUS" :value="status.id" :key="index">
              {{ status.name }}
            </option>
        </select>
      </div>
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
        <span class="q-table__title tw-inline-block">Danh sách mời phỏng vấn</span>
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
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-if="props.row.mail_id != null">
            <q-btn
              class="sp:tw-text-[10px]"
              color="green-7"
              size="12px"
              @click.prevent="openModalMail(props)"
            >
              Xem trước mail
            </q-btn>
          </div>
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-else></div>
        </q-td>
      </template>
      <!-- Column type interview -->
      <template v-slot:body-cell-interview_form="props">
        <q-td :props="props" class="tw-w-[100px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block" v-for="(item, index) in TYPE_INTERVIEW_FORM" :key="index">
            <p v-if="props.row.interview_form == item.id">
              {{ item.name }}
            </p>
          </div>
        </q-td>
      </template>
      <!-- Column status -->
      <template v-slot:body-cell-status="props">
        <q-td :props="props" class="tw-w-[100px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <p>
              {{ props.row.status }}
            </p>
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

    <!-- Modal show mail content -->
    <q-dialog v-model="modalMail">
      <q-card style="width: 950px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Thông tin mail gửi mời phỏng vấn cho ứng viên {{ dataMail.name }}</div>
          <q-space />
        </q-card-section>

        <q-card-section style="width: 100%; height: max-content">
          <div class="sp:tw-mt-1">
            <div class="tw-w-[120px] tw-text-right tw-inline-block tw-mr-8">
              <label class="tw-font-bold" for="name">Tiêu đề:</label>
            </div>
            <input
              type="text"
              id="name"
              class="tw-rounded-md tw-border tw-border-gray-300
                tw-py-[3px] tw-pl-2 tw-w-[56%] tw-inline
                focus:tw-outline-none focus:tw-border-sky-500"
              placeholder="Nhập tiêu đề"
              v-model="dataMail.title"
            >
          </div>
          <div class="tw-mt-3">
            <div class="tw-w-[120px] tw-text-right tw-inline-block tw-mr-8">
              <label class="tw-font-bold" for="name">Người nhận:</label>
            </div>
            <input
              type="text"
              id="name"
              class="tw-rounded-md tw-border tw-border-gray-300
                tw-py-[3px] tw-pl-2 tw-w-[30%] tw-inline
                focus:tw-outline-none focus:tw-border-sky-500"
              placeholder="Email người nhận"
              v-model="dataMail.candidate_email"
            >
            <label for="cc" class="tw-ml-[50px] tw-font-bold tw-cursor-pointer" @click.prevent="addEmailCc"
              :class="dataMail.carbon_copy.length >= limitEmailCc ? 'disabled' : ''">Thêm Cc</label>
          </div>
          <template v-for="(email, index) in dataMail.carbon_copy" :key="index">
            <div class="tw-mt-3">
              <div class="tw-w-[120px] tw-text-right tw-inline-block tw-mr-8">
                <label class="tw-font-bold" for="name">Người nhận Cc:</label>
              </div>
              <input
                type="text"
                id="name"
                class="tw-rounded-md tw-border tw-border-gray-300
                  tw-py-[3px] tw-pl-2 tw-w-[30%] tw-mr-5
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
          </template>
          <div class="tw-mt-7 tw-flex">
            <div class="tw-w-[120px] tw-text-right tw-mr-8">
              <label class="tw-font-bold " for="name">Nội dung:</label>
            </div>
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
          </div>
        </q-card-section>
        <!-- Button bottom -->
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup/>
          <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" @click.prevent="openModalSaveMail()" label="Lưu"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Modal preview mail -->
    <q-dialog v-model="modalPreviewMail">
      <q-card style="width: 950px; max-width: 80vw; height: max-content">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">
            Thông tin mail gửi mời phỏng vấn cho các ứng viên
          </div>
          <q-space />
        </q-card-section>

        <q-card-section
          v-for="(mail, index) in dataMail"
          :key="mail.id"
          class="tw-w-full tw-text-gray-700"
          :class="index % 2 !== 0 ? 'tw-bg-[whitesmoke]' : ''"
        >
          <table class="tw-w-full">
            <tbody>
              <tr>
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Họ tên:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">{{ mail.name }}</td>
              </tr>
              <tr>
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Tiêu đề:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">{{ mail.title }}</td>
              </tr>
              <tr>
                <th class="tw-text-right tw-pr-2 tw-border-collapse tw-border tw-w-[120px] tw-py-2">Người nhận:</th>
                <td class="tw-border-collapse tw-border tw-py-2 tw-pl-2">{{ mail.candidate_email }}</td>
              </tr>
              <tr v-if="mail.carbon_copy">
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
            </tbody>
          </table>
        </q-card-section>
        <!-- Button bottom -->
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup/>
          <q-btn class="bg-green-7 tw-w-[100px] tw-text-white" @click.prevent="sendMail" label="Gửi mail"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import inviteInterviewService from 'services/invite-interview.service';
import positionService from 'services/position.service';
import teamService from 'services/team.service';
import officeService from 'services/office.service';
import mailService from 'services/mail.service';
import { onMounted, reactive, ref } from 'vue';
import useMixin from 'mixins/common.js';
import { useAuthStore } from 'stores/auth-store';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, TYPE_INTERVIEW_FORM,
  INVITE_STATUS, GENDER,
} from 'utilities/const';
import { cloneDeep } from 'lodash';
import { searchItems } from 'utilities/common';
import { MESSAGE, WARNING } from 'utilities/message';
import ToastUtil from 'utilities/toast';
import candidateMailSchema from 'schemas/mail/candidate-mail';
import useValidate from 'composables/validate';

// 1) ======= INITIALIZATION ========

// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others
const { errors, validate } = useValidate();

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
    name: 'time_interview',
    align: 'left',
    label: 'Thời gian PV',
    field: 'time_interview',
    sortable: true,
  },
  {
    name: 'office',
    align: 'left',
    label: 'Địa điểm PV',
    field: 'office',
    sortable: true,
  },
  {
    name: 'interview_form',
    align: 'left',
    label: 'Loại PV',
    field: 'interview_form',
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

const rows = ref([]);

const listTeam = ref([]);

const listPosition = ref([]);

const listOffice = ref([]);

const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});

const candidateSelected = ref([]);
const interviewDayFromFocus = ref(false);
const interviewDayToFocus = ref(false);
const modalMail = ref(false);
const modalPreviewMail = ref(false);
const dataMail = ref(null);
const loading = ref(true);

const limitEmailCc = ref(3);

const dataSearch = reactive({
  search_key: '',
  advance: {
    position: '',
    team: '',
    date_interview_from: '',
    date_interview_to: '',
    office: '',
    status: '',
    gender: '',
  },
});

const totalRecord = ref(rows.value.length);
const records = ref([]);

const qDateProxyFrom = ref();
const qDateProxyTo = ref();

// 3) ======= METHOD/FUNCTION ========

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

// Create mail
const createMail = async () => {
  const idsSelected = [];
  let flagStopCreateMail = false;
  candidateSelected.value.forEach((candidate) => {
    if (candidate.mail_id !== null) {
      ToastUtil.warning(WARNING.CANDIDATE_HAVE_MAIL);
      flagStopCreateMail = true;
    }
    idsSelected.push(candidate.id);
  });

  if (flagStopCreateMail) {
    return;
  }

  // Handle create mail
  const newMails = await inviteInterviewService.createInviteMails(idsSelected);
  if (newMails) {
    idsSelected.value = [];
    records.value.forEach((record) => {
      newMails.forEach((mail) => {
        if (record.id === mail.candidate_id) {
          record.title = mail.title;
          record.body = mail.body;
          record.mail_id = mail.id;
        }
      });
      return record;
    });
    rows.value.forEach((row) => {
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
  candidateSelected.value = [];
};

// Open modal confirm create mail
const confirmCreateMail = () => {
  if (candidateSelected.value.length > 0) {
    confirmPopup(MESSAGE.INVITE.CREATE_MAIL.CONFIRM_TITLE, MESSAGE.INVITE.CREATE_MAIL.CONFIRM_QUESTION, createMail);
  } else {
    ToastUtil.warning(WARNING.NOT_SELECTED);
  }
};

// Open modal edit mail
const openModalMail = (data) => {
  modalMail.value = true;
  const templateMail = cloneDeep(data);
  dataMail.value = {
    id: templateMail.row.mail_id,
    title: templateMail.row.title,
    body: templateMail.row.body,
    candidate_id: templateMail.row.id,
    name: templateMail.row.fullname,
    candidate_email: templateMail.row.email,
    carbon_copy: templateMail.row.carbon_copy !== null ? templateMail.row.carbon_copy : [],
  };
};

// Save mail
const saveMail = async () => {
  // Handle save mail
  const updated = await mailService.update(dataMail.value.id, {
    title: dataMail.value.title,
    body: dataMail.value.body,
    carbon_copy: dataMail.value.carbon_copy,
  });

  if (updated) {
    rows.value.forEach((row, index) => {
      if (row.mail_id === dataMail.value.id) {
        rows.value[index].title = dataMail.value.title;
        rows.value[index].body = dataMail.value.body;
        rows.value[index].carbon_copy = dataMail.value.carbon_copy;
      }
    });

    // Update data to records
    records.value.forEach((record, index) => {
      if (record.mail_id === dataMail.value.id) {
        records.value[index].title = dataMail.value.title;
        records.value[index].body = dataMail.value.body;
        records.value[index].carbon_copy = dataMail.value.carbon_copy;
      }
    });
  }
};

// Reopen modal confirm save mail
const reopenSaveMailModal = () => {
  modalMail.value = true;
};

// Open modal confirm save mail
const openModalSaveMail = () => {
  const mail = {
    title: dataMail.value.title,
    candidate_email: dataMail.value.candidate_email,
    body: extractContent(dataMail.value.body),
  };
  dataMail.value.carbon_copy.forEach((email, index) => {
    mail[`receiver_cc${index}`] = email;
  });

  const isValid = validate(candidateMailSchema, mail);
  if (!isValid) {
    return;
  }
  modalMail.value = false;

  confirmPopup(MESSAGE.INVITE.SAVE_MAIL.CONFIRM_TITLE, MESSAGE.INVITE.SAVE_MAIL.CONFIRM_QUESTION, saveMail, reopenSaveMailModal);
};

// Add email Cc
const addEmailCc = () => {
  if (dataMail.value.carbon_copy.length < limitEmailCc.value) {
    dataMail.value.carbon_copy.push('');
  }
};

// Remove email Cc
const removeEmailCc = (index) => {
  dataMail.value.carbon_copy.splice(index, 1);
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
  rows.value = searchItems(dataSearch, records.value);
  totalRecord.value = rows.value.length;
  updatePaginate(totalRecord.value);
};

// Get list candidate
const getListCandidate = async (flagLoading = true) => {
  const data = await inviteInterviewService.getList(flagLoading);
  if (data) {
    data.item.forEach((candidate) => {
      candidate.time_interview = `${candidate.date !== null ? candidate.date : ''} ${candidate.time !== null ? candidate.time : ''}`;

      CANDIDATE_STATUS.forEach((itemStatus) => {
        if (itemStatus.id === candidate.status) {
          candidate.status = itemStatus.name;
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

// Reset search data
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.advance.position = '';
  dataSearch.advance.team = '';
  dataSearch.advance.date_interview_from = '';
  dataSearch.advance.date_interview_to = '';
  dataSearch.advance.status = '';
  dataSearch.advance.gender = '';
  searchHandle();
};

// Send mail
const sendMail = async () => {
  // Handle send mail
  const candidateIds = [];
  dataMail.value.forEach((mail) => {
    candidateIds.push(mail.candidate_id);
  });
  modalPreviewMail.value = false;
  const sent = await inviteInterviewService.sendMailsInvite(candidateIds);
  if (sent) {
    // Delete candidate in rows, records
    rows.value = rows.value.filter((row) => !candidateIds.includes(row.id));
    records.value = records.value.filter((row) => !candidateIds.includes(row.id));
    totalRecord.value = rows.value.length;
    updatePaginate(totalRecord.value);
    // Update count record of menu
    countRecord();
    candidateSelected.value = [];
    dataMail.value = null;
  }
};

// Open modal confirm send mail
const confirmSendMail = () => {
  if (candidateSelected.value.length > 0) {
    let flagStopSendMail = false;
    const mails = [];
    candidateSelected.value.forEach((candidate) => {
      if (candidate.mail_id === null) {
        flagStopSendMail = true;
        return;
      }
      mails.push({
        id: candidate.mail_id,
        title: candidate.title,
        body: candidate.body,
        candidate_id: candidate.id,
        name: candidate.fullname,
        carbon_copy: candidate.carbon_copy,
        candidate_email: candidate.email,
      });
    });

    if (flagStopSendMail) {
      ToastUtil.warning(WARNING.CANDIDATE_NOT_HAVE_MAIL);
      return;
    }
    dataMail.value = mails;
    modalPreviewMail.value = true;
  } else {
    ToastUtil.warning(WARNING.NOT_SELECTED);
  }
};

// 4) ======= VUEJS LIFECYCLE ========

onMounted(async () => {
  await Promise.all([
    getListOffice(),
    getListPosition(),
    getListTeam(),
  ]);

  await getListCandidate(false);
  loading.value = false;
});

</script>

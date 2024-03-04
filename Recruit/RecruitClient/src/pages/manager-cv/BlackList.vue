<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Danh sách đen</h1>
    <!-- Search Advance -->
    <q-form class="tw-mt-3 tw-border tw-border-gray-300 tw-p-5 tw-rounded-md">
      <div class="tw-flex tw-flex-wrap">
        <div class="tw-mr-4 sp:tw-mt-1 sp:tw-w-[45%]">
          <label class="tw-block" for="position">Chức danh:</label>
          <select
            id="position"
            class="tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1 tw-min-w-[100px] tw-rounded-md"
            @focusin="onFocusInput($event, true)"
            @focusout="onFocusInput"
            v-model="dataSearch.advance.position"
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option
              v-for="position in listPosition"
              :value="position.name"
              :key="position"
            >
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
          <label class="tw-block" for="team">Vị trí:</label>
          <select
            id="team"
            class="tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1 tw-min-w-[100px] tw-rounded-md"
            @focusin="onFocusInput($event, true)"
            @focusout="onFocusInput"
            v-model="dataSearch.advance.team"
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option
              v-for="(team, index) in listTeam"
              :value="team.name"
              :key="index"
            >
              {{ team.name }}
            </option>
          </select>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1">
          <label class="tw-block">Địa điểm PV:</label>
          <select
            id="position"
            class="tw-rounded-md tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1 tw-w-[100px]"
            @focusin="onFocusInput($event, true)"
            @focusout="onFocusInput"
            v-model="dataSearch.advance.office"
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option
              v-for="(team, index) in listOffice"
              :value="team.name"
              :key="index"
            >
              {{ team.name }}
            </option>
          </select>
        </div>
      </div>
      <!-- Btn Search -->
      <div class="tw-mt-3">
        <button
          type="button"
          class="bg-green-7 text-white tw-py-[5px] tw-px-2 tw-rounded"
          @click.prevent="resetSearch"
        >
          Đặt lại
        </button>
      </div>
    </q-form>
    <!-- Dialog show cv -->
    <q-dialog v-model="showDialogCv">
      <q-card class="tw-w-[900px] tw-max-w-[80vw!important] tw-h-max">
        <q-card-section
          class="row items-center q-pb-lg tw-bg-[#17a2b8!important]"
        >
          <div class="tw-text-[18px] text-white">
            Xem CV của ứng viên {{ candidate.fullname }}
          </div>
          <q-space />
        </q-card-section>

        <q-card-section class="tw-w-full tw-h-[650px]">
          <iframe
            :title="candidate.fullname"
            :src="candidate.cv_file_path"
            height="100%"
            width="100%"
          ></iframe>
        </q-card-section>
      </q-card>
    </q-dialog>
    <!-- Dialog edit cv -->
    <q-dialog v-model="showDialogEditCandidate">
      <q-card class="tw-min-h-[530px] tw-min-w-[1200px!important] sp:tw-min-w-[100px!important] tw-pb-3">
        <q-card-section
          class="row items-center q-pb-lg tw-bg-[#17a2b8!important]"
        >
          <div class="tw-text-[18px] text-white">
            Thông tin ứng viên {{ candidate.fullname }}
          </div>
          <q-space />
        </q-card-section>
        <q-card-section class="tw-w-full tw-h-[max-content]">
          <div class="tw-rounded tw-p-2">
            <div class="tw-justify-between">
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Họ tên</label>
                    <input
                      type="text"
                      readonly
                      id="name"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px] tw-pl-2 tw-w-full"
                      v-model="candidate.fullname"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                    />
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block">Email</label>
                    <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md
                        tw-py-[4px] tw-pl-2 tw-w-full tw-block"
                      readonly
                      v-model="candidate.email"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                    />
                  </div>
                </div>
              </div>
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Chức danh</label>
                    <select
                      class="tw-border tw-block tw-border-gray-300 tw-py-[4px] tw-pl-1
                        tw-min-w-[100px] tw-rounded-md tw-w-full disabled:tw-opacity-[1!important]"
                      @focusin="onFocusInput($event, true)"
                      readonly
                      disabled
                      @focusout="onFocusInput"
                      v-model="candidate.position_id"
                    >
                      <option
                        v-for="(position, index) in listPosition"
                        :value="position.id"
                        :key="index"
                      >
                        {{ position.name }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block">Vị trí</label>
                    <select
                      class="tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1
                        tw-min-w-[100px] tw-rounded-md tw-block tw-w-full disabled:tw-opacity-[1!important]"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      disabled
                      readonly
                      v-model="candidate.team_id"
                    >
                      <option value="">Tất cả</option>
                      <option
                        v-for="(team, index) in listTeam"
                        :value="team.id"
                        :key="index"
                      >
                        {{ team.name }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Số điện thoại</label>
                    <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full tw-block"
                      readonly
                      v-model="candidate.telephone_no"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                    />
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block">Trạng thái:</label>
                    <select
                      class="tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1
                        tw-min-w-[100px] tw-rounded-md tw-block tw-w-full disabled:tw-opacity-[1!important]"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      disabled
                      v-model="candidate.status"
                    >
                      <option value="">Tất cả</option>
                      <option v-for="(item_status) in CANDIDATE_STATUS" :key="item_status" :value="item_status.id">{{ item_status.name }}</option>
                    </select>
                  </div>
                </div>
              </div>
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Người giới thiệu:</label>
                    <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full tw-block tw-text-black"
                      readonly
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      v-model="candidate.recommender_name"
                    />
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block">Ngày sinh</label>
                    <div
                      class="tw-pr-4 tw-pl-2 tw-py-[4px] tw-border tw-border-gray-300 tw-rounded-md
                        tw-focus:tw-outline-none tw-text-gray-600"
                    >
                      <input
                        id="birthday"
                        type="text"
                        class="tw-outline-0 tw-w-[91%]"
                        placeholder="yyyy/mm/dd"
                        v-model="candidate.birthday"
                        readonly
                        @focusin="onFocusInput($event, true)"
                        @focusout="onFocusInput"
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3">
              <label class="tw-block">Địa chỉ
                <textarea
                  class="tw-border tw-border-gray-300 tw-pl-2
                    tw-bg-white tw-w-full tw-rounded-md tw-p-2"
                  placeholder="Nhập địa chỉ"
                  v-model="candidate.full_address"
                  @focusin="onFocusInput($event, true)"
                  readonly
                  @focusout="onFocusInput"
                ></textarea>
              </label>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3">
              <label class="tw-block">Ghi chú:
                <input
                  class="tw-border tw-border-gray-300 tw-pl-2
                    tw-bg-white tw-w-full tw-rounded-md tw-p-2"
                  placeholder="Ghi chú"
                  @focusin="onFocusInput($event, true)"
                  readonly
                  @focusout="onFocusInput"
                  v-model="candidate.note"
                />
              </label>
            </div>
            <div class="sp:tw-mt-1 tw-mt-5">
              Danh sách những lần apply:
              <table class="tw-w-full tw-border-collapse tw-border">
                <caption class="tw-hidden">Danh sách những lần apply</caption>
                <thead class="row thead-dark">
                  <th class="col-2 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Ngày phỏng vấn</th>
                  <th class="col-2 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Người phỏng vấn</th>
                  <th class="col-2 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Tình trạng</th>
                  <th class="col-6 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Nhận xét</th>
                </thead>
                <tbody v-if="(candidate.list_interview.length > 0)">
                  <tr class="row" v-for="interview in candidate.list_interview" :key="interview">
                    <td class="col-2 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.time.slice(0, 10) }}</td>
                    <td class="col-2 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.fullname }}</td>
                    <td class="col-2 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.status }}</td>
                    <td class="col-6 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.comment }}</td>
                  </tr>
                </tbody>
                <tbody v-else class="tw-text-center tw-text-[16px]">
                  Không có lịch sử apply
                </tbody>
              </table>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
    <!-- List of candidates -->
    <q-table
      class="tw-mt-8 tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      hide-pagination
      loading-label="Đang tìm kiếm dữ liệu ..."
      :loading="loading"
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
    >
      <!-- Column serial -->
      <template v-slot:body-cell-serial="props">
        <q-td :props="props" class="tw-w-[30px]">
          {{ props.pageIndex + 1 }}
        </q-td>
      </template>

      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên</span>
        <q-form class="tw-inline-block sp:tw-ml-0 tw-ml-10 tw-translate-y-px">
          <q-input
            dense
            debounce="300"
            input-class="tw-py-0 tw-w-[300px]"
            v-model="dataSearch.search_key"
            placeholder="Tìm kiếm theo Họ tên, email, số điện thoại"
            @update:model-value="searchHandler"
          >
            <template v-slot:append>
              <q-btn
                @click="searchHandler"
                type="submit"
                dense
                unelevated
                round
                icon="search"
              />
            </template>
          </q-input>
        </q-form>
      </template>
      <!-- Choose perpage -->
      <template v-slot:top-right>
        <div class="sp:tw-w-screen sp:tw-mt-3">
          <span class="tw-mr-8 sp:tw-block"
            >Tổng số bản ghi: {{ totalRecord }}</span
          >
          <label for="per_page" class="tw-mr-2">Số bản ghi mỗi page:</label>
          <select
            id="per_page"
            @change="searchHandler()"
            v-model="pagination.rowsPerPage"
            class="tw-outline-none"
          >
            <option
              v-for="option in PERPAGE_OPTIONS"
              :key="option.id"
              :value="option"
            >
              {{ option }}
            </option>
          </select>
        </div>
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
      <!-- Field name -->
      <template v-slot:body-cell-fullname="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <p class="tooltip tw-text-sky-600 tw-cursor-pointer hover:tw-underline tw-w-[180px] tw-text-ellipsis tw-overflow-hidden
            hover:tw-underline-offset-1" @click.prevent="openModalCv(props.row)">
            {{ props.row.fullname }}
            <span class="tooltiptext">{{ props.row.fullname }}</span>
          </p>
        </q-td>
      </template>
      <!-- Field name -->
      <template v-slot:body-cell-email="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <p class="tooltip tw-w-[180px] tw-text-ellipsis tw-overflow-hidden">
            {{ props.row.email }}
            <span class="tooltiptext">{{ props.row.email }}</span>
          </p>
        </q-td>
      </template>
      <!-- Field action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[240px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px]"
              color="green-7"
              icon="visibility"
              @click="viewCandidate(props.row.id)"
            >
              Xem
            </q-btn>
          </div>
        </q-td>
      </template>
    </q-table>
    <!-- Pagination -->
    <div class="q-pt-sm flex tw-justify-center">
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
import { onMounted, reactive, ref } from 'vue';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, GENDER,
} from 'utilities/const';
import blackListService from 'services/black-list.service';
import { searchItems } from 'utilities/common';
import positionService from 'services/position.service';
import officeService from 'services/office.service';
import teamService from 'services/team.service';
import { cloneDeep } from 'lodash';
import { useAuthStore } from 'stores/auth-store';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others

// 2) ======= VARIABLE REF ========

const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: PAGINATION_DEFAULT.OFFSET,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});
const totalRecord = ref(0);
const dataSearch = reactive({
  search_key: '',
  advance: {
    team: '',
    position: '',
    office: '',
    previous_status: '',
    status: '',
    gender: '',
  },
});
const showDialogCv = ref(false);
const showDialogEditCandidate = ref(false);
const idInputsDate = ['date_interview_from', 'date_interview_to', 'birthday'];
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
    name: 'recommender_name',
    align: 'left',
    label: 'Người giới thiệu',
    field: 'recommender_name',
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
    name: 'action',
    align: 'left',
    label: 'Hành động',
    field: 'action',
    sortable: true,
  },
];
const rows = ref([]);
const listPosition = ref([]);
const listTeam = ref([]);
const listOffice = ref([]);
const records = ref([]);
const candidate = reactive({
  id: '',
  fullname: '',
  email: '',
  birthday: '',
  full_address: '',
  position_id: '',
  recommender_name: '',
  status: '',
  team_id: '',
  telephone_no: '',
  cv_file_path: '',
  list_interview: [],
});
const loading = ref(true);

// 3) ======= METHOD/FUNCTION ========
/**
 * Handle show dialog edit candidate
 *
 * @param object row
 * @return void
 */
const viewCandidate = async (idCandidate) => {
  const resultCandidate = await blackListService.getCandidate(idCandidate);
  if (resultCandidate) {
    candidate.id = resultCandidate.candidate.id;
    candidate.fullname = resultCandidate.candidate.fullname;
    candidate.email = resultCandidate.candidate.email;
    candidate.birthday = resultCandidate.candidate.birthday.replaceAll('-', '/');
    candidate.full_address = resultCandidate.candidate.full_address;
    candidate.recommender_name = resultCandidate.candidate.recommender_name;
    candidate.status = resultCandidate.candidate.status;
    candidate.team_id = resultCandidate.candidate.team_id;
    candidate.position_id = resultCandidate.candidate.position_id;
    candidate.telephone_no = resultCandidate.candidate.telephone_no;
    candidate.list_interview = resultCandidate.list_interview;
    candidate.cv_file_path = resultCandidate.cv_file_path;
    showDialogEditCandidate.value = true;
  }
};

/**
 * Handle update paginate
 *
 * @param int totalItem
 * @return void
 */
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(
    totalItem / pagination.value.rowsPerPage,
  );
};

/**
 * Handle open dialog cv
 *
 * @param object row
 * @return void
 */
const openModalCv = (row) => {
  candidate.fullname = row.fullname;
  candidate.cv_file_path = `${row.cv_file_path}/`;
  showDialogCv.value = true;
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
    element.classList.add('tw-border-gray-300', 'tw-outline-none');
  } else {
    // focusOut
    element.classList.remove('tw-border-gray-300', 'tw-outline-none');
  }
};

// Get list candidate
const searchHandler = async () => {
  rows.value = searchItems(dataSearch, records.value);
  totalRecord.value = rows.value.length;
  updatePaginate(rows.value.length);
};

// Reset search data
const resetSearch = () => {
  dataSearch.search_key = '';
  dataSearch.advance.position = '';
  dataSearch.advance.team = '';
  dataSearch.advance.gender = '';
  searchHandler();
};

// 4) ======= VUEJS LIFECYCLE ========
onMounted(async () => {
  const [listPositions, listTeams, listOffices] = await Promise.all([
    positionService.getList(),
    teamService.getList(),
    officeService.getList(),
  ]);
  // Get position
  listPosition.value = listPositions;
  listTeam.value = listTeams;
  listOffice.value = listOffices.list_office;
  listOffice.value.forEach((item) => {
    if (item.id === user.office_id) {
      dataSearch.advance.office = item.name;
    }
  });

  const listCandidates = await blackListService.getList(false);

  if (listCandidates) {
    records.value = cloneDeep(listCandidates.item);
    rows.value = searchItems(dataSearch, records.value);
    totalRecord.value = rows.value.length;
    updatePaginate(rows.value.length);
  }
  loading.value = false;
});
</script>

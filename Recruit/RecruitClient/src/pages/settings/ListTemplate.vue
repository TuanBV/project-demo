<template>
  <div class="q-pa-md">
    <!-- Dialog -->
    <q-dialog v-model="dialog" :full-height="true">
      <q-card class="tw-max-w-[1200px!important]">
        <q-card-section class="row tw-align-center tw-bg-[#17a2b8!important]">
          <span class="tw-text-sm tw-text-white tw-text-[18px]">Cập nhật email template</span>
        </q-card-section>

        <q-card-section>
          <div class="tw-justify-center tw-sm:tw-py-12 tw-flex tw-flex-col">
            <div class="tw-relative tw-w-full">
              <div class="tw-relative tw-bg-white tw-w-full">
                  <div class="row tw-w-full row tw-items-center">
                    <div class="tw-text-start tw-w-[10%] sp:tw-w-full tw-font-bold">Tiêu đề</div>
                    <div class="tw-w-[88%] sp:tw-w-full">
                      <input type="text" v-model="template.title"
                        id="editorTitle"
                        @focus="(flagTitle=true, flagBody=false)"
                        class="tw-px-4 tw-py-2 tw-ml-5 sp:tw-ml-0 tw-border tw-w-full focus:tw-border-sky-500 tw-h-[36px] tw-justify-self-center
                        tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600" placeholder="VN0021">
                      <span v-if="(errors.title)" class="text-red tw-ml-5 tw-text-xs">*{{ errors.title }}</span>
                    </div>
                  </div>
                  <div class="row tw-w-full row tw-mt-[10px] tw-items-center">
                    <div class="tw-text-start tw-w-[10%] sp:tw-w-full tw-font-bold">Param</div>
                    <div class="tw-px-4 tw-py-2 tw-ml-5 sp:tw-ml-0 tw-w-[88%] sp:tw-w-full tw-justify-self-center tw-flex-wrap
                      tw-text-gray-600 tw-flex" placeholder="VN0021">
                      <div v-for="item in items" :key="item" class="tw-mr-2">
                        <q-btn
                          color="grey-4"
                          text-color="grey-9"
                          class="tw-mt-2 sp:tw-text-[9px]"
                          no-caps rounded
                          @click="addParam(`$${item}`)"
                        >
                          ${{item}}
                        </q-btn>
                      </div>
                    </div>
                  </div>
                  <div class="tw-w-full row tw-mt-[10px] sp:tw-block tw-items-start">
                    <div class="tw-text-start tw-w-[10%] sp:tw-w-full tw-font-bold tw-pt-2">Nội dung</div>
                    <div class="tw-w-[88%] sp:tw-w-full tw-justify-self-center">
                      <div class="tw-py-2 tw-ml-5 sp:tw-ml-0 tw-w-[100%!important] focus:tw-border-sky-500 focus:tw-outline-none tw-text-gray-600">
                        <q-editor
                          class="tw-rounded-[0.375rem]"
                          id="editorBody"
                          ref="editor"
                          paragraph-tag="div"
                          @focus="(flagBody=true, flagTitle=false)"
                          v-model="template.body"
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
                                options: ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'code'],
                              },
                              {
                                label: $q.lang.editor.fontSize,
                                icon: $q.iconSet.editor.fontSize,
                                fixedLabel: true,
                                fixedIcon: true,
                                list: 'no-icons',
                                options: ['size-1', 'size-2', 'size-3', 'size-4', 'size-5', 'size-6', 'size-7'],
                              },
                              {
                                label: $q.lang.editor.defaultFont,
                                icon: $q.iconSet.editor.font,
                                fixedIcon: true,
                                list: 'no-icons',
                                options: ['default_font', 'arial', 'arial_black', 'comic_sans', 'courier_new', 'impact', 'lucida_grande', 'times_new_roman', 'verdana'],
                              },
                              'removeFormat',
                            ],
                            ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
                            ['undo', 'redo'],
                            ['viewsource'],
                          ]"
                          :fonts="{
                            arial: 'Arial',
                            arial_black: 'Arial Black',
                            comic_sans: 'Comic Sans MS',
                            courier_new: 'Courier New',
                            impact: 'Impact',
                            lucida_grande: 'Lucida Grande',
                            times_new_roman: 'Times New Roman',
                            verdana: 'Verdana',
                          }"
                        />
                        <span v-if="(errors.body)" class="text-red tw-text-xs">*{{ errors.body }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="row tw-w-full tw-mt-[10px] row tw-items-center">
                    <div class="tw-text-start tw-w-[10%] sp:tw-w-full tw-font-bold">Ghi chú</div>
                    <div class="tw-w-[88%] sp:tw-w-full">
                      <input type="text" v-model="template.note"
                        class="tw-px-4 tw-py-2 tw-ml-5 sp:tw-ml-0 tw-border tw-w-full focus:tw-border-sky-500 tw-h-[36px] tw-justify-self-center
                        tw-sm:tw-text-sm tw-border-gray-300 tw-rounded-md focus:tw-outline-none tw-text-gray-600" placeholder="VN0021">
                      <span v-if="(errors.note)" class="text-red tw-ml-5 tw-text-xs">*{{ errors.note }}</span>
                    </div>
                  </div>
              </div>
            </div>
          </div>
        </q-card-section>

        <!-- Notice v-close-popup -->
        <q-card-actions align="center" class="tw-pb-[20px] tw-pt-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" @click="updateTemplate()" label="Cập nhật"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-table
      class="tw-max-w-[100vw]"
      table-class="tw-overflow-x-auto tw-max-w-[100vw]"
      no-data-label="Không có dữ liệu"
      loading-label="Đang tìm kiếm dữ liệu ..."
      :loading="loading"
      v-model:pagination="pagination"
      :rows="rows"
      :columns="columns"
      hide-pagination
    >
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách mail mẫu</span>
        <q-form
          class="tw-inline-block sp:tw-ml-0 tw-ml-10 tw-translate-y-px"
        >
          <q-input
            dense
            debounce="300"
            input-class="tw-py-0"
            v-model="dataSearch.search_key"
            @update:model-value="searchHandler"
            placeholder="Tìm kiếm"
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
            <q-btn color="green-7" @click="viewTemplate(props.row.id)" size="12px"><q-icon name="visibility"></q-icon>Xem</q-btn>
          </div>
        </q-td>
      </template>
      <!-- Message no data -->
      <template v-slot:no-data="{ message }">
        <div class="full-width row flex-center q-gutter-sm tw-text-sm tw-mt-1">
          {{ message }}
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
        color="grey"
        active-color="primary"
        boundary-numbers
      />
    </div>

  </div>
</template>

<script setup>
import {
  onMounted, reactive, ref,
} from 'vue';
import { cloneDeep } from 'lodash';
import { MESSAGE } from 'utilities/message';
import { PERPAGE_OPTIONS, PAGINATION_DEFAULT } from 'utilities/const';
import toast from 'utilities/toast';
import { searchItems } from 'utilities/common';
import paramService from 'services/parameter.service';
import templateService from 'services/template.service';
import useValidate from '../../composables/validate.js';
import useMixin from '../../mixins/common.js';
import templateSchema from '../../validations/schemas/template/template.js';

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
const editor = ref(null);

const columns = ref([
  {
    name: 'id',
    align: 'left',
    label: 'STT',
    field: 'id',
    sortable: true,
  },
  {
    name: 'title',
    align: 'left',
    label: 'Tiêu đề email',
    field: 'title',
    sortable: true,
  },
  {
    name: 'note',
    align: 'left',
    label: 'Ghi chú',
    field: 'note',
    sortable: true,
  },
  {
    name: 'action',
    align: 'center',
    label: 'Hành động',
    field: 'action',
  },
]);
const pagination = ref({
  sortBy: 'desc',
  descending: false,
  page: 1,
  rowsPerPage: PAGINATION_DEFAULT.LIMIT,
  totalPage: 1,
});
const records = ref([]);
const rows = ref([]);
const dialog = ref(false);
const totalRecord = ref(0);
const template = reactive({
  id: 0,
  title: '',
  body: '',
  note: '',
});
const items = ref([]);
const flagTitle = ref(false);
const flagBody = ref(false);
const loading = ref(true);
// 3) ======= FUNCTION ========
// Get list param
const listParam = async () => {
  items.value = [];
  const listParams = await paramService.getList();
  listParams.list_param.forEach((param) => {
    items.value.push(param.name);
  });
};

// Update pagination
const updatePaginate = (totalItem) => {
  pagination.value.totalPage = Math.ceil(totalItem / pagination.value.rowsPerPage);
};

// Get list template mail
const searchHandler = async () => {
  rows.value = searchItems(dataSearch, records.value);
  totalRecord.value = rows.value.length;
  updatePaginate(rows.value.length);
};

// View mail template
const viewTemplate = async (idTemplate) => {
  flagBody.value = false;
  flagTitle.value = false;
  listParam();
  const viewTemp = await templateService.get(idTemplate);
  if (viewTemp) {
    template.id = viewTemp.id;
    template.title = viewTemp.title;
    template.note = viewTemp.note;
    template.body = viewTemp.body;
  }
  dialog.value = true;
};

// Close model
const onClose = () => {
  dialog.value = true;
};

// Call api edit template
const editTemplate = async () => {
  const updateTem = await templateService.edit(template);
  if (updateTem) {
    // Update data to records
    records.value.forEach((row, index) => {
      if (row.id === template.id) {
        records.value[index].title = template.title;
        records.value[index].body = template.body;
        records.value[index].note = template.note;
      }
    });
    toast.success(MESSAGE.TEMPLATE.UPDATE.SUCCESS);
    searchHandler();
    return;
  }
  toast.error(MESSAGE.TEMPLATE.UPDATE.ERROR);
};

// View mail template
const updateTemplate = () => {
  const isValid = validate(templateSchema, template);
  if (!isValid) {
    return;
  }
  dialog.value = false;
  confirmPopup(
    MESSAGE.TEMPLATE.UPDATE.CONFIRM_TITLE,
    `${MESSAGE.TEMPLATE.UPDATE.CONFIRM_QUESTION}<b>${template.title}</b>?`,
    editTemplate,
    onClose,
  );
};

// Handle add param
const addParam = (param) => {
  editor.value.runCmd('insertText', param);
};

// 4) ======= VUEJS LIFECYCLE ========
onMounted(async () => {
  const [listTemplates] = await Promise.all([templateService.getList()]);
  // Check data list template
  if (listTemplates) {
    records.value = cloneDeep(listTemplates.list_templates);
    rows.value = searchItems(dataSearch, records.value);
    totalRecord.value = rows.value.length;
    updatePaginate(rows.value.length);
  }
  loading.value = false;
});

</script>

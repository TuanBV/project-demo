<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Danh sách nhân viên</h1>
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
          <label class="tw-block">Văn phòng:</label>
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
      <q-card style="width: 900px; max-width: 80vw; height: max-content">
        <q-card-section
          class="row items-center q-pb-lg tw-bg-[#17a2b8!important]"
        >
          <div class="tw-text-[18px] text-white">
            Xem CV của nhân viên {{ candidate.fullname }}
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
            Chỉnh sửa ứng viên {{ candidate.fullname }}
          </div>
          <q-space />
        </q-card-section>
        <q-card-section class="tw-w-full tw-h-[max-content]">
          <div class="tw-rounded tw-p-2">
            <div class="tw-justify-between">
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Họ tên <span class="text-red">(*)</span></label>
                    <input
                      type="text"
                      id="name"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full"
                      v-model="candidate.fullname"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                    />
                    <span v-if="(errors.fullname)" class="text-red tw-text-xs">*{{ errors.fullname }}</span>
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block">Email <span class="text-red">(*)</span></label>
                    <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md
                        tw-py-[4px] tw-pl-2 tw-w-full tw-block"
                      v-model="candidate.email"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                    />
                    <span v-if="(errors.email)" class="text-red tw-text-xs">*{{ errors.email }}</span>
                  </div>
                </div>
              </div>
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Chức danh <span class="text-red">(*)</span></label>
                    <select
                      class="tw-border tw-block tw-border-gray-300 tw-py-[4px] tw-pl-1
                        tw-min-w-[100px] tw-rounded-md tw-w-full"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      v-model="candidate.position_id"
                    >
                      <option value="">Tất cả</option>
                      <option
                        v-for="(position, index) in listPosition"
                        :value="position.id"
                        :key="index"
                      >
                        {{ position.name }}
                      </option>
                    </select>
                    <span v-if="(errors.position_id)" class="text-red tw-text-xs">*{{ errors.position_id }}</span>
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block">Vị trí <span class="text-red">(*)</span></label>
                    <select
                      class="tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1
                        tw-min-w-[100px] tw-rounded-md tw-block tw-w-full"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      value=""
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
                    <span v-if="(errors.team_id)" class="text-red tw-text-xs">*{{ errors.team_id }}</span>
                  </div>
                </div>
              </div>
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block tw-h-[25px]" for="name">Số điện thoại <span class="text-red">(*)</span></label>
                    <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full tw-block"
                      v-model="candidate.telephone_no"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      maxlength="11"
                    />
                    <span v-if="(errors.telephone_no)" class="text-red tw-text-xs">*{{ errors.telephone_no }}</span>
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block tw-h-[25px]">Trạng thái:</label>
                    <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full tw-block tw-text-black disabled:tw-opacity-[1!important]" disabled
                      v-model="candidate.status"
                    />
                  </div>
                </div>
              </div>
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Người giới thiệu:</label>
                    <select
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full tw-block tw-text-black disabled:tw-opacity-[1!important]"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      v-model="candidate.recommender_id"
                      @change="searchHandler()"
                    >
                      <option value="0"></option>
                      <option
                        v-for="recommender in listRecommender"
                        :value="recommender.id"
                        :key="recommender"
                      >
                        {{ recommender.fullname }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block">Ngày sinh <span class="text-red">(*)</span></label>
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
                        @focusin="onFocusInput($event, true)"
                        @focusout="onFocusInput"
                      >
                      <q-icon name="event" class="cursor-pointer" style="float: right;" size="xs">
                        <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxy">
                          <q-date v-model="candidate.birthday" @update:model-value="qDateProxy.hide()">
                          </q-date>
                        </q-popup-proxy>
                      </q-icon>
                    </div>
                    <span v-if="errors.birthday" class="text-red tw-text-xs">*{{ errors.birthday }}</span>
                  </div>
                </div>
              </div>
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block">Ngày apply: </label>
                    <div
                      class="tw-pr-4 tw-pl-2 tw-py-[4px] tw-border tw-border-gray-300 tw-rounded-md
                        tw-focus:tw-outline-none tw-text-gray-600"
                    >
                      <input
                        type="text"
                        class="tw-outline-0 tw-w-[91%]"
                        placeholder="yyyy/mm/dd"
                        v-model="candidate.application_date"
                        @focusin="onFocusInput($event, true)"
                        @focusout="onFocusInput"
                      >
                    </div>
                    <span v-if="errors.application_date" class="text-red tw-text-xs">*{{ errors.application_date }}</span>
                  </div>
                </div>
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full tw-float-right">
                    <label class="tw-block" for="cv">Cập nhật CV:</label>
                    <input type="file" name="cv" id="cv" class="tw-border-gray-300
                      tw-w-[280px] focus:tw-outline-none focus:tw-border-sky-500"
                      @change="uploadFile"
                    >
                    <span v-if="errors['cv_file/file']" class="text-red tw-text-xs">*{{ errors['cv_file/file']}}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3">
              <label class="tw-block">Địa chỉ <span class="text-red">(*)</span>
                <textarea
                  class="tw-border tw-border-gray-300 tw-pl-2
                    tw-bg-white tw-w-full tw-rounded-md tw-p-2"
                  placeholder="Nhập địa chỉ"
                  v-model="candidate.full_address"
                  @focusin="onFocusInput($event, true)"
                  @focusout="onFocusInput"
                ></textarea>
                <span v-if="errors.full_address" class="text-red tw-text-xs">*{{ errors.full_address }}</span>
              </label>
            </div>
            <div class="sp:tw-mt-1 tw-mt-3">
              <label class="tw-block">Ghi chú:
                <input
                  class="tw-border tw-border-gray-300 tw-pl-2
                    tw-bg-white tw-w-full tw-rounded-md tw-p-2"
                  placeholder="Ghi chú"
                  v-model="candidate.note"
                />
                <span v-if="errors.note" class="text-red tw-text-xs">*{{ errors.note }}</span>
              </label>
            </div>
            <div class="sp:tw-mt-1 tw-mt-5">
              Danh sách những lần apply:
              <table class="tw-w-full tw-border-collapse tw-border">
                <caption class="tw-hidden">Danh sách những lần apply</caption>
                <thead class="row thead-dark">
                  <th class="col-2 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Ngày phỏng vấn</th>
                  <th class="col-2 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Người phỏng vấn</th>
                  <th class="col-2 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Loại phỏng vấn</th>
                  <th class="col-2 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Tình trạng</th>
                  <th class="col-4 tw-py-1 tw-border-collapse tw-border tw-bg-blue-200">Nhận xét</th>
                </thead>
                <tbody v-if="(candidate.list_interview.length > 0)">
                  <tr class="row" v-for="interview in candidate.list_interview" :key="interview">
                    <td class="col-2 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.time.slice(0, 10) }}</td>
                    <td class="col-2 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.fullname }}</td>
                    <td class="col-2 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.type_kbn }}</td>
                    <td class="col-2 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.status }}</td>
                    <td class="col-4 tw-text-center tw-py-1 tw-border-collapse tw-border">{{ interview.comment }}</td>
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
          <q-btn class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" @click.prevent="validateCandidate()" label="Lưu"/>
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
        <q-td :props="props" class="tw-w-[70px]">
          {{ props.pageIndex + 1 }}
        </q-td>
      </template>
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách nhân viên</span>
        <q-form class="tw-inline-block sp:tw-ml-0 tw-ml-10 tw-translate-y-px">
          <q-input
            dense
            debounce="300"
            input-class="tw-py-0"
            v-model="dataSearch.search_key"
            placeholder="Tìm kiếm"
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
            hover:tw-underline-offset-1" @click.prevent="openModalCv(props.row.fullname, props.row.cv_file_path)">
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
        <q-td :props="props" class="tw-w-[200px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn
              class="sp:tw-text-[10px]"
              color="green-7"
              size="12px"
              @click.prevent="viewCandidates(props.row.id)"
            >
              <q-icon name="visibility" class="tw-mr-2"/>Xem
            </q-btn>
            <q-btn
              class="tw-text-[12px] sp:tw-text-[10px] tw-ml-3"
              color="red-7"
              icon="delete"
              @click="deleteStaff(props.row.id)"
            >
              Xóa
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

    <q-dialog v-model="modalInforEmpl">
      <q-card class="tw-min-w-[480px]">
        <q-card-section class="row items-center q-pb-lg tw-bg-[#17a2b8!important]">
          <div class="tw-text-[18px] text-white">Thông tin ứng viên {{ candidateInfor.fullname }}</div>
          <q-space />
        </q-card-section>

        <q-card-section>
          <div class="tw-divide-y tw-divide-slate-300 tw-mt-[-10px]">
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Họ tên:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.fullname }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Ngày sinh:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.birthday }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Vị trí:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.team }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Chức danh:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.position }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Số CCCD:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.identification_number }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Nơi cấp:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.place_issued_identification }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Ngày cấp:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.date_issued_identification }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">TK ngân hàng:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.bank_account }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Chi nhánh:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.bank_branch }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Biển số xe:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.vehicle_number }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Số điện thoại:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.telephone_no }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Email:</label>
              </div>
              <div class="tw-w-[200px] hidden-text">{{ candidateInfor.email }}</div>
            </div>
            <div class="sp:tw-mt-1 tw-flex tw-mx-[10px] tw-py-[10px] tw-bg-slate-100 tw-px-3">
              <div class="tw-w-[120px] tw-text-start tw-inline-block]">
                <label class="tw-font-bold" for="name">Ngày dự kiến đi làm:</label>
              </div>
              <div class="tw-w-[200px]">{{ candidateInfor.start_join_date }}</div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import {
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, LIST_CANDIDATE_STATUS_FAIL,
  GENDER,
} from 'utilities/const';
import candidateConfirmService from 'services/candidate-confirm.service';
import staffListService from 'services/staff-list.service';
import { searchItems } from 'utilities/common';
import positionService from 'services/position.service';
import officeService from 'services/office.service';
import teamService from 'services/team.service';
import { cloneDeep } from 'lodash';
import { useAuthStore } from 'stores/auth-store';
import toast from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

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
    name: 'application_date',
    align: 'left',
    label: 'Ngày apply',
    field: 'application_date',
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
const listRecommender = ref([]);
const records = ref([]);
const candidate = reactive({
  id: '',
  cv_file_path: '',
});
const loading = ref(true);
const modalInforEmpl = ref(false);

const candidateInfor = reactive({
  id: '',
  fullname: '',
  team: '',
  position: '',
  email: '',
  telephone_no: '',
  birthday: '',
  school: '',
  place_issued_identification: '',
  identification_number: '',
  date_issued_identification: '',
  start_join_date: '',
  class: '',
  bank_account: '',
  bank_branch: '',
  vehicle_number: '',
  faculty: '',
});

const qDateProxy = ref();

// 3) ======= METHOD/FUNCTION ========
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
const openModalCv = (fullname, cvFilePath) => {
  showDialogCv.value = true;
  candidate.fullname = fullname;
  candidate.cv_file_path = `${cvFilePath}/`;
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
  } else {
    // focusOut
    element.classList.remove('tw-border-sky-500', 'tw-outline-none');
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
  dataSearch.advance.previous_status = '';
  dataSearch.advance.status = '';
  dataSearch.advance.team = '';
  dataSearch.advance.gender = '';
  searchHandler();
};

/**
 * Handle show dialog edit candidate
 *
 * @param object row
 * @return void
 */
const deleteStaff = async (idCandidate) => {
  const isDelete = await staffListService.delete(idCandidate);
  if (isDelete === false) {
    toast.errors(MESSAGE.CANDIDATE.DELETE.ERROR);
    return;
  }

  rows.value.forEach((row, index) => {
    if (row.id === idCandidate) {
      rows.value.splice(index, 1);
    }
  });
  records.value.forEach((row, index) => {
    if (row.id === idCandidate) {
      records.value.splice(index, 1);
    }
  });

  toast.success(MESSAGE.CANDIDATE.DELETE.SUCCESS);
};

// View candidate
const viewCandidates = async (idCandidate) => {
  const infoCandidate = await candidateConfirmService.getConfirmCandidate(idCandidate);
  if (infoCandidate) {
    candidateInfor.id = infoCandidate.id;
    candidateInfor.fullname = infoCandidate.fullname;
    candidateInfor.team = infoCandidate.team;
    candidateInfor.position = infoCandidate.position;
    candidateInfor.email = infoCandidate.email;
    candidateInfor.telephone_no = infoCandidate.telephone_no;
    candidateInfor.birthday = infoCandidate.birthday;
    candidateInfor.school = infoCandidate.school;
    candidateInfor.place_issued_identification = infoCandidate.place_issued_identification;
    candidateInfor.identification_number = infoCandidate.identification_number;
    candidateInfor.date_issued_identification = infoCandidate.date_issued_identification;
    candidateInfor.school = infoCandidate.school;
    candidateInfor.start_join_date = infoCandidate.start_join_date;
    candidateInfor.class = infoCandidate.class;
    candidateInfor.bank_account = infoCandidate.bank_account;
    candidateInfor.bank_branch = infoCandidate.bank_branch;
    candidateInfor.vehicle_number = infoCandidate.vehicle_number;
    candidateInfor.faculty = infoCandidate.faculty;
    modalInforEmpl.value = true;
  }
};

// 4) ======= VUE JS LIFECYCLE ========
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

  const listCandidates = await staffListService.getList(false);

  if (listCandidates) {
    listRecommender.value = listCandidates.list_recommender;
    records.value = cloneDeep(listCandidates.item);
    rows.value = searchItems(dataSearch, records.value);
    rows.value.forEach((row) => {
      row.isFlagButton = false;
      CANDIDATE_STATUS.forEach((status) => {
        if (status.id === Number(row.status)) {
          row.status = status.name;
          if (LIST_CANDIDATE_STATUS_FAIL.includes(row.status)) {
            row.isFlagButton = true;
          }
        }
        if (status.id === Number(row.previous_status)) {
          row.previous_status = status.name;
        }
      });
    });
    totalRecord.value = rows.value.length;
    updatePaginate(rows.value.length);
  }
  loading.value = false;
});
</script>

<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Danh sách tất cả ứng viên</h1>
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
        <div class="tw-mr-4 sp:tw-mt-1">
          <label class="tw-block">Đã từng Apply:</label>
          <select
            id="position"
            class="tw-rounded-md tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1 tw-w-[100px]"
            @focusin="onFocusInput($event, true)"
            @focusout="onFocusInput"
            v-model="dataSearch.advance.previous_status"
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option v-for="(item_status) in CANDIDATE_STATUS" :key="item_status" :value="item_status.name">{{ item_status.name }}</option>
          </select>
        </div>
        <div class="tw-mr-4 sp:tw-mt-1">
          <label class="tw-block">Trạng thái:</label>
          <select
            id="position"
            class="tw-rounded-md tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1 tw-w-[100px]"
            @focusin="onFocusInput($event, true)"
            @focusout="onFocusInput"
            v-model="dataSearch.advance.status"
            @change="searchHandler()"
          >
            <option value="">Tất cả</option>
            <option v-for="(item_status) in CANDIDATE_STATUS" :key="item_status" :value="item_status.name">{{ item_status.name }}</option>
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
    <!-- Dialog popup black list -->
    <q-dialog v-model="isBlackList">
      <q-card style="width: 700px; max-width: 80vw; height: max-content">
        <q-card-section
          class="row items-center tw-bg-[#17a2b8!important]"
        >
          <div class="tw-text-[20px] text-white">
            Nguyên nhân <span class="text-red">(*)</span>
          </div>
          <q-space />
        </q-card-section>
        <q-card-section class="tw-w-full tw-h-[max-content]">
          <div class="tw-rounded tw-p-2">
            <div class="tw-justify-between">
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[100%] sp:tw-w-full">
                  <div class="tw-w-[100%] sp:tw-w-full">
                    <textarea
                      type="text"
                      v-model="candidateRemove.reason"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full tw-min-h-[100px]"
                    ></textarea>
                    <span class="text-red tw-text-xs">* Cần phải nhập lý do</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
        <q-card-actions align="center" class="tw-pb-[20px]">
          <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
          <q-btn :disable="true ? candidateRemove.reason : false"
            class="tw-bg-[#ff9800] tw-w-[100px] tw-text-white" :class="{'disabled': !candidateRemove.reason}" @click.prevent="moveBlackList()" label="Lưu"/>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dialog show cv -->
    <q-dialog v-model="showDialogCv">
      <q-card style="width: 900px; max-width: 80vw; height: max-content">
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
            Chỉnh sửa ứng viên {{ candidate.fullname }}
          </div>
          <q-space />
        </q-card-section>
        <q-card-section class="tw-w-full tw-h-[max-content]">
          <div class="tw-rounded tw-p-2">
            <div class="tw-justify-between">
              <!-- Full name and Email -->
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Họ tên <span class="text-red">(*)</span></label>
                    <input
                      type="text"
                      id="name"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px] tw-h-[31px]
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
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-h-[31px]
                        tw-py-[4px] tw-pl-2 tw-w-full tw-block"
                      v-model="candidate.email"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                    />
                    <span v-if="(errors.email)" class="text-red tw-text-xs">*{{ errors.email }}</span>
                  </div>
                </div>
              </div>
              <!-- Position and Team -->
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Chức danh <span class="text-red">(*)</span></label>
                    <select
                      class="tw-border tw-block tw-border-gray-300 tw-py-[4px] tw-pl-1 tw-h-[31px]
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
                      class="tw-border tw-border-gray-300 tw-py-[4px] tw-pl-1 tw-h-[31px]
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
              <!-- Telephone no and Status -->
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block tw-h-[25px]" for="name">Số điện thoại <span class="text-red">(*)</span></label>
                    <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px] tw-h-[31px]
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
                    <select
                      class="tw-rounded-md tw-border tw-w-full tw-border-gray-300 tw-py-[4px] tw-pl-2 tw-h-[31px]"
                      @focusin="onFocusInput($event, true)"
                      @focusout="onFocusInput"
                      v-model="candidate.status"
                      @change="searchHandler()"
                    >
                      <option value=""></option>
                      <option v-for="(item_status) in CANDIDATE_STATUS" :key="item_status" :value="item_status.name">{{ item_status.name }}</option>
                    </select>
                    <span v-if="(errors.status)" class="text-red tw-text-xs">*{{ errors.status }}</span>

                    <!-- <input
                      type="text"
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px]
                        tw-pl-2 tw-w-full tw-block tw-text-black"
                      v-model="candidate.status"
                    /> -->
                  </div>
                </div>
              </div>
              <!-- Recommender and Birthday -->
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block" for="name">Người giới thiệu:</label>
                    <select
                      class="tw-border tw-border-gray-300 tw-rounded-md tw-py-[4px] tw-h-[31px]
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
                      class="tw-pr-4 tw-pl-2 tw-py-[4px] tw-border tw-border-gray-300 tw-rounded-md tw-h-[31px]
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
              <!-- Application date and Upload CV -->
              <div class="tw-w-full tw-mb-4 row tw-justify-center">
                <div class="tw-w-[50%] sp:tw-w-full">
                  <div class="tw-w-[95%] sp:tw-w-full">
                    <label class="tw-block">Ngày apply: </label>
                    <div
                      class="tw-pr-4 tw-pl-2 tw-py-[4px] tw-border tw-border-gray-300 tw-rounded-md
                        tw-focus:tw-outline-none tw-text-gray-600 tw-h-[31px]"
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
                      tw-w-[280px] focus:tw-outline-none focus:tw-border-sky-500 tw-h-[31px]"
                      @change="uploadFile"
                    >
                    <span v-if="errors['cv_file/file']" class="text-red tw-text-xs">*{{ errors['cv_file/file']}}</span>
                  </div>
                </div>
              </div>
            </div>
            <!-- Address -->
            <div class="sp:tw-mt-1 tw-mt-3">
              <label class="tw-block">Địa chỉ <span class="text-red">(*)</span>
                <textarea
                  class="tw-border tw-border-gray-300 tw-pl-2 tw-max-h-[60px]
                    tw-bg-white tw-w-full tw-rounded-md tw-p-2"
                  placeholder="Nhập địa chỉ"
                  v-model="candidate.full_address"
                  @focusin="onFocusInput($event, true)"
                  @focusout="onFocusInput"
                ></textarea>
                <span v-if="errors.full_address" class="text-red tw-text-xs">*{{ errors.full_address }}</span>
              </label>
            </div>
            <!-- Note -->
            <div class="sp:tw-mt-1 tw-mt-3">
              <label class="tw-block">Ghi chú:
                <input
                  class="tw-border tw-border-gray-300 tw-pl-2 tw-h-[31px]
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
      <!-- Title table and btn search -->
      <template v-slot:top-left>
        <span class="q-table__title tw-inline-block">Danh sách ứng viên</span>
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
      <!-- Column serial -->
      <template v-slot:body-cell-serial="props">
        <q-td :props="props" class="tw-w-[70px]">
          {{ props.pageIndex + 1 }}
        </q-td>
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
      <!-- Field email -->
      <template v-slot:body-cell-email="props">
        <q-td :props="props" class="md:tw-w-[150px]">
          <p class="tooltip tw-w-[180px] tw-text-ellipsis tw-overflow-hidden">
            {{ props.row.email }}
            <span class="tooltiptext">{{  props.row.email }}</span>
          </p>
        </q-td>
      </template>
      <!-- Field action -->
      <template v-slot:body-cell-action="props">
        <q-td :props="props" class="md:tw-w-[200px]">
          <div class="sp:tw-w-[170px] md:tw-inline-block">
            <q-btn v-if="!props.row.isFlagButton"
              class="tw-text-[12px] tw-w-[130px!important] sp:tw-text-[10px]"
              color="green-7"
              icon="edit"
              @click="viewCandidate(props.row.id)"
            >
              Chỉnh sửa
            </q-btn>
            <q-btn v-else
              class="tw-text-[12px] tw-w-[130px!important] sp:tw-text-[10px] tw-bg-[#f1b315] text-white"
              icon="edit"
              @click="viewCandidate(props.row.id)"
            >
              Nhận lại CV
            </q-btn>
            <q-btn
              class="tw-text-[12px] tw-w-[100px!important] sp:tw-text-[10px] tw-ml-[5px]"
              color="red"
              icon="warning"
              @click="{candidateRemove.id = props.row.id; candidateRemove.reason = '';isBlackList = true;}"
            >
              DS Đen
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
  PAGINATION_DEFAULT, PERPAGE_OPTIONS, CANDIDATE_STATUS, LIST_CANDIDATE_STATUS_FAIL, MAX_SIZE_PDF,
  GENDER,
} from 'utilities/const';
import candidateListService from 'services/candidate-list.service';
import { MESSAGE } from 'utilities/message';
import { searchItems, setDataFile } from 'utilities/common';
import positionService from 'services/position.service';
import officeService from 'services/office.service';
import teamService from 'services/team.service';
import toast from 'utilities/toast';
import useMixin from 'mixins/common.js';
import { cloneDeep } from 'lodash';
import { useAuthStore } from 'stores/auth-store';
import useValidate from '../../composables/validate.js';
import editCandidateSchema from '../../validations/schemas/candidate/candidate_list.js';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const { user } = useAuthStore();
// ==> 1.2) actions
// ==> 1.3) Others
const { confirmPopup, countRecord } = useMixin();
const { errors, validate } = useValidate();

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
    name: 'previous_status',
    align: 'left',
    label: 'Đã từng apply',
    field: 'previous_status',
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
  fullname: '',
  email: '',
  birthday: '',
  full_address: '',
  position_id: '',
  recommender_id: '',
  status: '',
  team_id: '',
  telephone_no: '',
  cv_file_path: '',
  list_interview: [],
  file_size: '',
  file_ext: '',
  file: '',
  application_date: '',
});
const isBlackList = ref(false);
const loading = ref(true);
const flagCvFile = ref(true);
const textCvFile = ref('');
const candidateRemove = reactive({
  id: '',
  reason: '',
});
const qDateProxy = ref();

// 3) ======= METHOD/FUNCTION ========
// Set data cv file
const setDataCv = (input, e) => {
  const newInput = input;
  const dataFile = setDataFile(newInput.files[0], e.target.result);
  candidate.file_size = dataFile.size;
  candidate.file_ext = dataFile.ext;
  candidate.file = dataFile.name;
};

// Read file
const handleReadFile = (input) => {
  const reader = new FileReader();
  reader.onload = (e) => {
    setDataCv(input, e);
  };
  reader.readAsDataURL(input.files[0]);
};

// Check size and ext
const checkSizeAndExt = (fileSize, fileExt) => {
  // File size greater than 5mb or not pdf type
  // will return an error
  if ((fileSize !== '' && fileSize > MAX_SIZE_PDF)
  || (fileExt !== '' && fileExt !== 'pdf')) {
    flagCvFile.value = false;
    textCvFile.value = 'File không hợp lệ';
  }
};

// Validate upload file function
const checkFile = (input) => {
  const file = input.files[0];
  flagCvFile.value = true;
  textCvFile.value = '';
  const fileSize = file.size.toString();
  const arrFileExt = file.type.toString().split('/');
  const fileExt = arrFileExt[1].toString();

  checkSizeAndExt(fileSize, fileExt);
};

// Upload cv
const uploadFile = (event) => {
  const input = event.target;
  // Have upload file
  if (input.files[0]) {
    checkFile(input);
    // Flag check file are true will read file
    if (flagCvFile.value) {
      handleReadFile(input);
    } else {
      input.value = null;
    }
  }
};

/**
 * Handle show dialog edit candidate
 *
 * @param object row
 * @return void
 */
const viewCandidate = async (idCandidate) => {
  errors.value = {};
  const resultCandidate = await candidateListService.getCandidate(idCandidate);
  if (resultCandidate) {
    candidate.id = resultCandidate.candidate.id;
    candidate.fullname = resultCandidate.candidate.fullname;
    candidate.email = resultCandidate.candidate.email;
    candidate.birthday = resultCandidate.candidate.birthday.replaceAll('-', '/');
    candidate.full_address = resultCandidate.candidate.full_address;
    candidate.recommender_id = resultCandidate.candidate.recommender_id;
    CANDIDATE_STATUS.forEach((status) => {
      if (status.id === Number(resultCandidate.candidate.status)) {
        candidate.status = status.name;
        if (LIST_CANDIDATE_STATUS_FAIL.includes(candidate.status)) {
          candidate.status = CANDIDATE_STATUS[0].name;
        }
      }
    });
    candidate.team_id = resultCandidate.candidate.team_id;
    candidate.position_id = resultCandidate.candidate.position_id;
    candidate.telephone_no = resultCandidate.candidate.telephone_no;
    candidate.list_interview = resultCandidate.list_interview;
    candidate.cv_file_path = resultCandidate.cv_file_path;
    candidate.file_ext = '';
    candidate.file_size = '';
    candidate.file = '';
    candidate.application_date = resultCandidate.candidate.application_date.replaceAll('-', '/');
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
  rows.value.forEach((row, index) => {
    CANDIDATE_STATUS.forEach((status) => {
      if (status.id === Number(row.status)) {
        rows.value[index].status = status.name;
      }
      if (status.id === Number(row.previous_status)) {
        row.previous_status = status.name;
      }
    });
  });
  updatePaginate(rows.value.length);
};

const handleUpdateCandidate = async () => {
  const isEdit = await candidateListService.editCandidate(candidate);
  if (isEdit) {
    // Update data to records
    records.value.forEach((row, index) => {
      if (row.id === candidate.id) {
        records.value[index].fullname = candidate.fullname;
        records.value[index].email = candidate.email;
        records.value[index].telephone_no = candidate.telephone_no;
        records.value[index].isFlagButton = false;
        records.value[index].note = candidate.note;
        records.value[index].recommender_id = candidate.recommender_id ? candidate.recommender_id : 0;
        records.value[index].recommender_name = '';
        listRecommender.value.forEach((recommender) => {
          if (recommender.id === Number(candidate.recommender_id)) {
            records.value[index].recommender_name = recommender.fullname;
          }
        });
        listPosition.value.forEach((position) => {
          if (position.id === Number(candidate.position_id)) {
            records.value[index].position = position.name;
          }
        });
        listTeam.value.forEach((team) => {
          if (team.id === Number(candidate.team_id)) {
            records.value[index].team = team.name;
          }
        });
        CANDIDATE_STATUS.forEach((status) => {
          if (status.id === Number(candidate.status)) {
            records.value[index].status = status.name;
            if (CANDIDATE_STATUS.includes(records.value[index].status)) {
              row.isFlagButton = true;
            }
          }
        });
      }
    });

    // Update data to rows
    rows.value.forEach((row, index) => {
      if (row.id === candidate.id) {
        rows.value[index].fullname = candidate.fullname;
        rows.value[index].email = candidate.email;
        rows.value[index].telephone_no = candidate.telephone_no;
        rows.value[index].isFlagButton = false;
        rows.value[index].note = candidate.note;
        rows.value[index].recommender_id = candidate.recommender_id ? candidate.recommender_id : 0;
        rows.value[index].recommender_name = '';
        listRecommender.value.forEach((recommender) => {
          if (recommender.id === Number(candidate.recommender_id)) {
            rows.value[index].recommender_name = recommender.fullname;
          }
        });
        listPosition.value.forEach((position) => {
          if (position.id === Number(candidate.position_id)) {
            rows.value[index].position = position.name;
          }
        });
        listTeam.value.forEach((team) => {
          if (team.id === Number(candidate.team_id)) {
            rows.value[index].team = team.name;
          }
        });
        CANDIDATE_STATUS.forEach((status) => {
          if (status.id === Number(candidate.status)) {
            rows.value[index].status = status.name;
            if (CANDIDATE_STATUS.includes(rows.value[index].status)) {
              row.isFlagButton = true;
            }
          }
        });
      }
    });

    // Update count record of menu
    countRecord();

    toast.success(MESSAGE.CANDIDATE.UPDATE.SUCCESS);
    searchHandler();
    return;
  }
  toast.success(MESSAGE.CANDIDATE.UPDATE.ERROR);
};
const moveBlackList = async () => {
  const isRemove = await candidateListService.moveBlackList(candidateRemove);
  if (isRemove) {
    // Update data to records
    records.value.forEach((row, index) => {
      if (row.id === candidateRemove.id) {
        records.value.splice(index, 1);
      }
    });
    // Update data to rows
    rows.value.forEach((row, index) => {
      if (row.id === candidate.id) {
        rows.value.splice(index, 1);
      }
    });
    // Update count record of menu
    countRecord();

    toast.success(MESSAGE.CANDIDATE.MOVE_BLACK_LIST.SUCCESS);
    searchHandler();
    isBlackList.value = false;
    return;
  }
  toast.error(MESSAGE.CANDIDATE.MOVE_BLACK_LIST.ERROR);
};

/**
 * Handle show dialog confirm edit candidate
 *
 * @return void
 */
const validateCandidate = () => {
  // Convert status text to status int
  CANDIDATE_STATUS.forEach((status) => {
    if (status.name === candidate.status) {
      candidate.status = status.id;
    }
  });
  // Validate user
  const isValid = validate(editCandidateSchema, candidate);
  if (!isValid) {
    return;
  }

  showDialogEditCandidate.value = false;
  // Show confirm popup edit candidate
  confirmPopup(
    MESSAGE.CANDIDATE.UPDATE.CONFIRM_TITLE,
    MESSAGE.CANDIDATE.UPDATE.CONFIRM_QUESTION.replace(':name', candidate.fullname),
    handleUpdateCandidate,
  );
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

  const listCandidates = await candidateListService.getList(false);

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

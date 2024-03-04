<template>
  <q-form
    @submit="sendForm"
    class="tw-px-6 tw-py-4 tw-mt-5 bg-white tw-w-1/2 tw-m-auto
      tw-rounded-md tw-shadow-[1px_1px_20px_#c3c3c3a3]"
  >
    <div class="tw-text-center q-pa-sm">
      <h1 class="tw-text-2xl">Các thông tin để làm hợp đồng và các thủ tục trước khi trở thành nhân viên SSV</h1>
    </div>
    <div class="tw-mt-2">
      <table class="tw-w-full">
        <caption class="tw-hidden">Form nhập thông tin ứng viên</caption>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="name">
            Họ tên<span class="text-red">*</span>
          </th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.fullname"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.fullname ? '' : 'tw-h-4'"
            >{{ errors.fullname ? `*${errors.fullname}` : '' }}</span>
          </td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="birthday">
            Ngày sinh<span class="text-red">*</span>
          </th>
          <td>
            <div
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-border-gray-300 tw-rounded-md
                tw-focus:tw-outline-none tw-text-gray-600 tw-w-[250px]"
            >
              <input
                id="birthday"
                type="text"
                class="tw-outline-0 tw-w-[91%]"
                placeholder="yyyy/mm/dd"
                v-model.trim="formData.birthday"
                @focusin="onFocusInput($event, true)"
                @focusout="onFocusInput"
              >
              <q-icon name="event" class="cursor-pointer" size="xs">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyBirth">
                  <q-date :mask="FORMAT_DATE" v-model="formData.birthday" @update:model-value="qDateProxyBirth.hide()">
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </div>
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.birthday ? '' : 'tw-h-4'"
            >{{ errors.birthday ? `*${errors.birthday}` : '' }}</span>
          </td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="place_of_birth">
            Nơi sinh<span class="text-red">*</span>
          </th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.place_of_birth"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.place_of_birth ? '' : 'tw-h-4'"
            >{{ errors.place_of_birth ? `*${errors.place_of_birth}` : '' }}</span>
          </td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="address">
            Địa chỉ<span class="text-red">*</span>
          </th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.full_address"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.full_address ? '' : 'tw-h-4'"
            >{{ errors.full_address ? `*${errors.full_address}` : '' }}</span>
          </td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="id_number">
            Số CMND hoặc hộ chiếu<span class="text-red">*</span>
          </th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.identification_number"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.identification_number ? '' : 'tw-h-4'"
            >{{ errors.identification_number ? `*${errors.identification_number}` : '' }}</span>
          </td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="day_identity_id_number">
            Ngày cấp<span class="text-red">*</span>
          </th>
          <td>
            <div
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-border-gray-300 tw-rounded-md
                tw-focus:tw-outline-none tw-text-gray-600 tw-w-[250px]"
            >
              <input
                id="date_issued_identification"
                type="text"
                class="tw-outline-0 tw-w-[91%]"
                placeholder="yyyy/mm/dd"
                v-model.trim="formData.date_issued_identification"
                @focusin="onFocusInput($event, true)"
                @focusout="onFocusInput"
              >
              <q-icon name="event" class="cursor-pointer" size="xs">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyIdentity">
                  <q-date :mask="FORMAT_DATE" v-model="formData.date_issued_identification" @update:model-value="qDateProxyIdentity.hide()">
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </div>
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.date_issued_identification ? '' : 'tw-h-4'"
            >{{ errors.date_issued_identification ? `*${errors.date_issued_identification}` : '' }}</span>
          </td>
          <th
            class="tw-text-right tw-font-normal tw-pr-6"
            id="place_identity_id_number"
          >
            Nơi cấp<span class="text-red">*</span>
          </th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.place_issued_identification"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.place_issued_identification ? '' : 'tw-h-4'"
            >{{ errors.place_issued_identification ? `*${errors.place_issued_identification}` : '' }}</span>
          </td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="bank_acc_number">Số TK ngân hàng BIDV</th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.bank_account"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.bank_account ? '' : 'tw-h-4'"
            >{{ errors.bank_account ? `*${errors.bank_account}` : '' }}</span>
          </td>
          <th class="tw-font-normal tw-pr-6 tw-text-right" id="branch">Chi nhánh</th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.bank_branch"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.bank_branch ? '' : 'tw-h-4'"
            >{{ errors.bank_branch ? `*${errors.bank_branch}` : '' }}</span>
          </td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="license_plates">Biển số xe</th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              v-model="formData.vehicle_number"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.vehicle_number ? '' : 'tw-h-4'"
            >{{ errors.vehicle_number ? `*${errors.vehicle_number}` : '' }}</span>
          </td>
          <td><span>(Đăng ký logo gửi xe)</span></td>
        </tr>
        <tr>
          <th class="tw-text-left tw-font-normal tw-pr-6" id="phone_number">
            Số điện thoại<span class="text-red">*</span>
          </th>
          <td>
            <input
              type="text"
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-h-[36px] tw-w-[250px]
                tw-border-gray-300 tw-rounded-md tw-outline-none focus:tw-border-sky-500
                tw-outline-0 tw-text-gray-600"
              maxlength="11"
              v-model="formData.telephone_no"
            >
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.telephone_no ? '' : 'tw-h-4'"
            >{{ errors.telephone_no ? `*${errors.telephone_no}` : '' }}</span>
          </td>
          <th class="tw-text-right tw-font-normal tw-pr-6" id="start_join">
            Ngày đi làm dự kiến<span class="text-red">*</span>
          </th>
          <td>
            <div
              class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-border-gray-300 tw-rounded-md
                tw-focus:tw-outline-none tw-text-gray-600 tw-w-[250px]"
            >
              <input
                id="start_join_date"
                type="text"
                class="tw-outline-0 tw-w-[91%]"
                placeholder="yyyy/mm/dd"
                v-model.trim="formData.start_join_date"
                @focusin="onFocusInput($event, true)"
                @focusout="onFocusInput"
              >
              <q-icon name="event" class="cursor-pointer" size="xs">
                <q-popup-proxy cover transition-show="scale" transition-hide="scale" ref="qDateProxyJoin">
                  <q-date :mask="FORMAT_DATE" v-model="formData.start_join_date" @update:model-value="qDateProxyJoin.hide()">
                  </q-date>
                </q-popup-proxy>
              </q-icon>
            </div>
            <span
              class="text-red tw-text-xs tw-block tw-ml-1"
              :class="errors.start_join_date ? '' : 'tw-h-4'"
            >{{ errors.start_join_date ? `*${errors.start_join_date}` : '' }}</span>
          </td>
        </tr>
      </table>
    </div>
    <div class="tw-italic tw-leading-7">
      <strong>Lưu ý:</strong>
      <ul class="tw-list-[auto!important]">
        <li>Trong tuần đầu tiên đi làm, nhân viên cần nộp đầy đủ hồ sơ xin việc bao gồm
          <ul class="tw-list-[lower-alpha!important]">
            <li>Sơ yếu lý lịch có xác nhận của chính quyền địa phương (có hiệu lực trong thời gian 6 tháng).</li>
            <li>Bản sao giấy chứng minh nhân dân.</li>
            <li>Bản sao công chứng giấy khai sinh.</li>
            <li>Giấy chứng nhận sức khỏe cấp bởi cơ quan y tế có thẩm quyền (trong thời gian 03 tháng).</li>
            <li>Bản sao công chứng các văn bằng chứng chỉ có liên quan.</li>
            <li>Đơn xin việc bằng tiếng Việt hoặc tiếng Anh hoặc tiếng Nhật</li>
            <li>Bản sao bằng lái xe máy hoặc ô tô</li>
          </ul>
        </li>
        <li>
          Saishunkan System Việt Nam thanh toán lương qua hình thức chuyển khoản qua ngân hàng <strong>BIDV</strong>
          do đó trước khi vào làm tại Công ty ứng viên cần mở tài khoản tại các chi nhánh của BIDV.
        </li>
      </ul>
    </div>
    <button class=" tw-mt-3 tw-rounded-md tw-px-3 tw-py-2 text-white bg-green-7">Gửi thông tin</button>
  </q-form>
</template>

<script setup>
import { reactive, ref } from 'vue';
import useValidate from 'composables/validate';
import formCandidateSchema from 'schemas/form-candidate';
import candidateService from 'services/candidate.service';
import { candidateStore } from 'stores/candidate-store';
import { FORMAT_DATE } from 'utilities/const';
import dayjs from 'utilities/day';
import { useRouter } from 'vue-router';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const { candidate } = candidateStore();
// ==> 1.2) actions
// ==> 1.3) Others
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF, REACTIVE ========
const router = useRouter();
const idInputsDate = ['birthday', 'date_issued_identification', 'start_join_date'];
const formData = reactive({
  fullname: candidate.fullname,
  birthday: dayjs(candidate.birthday).format(FORMAT_DATE),
  place_of_birth: candidate.place_of_birth,
  full_address: candidate.full_address,
  identification_number: candidate.identification_number,
  date_issued_identification: candidate.date_issued_identification
    ? dayjs(candidate.date_issued_identification).format(FORMAT_DATE) : '',
  place_issued_identification: candidate.place_issued_identification,
  bank_account: candidate.bank_account,
  bank_branch: candidate.bank_branch,
  vehicle_number: candidate.vehicle_number,
  telephone_no: candidate.telephone_no,
  start_join_date: dayjs(candidate.start_join_date).format(FORMAT_DATE),
});

const qDateProxyBirth = ref();
const qDateProxyIdentity = ref();
const qDateProxyJoin = ref();

// 3) ======= FUNCTION ========
const sendForm = async () => {
  const isValid = validate(formCandidateSchema, formData);
  if (!isValid) {
    return;
  }
  const query = window.location.href.split('?');
  const urlParams = new URLSearchParams(`?${query[1]}`);
  const token = urlParams.get('token');
  const response = await candidateService.editForm(token, formData);

  if (response) {
    router.push('/form-success');
  }
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
</script>

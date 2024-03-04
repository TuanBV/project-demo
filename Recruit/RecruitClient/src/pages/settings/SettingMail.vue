<template>
  <div class="q-pa-md">
    <h1 class="tw-text-2xl">Cài đặt mail cho các văn phòng</h1>
    <q-form class="tw-w-[500px] tw-pt-3" @submit="updateSettingMail(OFFICES.HANOI)">
      <label class="tw-leading-loose">Email của văn phòng Hà Nội:</label>
      <input
        type="text"
        class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-w-full tw-border-gray-300 tw-rounded-md
          tw-outline-0 tw-text-gray-600 focus:tw-border-sky-500 tw-outline-none"
        v-model.trim="mailsHanoi.mail_hanoi"
      >
      <span
        class="text-red tw-text-xs tw-block tw-ml-1"
        :class="!errors.mail ? 'tw-h-[16px]' : ''"
      >
        {{ errors.mail_hanoi ? `*${errors.mail_hanoi}` : '' }}
      </span>
      <label class="tw-leading-loose">Password Email văn phòng Hà Nội:</label>
      <input
        type="password"
        class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-w-full tw-border-gray-300 tw-rounded-md
          tw-outline-0 tw-text-gray-600 focus:tw-border-sky-500 tw-outline-none"
        v-model.trim="mailsHanoi.password_hanoi"
      >
      <span
        class="text-red tw-text-xs tw-block tw-ml-1"
        :class="!errors.password_hanoi ? 'tw-h-[16px]' : ''"
      >
        {{ errors.password_hanoi ? `*${errors.password_hanoi}` : '' }}
      </span>
      <q-btn class="tw-mt-[2px] bg-green-7 tw-text-white" label="Cập nhật" type="submit"/>
    </q-form>
    <q-form class="tw-w-[500px] tw-pt-3" @submit="updateSettingMail(OFFICES.HUE)">
      <label class="tw-leading-loose">Email của văn phòng Huế:</label>
      <input
        type="text"
        class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-w-full tw-border-gray-300 tw-rounded-md
          tw-outline-0 tw-text-gray-600 focus:tw-border-sky-500 tw-outline-none"
        v-model.trim="mailsHue.mail_hue"
      >
      <span
        class="text-red tw-text-xs tw-block tw-ml-1"
        :class="!errors.mail_hue ? 'tw-h-[16px]' : ''"
      >
        {{ errors.mail_hue ? `*${errors.mail_hue}` : '' }}
      </span>
      <label class="tw-leading-loose">Password Email văn phòng Huế:</label>
      <input
        type="password"
        class="tw-pr-4 tw-pl-2 tw-py-2 tw-border tw-w-full tw-border-gray-300 tw-rounded-md
          tw-outline-0 tw-text-gray-600 focus:tw-border-sky-500 tw-outline-none"
        v-model.trim="mailsHue.password_hue"
      >
      <span
        class="text-red tw-text-xs tw-block tw-ml-1"
        :class="!errors.password_hue ? 'tw-h-[16px]' : ''"
      >
        {{ errors.password_hue ? `*${errors.password_hue}` : '' }}
      </span>
      <q-btn class="tw-mt-[2px] bg-green-7 tw-text-white" label="Cập nhật" type="submit"/>
    </q-form>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import useValidate from 'composables/validate';
import useMixin from 'mixins/common';
import { MESSAGE } from 'utilities/message';
import { OFFICES } from 'utilities/const';
import officeService from 'services/office.service';
import settingMailSchema from 'schemas/setting/setting-mail';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
// ==> 1.2) actions
// ==> 1.3) Others
const { confirmPopup } = useMixin();
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF ========
const mailsHanoi = reactive({
  mail_hanoi: '',
  password_hanoi: '',
  office: OFFICES.HANOI,
});

const mailsHue = reactive({
  mail_hue: '',
  password_hue: '',
  office: OFFICES.HUE,
});

const officeSetting = ref(OFFICES.HANOI);

// 3) ======= METHOD/FUNCTION ========
/**
 * Handle update setting mail
 */
const handleUpdateSettingMail = () => {
  let dataMail = {
    mail: mailsHanoi.mail_hanoi,
    password: mailsHanoi.password_hanoi,
    office: mailsHanoi.office,
  };

  if (officeSetting.value === OFFICES.HUE) {
    dataMail = {
      mail: mailsHue.mail_hue,
      password: mailsHue.password_hue,
      office: mailsHue.office,
    };
  }

  officeService.updateMails(dataMail);
};

/**
 * Validate and show confirm popup update setting mail
 */
const updateSettingMail = (office) => {
  let dataMail = mailsHanoi;
  let schemaValidate = settingMailSchema.settingMailHanoiSchema;
  officeSetting.value = OFFICES.HANOI;

  if (office === OFFICES.HUE) {
    dataMail = mailsHue;
    schemaValidate = settingMailSchema.settingMailHueSchema;
    officeSetting.value = OFFICES.HUE;
  }

  const isValid = validate(schemaValidate, dataMail);
  if (!isValid) {
    return;
  }
  confirmPopup(
    MESSAGE.SETTING_MAIL.CONFIRM.CONFIRM_TITLE,
    MESSAGE.SETTING_MAIL.CONFIRM.CONFIRM_QUESTION,
    handleUpdateSettingMail,
  );
};

// 4) ======= VUEJS LIFECYCLE ========
onMounted(async () => {
  const offices = await officeService.getMails();
  mailsHanoi.mail_hanoi = offices[0].mail_admin;
  mailsHue.mail_hue = offices[1].mail_admin;
});
</script>

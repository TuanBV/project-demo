<template>
  <q-form
    @submit="sendMailForgotPassword"
    class="tw-px-6 tw-py-4 tw-w-96 bg-white
      tw-rounded-md tw-shadow-[1px_1px_2px_#bbb5b5]"
  >
    <div class="tw-text-center q-pa-sm">
      <p class="tw-text-xl">Quên mật khẩu</p>
    </div>
    <div class="tw-mt-2">
      <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]">Mail</span>
      <q-input
        outlined
        v-model.trim="email"
        autocomplete="off"
        lazy-rules
        maxlength="256"
        :error="!!errors.email"
        :error-message="errors.email"
      >
        <template v-slot:prepend>
          <q-icon color="" name="person" />
        </template>
      </q-input>
    </div>
    <div class="text-center">
      <q-btn
        class="tw-w-full q-mt-md tw-py-2"
        :label="labelSendMail"
        type="submit"
        color="primary"
        size="md"
        :disable="disableSendMail"
      />
    </div>
    <div class="tw-mt-2 tw-text-center">
      <router-link to="/login">Đăng nhập</router-link>
    </div>
  </q-form>
</template>

<script setup>
import { ref } from 'vue';
import useValidate from 'composables/validate';
import forgotPasswordSchema from 'schemas/auth/forgot-password';
import userService from 'services/user.service';
import { MESSAGE } from 'src/shared/utilities/message';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
// ==> 1.2) actions
// ==> 1.3) Others
const { errors, validate } = useValidate();

// 2) ======= VARIABLE REF, REACTIVE ========
const email = ref('');
const labelBtn = 'Gửi mail';
const labelSendMail = ref(labelBtn);
const disableSendMail = ref(false);

// 3) ======= FUNCTION ========
const sendMailForgotPassword = async () => {
  const isValid = validate(forgotPasswordSchema, { email: email.value });
  if (!isValid) {
    return;
  }
  const sent = await userService.forgotPassword(email.value);
  if (sent) {
    disableSendMail.value = true;
    let countdown = 60;
    const interval = setInterval(() => {
      if (countdown > 0) {
        labelSendMail.value = MESSAGE.FORGOT_PASSWORD.LABEL_SEND_MAIL.replace(':countdown', countdown);
        countdown--;
      } else {
        clearInterval(interval);
        labelSendMail.value = labelBtn;
        disableSendMail.value = false;
      }
    }, 1000);
  }
};
</script>

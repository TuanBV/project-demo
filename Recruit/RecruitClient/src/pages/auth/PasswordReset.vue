<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container class="tw-bg-gradient-to-r tw-from-[#54a3bd] tw-to-[#f3eeee]">
      <div
        class="window-height window-width tw-flex tw-justify-center
        tw-items-center sp:tw-px-3"
      >
        <q-form
          @submit="sendMailForgotPassword"
          class="tw-px-6 tw-py-4 tw-w-96 bg-white
            tw-rounded-md tw-shadow-[1px_1px_2px_#bbb5b5]"
        >
          <div class="tw-text-center q-pa-sm">
            <p class="tw-text-xl">Đặt lại mật khẩu</p>
          </div>
          <div class="tw-mt-2">
            <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]">Mật khẩu</span>
            <q-input
              :type="showNewPassword ? 'text' : 'password'"
              outlined
              v-model.trim="formPasswordReset.new_password"
              autocomplete="off"
              lazy-rules
              maxlength="24"
              :error="!!errors.new_password"
              :error-message="errors.new_password"
            >
              <template v-slot:prepend>
                <q-icon color="" name="lock" />
              </template>
              <template v-slot:append>
                <q-icon
                  :name="showNewPassword ? 'visibility_off' : 'visibility'"
                  @click="showNewPassword = !showNewPassword"
                  left
                  class="cursor-pointer"
                />
              </template>
            </q-input>
          </div>
          <div class="tw-mt-2">
            <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]">Nhập lại mật khẩu</span>
            <q-input
              :type="showConfirmPassword ? 'text' : 'password'"
              outlined
              v-model.trim="formPasswordReset.confirm_password"
              autocomplete="off"
              lazy-rules
              maxlength="24"
              :error="!!errors.confirm_password"
              :error-message="errors.confirm_password"
            >
              <template v-slot:prepend>
                <q-icon color="" name="lock" />
              </template>
              <template v-slot:append>
                <q-icon
                  :name="showConfirmPassword ? 'visibility_off' : 'visibility'"
                  @click="showConfirmPassword = !showConfirmPassword"
                  left
                  class="cursor-pointer"
                />
              </template>
            </q-input>
          </div>
          <div class="text-center">
            <q-btn
              class="tw-w-full q-mt-md tw-py-2"
              label="Đặt lại"
              type="submit"
              color="primary"
              size="md"
            />
          </div>
          <div class="tw-mt-2 tw-text-center">
            <router-link to="/login">Đăng nhập</router-link>
          </div>
        </q-form>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, reactive } from 'vue';
import useValidate from 'composables/validate';
import passwordResetSchema from 'schemas/auth/password-reset';
import userService from 'services/user.service';
import { useRouter } from 'vue-router';
import toast from 'utilities/toast';
import { MESSAGE } from 'utilities/message';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
// ==> 1.2) actions
// ==> 1.3) Others
const { errors, validate } = useValidate();
const router = useRouter();

// 2) ======= VARIABLE REF, REACTIVE ========
const formPasswordReset = reactive({
  new_password: '',
  confirm_password: '',
});
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);

// 3) ======= FUNCTION ========
const sendMailForgotPassword = async () => {
  const isValid = validate(passwordResetSchema, {
    new_password: formPasswordReset.new_password,
    confirm_password: formPasswordReset.confirm_password,
  });
  if (!isValid) {
    return;
  }

  const query = window.location.href.split('?');
  const urlParams = new URLSearchParams(`?${query[1]}`);
  const reseted = userService.resetPassword(urlParams.get('token'), formPasswordReset);
  if (reseted) {
    toast.success(MESSAGE.RESET_PASSWORD.SUCCESS);
    router.push('/login');
  }
};
</script>

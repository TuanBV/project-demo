<template>
  <q-form
    @submit="login"
    class="tw-px-6 tw-py-4 tw-w-96 bg-white
      tw-rounded-md tw-shadow-[1px_1px_2px_#bbb5b5]"
  >
    <div class="tw-text-center q-pa-sm">
      <p class="tw-text-xl">Đăng nhập</p>
    </div>
    <div class="tw-mt-2">
      <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]">Mail</span>
      <q-input
        outlined
        v-model.trim="formData.email"
        autocomplete="off"
        lazy-rules
        maxlength="255"
        :error="!!errors.email"
        :error-message="errors.email"
      >
        <template v-slot:prepend>
          <q-icon color="" name="person" />
        </template>
      </q-input>
    </div>
    <div class="tw-mt-2">
      <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]"
        >Password</span
      >
      <q-input
        outlined
        v-model="formData.password"
        autocomplete="off"
        :type="showPassword ? 'text' : 'password'"
        lazy-rules
        maxlength="64"
        :error="!!errors.password"
        :error-message="errors.password"
      >
        <template v-slot:prepend>
          <q-icon color="" name="lock" />
        </template>
        <template v-slot:append>
          <q-icon
            :name="showPassword ? 'visibility_off' : 'visibility'"
            @click="showPassword = !showPassword"
            left
            class="cursor-pointer"
          />
        </template>
      </q-input>
    </div>
    <div class="text-center">
      <q-btn
        :class="{'disabled' : !formData.email && !formData.password}"
        class="tw-w-full q-mt-md tw-py-2"
        label="Login"
        type="submit"
        color="primary"
        size="md"
      />
    </div>
    <div class="tw-mt-2 tw-text-center">
      <router-link to="forgot-password">Quên mật khẩu</router-link>
    </div>
  </q-form>
</template>

<script setup>
import { ref, reactive } from 'vue';
import useValidate from 'composables/validate';
import loginSchema from 'schemas/auth/login';
import toast from 'utilities/toast';
import { MESSAGE } from 'utilities/message';
import { useRouter } from 'vue-router';
import userService from 'services/user.service';
import { POSITION_ID } from 'utilities/const';

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
// ==> 1.2) actions
// ==> 1.3) Others
const { errors, validate } = useValidate();
const router = useRouter();

// 2) ======= VARIABLE REF, REACTIVE ========
const formData = reactive({
  email: '',
  password: '',
});
const showPassword = ref(false);

// 3) ======= FUNCTION ========
const login = async () => {
  const isValid = validate(loginSchema, formData);
  if (!isValid) {
    return;
  }
  // send login request
  const user = await userService.login(formData);
  if (user) {
    toast.success(MESSAGE.LOGIN_SUCCESSFULLY);
    if (user.position_id === POSITION_ID.ADMIN || user.position_id === POSITION_ID.MANAGER || user.position_id === POSITION_ID.LEADER) {
      router.push('/');
    } else {
      router.push('/add-cv');
    }
  }
};
</script>

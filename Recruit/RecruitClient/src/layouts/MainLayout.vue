<template>
  <q-layout view="hHh lpR fFf" class="bg-grey-1">
    <q-drawer v-model="drawerOpen" show-if-above class="bg-white" :width="300">
      <q-scroll-area class="fit">
        <q-img no-spinner src="https://cdn.quasar.dev/img/material.png" class="tw-h-[140px]">
          <div
            class="tw-absolute tw-top-1/2 bg-transparent tw-p-[0_4px_!important]
              -tw-translate-y-1/2 tw-h-fit"
          >
            <q-avatar size="56px" class="tw-inline-block tw-mr-2">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png" alt="">
            </q-avatar>
            <q-btn-dropdown
              color="green-7"
              size="10px"
              :label="user.fullname"
              class="tw-inline-block"
            >
              <q-list>
                <q-item clickable v-close-popup @click="showDialogChangePassword">
                  <q-item-section>
                    <q-item-label>Đổi mật khẩu</q-item-label>
                  </q-item-section>
                </q-item>
                <q-item clickable v-close-popup @click="logOut">
                  <q-item-section>
                    <q-item-label>Đăng xuất</q-item-label>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-btn-dropdown>
          </div>
        </q-img>
        <!-- List Function -->
        <q-list class="rounded-borders">
          <template v-for="(item) in items" :key="item">
            <q-expansion-item
              v-if="item.role"
              expand-separator
              square
              class="text-blue-grey-7 border-aea7a7"
              :icon="item.icon"
              :label="item.text"
              :default-opened="defaultOpenedExpansionItem(item)"
              :hide-expand-icon="!!item.route_name"
              :class="currentRouterName === item.route_name ? 'bg-blue-grey-1' : ''"
              :to="item.route_name ? { name: item.route_name } : undefined"
            >
              <q-item
                v-for="child in item.children" :key="child"
                class="tw-pl-[10%] text-blue-grey-7"
                :class="currentRouterName === child.route_name ? 'bg-blue-grey-1 tw-text-[#1976D2!important]' : ''"
                :to="{ name: child.route_name }"
              >
                <q-item-section avatar>
                  <q-icon :name="child.icon" />
                </q-item-section>
                <q-item-section>
                  <q-item-label>
                    {{ child.text }}
                    <span v-if="countRecord && countRecord[child.route_name]" class="tw-min-w-[20px] tw-h-[20px] tw-border-none tw-text-center
                      tw-text-white tw-inline-block tw-text-[10px] tw-rounded-[50%] tw-bg-[#db2828] tw-leading-[20px] tw-ml-[10px]
                    ">{{ countRecord[child.route_name] }}</span>
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-expansion-item>
          </template>
        </q-list>
      </q-scroll-area>
    </q-drawer>
    <!-- Dialog add recommender -->
    <q-dialog v-model="dialogChangePassword">
      <q-card class="tw-mt-[-120px]">
        <q-card-section class="row tw-align-center tw-bg-[#17a2b8]">
          <span class="tw-text-sm tw-text-white tw-text-[18px]">
            Đổi mật khẩu
          </span>
        </q-card-section>
        <q-form
          @submit="changePassword"
          class="tw-px-6 tw-py-4 tw-w-96"
        >
          <div class="tw-mt-2">
            <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]">
              Mật khẩu<span class="text-red">*</span>
            </span>
            <q-input
              :type="showPassword ? 'text' : 'password'"
              outlined
              v-model.trim="formChangePassword.password"
              autocomplete="off"
              lazy-rules
              maxlength="64"
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
            <span v-if="errors.password" class="text-red tw-text-xs">*{{ errors.password }}</span>
          </div>
          <div class="tw-mt-2">
            <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]">
              Mật khẩu mới<span class="text-red">*</span>
            </span>
            <q-input
              :type="showNewPassword ? 'text' : 'password'"
              outlined
              v-model.trim="formChangePassword.new_password"
              autocomplete="off"
              lazy-rules
              maxlength="64"
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
            <span v-if="errors.new_password" class="text-red tw-text-xs">*{{ errors.new_password }}</span>
          </div>
          <div class="tw-mt-2">
            <span class="tw-font-bold tw-text-sm tw-text-[#4B5C6B]">
              Nhập lại mật khẩu<span class="text-red">*</span>
            </span>
            <q-input
              :type="showConfirmPassword ? 'text' : 'password'"
              outlined
              v-model.trim="formChangePassword.confirm_password"
              autocomplete="off"
              lazy-rules
              maxlength="64"
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
            <span v-if="errors.confirm_password" class="text-red tw-text-xs">*{{ errors.confirm_password }}</span>
          </div>
          <q-card-actions align="center" class="tw-pb-[10px] tw-pt-[10px]">
            <q-btn color="red" label="Thoát" class="tw-w-[100px]" v-close-popup />
            <q-btn color="green-7" type="submit" label="Đổi mật khẩu"/>
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>
    <q-page-container>
      <q-page>
        <q-toolbar class="tw-bg-[#549CB9] tw-text-slate-50">
          <q-btn flat round dense icon="menu" class="q-mr-sm" @click="openDrawer"></q-btn>
          <q-toolbar-title>Saishunkan System</q-toolbar-title>
        </q-toolbar>
        <router-view />
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import {
  ref, reactive, computed,
} from 'vue';
import { useAuthStore } from 'stores/auth-store';
import { useAppStore } from 'stores/app-store';
import { countStore } from 'stores/count-store';
import UserService from 'services/user.service';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import useValidate from 'composables/validate';
import changePasswordSchema from 'schemas/auth/change-password';
import { POSITION_ID } from 'utilities/const';
// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const { user } = useAuthStore();
const { currentRouterName } = storeToRefs(useAppStore());
// ==> 1.2) Others
const { errors, validate } = useValidate();
const router = useRouter();

// 2) ======= VARIABLE REF ========
const drawerOpen = ref(false);
const dialogChangePassword = ref(false);
const formChangePassword = reactive({
  password: '',
  new_password: '',
  confirm_password: '',
});
const showPassword = ref(false);
const showNewPassword = ref(false);
const showConfirmPassword = ref(false);
let items = [
  {
    icon: 'web',
    text: 'Quản lí cv',
    role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER, POSITION_ID.STAFF, POSITION_ID.COLLABORATORS, POSITION_ID.INTERN].includes(user.position_id),
    children: [
      {
        icon: 'content_copy',
        text: 'Nhập thông tin CV',
        route_name: 'add_cv',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER, POSITION_ID.STAFF, POSITION_ID.COLLABORATORS, POSITION_ID.INTERN].includes(user.position_id),
      },
      {
        icon: 'playlist_add_check',
        text: 'Liên hệ ứng viên',
        route_name: 'contact_candidate',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'drive_file_rename_outline',
        text: 'Duyệt bài test',
        route_name: 'confirm_test',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'email',
        text: 'Mời phỏng vấn',
        route_name: 'invite_interview',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'calendar_month',
        text: 'Quản lý lịch phỏng vấn',
        route_name: 'interview_schedule',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'rate_review',
        text: 'Đánh giá ứng viên',
        route_name: 'candidate_assessment',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'forward_to_inbox',
        text: 'Gửi kết quả',
        route_name: 'send_results',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'fact_check',
        text: 'Cập nhật trạng thái offer',
        route_name: 'update_offers',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'library_add',
        text: 'Gửi link form',
        route_name: 'send_forms',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'how_to_reg',
        text: 'Duyệt thông tin ứng viên',
        route_name: 'candidate_confirm',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'checklist',
        text: 'DS ứng viên đã pass',
        route_name: 'candidate_pass_list',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'people',
        text: 'DS tất cả ứng viên',
        route_name: 'candidate_list',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'people',
        text: 'DS Nhân viên',
        route_name: 'staff_list',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'warning',
        text: 'Danh sách đen',
        route_name: 'black_list',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
    ],
  },
  {
    icon: 'account_circle',
    text: 'Quản lí users',
    role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
    route_name: 'list_user',
  },
  {
    icon: 'supervisor_account',
    text: 'Quản lí người giới thiệu',
    route_name: 'recommender',
    role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
  },
  {
    icon: 'settings',
    text: 'Cài đặt',
    role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
    children: [
      {
        icon: 'email',
        text: 'Cài đặt mail mẫu',
        route_name: 'list_template',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'settings_suggest',
        text: 'Danh sách param',
        route_name: 'list_param',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
      {
        icon: 'alternate_email',
        text: 'Setting mail',
        route_name: 'setting_mail',
        role: [POSITION_ID.ADMIN, POSITION_ID.MANAGER, POSITION_ID.LEADER].includes(user.position_id),
      },
    ],
  },
];

items = items.filter((item) => {
  if (item.children) {
    item.children = item.children.filter((child) => child.role);
  }
  return item;
});

const countRecord = computed(() => {
  const { count } = countStore();
  return count;
});
// 3) ======= METHOD/FUNCTION ========
const openDrawer = () => {
  drawerOpen.value = !drawerOpen.value;
};

/**
 * Handle user logout
 */
const logOut = async () => {
  const logout = await UserService.logout();
  if (logout) {
    router.push('/login');
  }
};

/**
 * Handle validate and change password
 */
const changePassword = async () => {
  const isValid = validate(changePasswordSchema, formChangePassword);
  if (!isValid) {
    return;
  }

  dialogChangePassword.value = false;
  const changed = await UserService.changePassword(formChangePassword);
  if (!changed) {
    dialogChangePassword.value = true;
  }
};

/**
 * Show dialog change password and clear errors, inputs
 */
const showDialogChangePassword = () => {
  errors.value = {};
  formChangePassword.password = '';
  formChangePassword.new_password = '';
  formChangePassword.confirm_password = '';
  showPassword.value = false;
  showNewPassword.value = false;
  showConfirmPassword.value = false;
  dialogChangePassword.value = true;
};

/**
 * Check default opened expansion item by route name
 *
 * @param {object} item
 * @return {boolean}
 */
const defaultOpenedExpansionItem = (item) => {
  let find = false;
  if (item.children) {
    item.children.forEach((child) => {
      if (child.route_name === currentRouterName.value) {
        find = true;
      }
    });
  }
  return find;
};
</script>

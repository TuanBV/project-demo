<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import userService from 'service/user.service'
import { useRouter } from 'vue-router'
import ToastUtil from 'utility/toast'

const router = useRouter()
const { locale } = useI18n()
const menu = ref([
  {
    name: 'nav.user',
    to: '/v1/admin/user',
    icon: 'user',
  },
  {
    name: 'nav.category',
    to: '/v1/admin/category',
    icon: 'list',
  },
  {
    name: 'nav.product',
    to: '/v1/admin/product',
    icon: 'box-archive',
  },
  {
    name: 'nav.order',
    to: '/v1/admin/order',
    icon: 'cart-shopping',
  },
  {
    name: 'nav.blog',
    to: '/v1/admin/blog',
    icon: 'blog',
  },
  {
    name: 'nav.slide',
    to: '/v1/admin/slide',
    icon: 'image',
  },
  {
    name: 'nav.email',
    to: '/v1/admin/email',
    icon: 'envelope',
  },
  {
    name: 'nav.post',
    to: '/v1/admin/post',
    icon: 'clipboard',
  },
  {
    name: 'nav.sale',
    to: '/v1/admin/sale',
    icon: 'percent',
  },
  {
    name: 'nav.chat',
    to: '/v1/admin/chat',
    icon: 'comments',
  },
])

const changeLanguage = () => {
  locale.value = locale.value === 'vi' ? 'en' : 'vi'
}

const logout = async () => {
  const res = await userService.logout()
  if (res) {
    ToastUtil.success('Log out successfully !!!')
    // Move to sign in page
    router.push('/v1/admin/sign-in')
  }
}
</script>
<template>
  <div class="col-span-1 bg-white">
    <div class="flex h-full w-full flex-col border-r bg-[#F9FBFF] p-2 dark:bg-gray-900">
      <!-- Logo -->
      <router-link to="/v1/admin" class="flex items-center justify-center">
        <img loading="lazy" src="assets/logo.svg" alt="" srcset="" width="70px" height="70px" />
      </router-link>

      <div
        class="flex h-full flex-grow flex-col justify-between overflow-y-auto overflow-x-hidden pt-2"
      >
        <div class="mx-1 flex flex-col space-y-1 pc:mt-1">
          <router-link
            v-for="(item, index) in menu"
            :key="index"
            class="hover:text-primary-400 flex h-12 cursor-pointer flex-row items-center justify-center rounded-md pr-3.5 font-semibold text-gray-500 focus:outline-none pc:justify-start pc:pr-6"
            :to="item.to"
            ><span class="ml-3.5 inline-flex items-center justify-center"
              ><font-awesome-icon :icon="['fas', item.icon]" class="h-4 w-4" /></span
            ><span class="ml-2 hidden truncate text-base font-normal capitalize pc:ml-2 pc:block">{{
              $t(item.name)
            }}</span></router-link
          >
        </div>
        <div class="mx-1 flex flex-col space-y-1 pc:mt-1">
          <select
            @change.prevent="changeLanguage"
            class="mx-3 h-12 cursor-pointer flex-row items-center justify-center rounded-md border px-3 font-semibold text-gray-500"
          >
            <option value="vn">VN</option>
            <option value="en">EN</option>
          </select>
          <router-link
            class="hover:text-primary-400 flex h-12 cursor-pointer flex-row items-center justify-center rounded-md pr-3.5 font-semibold text-gray-500 focus:outline-none pc:justify-start pc:pr-6"
            to="/v1/admin/setting"
            ><span class="ml-3.5 inline-flex items-center justify-center"
              ><font-awesome-icon :icon="['fas', 'gear']" class="h-4 w-4 rotate-180" /></span
            ><span class="ml-2 hidden truncate text-base font-normal capitalize pc:ml-2 pc:block">{{
              $t('nav.setting')
            }}</span></router-link
          >
        </div>
      </div>
      <div class="px-1">
        <button
          @click.prevent="logout"
          class="hover:text-primary-400 group flex h-12 cursor-pointer flex-row items-center justify-center rounded-md pr-3.5 font-semibold text-red-400 hover:text-red-600 focus:outline-none pc:justify-start pc:pr-6"
        >
          <span class="ml-3.5 inline-flex items-center justify-center"
            ><font-awesome-icon
              :icon="['fas', 'right-to-bracket']"
              class="h-4 w-4 rotate-180 text-red-400 group-hover:text-red-600" /></span
          ><span class="ml-2 hidden truncate text-base font-normal capitalize pc:block">
            {{ $t('nav.logout') }}
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

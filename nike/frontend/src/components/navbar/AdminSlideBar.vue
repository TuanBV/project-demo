<script setup>
import { ref } from 'vue'

const menu = ref([
  {
    name: 'Product',
    to: '/v1/admin/product',
    icon: 'box-archive'
  },
  {
    name: 'User',
    to: '/v1/admin/product',
    icon: 'user'
  },
  {
    name: 'Blog',
    to: '/v1/admin/blog',
    icon: 'blog'
  },
  {
    name: 'Product',
    to: '/v1/admin/product',
    icon: 'box-archive'
  }
])
</script>
<template>
  <div class="col-span-1 bg-white">
    <div
      class="flex h-full w-full flex-col border-r border-r-gray-200 bg-white p-2 dark:bg-gray-900"
    >
      <!-- Logo -->
      <router-link to="/v1/admin" class="flex items-center justify-center">
        <img src="assets/logo.svg" alt="" srcset="" width="70px" height="70px" />
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
              item.name
            }}</span></router-link
          >
        </div>
        <div class="mx-1 flex flex-col space-y-1 pc:mt-1">
          <router-link
            class="hover:text-primary-400 flex h-12 cursor-pointer flex-row items-center justify-center rounded-md pr-3.5 font-semibold text-gray-500 focus:outline-none pc:justify-start pc:pr-6"
            to="/v1/admin/setting"
            ><span class="ml-3.5 inline-flex items-center justify-center"
              ><font-awesome-icon :icon="['fas', 'gear']" class="h-4 w-4 rotate-180" /></span
            ><span class="ml-2 hidden truncate text-base font-normal capitalize pc:ml-2 pc:block"
              >Settings</span
            ></router-link
          >
        </div>
      </div>
      <div class="px-1">
        <button
          class="hover:text-primary-400 group flex h-12 cursor-pointer flex-row items-center justify-center rounded-md pr-3.5 font-semibold text-red-400 hover:text-red-600 focus:outline-none pc:justify-start pc:pr-6"
        >
          <span class="ml-3.5 inline-flex items-center justify-center"
            ><font-awesome-icon
              :icon="['fas', 'right-to-bracket']"
              class="h-4 w-4 rotate-180 text-red-400 group-hover:text-red-600" /></span
          ><span class="ml-2 hidden truncate text-base font-normal capitalize pc:block"
            >Logout</span
          >
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";

const menuDropdown = reactive([
  {
    name: 'Profile',
    url: '/profile'
  },
  {
    name: 'Settings',
    url: '/settings'
  },
  {
    name: 'Logout',
    url: '/logout'
  }
])

</script>


<template>
  <div class="dropdown inline-block relative">
    <button><i class="fa-solid fa-user"></i></button>
    <ul class="dropdown-content absolute hidden text-gray-700 font-medium bg-gray-200 right-0 rounded-md">
      <li v-for="item in menuDropdown" :key="item"
      class="px-7 py-3 hover:text-orange-600 border-b-[1px] border-white last:border-b-0"
      ><router-link :to="item.url">{{  item.name }}</router-link></li>
    </ul>
  </div>
</template>

<style scoped>
.dropdown:hover .dropdown-content {
  display: block;
}
</style>
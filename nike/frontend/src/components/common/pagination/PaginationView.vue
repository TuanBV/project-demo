<script setup>
import { computed, onMounted } from 'vue'

const pagination = defineModel()

const page = computed(() => pagination.total / pagination.show)

onMounted(() => {
  console.log(pagination)
})
</script>

<template>
  <div class="mt-5 flex flex-col justify-between pc:flex-row">
    <div class="flex flex-col items-center space-x-2 pc:flex-row">
      <select
        v-model="pagination.show"
        class="inline-flex items-center rounded border px-4 py-2 font-medium text-gray-600 hover:bg-gray-100 active:bg-gray-200 disabled:opacity-50"
      >
        <option value="10">10 items</option>
        <option value="20">20 items</option>
        <option value="30">30 items</option>
        <option value="50">50 items</option>
        <option value="100">100 items</option>
      </select>

      <p class="mt-4 text-gray-500 pc:mt-0">
        Showing {{ (pagination.current - 1) * pagination.show + 1 }} to
        {{ pagination.current * pagination.show + 1 }} of {{ pagination.total }} entires
      </p>
    </div>

    <nav
      aria-label="Pagination"
      class="mt-8 flex items-center justify-center text-gray-600 pc:mt-0"
    >
      <p class="mr-4 rounded p-2 hover:bg-gray-100">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </p>
      <p
        v-for="(item, index) in page"
        :key="index"
        class="rounded px-4 py-2 hover:bg-gray-100"
        :class="[item == pagination.current ? 'bg-gray-200' : '']"
      >
        {{ item }}
      </p>
      <!-- <p class="rounded bg-gray-200 px-4 py-2 font-medium text-gray-900 hover:bg-gray-100">2</p> -->
      <!-- <p class="rounded px-4 py-2 hover:bg-gray-100">3</p> -->
      <!-- <p class="rounded px-4 py-2 hover:bg-gray-100">...</p> -->
      <!-- <p class="rounded px-4 py-2 hover:bg-gray-100">9</p> -->
      <p class="ml-4 rounded p-2 hover:bg-gray-100">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </p>
    </nav>
  </div>
</template>

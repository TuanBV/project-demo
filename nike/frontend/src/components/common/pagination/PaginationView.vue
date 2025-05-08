<script setup>
import { computed, watch } from 'vue'
// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
// ==> 1.2) actions
// ==> 1.3) Others
// 2) ======= VARIABLE REF ========
const pagination = defineModel()
const page = computed(() => Math.ceil(pagination.value.total / pagination.value.show))
// 3) ======= METHOD/FUNCTION ========
// 4) ======= VUE JS LIFECYCLE ========
watch(page, () => {
  pagination.value.current = 1
})
</script>

<template>
  <div class="mt-5 flex flex-col justify-between border-t pt-5 pc:flex-row">
    <div class="flex flex-col items-center space-x-2 pc:flex-row">
      <select
        v-model="pagination.show"
        class="inline-flex items-center rounded border px-4 py-2 font-medium text-gray-600 hover:bg-gray-100 focus-visible:outline-none active:bg-gray-200 disabled:opacity-50"
      >
        <option :value="10">10 items</option>
        <option :value="20">20 items</option>
        <option :value="30">30 items</option>
        <option :value="50">50 items</option>
        <option :value="100">100 items</option>
      </select>

      <p class="mt-4 text-gray-500 pc:mt-0">
        Showing {{ (pagination.current - 1) * pagination.show + 1 }} to
        {{
          pagination.current != page ? pagination.current * pagination.show + 1 : pagination.total
        }}
        of {{ pagination.total }} entires
      </p>
    </div>
    <nav
      v-if="pagination.total < page * pagination.show"
      aria-label="Pagination"
      class="mt-8 flex cursor-pointer items-center justify-center text-gray-600 pc:mt-0"
    >
      <p
        class="mr-4 rounded p-2 hover:bg-gray-100"
        @click.prevent="pagination.current > 2 ? pagination.current-- : (pagination.current = 1)"
      >
        <font-awesome-icon :icon="['fas', 'angle-left']" class="group h-4 w-4" />
      </p>
      <p
        v-for="(item, index) in page"
        :key="index"
        class="rounded px-4 py-2 hover:bg-gray-100"
        :class="[item == pagination.current ? 'bg-gray-200' : '']"
        @click.prevent="pagination.current = item"
      >
        {{ item }}
      </p>
      <p
        class="ml-4 rounded p-2 hover:bg-gray-100"
        @click.prevent="
          pagination.current < page - 1 ? pagination.current++ : (pagination.current = page)
        "
      >
        <font-awesome-icon :icon="['fas', 'angle-right']" class="group h-4 w-4" />
      </p>
    </nav>
  </div>
</template>

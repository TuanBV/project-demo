<script setup>
import { ref, watch } from 'vue'

const type = ref()
watch(type, () => {
  setTimeout(() => {
    type.value = ''
  }, 3000)
})
</script>

<template>
  <div class="fixed bottom-5 right-2 z-[999]">
    <!-- component -->
    <div class="m-auto">
      <!-- Danger -->
      <div v-if="type == 'danger'" class="flex flex-row rounded-lg bg-white p-4 shadow-md">
        <div class="mr-1 inline-block rounded-lg bg-red-500 p-1"></div>
        <b class="p-1">Alert Title</b>
        <p class="p-1">This is a small alert!</p>
        <a class="inline-block h-5 w-5 p-1 text-gray-500">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </a>
      </div>
      <!-- Warning -->
      <div v-if="type == 'warning'" class="flex flex-row rounded-lg bg-white p-4 shadow-md">
        <div class="mr-1 inline-block rounded-lg bg-yellow-500 p-1"></div>
        <b class="p-1">Alert Title</b>
        <p class="p-1">This is a small alert!</p>
        <a class="inline-block h-5 w-5 p-1 text-gray-500">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </a>
      </div>
      <!-- Success -->
      <div v-if="type == 'success'" class="flex flex-row rounded-lg bg-white p-4 shadow-md">
        <div class="mr-1 inline-block rounded-lg bg-green-500 p-1"></div>
        <b class="p-1">Alert Title</b>
        <p class="p-1">This is a small alert!</p>
        <a class="inline-block h-5 w-5 p-1 text-gray-500">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clip-rule="evenodd"
            />
          </svg>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// Props
const props = defineProps(['isVisible', 'message', 'accept'])
// Emit
const emit = defineEmits(['cancel'])
</script>
<template>
  <div
    v-if="props.isVisible"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50"
  >
    <div class="rounded-lg bg-white p-6 text-center shadow-lg">
      <p class="mb-4 text-lg">{{ message }}</p>
      <div class="flex justify-center gap-5">
        <button
          @click.prevent="props.accept"
          class="rounded-md bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
        >
          Accept
        </button>
        <button
          @click.prevent="emit('cancel')"
          class="rounded-md bg-red-500 px-4 py-2 text-white hover:bg-gray-600"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

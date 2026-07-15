<script setup>
import { computed } from 'vue'
import { API_BASE_URL } from 'utility/env'
import placeholderImage from 'assets/logo.svg'

const props = defineProps(['itemProduct'])
const emit = defineEmits(['update:itemProduct'])

const imageSrc = computed(() => {
  const firstImage = props.itemProduct.images?.[0]
  return firstImage ? `${API_BASE_URL}/${firstImage.path}` : placeholderImage
})
</script>
<template>
  <div class="group block overflow-hidden" @click="emit('update:itemProduct', props.itemProduct)">
    <img
      loading="lazy"
      :alt="props.itemProduct.name"
      :src="imageSrc"
      class="mx-auto aspect-square object-cover transition duration-500 group-hover:scale-105"
      width="300"
      height="300"
    />

    <div class="relative flex justify-between bg-white px-2 pt-3">
      <div>
        <h3 class="text-gray-700 group-hover:underline group-hover:underline-offset-4">
          {{ props.itemProduct.name }}
        </h3>
        <p class="mt-1">
          <span class="text-sm text-gray-900"> £{{ props.itemProduct.price }} </span>
        </p>
      </div>
      <button>
        <font-awesome-icon
          :icon="['fas', 'plus']"
          class="h-3 w-3 rounded-full border-[1px] border-[#14B8A6] p-1 text-[#14B8A6]"
        />
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps(['itemProduct'])
// const product = defineModel()
const emit = defineEmits(['update:itemProduct'])
</script>
<template>
  <!-- @click="product = props.itemProduct -->
  <div class="group block overflow-hidden" @click="emit('update:itemProduct', props.itemProduct)">
    <img
      loading="lazy"
      :alt="props.itemProduct.name"
      :src="props.itemProduct.image[0]"
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

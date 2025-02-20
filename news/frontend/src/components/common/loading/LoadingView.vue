<template>
  <slot name="loading">
    <div class="fixed left-0 top-0 z-[999] h-full w-full bg-white opacity-75">
      <div class="mt-[50vh] flex items-center justify-center">
        <font-awesome-icon :icon="['fas', 'spinner']" class="animate-spin text-4xl text-gray-600" />
      </div>
    </div>
  </slot>
</template>

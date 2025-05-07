<script setup>
import 'quill/dist/quill.snow.css'
const preview = defineModel()
</script>

<template>
  <div
    v-if="preview.isModal"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="preview.isModal = !preview.isModal"
  >
    <div class="h-[80%] max-h-[80%] w-[80%] overflow-hidden rounded-lg bg-white p-5 shadow-2xl">
      <div class="mb-5 flex items-start justify-between border-b pb-2">
        <h1 class="text-3xl font-medium">Preview post</h1>
        <button class="float-end" @click="preview.isModal = false">
          <font-awesome-icon :icon="['fas', 'close']" />
        </button>
      </div>
      <div class="mx-auto h-full w-full overflow-y-auto py-2">
        <div class="flex items-center justify-center">
          <div class="mx-auto w-full bg-white">
            <div class="text-xl">{{ preview.post.title }}</div>
            <div class="ql-editor" v-html="preview.post.content"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

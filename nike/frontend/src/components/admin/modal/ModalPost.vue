<script setup>
import { ref, watch } from 'vue'
// import userService from 'service/user.service'
// import useValidate from 'composables/validate'
// import addUserSchema from 'schemas/admin/addUser'
// import ToastUtil from 'utility/toast'
// const { validate, errors } = useValidate()

const isModal = defineModel()
const selectedFile = ref()
const post = ref({
  title: '',
  recipient: [],
  body: '',
  attachedFile: null,
  cc: []
})

watch(isModal, () => {
  // errors.value = []
  selectedFile.value = null
})
</script>

<template>
  <div
    v-if="isModal"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="isModal = !isModal"
  >
    <div
      class="h-[80%] w-[80%] overflow-y-auto overflow-x-hidden rounded-lg bg-white p-5 shadow-2xl pc:h-auto pc:w-[60%]"
    >
      <h2 class="mb-6 text-center text-2xl font-semibold">Create new post</h2>
      <!-- Title -->
      <div class="mb-4">
        <div class="flex items-center justify-between">
          <label for="subject" class="block text-sm font-medium text-gray-700">Title</label>
        </div>
        <input
          type="text"
          v-model="post.subject"
          id="subject"
          placeholder="Type title"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- Body -->
      <div class="mb-4">
        <label for="body" class="block text-sm font-medium text-gray-700">Body</label>
      </div>
      <button
        type="submit"
        @click.prevent="console.log(content)"
        class="w-full rounded-md bg-blue-500 py-3 font-semibold text-white transition duration-200 hover:bg-blue-600"
      >
        Create Post
      </button>
    </div>
  </div>
</template>

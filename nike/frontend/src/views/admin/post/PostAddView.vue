<script setup>
import { ref, onMounted, watch } from 'vue'
// import userService from 'service/user.service'
// import useValidate from 'composables/validate'
// import addUserSchema from 'schemas/admin/addUser'
// import ToastUtil from 'utility/toast'
// const { validate, errors } = useValidate()
import RichTextView from 'components/admin/modal/RichTextView.vue'

const content = ref()
</script>

<template>
  <div class="h-full items-center justify-center">
    <div class="mb-5 flex items-center gap-2 border-b pb-3">
      <router-link to="post"
        ><font-awesome-icon
          :icon="['fas', 'arrow-left']"
          class="hover:scale-110"
        ></font-awesome-icon
      ></router-link>
      <h1 class="text-2xl font-medium tracking-wider">Create new post</h1>
    </div>
    <!-- Title -->
    <div class="mb-4">
      <div class="flex items-center justify-between">
        <label for="title" class="block text-sm font-medium text-gray-700">Title</label>
      </div>
      <input
        type="text"
        id="title"
        placeholder="Type title"
        class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
    </div>

    <!-- Body -->
    <div class="mb-4">
      <label for="body" class="block text-sm font-medium text-gray-700">Body</label>
      <div ref="editor"></div>
      <RichTextView v-model="content" />
    </div>
    <div class="mb-4">
      <label for="StartDate" class="mb-2 block text-base font-medium">
        Start date <span class="text-red-500"></span
      ></label>
      <input
        type="date"
        name="start_date"
        placeholder="YYYY-MM-DD"
        class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
      />
    </div>
    <button
      type="submit"
      class="rounded-md bg-blue-500 px-5 py-3 font-semibold text-white transition duration-200 hover:bg-blue-600"
    >
      Create Post
    </button>
  </div>
</template>
<style>
.ql-editor {
  min-height: 400px !important;
}
.ql-toolbar.ql-snow {
  border-top-right-radius: 6px !important;
  border-top-left-radius: 6px !important;
  border-color: #e5e7eb;
  border-bottom: 0px;
}
</style>

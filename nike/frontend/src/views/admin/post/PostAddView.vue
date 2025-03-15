<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import postService from 'service/post.service'
// import useValidate from 'composables/validate'
// import addUserSchema from 'schemas/admin/addUser'
import ToastUtil from 'utility/toast'
import PostPreview from 'components/admin/modal/PostPreview.vue'

// const { validate, errors } = useValidate()
import RichTextView from 'components/admin/modal/RichTextView.vue'

const router = useRouter()

const post = ref({
  title: '',
  content: '',
  start_date: ''
})
const preview = ref({
  isModal: false,
  post: ''
})

const add = async () => {
  const res = await postService.add(post.value)
  if (res) {
    ToastUtil.success('Post added successfully!')
    router.push('admin-post')
    return
  }
  ToastUtil.error('Post add failed!')
}
</script>

<template>
  <div class="h-full items-center justify-center">
    <div class="mb-5 flex items-center justify-between border-b pb-3">
      <div class="flex items-center gap-2">
        <router-link to="post"
          ><font-awesome-icon
            :icon="['fas', 'arrow-left']"
            class="hover:scale-110"
          ></font-awesome-icon
        ></router-link>
        <h1 class="text-2xl font-medium tracking-wider">Create new post</h1>
      </div>
      <button
        @click="(preview.isModal = true), (preview.post = post)"
        class="flex items-center gap-2 rounded-md border px-3 py-1 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
      >
        <font-awesome-icon :icon="['fas', 'eye']" class="group h-4 w-4 text-yellow-500" />
        <span class="text-sm font-semibold text-yellow-500">Preview</span>
      </button>
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
        v-model="post.title"
      />
    </div>

    <!-- Body -->
    <div class="mb-4">
      <label for="body" class="block text-sm font-medium text-gray-700">Body</label>
      <RichTextView v-model="post.content" />
    </div>

    <div class="mb-4">
      <label for="StartDate" class="mb-2 block text-base font-medium">
        Start date <span class="text-red-500"></span
      ></label>
      <input
        type="date"
        v-model="post.start_date"
        name="start_date"
        placeholder="YYYY-MM-DD"
        class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
      />
    </div>
    <button
      class="rounded-md bg-blue-500 px-5 py-3 font-semibold text-white transition duration-200 hover:bg-blue-600"
      @click.prevent="add"
    >
      Create Post
    </button>
    <PostPreview v-model="preview" />
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

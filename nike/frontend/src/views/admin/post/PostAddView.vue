<script setup>
import { onBeforeMount, defineAsyncComponent, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { StatusPost } from 'utility/const'
import useValidate from 'composables/validate'
import postSchema from 'schemas/admin/post'
import postService from 'service/post.service'
import ToastUtil from 'utility/toast'
import PostPreview from 'components/admin/modal/PostPreview.vue'

const RichTextEditor = defineAsyncComponent(
  () => import('components/admin/modal/RichTextCustom.vue')
)
const router = useRouter()
const route = useRoute()
const { validate, errors } = useValidate()
const keyRenderComponent = ref('')
const post = ref({
  id: null,
  title: '',
  content: '',
  status: 1,
})

const errorContent = ref(false)

const preview = ref({
  isModal: false,
  post: '',
})

const handlePost = async status => {
  post.value.status = status
  // Check valid data
  const isValid = validate(postSchema, post.value)
  if (!isValid) return
  // Call api
  const res = await postService.add(post.value)
  if (res) {
    ToastUtil.success('Post added successfully!')
    router.push('admin-post')
    return
  }
  ToastUtil.error('Post add failed!')
}
// Call api
const getPost = async idPost => {
  const res = await postService.getByPostId(idPost)
  if (res) {
    post.value.id = res.id
    post.value.title = res.title
    post.value.content = res.content
    return
  }
  ToastUtil.error('Error get info post')
}

onBeforeMount(async () => {
  if (route.params.idPost) {
    await getPost(route.params.idPost)
    keyRenderComponent.value = btoa(route.params.id)
  } else {
    keyRenderComponent.value = btoa(new Date().toString())
  }
})
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
      <p v-if="errors.title" class="mt-1 text-xs leading-4 text-red-500">
        {{ errors.title }}
      </p>
    </div>
    <!-- Content -->
    <div class="mb-4">
      <label for="body" class="block text-sm font-medium text-gray-700">Body</label>
      <RichTextEditor
        :key="keyRenderComponent"
        v-model="post.content"
        :errorContent="errorContent"
        @update="value => (errorContent = value)"
      />
    </div>
    <!-- Button -->
    <div class="flex gap-3">
      <button
        class="rounded-md bg-yellow-500 px-5 py-3 font-semibold text-white transition duration-200 hover:bg-yellow-600"
        @click.prevent="handlePost(StatusPost.SAVE)"
      >
        Save
      </button>
      <button
        class="rounded-md bg-blue-500 px-5 py-3 font-semibold text-white transition duration-200 hover:bg-blue-600"
        @click.prevent="handlePost(StatusPost.ADD)"
      >
        Post
      </button>
    </div>
    <PostPreview v-model="preview" />
  </div>
</template>
<style>
.ql-editor {
  min-height: 500px !important;
}
.ql-toolbar.ql-snow {
  border-top-right-radius: 6px !important;
  border-top-left-radius: 6px !important;
  border-color: #e5e7eb;
  border-bottom: 0px;
}
</style>

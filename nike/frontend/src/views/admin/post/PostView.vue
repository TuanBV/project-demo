<script setup>
import { defineAsyncComponent, onMounted, ref } from 'vue'
import postService from 'service/post.service'
import ToastUtil from 'utility/toast'
import { useRouter } from 'vue-router'

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const router = useRouter()
const PaginationView = defineAsyncComponent(() => {
  return import('components/common/pagination/PaginationView.vue')
})
// ==> 1.2) actions
// ==> 1.3) Others
// 2) ======= VARIABLE REF ========
const postList = ref([])
const pagination = ref({
  current: 2,
  show: 20,
  total: 94,
})

// 3) ======= METHOD/FUNCTION ========
// Get list post
const getList = async () => {
  const res = await postService.getList()
  if (res) {
    postList.value = res.item
    return
  }
  ToastUtil.error('Error fetching post list')
}
// Handel delete and active post
const deletePost = async id => {
  // Call api
  const res = await postService.delete(id)
  if (res) {
    const post = postList.value.find(post => post.id === id)
    post.flg_del = !post.flg_del
    ToastUtil.success(post.flg_del ? 'Delete post success' : 'Active post success')
    return
  }
  ToastUtil.error('Error')
}

// 4) ======= VUE JS LIFECYCLE ========
onMounted(async () => {
  await getList()
})
</script>

<template>
  <div>
    <h1 class="mb-5 text-2xl font-medium tracking-wider">Manage Post</h1>
    <div class="mb-2 mt-5 flex justify-between">
      <h1 class="text-xl tracking-wide">List Post</h1>
      <router-link
        to="post-add"
        class="flex cursor-pointer items-center justify-center gap-2 rounded-md bg-green-500 px-3 py-2 font-medium text-white duration-300 hover:scale-105"
      >
        <font-awesome-icon :icon="['fas', 'add']" class="group h-4 w-4" />
        <span>Create Post</span>
      </router-link>
    </div>
    <div class="overflow-hidden rounded-xl shadow-xl">
      <table class="w-full table-fixed">
        <thead>
          <tr class="bg-gray-100">
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">STT</th>
            <th class="w-7/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Tile</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Status</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Action</th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr
            class="border-b border-gray-300"
            v-for="(item, index) in postList"
            :key="index"
            :class="[item.flg_del ? 'bg-gray-300' : '']"
          >
            <td class="truncate border-b border-gray-200 px-6 py-4">{{ index + 1 }}</td>
            <td class="border-b border-gray-200 px-6 py-4">{{ item.title }}</td>
            <td class="border-b border-gray-200 px-6 py-4">
              <span
                v-if="!item.flg_del"
                class="rounded-full px-2 py-1 text-xs text-white"
                :class="item.status ? 'bg-yellow-500' : 'bg-green-500'"
                >{{ item.status ? 'Lưu tạm' : 'Đã đăng' }}</span
              >
            </td>
            <td class="border-b border-gray-200 px-6 py-4">
              <div class="flex items-center gap-5">
                <!-- Button edit -->
                <button
                  @click.prevent="
                    router.push({ name: 'admin-post-add', params: { idPost: item.id } })
                  "
                  class="flex gap-1 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
                >
                  <font-awesome-icon :icon="['fas', 'edit']" class="group h-4 w-4 text-green-500" />
                  <span class="text-sm font-semibold text-green-500">Edit</span>
                </button>
                <!-- Button active -->
                <button
                  class="flex gap-1 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
                  @click.prevent="deletePost(item.id)"
                  v-if="item.flg_del"
                >
                  <font-awesome-icon
                    :icon="['fas', 'power-off']"
                    class="group h-4 w-4 text-green-500"
                  />
                  <span class="text-sm font-semibold text-green-500">Active</span>
                </button>
                <!-- Button delete -->
                <button
                  class="flex gap-1 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
                  @click.prevent="deletePost(item.id)"
                  v-else
                >
                  <font-awesome-icon
                    :icon="['fas', 'power-off']"
                    class="group h-4 w-4 text-red-500"
                  />
                  <span class="text-sm font-semibold text-red-500">Delete</span>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <PaginationView v-model="pagination" />
  </div>
</template>

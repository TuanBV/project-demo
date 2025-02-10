<script setup>
import { defineAsyncComponent, onMounted, ref, watch } from 'vue'
import ConfirmPopup from 'components/ConfirmPopup.vue'
import categoryService from 'service/category.service'
import ToastUtil from 'utility/toast'

const categories = ref([])
const refConfirmPopup = ref({
  isVisible: false,
  message: '',
  confirmAction: null
})
const childCategory = ref({
  isModalCategory: false,
  categoryId: ''
})
const getList = async () => {
  const res = await categoryService.getList()
  if (res) {
    categories.value = res.item
  }
}

const ModalCategory = defineAsyncComponent(() => {
  return import('components/admin/modal/ModalCategory.vue')
})

const deleteCategory = async (categoryId) => {
  const res = await categoryService.delete(categoryId)
  if (res) {
    await getList()
    ToastUtil.success('Delete category successfully')
  }
}

const activeCategory = async (categoryId) => {
  const res = await categoryService.active(categoryId)
  if (res) {
    await getList()
    ToastUtil.success('Active category successfully')
  }
}

const confirmPopup = (title, methodAction) => {
  refConfirmPopup.value.isVisible = true
  refConfirmPopup.value.message = title
  refConfirmPopup.value.confirmAction = methodAction
}

watch(childCategory.value, async () => {
  if (!childCategory.value.isModalCategory) await getList()
})

onMounted(async () => {
  await getList()
})
</script>
<template>
  <div>
    <h1 class="mb-5 border-b pb-3 text-2xl font-medium tracking-wider">Category Management</h1>

    <div class="mb-3 flex items-center justify-between">
      <div class="text-base font-medium">Category List</div>
      <button
        @click.prevent="childCategory.isModalCategory = true"
        class="flex cursor-pointer items-center justify-center rounded-md bg-green-500 px-3 py-2 font-medium text-white duration-300 hover:scale-105"
      >
        <font-awesome-icon :icon="['fas', 'add']" class="group h-4 w-4" />
        <span>Add Category</span>
      </button>
    </div>
    <div class="overflow-hidden rounded-xl shadow-xl">
      <table class="w-full table-fixed">
        <thead>
          <tr class="bg-gray-100">
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">STT</th>
            <th class="w-8/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Name</th>
            <th class="w-3/12 px-6 py-4 text-center font-bold uppercase text-gray-600">Action</th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr
            v-for="(item, index) in categories"
            :key="index"
            class="border-b border-gray-300"
            :class="item.flg_del ? 'bg-gray-200' : ''"
          >
            <td class="truncate px-6 py-4">{{ index + 1 }}</td>
            <td class="px-6 py-4">{{ item.name }}</td>
            <td class="flex items-center justify-center gap-4 border-gray-200 px-6 py-4">
              <button
                v-if="!item.flg_del"
                @click.prevent="
                  (childCategory.categoryId = item.id), (childCategory.isModalCategory = true)
                "
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon :icon="['fas', 'edit']" class="group h-4 w-4 text-green-500" />
                <span class="text-sm font-semibold text-green-500">Edit</span>
              </button>
              <button
                v-if="!item.flg_del"
                @click.prevent="
                  confirmPopup('Bạn muốn xóa danh mục ' + item.name + ' ?', () => {
                    deleteCategory(item.id), (refConfirmPopup.isVisible = false)
                  })
                "
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon
                  :icon="['fas', 'power-off']"
                  class="group h-4 w-4 text-red-500"
                />
                <span class="text-sm font-semibold text-red-500">Delete</span>
              </button>
              <button
                v-else
                @click.prevent="
                  confirmPopup('Bạn muốn thêm lại danh mục ' + item.name + ' ?', () => {
                    activeCategory(item.id), (refConfirmPopup.isVisible = false)
                  })
                "
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon
                  :icon="['fas', 'power-off']"
                  class="group h-4 w-4 text-yellow-600"
                />
                <span class="text-sm font-semibold text-yellow-600">Active</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Modal category -->
    <ModalCategory v-model="childCategory" />
    <!-- Confirm popup -->
    <ConfirmPopup
      :isVisible="refConfirmPopup.isVisible"
      :message="refConfirmPopup.message"
      :accept="refConfirmPopup.confirmAction"
      @cancel="() => (refConfirmPopup.isVisible = false)"
    />
  </div>
</template>

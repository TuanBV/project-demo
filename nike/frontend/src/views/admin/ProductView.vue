<script setup>
import { onMounted, ref } from 'vue'
import categoryService from 'service/category.service'
// import userService from 'service/user.service'
import ToastUtil from 'utility/toast'

const users = ref()
const categories = ref([])
const childProduct = ref({
  isModalProduct: false,
  productId: ''
})

const getCategory = async () => {
  const res = await categoryService.getList()
  if (res) {
    categories.value = res.item
    users.value = [
      {
        productId: '1',
        name: 'User 1',
        image: '',
        categoryId: 1,
        quantity: 20,
        price: 10000,
        sale: 500
      }
    ]
    return
  }
  ToastUtil.error('Error!')
}

const edit = async (userId) => {
  console.log(userId)
}

const returnCategory = (categoryId) => {
  let letCategory = categories.value.find((item) => item.id == categoryId)
  console.log(typeof letCategory)
  return letCategory.name
}

onMounted(async () => {
  await Promise.all([
    getCategory()
    // getUserList()
  ])
})
</script>
<template>
  <div>
    <h1 class="mb-5 border-b pb-3 text-2xl font-medium tracking-wider">Product Management</h1>

    <div class="mb-3 flex items-center justify-between">
      <div class="text-base font-medium">Product List</div>
      <button
        @click.prevent="childCategory.isModalCategory = true"
        class="flex cursor-pointer items-center justify-center rounded-md bg-green-500 px-3 py-2 font-medium text-white duration-300 hover:scale-105"
      >
        <font-awesome-icon :icon="['fas', 'add']" class="group h-4 w-4" />
        <span>Add Product</span>
      </button>
    </div>
    <div class="overflow-hidden rounded-xl shadow-xl">
      <table class="w-full table-fixed">
        <thead>
          <tr class="bg-gray-100">
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">STT</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Name</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Image</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Category</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Quantity</th>
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Price</th>
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Sale</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600"></th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr class="border-b border-gray-300" v-for="(item, index) in users" :key="index">
            <td class="truncate border-b border-gray-200 px-6 py-4">{{ index + 1 }}</td>
            <td class="border-b border-gray-200 px-6 py-4">{{ item.name }}</td>
            <td class="border-b border-gray-200 px-6 py-4">
              {{ item.image }}
            </td>
            <td class="border-b border-gray-200 px-6 py-4">
              {{ returnCategory(item.categoryId) }}
            </td>
            <td class="border-b border-gray-200 px-6 py-4">
              {{ item.quantity }}
            </td>
            <td class="border-b border-gray-200 px-6 py-4">
              {{ item.price }}
            </td>
            <td class="border-b border-gray-200 px-6 py-4">
              {{ item.sale }}
            </td>
            <td class="flex items-center gap-4 border-gray-200 px-6 py-4">
              <button
                @click.prevent="edit(item.user_id)"
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon :icon="['fas', 'edit']" class="group h-4 w-4 text-green-500" />
                <span class="text-sm font-semibold text-green-500">Edit</span>
              </button>
              <button
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon
                  :icon="['fas', 'power-off']"
                  class="group h-4 w-4 text-red-500"
                />
                <span class="text-sm font-semibold text-red-500">Delete</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

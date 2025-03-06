<script setup>
import { onMounted, ref } from 'vue'
import categoryService from 'service/category.service'
import productService from 'service/product.service'
// import userService from 'service/user.service'
import ToastUtil from 'utility/toast'
// 1) ======= INITIALIZATION ========

// 2) ======= VARIABLE REF ========
const products = ref()
const categories = ref([])
const childProduct = ref({
  isModalProduct: false,
  productId: ''
})

// 3) ======= METHOD/FUNCTION ========
const getCategory = async () => {
  const res = await categoryService.getList()
  if (res) {
    categories.value = res.item
    return
  }
  ToastUtil.error('Error!')
}

const getProduct = async () => {
  const res = await productService.getList()
  console.log(res)

  if (res) {
    products.value = res.item
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
  return ''
}
// 4) ======= VUE JS LIFECYCLE ========

onMounted(async () => {
  await Promise.all([getCategory(), getProduct()])
})
</script>

<template>
  <div>
    <h1 class="mb-5 border-b pb-3 text-2xl font-medium tracking-wider">Product Management</h1>

    <div class="mb-3 flex items-center justify-between">
      <div class="text-base font-medium">Product List</div>
      <router-link
        to="product-add"
        class="flex cursor-pointer items-center justify-center rounded-md bg-green-500 px-3 py-2 font-medium text-white duration-300 hover:scale-105"
      >
        <font-awesome-icon :icon="['fas', 'add']" class="group h-4 w-4" />
        <span>Add Product</span>
      </router-link>
    </div>
    <div class="overflow-hidden rounded-xl shadow-xl">
      <table class="w-full table-fixed">
        <thead>
          <tr class="bg-gray-100">
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">STT</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Name</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Image</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Category</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Kind</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Quantity</th>
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Price</th>
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Sale</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600"></th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr class="border-b border-gray-300" v-for="(item, index) in products" :key="index">
            <td class="truncate border-b border-gray-200 px-6 py-4">{{ index + 1 }}</td>
            <td class="border-b border-gray-200 px-6 py-4">{{ item.name }}</td>
            <td class="border-b border-gray-200 px-6 py-4">
              <img :src="'http://localhost:8000/' + item.images[0].path" alt="" srcset="" />
            </td>
            <td class="border-b border-gray-200 px-6 py-4">
              {{ item.category_name }}
            </td>
            <td class="border-b border-gray-200 px-6 py-4">
              {{ item.kind_name }}
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

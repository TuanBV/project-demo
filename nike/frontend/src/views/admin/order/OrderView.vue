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
const searchFilter = ref({
  name: '',
  code: '',
  phone_number: '',
  date_search: '',
  record: 20,
  sort: ''
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
    // products.value = res.item
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
    <h1 class="mb-5 border-b pb-3 text-2xl font-medium tracking-wider">Order Management</h1>
    <!-- Search filter -->
    <div class="mb-3 flex items-center gap-3">
      <p class="text-lg">Search filters</p>
      <div class="flex gap-4">
        <input
          type="text"
          id="name"
          v-model="searchFilter.name"
          placeholder="Type order name"
          class="col-span-1 rounded-md border border-gray-200 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          id="code"
          v-model="searchFilter.code"
          placeholder="Type order code"
          class="col-span-1 rounded-md border border-gray-200 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          id="phone_number"
          v-model="searchFilter.phone_number"
          placeholder="Type phone number"
          class="col-span-1 rounded-md border border-gray-200 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="date"
          id="date_search"
          v-model="searchFilter.date_search"
          class="col-span-1 rounded-md border border-gray-200 px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          v-if="
            searchFilter.code ||
            searchFilter.name ||
            searchFilter.date_search ||
            searchFilter.phone_number
          "
          class="flex items-center gap-2 rounded-md border px-1 text-xs text-red-500 hover:scale-110 hover:font-medium"
          @click.prevent="
            searchFilter.code =
              searchFilter.name =
              searchFilter.phone_number =
              searchFilter.date_search =
                ''
          "
        >
          <font-awesome-icon :icon="['fas', 'close']" />Clear filter
        </button>
      </div>
    </div>
    <!-- Total record, choose view record and choose sort -->
    <div class="overflow-hidden rounded-xl shadow-xl">
      <div class="flex justify-end gap-2 pb-2">
        <p class="flex items-center">Total: 0 record</p>
        <!-- Choose view record -->
        <select
          v-model="searchFilter.record"
          class="rounded-md border border-gray-200 px-2 py-1 text-end focus:outline-none focus:ring-2 focus:ring-blue-500"
          id="category"
        >
          <option disabled value="10">10 records</option>
          <option disabled value="20">20 records</option>
          <option disabled value="50">50 records</option>
          <option disabled value="100">100 records</option>
        </select>
        <!-- Choose sort -->
        <select
          v-model="searchFilter.sort"
          class="rounded-md border border-gray-200 px-2 py-1 text-end focus:outline-none focus:ring-2 focus:ring-blue-500"
          id="category"
        >
          <option disabled value="">Sort default</option>
          <option disabled value="name">Sort by name</option>
          <option disabled value="code">Sort by code</option>
          <option disabled value="date">Sort by date</option>
        </select>
      </div>
      <!-- Table -->
      <table class="w-full table-fixed">
        <thead>
          <tr class="bg-gray-100">
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">STT</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Name</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Price</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Time</th>
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Address</th>
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Status</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600"></th>
          </tr>
        </thead>
        <tbody class="bg-white" v-if="products">
          <tr class="border-b border-gray-300" v-for="(item, index) in products" :key="index">
            <td class="truncate border-b border-gray-200 px-6 py-4">{{ index + 1 }}</td>
            <td class="border-b border-gray-200 px-6 py-4">{{ item.name }}</td>
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
              {{ item.quantity }}
            </td>
            <td>
              <div class="flex items-center gap-4 border-gray-200 px-6 py-4">
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
              </div>
            </td>
          </tr>
        </tbody>
        <tbody class="bg-white">
          <tr class="text-center">
            <td colspan="7" class="py-3 font-medium">No orders</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

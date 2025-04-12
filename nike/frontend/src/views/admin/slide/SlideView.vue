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
    <div
      class="mb-5 flex items-center justify-between border-b pb-3 text-2xl font-medium tracking-wider"
    >
      <h1>Slide Management</h1>
      <router-link :to="{ name: 'admin-slide-add' }">
        <font-awesome-icon :icon="['fas', 'plus']" class="h-5 w-5 text-green-600" />
      </router-link>
    </div>
    <!-- Search filter -->
    <div class="mb-3 flex items-center justify-between gap-3">
      <div class="relative flex h-10 w-96 rounded-md">
        <input
          required=""
          class="peer w-full rounded-xl border bg-transparent bg-white px-4 text-base outline-none focus:shadow-md"
          id="address"
          type="text"
        />
        <label
          class="absolute left-4 top-1/2 translate-y-[-50%] bg-white px-2 text-base duration-150 peer-valid:-top-0 peer-valid:left-3 peer-valid:text-sm peer-focus:left-3 peer-focus:top-0 peer-focus:text-sm"
          for="address"
        >
          Search by ...</label
        >
      </div>
      <div class="flex h-10 items-center gap-2">
        <p class="flex items-center">Total: 0 record</p>
        <!-- Choose view record -->
        <select
          v-model="searchFilter.record"
          class="rounded-md border border-gray-200 px-2 py-1 text-start focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option disabled value="10">10 records</option>
          <option disabled value="20">20 records</option>
          <option disabled value="50">50 records</option>
          <option disabled value="100">100 records</option>
        </select>
        <!-- Choose sort -->
        <select
          v-model="searchFilter.sort"
          class="rounded-md border border-gray-200 px-2 py-1 text-start focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option disabled value="">Sort default</option>
          <option disabled value="name">Sort by name</option>
          <option disabled value="date">Sort by date</option>
        </select>
      </div>
    </div>
    <!-- Total record, choose view record and choose sort -->
    <div class="overflow-hidden rounded-xl shadow-xl">
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

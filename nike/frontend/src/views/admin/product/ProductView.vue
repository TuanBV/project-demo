<script setup>
import { onMounted, ref, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import categoryService from 'service/category.service'
import kindService from 'service/kind.service'
import productService from 'service/product.service'
import ToastUtil from 'utility/toast'
import { API_BASE_URL } from 'utility/env'
import placeholderImage from 'assets/logo.svg'
import PaginationView from 'components/common/pagination/PaginationView.vue'

const productImageSrc = item => {
  const firstImage = item.images?.[0]
  return firstImage ? `${API_BASE_URL}/${firstImage.path}` : placeholderImage
}
// 1) ======= INITIALIZATION ========

// 2) ======= VARIABLE REF ========
const products = ref([])
const categories = ref([])
const kinds = ref([])
const filters = ref({
  category_id: '',
  kind_id: '',
  name: '',
})
const pagination = ref({
  current: 1,
  show: 12,
  total: 0,
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

const getKind = async () => {
  const res = await kindService.getList()
  if (res) {
    kinds.value = res.item
    return
  }
  ToastUtil.error('Error!')
}

const getProduct = async () => {
  const res = await productService.getList({
    page: pagination.value.current,
    page_size: pagination.value.show,
    category_id: filters.value.category_id || undefined,
    kind_id: filters.value.kind_id || undefined,
    name: filters.value.name || undefined,
  })

  if (res) {
    products.value = res.item
    pagination.value.total = res.total
    return
  }
  ToastUtil.error('Error!')
}

const edit = async userId => {
  console.log(userId)
}

// Category/kind filters take effect immediately; page resets to 1 so the
// user doesn't land on a page number that no longer exists under the filter.
const onFilterChange = () => {
  pagination.value.current = 1
}

// Free-text search is debounced so it doesn't fire a request per keystroke.
const onSearchInput = useDebounceFn(() => {
  pagination.value.current = 1
  getProduct()
}, 400)

// 4) ======= VUE JS LIFECYCLE ========
watch(
  () => [pagination.value.current, pagination.value.show, filters.value.category_id, filters.value.kind_id],
  () => getProduct()
)

onMounted(async () => {
  await Promise.all([getCategory(), getKind()])
  await getProduct()
})
</script>

<template>
  <div>
    <h1 class="mb-5 border-b pb-3 text-2xl font-medium tracking-wider">Product Management</h1>

    <div class="mb-3 flex items-center justify-between">
      <div class="text-base font-medium">Product List</div>
      <router-link
        to="product/add"
        class="flex cursor-pointer items-center justify-center rounded-md bg-green-500 px-3 py-2 font-medium text-white duration-300 hover:scale-105"
      >
        <font-awesome-icon :icon="['fas', 'add']" class="group h-4 w-4" />
        <span>Add Product</span>
      </router-link>
    </div>

    <div class="mb-4 flex flex-wrap items-center gap-3">
      <input
        v-model="filters.name"
        @input="onSearchInput"
        type="text"
        placeholder="Search by name..."
        class="rounded-md border px-3 py-2 text-sm"
      />
      <select
        v-model="filters.category_id"
        @change="onFilterChange"
        class="rounded-md border px-3 py-2 text-sm"
      >
        <option value="">All categories</option>
        <option v-for="item in categories" :key="item.id" :value="item.id">{{ item.name }}</option>
      </select>
      <select
        v-model="filters.kind_id"
        @change="onFilterChange"
        class="rounded-md border px-3 py-2 text-sm"
      >
        <option value="">All kinds</option>
        <option v-for="item in kinds" :key="item.id" :value="item.id">{{ item.name }}</option>
      </select>
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
              <div class="flex h-[100px] w-[100px] items-center overflow-hidden">
                <img
                  :src="productImageSrc(item)"
                  alt=""
                  class="object-cover"
                  width="100%"
                  height="100%"
                  srcset=""
                />
              </div>
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
                  <span class="text-sm font-semibold text-red-500"> Delete</span>
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="!products.length">
            <td colspan="9" class="px-6 py-8 text-center text-gray-500">No products found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <PaginationView v-model="pagination" />
  </div>
</template>

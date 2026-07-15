<script setup>
import { ref, onMounted, watch } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import productService from 'service/product.service'
import categoryService from 'service/category.service'
import kindService from 'service/kind.service'
import ToastUtil from 'utility/toast'
import ItemProduct from 'components/user/product/ItemProduct.vue'
import ProductDetailView from 'components/user/product/ProductDetailView.vue'
import PaginationView from 'components/common/pagination/PaginationView.vue'

const productList = ref([])
const product = ref()
const isModal = ref(false)
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

// Get list product
const getList = async () => {
  const res = await productService.getList({
    page: pagination.value.current,
    page_size: pagination.value.show,
    category_id: filters.value.category_id || undefined,
    kind_id: filters.value.kind_id || undefined,
    name: filters.value.name || undefined,
  })
  if (res) {
    productList.value = res.item
    pagination.value.total = res.total
    return
  }
  ToastUtil.error('Get list product failed')
}

const getCategory = async () => {
  const res = await categoryService.getList()
  if (res) categories.value = res.item
}

const getKind = async () => {
  const res = await kindService.getList()
  if (res) kinds.value = res.item
}

// Category/kind filters take effect immediately; page resets to 1 so the
// user doesn't land on a page number that no longer exists under the filter.
const onFilterChange = () => {
  pagination.value.current = 1
}

// Free-text search is debounced so it doesn't fire a request per keystroke.
const onSearchInput = useDebounceFn(() => {
  pagination.value.current = 1
  getList()
}, 400)

watch(
  () => [pagination.value.current, pagination.value.show, filters.value.category_id, filters.value.kind_id],
  () => getList()
)

onMounted(async () => {
  await Promise.all([getCategory(), getKind()])
  await getList()
})
</script>

<template>
  <section>
    <div class="mx-auto max-w-7xl px-10 py-8 tablet:px-6 pc:px-8 pc:py-12">
      <header>
        <h2 class="text-xl font-bold text-gray-900 sm:text-3xl">Product Collection</h2>

        <p class="mt-4 text-gray-500">
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Itaque praesentium cumque iure
          dicta incidunt est ipsam, officia dolor fugit natus?
        </p>
      </header>

      <!-- Filters -->
      <div class="mt-6 flex flex-wrap items-center gap-3">
        <input
          v-model="filters.name"
          @input="onSearchInput"
          type="text"
          placeholder="Search products..."
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

      <!-- List product -->
      <div class="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 tablet:grid-cols-3 pc:grid-cols-4">
        <div v-for="(item, index) in productList" :key="index">
          <ItemProduct
            :itemProduct="item"
            @update:itemProduct="newValue => ((product = newValue), (isModal = true))"
          />
        </div>
      </div>
      <p v-if="!productList.length" class="mt-8 text-center text-gray-500">No products found.</p>

      <PaginationView v-model="pagination" />
    </div>
    <ProductDetailView
      :product="product"
      :isModal="isModal"
      @closeModal="value => (isModal = value)"
      @clearProduct="() => console.log('aas')"
    />
  </section>
</template>

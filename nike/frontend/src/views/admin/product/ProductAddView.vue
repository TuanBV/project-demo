<script setup>
import { onMounted, ref } from 'vue'
import categoryService from 'service/category.service'
import kindService from 'service/kind.service'
import saleService from 'service/sale.service'
import productService from 'service/product.service'
import ToastUtil from 'utility/toast'
import ImageListView from 'components/admin/modal/ImageListView.vue'
import useValidate from 'composables/validate'
import productSchema from 'validations/schemas/admin/product'
import { useRouter } from 'vue-router'

const { validate, errors } = useValidate()
const router = useRouter()
const flgImageList = ref(false)
const imageList = ref([])
const categories = ref()
const kinds = ref()
const sales = ref()
const product = ref({
  name: '',
  category_id: '',
  kind_id: '',
  sale_id: '',
  info: '',
  price: '',
  quantity: '',
  weight: '',
  height: '',
  images: []
})

const add = async () => {
  product.value.images = imageList.value.map((item) => item.id.toString())
  let valid = validate(productSchema, product.value)
  if (!valid) {
    return
  }
  console.log(product.value)
  const res = await productService.add(product.value)
  if (res) {
    ToastUtil.success('Add product successfully!')
    router.push({ name: 'admin-product' })
  }
}

onMounted(async () => {
  const [categoryRes, kindRes, saleRes] = await Promise.all([
    categoryService.getList(),
    kindService.getList(),
    saleService.getList()
  ])
  categories.value = categoryRes.item
  kinds.value = kindRes.item
  sales.value = saleRes.item
})
</script>
<template>
  <div class="grid grid-cols-1 items-center justify-center gap-y-4">
    <div class="mb-5 flex items-center gap-2 border-b pb-3">
      <router-link to="product"
        ><font-awesome-icon
          :icon="['fas', 'arrow-left']"
          class="hover:scale-110"
        ></font-awesome-icon
      ></router-link>
      <h1 class="text-2xl font-medium tracking-wider">Create new product</h1>
    </div>
    <!-- Name -->
    <div>
      <div class="flex items-center justify-between">
        <label for="name" class="block text-sm font-medium text-gray-700"
          >Product Name
          <span class="text-xs text-red-500">(*)</span>
        </label>
      </div>
      <input
        type="text"
        id="name"
        v-model="product.name"
        placeholder="Type name"
        class="mt-1 w-2/3 rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        required
      />
      <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.name">
        {{ errors.name }}
      </p>
    </div>
    <!-- Product category, type and sale program -->
    <div class="flex items-start gap-3">
      <div class="w-1/4">
        <div class="flex items-center justify-between">
          <label for="category" class="block text-sm font-medium text-gray-700"
            >Category
            <span class="text-xs text-red-500">(*)</span>
          </label>
        </div>
        <select
          v-model="product.category_id"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          id="category"
        >
          <option disabled value="">Please choose category</option>
          <option :value="item.id" v-for="(item, index) in categories" :key="index">
            {{ item.name }}
          </option>
        </select>
        <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.category_id">
          {{ errors.category_id }}
        </p>
      </div>
      <div class="w-1/4">
        <div class="flex items-center justify-between">
          <label for="category" class="block text-sm font-medium text-gray-700"
            >Type
            <span class="text-xs text-red-500">(*)</span>
          </label>
        </div>
        <select
          v-model="product.kind_id"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          id="category"
        >
          <option disabled value="">Please choose type</option>
          <option :value="item.id" v-for="(item, index) in kinds" :key="index">
            {{ item.name }}
          </option>
        </select>
        <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.category_id">
          {{ errors.kind_id }}
        </p>
      </div>
      <div class="w-1/4">
        <div class="flex items-center justify-between">
          <label for="title" class="block text-sm font-medium text-gray-700">Sale program</label>
        </div>
        <select
          v-model="product.sale_id"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          id="category"
        >
          <option disabled value="">Please choose sale</option>
          <option :value="item.id" v-for="(item, index) in sales" :key="index">
            {{ item.name }}
          </option>
        </select>
        <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.sale_id">
          {{ errors.sale_id }}
        </p>
      </div>
    </div>
    <!-- Info -->
    <div>
      <label for="info" class="block text-sm font-medium text-gray-700">Body</label>
      <textarea
        name=""
        v-model="product.info"
        id="info"
        class="mt-1 max-h-56 min-h-56 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      ></textarea>
      <p class="mt-1 text-xs text-red-500" v-if="errors.info">{{ errors.info }}</p>
    </div>
    <!-- Weight and height -->
    <div class="flex items-start gap-3">
      <div class="w-1/4">
        <div class="flex items-center justify-between">
          <label for="weight" class="block text-sm font-medium text-gray-700">Weight</label>
        </div>
        <input
          type="text"
          id="weight"
          v-model="product.weight"
          placeholder="Type weight"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.weight">{{ errors.weight }}</p>
      </div>
      <div class="w-1/4">
        <div class="flex items-center justify-between">
          <label for="height" class="block text-sm font-medium text-gray-700">Height</label>
        </div>
        <input
          type="text"
          id="height"
          v-model="product.height"
          placeholder="Type title"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.height">{{ errors.height }}</p>
      </div>
    </div>
    <!-- Price and quantity -->
    <div class="flex items-start gap-3">
      <div class="w-1/4">
        <div class="flex items-center justify-between">
          <label for="price" class="block text-sm font-medium text-gray-700"
            >Price
            <span class="text-xs text-red-500">(*)</span>
          </label>
        </div>
        <input
          type="text"
          id="price"
          v-model="product.price"
          placeholder="Type title"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.price">{{ errors.price }}</p>
      </div>
      <div class="w-1/4">
        <div class="flex items-center justify-between">
          <label for="quantity" class="block text-sm font-medium text-gray-700"
            >Quantity
            <span class="text-xs text-red-500">(*)</span>
          </label>
        </div>
        <input
          type="text"
          id="quantity"
          v-model="product.quantity"
          placeholder="Type title"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
        <p class="mt-1 text-xs leading-4 text-red-500" v-if="errors.quantity">
          {{ errors.quantity }}
        </p>
      </div>
    </div>
    <!-- Image -->
    <div class="">
      <div class="flex items-center gap-4">
        <span class="block text-base font-medium"> Choose Image</span>
        <button class="flex items-center hover:scale-110" @click.prevent="flgImageList = true">
          <font-awesome-icon :icon="['fas', 'cloud-arrow-up']" class="h-5 w-5" />
        </button>
        <button
          v-if="imageList.length"
          class="flex items-center gap-2 rounded-3xl border px-1 text-xs text-red-500 hover:scale-110 hover:font-medium"
          @click.prevent="imageList = []"
        >
          <font-awesome-icon :icon="['fas', 'close']" />Clear
        </button>
      </div>
      <div class="flex">
        <div class="flex flex-wrap content-start gap-4">
          <div v-for="(item, index) in imageList" :key="index">
            <div class="relative h-[150px] w-[150px] rounded-md border">
              <img
                :src="item.path"
                :alt="item.name"
                height="100%"
                width="100%"
                class="h-full w-full rounded-md object-contain"
              />
              <font-awesome-icon
                :icon="['fas', 'close']"
                @click.prevent="imageList = imageList.filter((i) => i != item)"
                class="absolute right-0 top-0 text-red-500"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- Button submit -->
    <div>
      <button
        @click.prevent="add"
        type="submit"
        class="rounded-md bg-blue-500 px-10 py-3 font-semibold text-white transition duration-200 hover:scale-110 hover:bg-blue-600"
      >
        Add
      </button>
    </div>
    <ImageListView
      :flgImageList="flgImageList"
      :imageList="imageList"
      @close="(value) => (flgImageList = value)"
      @update:imageList="(value) => (imageList = value)"
    />
  </div>
</template>

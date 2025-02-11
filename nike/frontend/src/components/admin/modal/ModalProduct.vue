<script setup>
import { ref, watch } from 'vue'
import categoryService from 'service/category.service'
import useValidate from 'composables/validate'
import CategorySchema from 'schemas/admin/category'
import ToastUtil from 'utility/toast'

const { validate, errors } = useValidate()
const childProduct = defineModel()
const category = ref({
  name: ''
})

const addCategory = async () => {
  const isValid = validate(CategorySchema, category.value)
  if (!isValid) return
  const res = await categoryService.add(category.value)
  if (res) {
    ToastUtil.success('Added category successfully !!!')
    childProduct.value.isModalProduct = false
    childProduct.value.productId = ''
  }
}
const updateCategory = async () => {
  const isValid = validate(CategorySchema, category.value)
  if (!isValid) return
  const res = await categoryService.update(childProduct.value.productId, category.value)
  if (res) {
    ToastUtil.success('Update category successfully !!!')
    childProduct.value.isModalProduct = false
    childProduct.value.productId = ''
  }
}

watch(childProduct.value, async () => {
  category.value.name = ''
  if (childProduct.value.productId) {
    const res = await categoryService.getByproductId(childProduct.value.productId)
    if (res) {
      category.value.name = res.name
      // Populate form data with fetched data
    }
  }
  if (!childProduct.value.isModalProduct) childProduct.value.productId = ''
  errors.value = []
})
</script>

<template>
  <div
    v-if="childProduct.isModalProduct"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="childProduct.isModalProduct = !childProduct.isModalProduct"
  >
    <div
      class="h-[80%] w-[80%] overflow-y-auto overflow-x-hidden rounded-lg bg-white p-5 shadow-2xl pc:h-auto pc:w-[45%]"
    >
      <div class="mb-5 flex items-start justify-between border-b pb-2">
        <h1 class="text-3xl font-medium">Add Category</h1>
        <button class="float-end" @click="childProduct.isModalProduct = false">
          <font-awesome-icon :icon="['fas', 'close']" />
        </button>
      </div>
      <div class="mx-auto h-full w-full py-2">
        <div class="flex items-center justify-center">
          <div class="mx-auto w-full bg-white">
            <div class="mb-4">
              <label for="phone" class="mb-2 block text-base font-medium">
                Category name <span class="text-red-500">(*)</span></label
              >
              <input
                type="text"
                name="Name"
                v-model="category.name"
                placeholder="Type category name"
                class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
              <p v-if="errors.name" class="mt-2 text-sm italic text-red-500">
                {{ errors.name }}
              </p>
            </div>
            <div>
              <button
                v-if="childProduct.productId"
                @click.prevent="updateCategory"
                class="hover:shadow-form w-full rounded-md bg-green-500 px-8 py-2 text-center text-base font-semibold text-white outline-none hover:bg-green-600"
              >
                Update
              </button>
              <button
                v-else
                @click.prevent="addCategory"
                class="hover:shadow-form w-full rounded-md bg-green-500 px-8 py-2 text-center text-base font-semibold text-white outline-none hover:bg-green-600"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

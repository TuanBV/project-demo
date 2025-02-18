<script setup>
import { ref, watch } from 'vue'
import saleService from 'service/sale.service'
import useValidate from 'composables/validate'
import SaleSchema from 'schemas/admin/sale'
import ToastUtil from 'utility/toast'

const { validate, errors } = useValidate()
const childSale = defineModel()
const sale = ref({
  name: '',
  discount: 0,
  file: '',
  file_ext: '',
  file_size: 0,
  start_date: '',
  end_date: ''
})
const image = ref()
// Convert to base64
const convertToBase64 = (file) => {
  const reader = new FileReader()
  reader.onloadend = () => {
    image.value = reader.result
    sale.value.file = reader.result.split(',')[1]
    sale.value.file_ext = file.name.split('.').at(-1)
    sale.value.file_size = file.size
  }
  reader.readAsDataURL(file)
}

// Read image file and convert to base64
const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    convertToBase64(file)
  }
}

const addSale = async () => {
  console.log(sale.value)

  const isValid = validate(SaleSchema, sale.value)
  if (!isValid) return
  const res = await saleService.add(sale.value)
  if (res) {
    ToastUtil.success('Added sale successfully !!!')
    childSale.value.isModalSale = false
    childSale.value.saleId = ''
  }
}

const updateSale = async () => {
  const isValid = validate(SaleSchema, sale.value)
  if (!isValid) return
  const res = await saleService.update(childSale.value.saleId, sale.value)
  if (res) {
    ToastUtil.success('Update sale successfully !!!')
    childSale.value.isModalSale = false
    childSale.value.saleId = ''
  }
}

watch(childSale.value, async () => {
  image.value = ''
  sale.value = {
    name: '',
    discount: 0,
    file: '',
    file_ext: '',
    file_size: 0,
    start_date: '',
    end_date: ''
  }
  if (childSale.value.saleId) {
    const res = await saleService.getBySaleId(childSale.value.saleId)
    if (res) {
      sale.value.name = res.name
      sale.value.discount = res.discount
      sale.value.start_date = res.start_date
      sale.value.end_date = res.end_date
      image.value = res.image
      // Populate form data with fetched data
    }
  }
  if (!childSale.value.isModalSale) childSale.value.saleId = ''
  errors.value = []
})
</script>

<template>
  <div
    v-if="childSale.isModalSale"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="childSale.isModalSale = !childSale.isModalSale"
  >
    <div
      class="h-[80%] w-[80%] overflow-y-auto overflow-x-hidden rounded-lg bg-white p-5 shadow-2xl pc:h-auto pc:w-[45%]"
    >
      <div class="mb-5 flex items-start justify-between border-b pb-2">
        <h1 class="text-3xl font-medium">Add Sale Program</h1>
        <button class="float-end" @click="childSale.isModalSale = false">
          <font-awesome-icon :icon="['fas', 'close']" />
        </button>
      </div>
      <div class="mx-auto h-full w-full py-2">
        <div class="flex items-center justify-center">
          <div class="mx-auto w-full bg-white">
            <div class="mb-4">
              <label for="Name" class="mb-2 block text-base font-medium">
                Program name <span class="text-red-500">(*)</span></label
              >
              <input
                type="text"
                name="Name"
                v-model="sale.name"
                placeholder="Type program name ..."
                class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
              <p v-if="errors.name" class="mt-2 text-sm italic text-red-500">
                {{ errors.name }}
              </p>
            </div>
            <div class="mb-4">
              <label for="Discount" class="mb-2 block text-base font-medium">Discount</label>
              <input
                type="integer"
                name="Discount"
                v-model="sale.discount"
                placeholder="Type discount ..."
                class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
              <p v-if="errors.discount" class="mt-2 text-sm italic text-red-500">
                {{ errors.discount }}
              </p>
            </div>
            <div class="mb-4 flex items-center">
              <label for="Image" class="me-3 text-base font-medium">Image</label>
              <div class="flex">
                <div v-if="image" class="flex max-h-[100px]">
                  <img
                    loading="lazy"
                    :src="image"
                    alt=""
                    height="auto"
                    width="auto"
                    class="max-h-[100px]"
                  />
                  <font-awesome-icon
                    :icon="['fas', 'close']"
                    @click.prevent="image = ''"
                    class="ms-[-7px] mt-[-7px] h-[14px] w-[14px] cursor-pointer rounded-[50%] border border-red-500 text-red-500 hover:scale-125"
                  />
                </div>
                <input
                  v-else
                  type="file"
                  name="Image"
                  @change="handleFileChange"
                  accept=".jpg, .jpeg, .png"
                  placeholder="Upload file ..."
                />
              </div>
            </div>
            <div class="grid grid-cols-2 gap-5">
              <div class="col">
                <label for="StartDate" class="mb-2 block text-base font-medium">
                  Start name <span class="text-red-500"></span
                ></label>
                <input
                  type="date"
                  name="StartDate"
                  @input="validateDate"
                  v-model="sale.start_date"
                  placeholder="YYYY-MM-DD"
                  class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                />
              </div>
              <div class="col">
                <label for="EndDate" class="mb-2 block text-base font-medium">
                  End name <span class="text-red-500"></span
                ></label>
                <div class="relative">
                  <input
                    type="date"
                    id="myDate"
                    @input="validateDate"
                    name="EndDate"
                    v-model="sale.end_date"
                    placeholder="YYYY-MM-DD"
                    class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                  />
                </div>
              </div>
            </div>
            <div class="mb-4">
              <p v-if="errors.start_date" class="mt-2 text-sm italic text-red-500">
                {{ errors.start_date }}
              </p>
              <p v-if="errors.end_date" class="mt-2 text-sm italic text-red-500">
                {{ errors.end_date }}
              </p>
            </div>

            <div>
              <button
                v-if="childSale.saleId"
                @click.prevent="updateSale"
                class="hover:shadow-form w-full rounded-md bg-green-500 px-8 py-2 text-center text-base font-semibold text-white outline-none hover:bg-green-600"
              >
                Update
              </button>
              <button
                v-else
                @click.prevent="addSale"
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

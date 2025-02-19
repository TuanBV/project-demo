<script setup>
import { ref, watch } from 'vue'
import saleService from 'service/sale.service'
import useValidate from 'composables/validate'
import SaleSchema from 'schemas/admin/sale'
import ToastUtil from 'utility/toast'

const { validate, errors } = useValidate()
const isImageList = defineModel()
const imageList = ref([
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' },
  { id: 1, file: '/src/assets/assets/images/air_force_1.png' }
])
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
    isImageList.value.isModalSale = false
    isImageList.value.saleId = ''
  }
}

const updateSale = async () => {
  const isValid = validate(SaleSchema, sale.value)
  if (!isValid) return
  const res = await saleService.update(isImageList.value.saleId, sale.value)
  if (res) {
    ToastUtil.success('Update sale successfully !!!')
    isImageList.value.isModalSale = false
    isImageList.value.saleId = ''
  }
}

watch(isImageList.value, async () => {
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
  if (isImageList.value.saleId) {
    const res = await saleService.getBySaleId(isImageList.value.saleId)
    if (res) {
      sale.value.name = res.name
      sale.value.discount = res.discount
      sale.value.start_date = res.start_date
      sale.value.end_date = res.end_date
      image.value = res.image
      // Populate form data with fetched data
    }
  }
  if (!isImageList.value.isModalSale) isImageList.value.saleId = ''
  errors.value = []
})
</script>

<template>
  <div
    v-if="isImageList"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="isImageList = !isImageList"
  >
    <div
      class="h-[80%] w-[80%] overflow-x-hidden overflow-y-hidden rounded-lg bg-white p-5 shadow-2xl"
    >
      <div class="mb-5 flex items-start justify-between border-b pb-2">
        <div class="text-3xl font-medium">Image list</div>
        <button class="float-end" @click="isImageList = false">
          <font-awesome-icon :icon="['fas', 'close']" />
        </button>
      </div>
      <div class="mb-3 overflow-hidden rounded-lg">
        <div class="md:flex">
          <div class="w-full">
            <div
              class="relative flex h-36 items-center justify-center rounded-lg border-2 border-blue-500 bg-gray-50 shadow-lg transition-shadow duration-300 ease-in-out hover:shadow-xl"
            >
              <div class="absolute flex flex-col items-center">
                <img
                  alt="File Icon"
                  class="mb-3"
                  height="50px"
                  width="50px"
                  src="https://img.icons8.com/?size=256&id=wNxEqErpHetl&format=png"
                />
                <span class="block font-semibold text-gray-500"
                  >Drag &amp; drop your files here</span
                >
                <span class="mt-1 block font-normal text-gray-400">or click to upload</span>
              </div>
              <input
                name=""
                class="h-full w-full cursor-pointer opacity-0"
                type="file"
                accept=".jpg, .jpeg, .png"
              />
            </div>
          </div>
        </div>
      </div>
      <div class="flex h-[500px] flex-wrap content-start gap-4 overflow-y-auto pb-20">
        <div v-for="(item, index) in imageList" :key="index">
          <div class="h-[150px] w-[150px] rounded-md border">
            <img
              src="../../../assets/images/air_force_1.png"
              :alt="item.id"
              height="100%"
              width="100%"
              class="rounded-md"
            />
          </div>
          <div class="mt-1 flex justify-center gap-3">
            <button class="rounded-md bg-green-500 px-2 text-white">Use</button
            ><button class="rounded-md bg-red-500 px-2 text-white">Del</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

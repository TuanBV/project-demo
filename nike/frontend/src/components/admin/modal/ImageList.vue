<script setup>
import { ref, watch } from 'vue'
import imageService from 'service/image.service'
import useValidate from 'composables/validate'
import ImageSchema from 'schemas/admin/image'
import ToastUtil from 'utility/toast'

const { validate, errors } = useValidate()
const imageList = defineModel()
const firstCallFunc = ref(false)
const imgList = ref([])
const chooses = ref([])
const image = ref({
  file: '',
  file_ext: '',
  file_size: 0
})

// Get list image
const getList = async () => {
  const res = await imageService.getList()
  if (res) {
    imgList.value = res.item
    firstCallFunc.value = true
  }
}

// Add image
const addImage = async () => {
  const isValid = validate(ImageSchema, image.value)
  if (!isValid) return
  const res = await imageService.add(image.value)
  if (res) {
    image.value.file = ''
    image.value.file_ext = ''
    image.value.file_size = 0
    ToastUtil.success('Added image successfully !!!')
    await getList()
    return
  }
  ToastUtil.error('Added image failed !!!')
}

// Convert to base64
const convertToBase64 = (file) => {
  const reader = new FileReader()
  reader.onloadend = () => {
    image.value.file = reader.result.split(',')[1]
    image.value.file_ext = file.name.split('.').at(-1)
    image.value.file_size = file.size
  }
  reader.readAsDataURL(file)
}

// Read image file and convert to base64
const handleFileChange = (event) => {
  const fileUpload = event.target.files[0]
  if (fileUpload) {
    convertToBase64(fileUpload)
  }
}
// Return the image to the calling source
const returnImage = (item) => {
  if (chooses.value.length) {
    imageList.value.images = chooses.value
  } else {
    imageList.value.images.push(item)
  }
  imageList.value.flag = false
}

watch(image.value, async () => {
  if (image.value.file) {
    await addImage()
  }
})

watch(imageList.value, async () => {
  if (!firstCallFunc.value) await getList()
  if (!imageList.value.flag) {
    chooses.value = []
    firstCallFunc.value = false
  }
})
</script>

<template>
  <div
    v-if="imageList.flag"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="imageList.flag = !imageList.flag"
  >
    <div
      class="h-[80%] w-[80%] overflow-x-hidden overflow-y-hidden rounded-lg bg-white p-5 shadow-2xl"
    >
      <div class="mb-5 flex items-start justify-between border-b pb-2">
        <div class="text-3xl font-medium">Image list</div>
        <button class="float-end" @click="imageList.flag = false">
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
                @change.prevent="handleFileChange"
              />
            </div>
          </div>
          <span v-if="errors.file || errors.file_ext || errors.file_size" class="text-red-500">{{
            errors.file
          }}</span>
        </div>
      </div>
      <div class="flex h-[500px] flex-wrap content-start gap-4 overflow-y-auto pb-20">
        <div v-for="(item, index) in imgList" :key="index">
          <div
            class="relative h-[150px] w-[150px] rounded-md border"
            :class="{ 'border-2 border-green-500': chooses.includes(item) }"
            @click.prevent="
              !chooses.includes(item)
                ? chooses.push(item)
                : (chooses = chooses.filter((i) => i !== item))
            "
          >
            <img
              :src="'http://localhost:8000/' + item.path"
              :alt="item.name"
              height="100%"
              width="100%"
              class="h-full w-full rounded-md object-contain"
            />
            <font-awesome-icon
              :icon="['fas', 'circle-check']"
              class="absolute right-0 top-0 text-green-500"
              :class="{ hidden: !chooses.includes(item) }"
            />
          </div>
          <div class="mt-1 flex justify-center gap-3">
            <button
              @click="returnImage(item)"
              class="rounded-md bg-green-500 px-2 text-white"
              :class="{ 'disabled bg-gray-400': chooses.length && !chooses.includes(item) }"
            >
              Use</button
            ><button
              class="rounded-md bg-red-500 px-2 text-white"
              :class="{ 'disabled bg-gray-400': chooses.length && !chooses.includes(item) }"
            >
              Del
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

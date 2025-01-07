<script setup>
import { ref, watch } from 'vue'
import * as XLSX from 'xlsx'
// import userService from 'service/user.service'
// import useValidate from 'composables/validate'
// import addUserSchema from 'schemas/admin/addUser'
// import ToastUtil from 'utility/toast'

// const { validate, errors } = useValidate()
const isCreateMail = defineModel()
const selectedFile = ref()
const attachedFile = ref()
const emailInput = ref()
const mail = ref({
  subject: '',
  recipient: [],
  body: '',
  attachedFile: null,
  cc: []
})
const isCheckedCC = ref(false)
const errorMailCc = ref()

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    readExcelFile(file)
  }
}

const readExcelFile = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    const binaryString = e.target.result
    const workbook = XLSX.read(binaryString, { type: 'binary' })

    // Get first sheet
    const sheetName = workbook.SheetNames[0]
    const worksheet = workbook.Sheets[sheetName]

    // Convert data to json
    const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 })
    // Get data (Don't get header)
    const dataGet = jsonData.slice(1)
    console.log(dataGet)
  }
  reader.readAsBinaryString(file)
}

const handleAttachedFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    attachedFile.value = file
  }
}
const addEmail = () => {
  const email = emailInput.value.trim()
  // Validate email
  const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
  if (!regex.test(emailInput.value) && emailInput.value.length > 0) {
    errorMailCc.value = 'Invalid email address'
    return
  }
  if (email && !mail.value.cc.includes(email)) {
    mail.value.cc.push(email)
  }
  errorMailCc.value = null
  emailInput.value = null
}
const removeEmail = (index) => {
  mail.value.cc.splice(index, 1)
}

watch(isCreateMail, () => {
  // errors.value = []
  selectedFile.value = null
})
</script>

<template>
  <div
    v-if="isCreateMail"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="isCreateMail = !isCreateMail"
  >
    <div
      class="h-[80%] w-[80%] overflow-y-auto overflow-x-hidden rounded-lg bg-white p-5 shadow-2xl pc:h-auto pc:w-[60%]"
    >
      <h2 class="mb-6 text-center text-2xl font-semibold">Send Email</h2>
      <!-- Subject -->
      <div class="mb-4">
        <div class="flex items-center justify-between">
          <label for="subject" class="block text-sm font-medium text-gray-700">Subject</label>
        </div>
        <input
          type="text"
          v-model="mail.subject"
          id="subject"
          placeholder="Enter subject"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- Recipient -->
      <div class="mb-4">
        <div class="flex items-center justify-between">
          <label for="recipient" class="block text-sm font-medium text-gray-700">Recipient</label>
          <div class="flex items-center">
            <div
              v-if="selectedFile"
              class="me-2 flex items-center rounded-2xl bg-gray-200 px-3 text-gray-700"
            >
              {{ selectedFile.name }}
              <font-awesome-icon
                @click.prevent="selectedFile = null"
                :icon="['fas', 'close']"
                class="h-4 w-4 cursor-pointer py-1 ps-1 text-red-500 transition duration-200 hover:text-red-700"
              />
            </div>
            <label
              for="file-input-recipient"
              class="inline-block cursor-pointer rounded-md bg-blue-500 px-2 py-1 text-white transition duration-200 hover:bg-blue-600"
            >
              <font-awesome-icon :icon="['fas', 'file-circle-plus']" class="h-4 w-4" />
            </label>
            <!-- Hidden file input -->
            <input
              id="file-input-recipient"
              type="file"
              class="hidden"
              @change.prevent="handleFileChange"
            />
          </div>
        </div>
        <input
          type="text"
          v-model="mail.recipient"
          id="recipient"
          placeholder="Enter recipient's email"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <!-- CC -->
      <div class="mb-4 flex items-center">
        <div class="me-2 flex items-center justify-between">
          <label
            for="cc"
            class="underline-offset-1ss block cursor-pointer text-sm font-medium leading-[42px] text-red-500 underline"
            >CC</label
          >
          <input type="checkbox" id="cc" class="hidden" v-model="isCheckedCC" />
        </div>
        <div class="w-full flex-col" v-if="isCheckedCC">
          <div class="flex-wrap items-center rounded-md border border-gray-200 p-2">
            <span
              v-for="(email, index) in mail.cc"
              :key="index"
              class="me-2 rounded-xl bg-gray-200 px-2"
            >
              {{ email }}
              <span
                class="cursor-pointer text-red-500 hover:text-red-700"
                @click="removeEmail(index)"
                >×</span
              >
            </span>
            <input
              v-model="emailInput"
              @keydown.enter="addEmail"
              @blur="addEmail"
              type="text"
              placeholder="Enter cc email address"
              class="w-full focus:outline-none"
            />
          </div>
          <p v-if="errorMailCc" class="mt-1 text-sm text-red-500">{{ errorMailCc }}</p>
        </div>
      </div>

      <!-- Body -->
      <div class="mb-4">
        <label for="body" class="block text-sm font-medium text-gray-700">Body</label>
        <textarea
          id="body"
          placeholder="Enter message"
          v-model="mail.body"
          rows="6"
          class="mt-1 w-full rounded-md border border-gray-200 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        ></textarea>
      </div>
      <!-- Attached file -->
      <div class="mb-4 flex items-center">
        <label for="attached-file" class="flex items-center">
          <span class="text-sm font-medium text-gray-700">Attached file:</span>
          <font-awesome-icon
            :icon="['fas', 'file-circle-plus']"
            class="ms-2 h-4 w-4 cursor-pointer rounded-md bg-blue-500 px-2 py-1 text-white transition duration-200 hover:bg-blue-600"
          />
        </label>
        <!-- Hidden file input -->
        <input
          id="attached-file"
          type="file"
          class="hidden"
          @change.prevent="handleAttachedFileChange"
        />
        <div v-if="mail.attachedFile" class="ms-2 flex items-center text-gray-700">
          {{ mail.attachedFile?.name }}
          <font-awesome-icon
            @click.prevent="mail.attachedFile = null"
            :icon="['fas', 'close']"
            class="h-4 w-4 cursor-pointer px-2 py-1 text-red-500 transition duration-200"
          />
        </div>
      </div>
      <button
        type="submit"
        class="w-full rounded-md bg-blue-500 py-3 font-semibold text-white transition duration-200 hover:bg-blue-600"
      >
        Send Email
      </button>
    </div>
  </div>
</template>

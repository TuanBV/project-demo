<script setup>
import { ref } from 'vue'
// import userService from 'service/user.service'
// import useValidate from 'composables/validate'
// import addUserSchema from 'schemas/admin/addUser'
// import ToastUtil from 'utility/toast'

// const { validate, errors } = useValidate()
const isAddUser = defineModel()
const selectedFile = ref()
const attachedFile = ref()
const mail = ref({
  subject: '',
  recipient: [],
  body: '',
  attachedFile: null,
  cc: []
})
const isCheckedCC = ref(false)

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
  }
}

const handleAttachedFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    attachedFile.value = file
  }
}

// watch(isAddUser, () => {
// errors.value = []
// })
</script>

<template>
  <div
    v-if="isAddUser"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="isAddUser = !isAddUser"
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
          class="mt-1 w-full rounded-md border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- Recipient -->
      <div class="mb-4">
        <div class="flex items-center justify-between">
          <label for="recipient" class="block text-sm font-medium text-gray-700">Recipient</label>
          <div class="flex items-center">
            <div v-if="selectedFile" class="me-2 flex items-center text-gray-700">
              {{ selectedFile.name }}
              <font-awesome-icon
                @click.prevent="selectedFile = null"
                :icon="['fas', 'close']"
                class="h-4 w-4 cursor-pointer px-2 py-1 text-red-500 transition duration-200"
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
            <div class="ms-2 flex items-center justify-between">
              <label
                for="cc"
                class="block cursor-pointer text-sm font-medium text-red-500 underline underline-offset-1"
                >CC</label
              >
              <input type="checkbox" id="cc" class="hidden" v-model="isCheckedCC" />
            </div>
          </div>
        </div>
        <input
          type="text"
          v-model="mail.recipient"
          id="recipient"
          placeholder="Enter recipient's email"
          class="mt-1 w-full rounded-md border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <!-- CC -->
      <div class="mb-4">
        <input
          v-if="isCheckedCC"
          type="text"
          placeholder="Enter cc email"
          class="mt-1 w-full rounded-md border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>
      <!-- Body -->
      <div class="mb-4">
        <label for="body" class="block text-sm font-medium text-gray-700">Body</label>
        <textarea
          id="body"
          placeholder="Enter message"
          v-model="mail.body"
          rows="6"
          class="mt-1 w-full rounded-md border border-gray-300 p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
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

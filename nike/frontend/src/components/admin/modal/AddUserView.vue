<script setup>
import { ref, watch } from 'vue'
import userService from 'service/user.service'
import useValidate from 'composables/validate'
import addUserSchema from 'schemas/admin/addUser'
import ToastUtil from 'utility/toast'

const { validate, errors } = useValidate()
const isAddUser = defineModel()
const user = ref({
  username: '',
  email: '',
  fullname: '',
  birthday: '',
  password: '',
  area: '',
  city: '',
  state: '',
  postcode: ''
})

const addUser = async () => {
  const isValid = validate(addUserSchema, user.value)
  if (!isValid) return
  const res = await userService.add(user.value)
  if (res) {
    ToastUtil.success('Added user successfully !!!')
    isAddUser.value = false
  }
}

watch(isAddUser, () => {
  errors.value = []
})
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
      <div class="flex items-start justify-between border-b pb-2">
        <h1 class="text-3xl font-medium">Add user</h1>
        <button class="float-end" @click="isAddUser = false">
          <font-awesome-icon :icon="['fas', 'close']" />
        </button>
      </div>
      <div class="mx-auto h-full w-full py-2">
        <div class="flex items-center justify-center">
          <div class="mx-auto w-full bg-white">
            <div class="mb-4">
              <label for="phone" class="block text-base font-medium">
                Username <span class="text-red-500">(*)</span></label
              >
              <input
                type="text"
                name="Username"
                v-model="user.username"
                placeholder="Enter your username"
                class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
              <p v-if="errors.username" class="mt-2 text-sm italic text-red-500">
                {{ errors.username }}
              </p>
            </div>
            <div class="mb-4">
              <label for="email" class="block text-base font-medium">
                Email Address <span class="text-red-500">(*)</span></label
              >
              <input
                type="email"
                name="email"
                v-model="user.email"
                placeholder="Enter your email"
                class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
              <p v-if="errors.email" class="mt-2 text-sm italic text-red-500">
                {{ errors.email }}
              </p>
            </div>
            <div class="mb-4">
              <label for="name" class="block text-base font-medium">
                Full Name <span class="text-red-500">(*)</span></label
              >
              <input
                type="text"
                name="name"
                v-model="user.fullname"
                placeholder="Full Name"
                class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
              <p v-if="errors.fullname" class="mt-2 text-sm italic text-red-500">
                {{ errors.fullname }}
              </p>
            </div>
            <div class="-mx-3 flex flex-wrap">
              <div class="w-full px-3 sm:w-1/2">
                <div class="mb-4">
                  <label for="date" class="block text-base font-medium"> Birthday </label>
                  <input
                    type="date"
                    name="date"
                    v-model="user.birthday"
                    class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                  />
                </div>
                <p v-if="errors.birthday" class="mt-2 text-sm italic text-red-500">
                  {{ errors.birthday }}
                </p>
              </div>
              <div class="w-full px-3 sm:w-1/2">
                <div class="mb-4">
                  <label for="password" class="block text-base font-medium">
                    Password <span class="text-red-500">(*)</span></label
                  >
                  <input
                    type="password"
                    name="password"
                    v-model="user.password"
                    class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                  />
                </div>
                <p v-if="errors.password" class="mt-2 text-sm italic text-red-500">
                  {{ errors.password }}
                </p>
              </div>
            </div>
            <div class="mb-4 pt-3">
              <label class="block text-base font-semibold"> Address Details </label>
              <div class="-mx-3 flex flex-wrap">
                <div class="w-full px-3 sm:w-1/2">
                  <div class="mb-4">
                    <input
                      type="text"
                      name="area"
                      v-model="user.area"
                      placeholder="Enter area"
                      class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    />
                  </div>
                  <p v-if="errors.area" class="mt-2 text-sm italic text-red-500">
                    {{ errors.area }}
                  </p>
                </div>
                <div class="w-full px-3 sm:w-1/2">
                  <div class="mb-4">
                    <input
                      type="text"
                      name="city"
                      v-model="user.city"
                      placeholder="Enter city"
                      class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    />
                  </div>
                  <p v-if="errors.city" class="mt-2 text-sm italic text-red-500">
                    {{ errors.city }}
                  </p>
                </div>
                <div class="w-full px-3 sm:w-1/2">
                  <div class="mb-4">
                    <input
                      type="text"
                      name="state"
                      v-model="user.state"
                      placeholder="Enter state"
                      class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    />
                  </div>
                  <p v-if="errors.state" class="mt-2 text-sm italic text-red-500">
                    {{ errors.state }}
                  </p>
                </div>
                <div class="w-full px-3 sm:w-1/2">
                  <div class="mb-4">
                    <input
                      type="text"
                      name="post-code"
                      v-model="user.postcode"
                      placeholder="Post Code"
                      class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                    />
                  </div>
                  <p v-if="errors.postcode" class="mt-2 text-sm italic text-red-500">
                    {{ errors.postcode }}
                  </p>
                </div>
              </div>
            </div>

            <div>
              <button
                @click.prevent="addUser"
                class="hover:shadow-form w-full rounded-md bg-green-500 px-8 py-2 text-center text-base font-semibold text-white outline-none hover:bg-green-600"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import userService from 'service/user.service'
import useValidate from 'composables/validate'
import userSchema from 'schemas/user/user'
import { useRouter } from 'vue-router'

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const { errors, validate } = useValidate()
const router = useRouter()
// ==> 1.2) actions
// ==> 1.3) Others
// 2) ======= VARIABLE REF ========
const data = ref({
  username: '',
  email: '',
  fullname: '',
  password: ''
})
// 3) ======= METHOD/FUNCTION ========
const addUser = async () => {
  const isValid = validate(userSchema, data.value)
  if (!isValid) return
  const res = await userService.add(data.value)
  if (res) {
    router.push({ name: 'sign-in' })
  }
}
// 4) ======= VUE JS LIFECYCLE ========

// onMounted(() => {
//   getUser()
// })
</script>
<template>
  <section class="flex min-h-screen items-center justify-center border-red-500 bg-gray-200">
    <div class="flex max-w-full rounded-2xl bg-gray-100 p-5 shadow-lg tablet:max-w-[50%]">
      <div class="px-5">
        <h2 class="text-2xl font-bold text-[#002D74]">Login</h2>
        <p class="mt-4 text-sm text-[#002D74]">If you have an account, please login</p>
        <div class="mt-6">
          <div>
            <label for="username" class="block text-gray-700">Username</label>
            <input
              v-model="data.username"
              type="text"
              name="username"
              placeholder="Enter Username"
              class="mt-2 w-full rounded-lg border bg-gray-200 px-4 py-3 focus:border-blue-500 focus:bg-white focus:outline-none"
              required
            />
            <p v-if="errors.username" class="mt-2 text-sm text-red-500">{{ errors.username }}</p>
          </div>
          <div class="mt-4">
            <label for="email" class="block text-gray-700">Email Address</label>
            <input
              v-model="data.email"
              type="email"
              name="email"
              placeholder="Enter Email Address"
              class="mt-2 w-full rounded-lg border bg-gray-200 px-4 py-3 focus:border-blue-500 focus:bg-white focus:outline-none"
              required
            />
            <p v-if="errors.email" class="mt-2 text-sm text-red-500">{{ errors.email }}</p>
          </div>
          <div class="mt-4">
            <label for="fullname" class="block text-gray-700">Fullname</label>
            <input
              v-model="data.fullname"
              type="text"
              name="fullname"
              placeholder="Enter name"
              class="mt-2 w-full rounded-lg border bg-gray-200 px-4 py-3 focus:border-blue-500 focus:bg-white focus:outline-none"
              required
            />
            <p v-if="errors.fullname" class="mt-2 text-sm text-red-500">{{ errors.fullname }}</p>
          </div>
          <div class="mt-4">
            <label for="password" class="block text-gray-700">Password</label>
            <input
              v-model="data.password"
              type="password"
              name=""
              placeholder="Enter Password"
              minlength="6"
              class="mt-2 w-full rounded-lg border bg-gray-200 px-4 py-3 focus:border-blue-500 focus:bg-white focus:outline-none"
              required
            />
            <p v-if="errors.password" class="mt mt-2 text-sm text-red-500">{{ errors.password }}</p>
          </div>

          <button
            type="submit"
            @click.prevent="addUser"
            class="mt-6 block w-full rounded-lg bg-blue-500 px-4 py-3 font-semibold text-white hover:bg-blue-400 focus:bg-blue-400"
          >
            Sign Up
          </button>
        </div>

        <div class="mt-7 grid grid-cols-3 items-center text-gray-500">
          <hr class="border-gray-500" />
          <p class="text-center text-sm">OR</p>
          <hr class="border-gray-500" />
        </div>

        <div class="mt-3 flex items-center justify-between text-sm">
          <p>If you have an account...</p>
          <router-link
            to="/sign-in"
            class="ml-3 rounded-xl border border-blue-400 bg-white px-5 py-2 font-medium duration-300 hover:scale-110"
          >
            Sign In
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

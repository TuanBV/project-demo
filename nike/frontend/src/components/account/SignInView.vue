<script setup>
import userService from 'service/user.service'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const router = useRouter()
// ==> 1.2) actions
// ==> 1.3) Others
// 2) ======= VARIABLE REF ========
const data = ref({
  email: '',
  password: '',
  role: 0
})

const login = async () => {
  const res = await userService.login(data.value)
  if (res) {
    router.push('/') // Redirect to home page after successful login
  }
}
</script>
<template>
  <section class="flex min-h-screen items-center justify-center border-red-500 bg-gray-200">
    <div class="flex max-w-3xl rounded-2xl bg-gray-100 p-5 shadow-lg">
      <div class="md:w-1/2 px-5">
        <h2 class="text-2xl font-bold text-[#002D74]">Login</h2>
        <p class="mt-4 text-sm text-[#002D74]">If you have an account, please login</p>
        <div class="mt-6">
          <div>
            <label for="email" class="block text-gray-700">Email Address</label>
            <input
              v-model="data.email"
              type="email"
              name=""
              id=""
              placeholder="Enter Email Address"
              class="mt-2 w-full rounded-lg border bg-gray-200 px-4 py-3 focus:border-blue-500 focus:bg-white focus:outline-none"
              autofocus
              required
            />
          </div>

          <div class="mt-4">
            <label for="password" class="block text-gray-700">Password</label>
            <input
              v-model="data.password"
              type="password"
              name=""
              id=""
              placeholder="Enter Password"
              minlength="8"
              class="mt-2 w-full rounded-lg border bg-gray-200 px-4 py-3 focus:border-blue-500 focus:bg-white focus:outline-none"
              required
            />
          </div>

          <div class="mt-2 text-right">
            <router-link
              to="/forgot-password"
              class="text-sm font-semibold text-gray-700 hover:text-blue-700 focus:text-blue-700"
              >Forgot Password?</router-link
            >
          </div>

          <button
            type="submit"
            @click.prevent="login"
            class="mt-6 block w-full rounded-lg bg-blue-500 px-4 py-3 font-medium text-white hover:bg-blue-400 focus:bg-blue-400"
          >
            Sign In
          </button>
        </div>

        <div class="mt-7 grid grid-cols-3 items-center text-gray-500">
          <hr class="border-gray-500" />
          <p class="text-center text-sm">OR</p>
          <hr class="border-gray-500" />
        </div>

        <button
          class="mt-5 flex w-full items-center justify-center rounded-xl border bg-white py-2 text-sm duration-300 hover:scale-105"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            class="h-6 w-6"
            viewBox="0 0 48 48"
          >
            <defs>
              <path
                id="a"
                d="M44.5 20H24v8.5h11.8C34.7 33.9 30.1 37 24 37c-7.2 0-13-5.8-13-13s5.8-13 13-13c3.1 0 5.9 1.1 8.1 2.9l6.4-6.4C34.6 4.1 29.6 2 24 2 11.8 2 2 11.8 2 24s9.8 22 22 22c11 0 21-8 21-22 0-1.3-.2-2.7-.5-4z"
              />
            </defs>
            <clipPath id="b"><use xlink:href="#a" overflow="visible" /></clipPath>
            <path clip-path="url(#b)" fill="#FBBC05" d="M0 37V11l17 13z" />
            <path clip-path="url(#b)" fill="#EA4335" d="M0 11l17 13 7-6.1L48 14V0H0z" />
            <path clip-path="url(#b)" fill="#34A853" d="M0 37l30-23 7.9 1L48 0v48H0z" />
            <path clip-path="url(#b)" fill="#4285F4" d="M48 48L17 24l-4-3 35-10z" />
          </svg>
          <span class="ml-4 font-medium">Login with Google</span>
        </button>

        <div class="mt-3 flex items-center justify-between text-sm">
          <p>If you don't have an account...</p>
          <router-link
            to="/sign-up"
            class="ml-3 rounded-xl border border-blue-400 bg-white px-5 py-2 font-medium duration-300 hover:scale-110"
          >
            Sign Up
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

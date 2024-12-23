<script setup>
import userService from 'service/user.service'
import { ref } from 'vue'
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
  role: 1
})

const login = async () => {
  const res = await userService.login(data.value)
  if (res) {
    router.push('/v1/admin') // Redirect to home page after successful login
  }
}
</script>
<template>
  <section class="flex min-h-screen items-center justify-center border-red-500 bg-gray-200">
    <div class="flex w-full rounded-2xl bg-gray-100 p-5 shadow-lg tablet:w-[60%] pc:w-[40%]">
      <div class="w-full px-5">
        <h2 class="text-2xl font-bold text-[#002D74]">Login</h2>
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
              minlength="6"
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
      </div>
    </div>
  </section>
</template>

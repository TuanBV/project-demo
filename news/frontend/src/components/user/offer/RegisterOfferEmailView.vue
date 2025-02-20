<script setup>
import { ref } from 'vue'
import ToastUtil from 'utility/toast'
const email = ref()
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

const registerOffer = () => {
  if (!email.value || !emailRegex.test(email.value)) {
    ToastUtil.error('Please enter a valid email address.')
    return
  }
  // Your email validation logic here... then call APi
}
</script>

<template>
  <div
    class="mx-auto max-w-[1300px] px-7 py-10"
    data-aos="fade-up"
    data-aos-offset="200"
    data-aos-delay="50"
    data-aos-easing="ease-in-out"
    data-aos-anchor-placement="top-bottom"
  >
    <p class="mb-3">
      Sign up with your email to get access to special deals and big sale events from our store.
    </p>
    <div class="block gap-5 tablet:flex">
      <input
        type="email"
        v-model="email"
        @keyup.enter="registerOffer"
        placeholder="Please enter your email ..."
        class="w-full rounded-lg border border-gray-300 px-2 py-1 hover:border-gray-400 tablet:w-[50%]"
      />
      <button
        @click.prevent="registerOffer"
        class="before:content[''] after:content[''] after:w20 after:roundedfull group relative h-16 origin-left overflow-hidden rounded-lg border bg-neutral-800 p-3 pr-28 text-left text-xl font-bold uppercase text-gray-50 underline underline-offset-2 duration-500 before:absolute before:right-1 before:top-1 before:z-10 before:h-12 before:w-12 before:rounded-full before:bg-violet-500 before:blur-lg before:duration-500 after:absolute after:right-8 after:top-3 after:z-10 after:h-20 after:bg-rose-300 after:blur-lg after:duration-500 hover:border-rose-300 hover:text-rose-300 hover:underline hover:decoration-2 hover:underline-offset-4 hover:duration-500 hover:before:-bottom-8 hover:before:right-12 hover:before:blur hover:before:[box-shadow:_20px_20px_20px_30px_#a21caf] hover:after:-right-8 group-hover:before:duration-500 group-hover:after:duration-500"
      >
        <font-awesome-icon :icon="['fas', 'percent']" />
        <span class="mx-2">Register Offer Now</span><font-awesome-icon :icon="['fas', 'percent']" />
      </button>
    </div>
  </div>
</template>

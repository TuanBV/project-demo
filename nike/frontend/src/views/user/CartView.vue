<script setup>
import { ref } from 'vue'
const products = ref([
  {
    image: 'assets/images/air_force_1.png',
    name: 'Air Force 1',
    code: 'AF001',
    price: 999,
    quantity: 1
  }
])
</script>
<template>
  <div class="mx-auto mt-10 max-w-[1300px]">
    <div class="m-10 gap-10 sm:flex">
      <div class="w-full sm:w-3/5 pc:w-2/3">
        <div class="border-b pb-8">
          <h1 class="text-2xl font-medium">Shopping Cart</h1>
        </div>
        <div
          class="items-stretch gap-5 border-b border-gray-200 py-5 sm:flex"
          v-for="(item, index) in products"
          :key="index"
        >
          <div class="w-full sm:w-1/4 pc:w-4/12">
            <img
              loading="lazy"
              src="assets/images/air_force_1.png"
              alt="Air Force 1"
              class="object-cover object-center"
            />
          </div>
          <div class="flex flex-col justify-center sm:w-3/4 pc:w-8/12">
            <p class="pt-4 text-xs leading-3 text-gray-800 sm:pt-0">RF293</p>
            <p class="pt-4 text-base font-black leading-none text-gray-800">Luxe card holder</p>
            <p class="pt-4 text-xs leading-3 text-gray-600">Height: 10 inches</p>
            <p class="py-4 text-xs leading-3 text-gray-600">Color: Black</p>
            <p class="w-96 text-xs leading-3 text-gray-600">Composition: 100% calf leather</p>
            <div class="flex items-center justify-between pt-5">
              <div class="itemms-center flex">
                <p class="cursor-pointer text-xs leading-3 text-gray-800 underline">
                  Add to favorites
                </p>
                <p class="cursor-pointer pl-5 text-xs leading-3 text-red-500 underline">Remove</p>
              </div>
              <p class="text-base font-black leading-none text-gray-800">500 $</p>
            </div>
          </div>
        </div>
        <router-link to="/product" class="mt-10 flex text-sm font-medium text-indigo-600">
          <svg class="mr-2 w-4 fill-current text-indigo-600" viewBox="0 0 448 512">
            <path
              d="M134.059 296H436c6.627 0 12-5.373 12-12v-56c0-6.627-5.373-12-12-12H134.059v-46.059c0-21.382-25.851-32.09-40.971-16.971L7.029 239.029c-9.373 9.373-9.373 24.569 0 33.941l86.059 86.059c15.119 15.119 40.971 4.411 40.971-16.971V296z"
            />
          </svg>
          Continue Shopping
        </router-link>
      </div>
      <div id="summary" class="w-full sm:w-2/5 pc:w-1/3">
        <h1 class="border-b pb-8 text-2xl font-medium">Order Summary</h1>
        <div class="mb-5 mt-10 flex justify-between">
          <span class="text-sm font-medium uppercase">Items 3</span>
          <span class="text-sm font-medium">590$</span>
        </div>
        <div>
          <label class="mb-3 inline-block text-sm font-medium uppercase"> Shipping </label>
          <select class="block w-full rounded border-[1px] p-2 text-sm text-gray-600">
            <option>Standard shipping - $10.00</option>
          </select>
        </div>
        <div class="py-10">
          <label for="promo" class="mb-3 inline-block text-sm font-medium uppercase">
            Promo Code
          </label>
          <input
            type="text"
            id="promo"
            placeholder="Enter your code"
            class="w-full rounded border-[1px] p-2 text-sm"
          />
        </div>
        <button class="bg-red-500 px-5 py-2 text-sm uppercase text-white hover:bg-red-600">
          Apply
        </button>
        <div class="mt-8 border-t">
          <div class="flex justify-between py-6 text-sm font-medium uppercase">
            <span>Total cost</span>
            <span>$600</span>
          </div>
          <button
            class="w-full rounded bg-indigo-500 py-3 text-sm font-medium uppercase text-white hover:bg-indigo-600"
          >
            Checkout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

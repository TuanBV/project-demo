<script setup>
import { onMounted, ref } from 'vue'
import ProductDetailView from 'components/product/ProductDetailView.vue'
import ItemProduct from 'components/product/ItemProduct.vue'

const productList = ref([
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  },
  {
    id: 1,
    name: 'Basic Tee',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    price: 99.99,
    image: [
      '/src/assets/images/air_force_1.png',
      '/src/assets/images/air_jordan_1.png',
      '/src/assets/images/dunks.png',
      '/src/assets/images/killshot.png',
      '/src/assets/images/pegasus_41.png',
      '/src/assets/images/v2k.png'
    ]
  }
])
const product = ref()

onMounted(() => {
  console.log('aaa')
})
</script>

<template>
  <section>
    <div class="mx-auto max-w-7xl px-10 py-8 tablet:px-6 pc:px-8 pc:py-12">
      <header>
        <h2 class="text-xl font-bold text-gray-900 sm:text-3xl">Product Collection</h2>

        <p class="mt-4 text-gray-500">
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Itaque praesentium cumque iure
          dicta incidunt est ipsam, officia dolor fugit natus?
        </p>
      </header>

      <div class="mt-8">
        <p class="text-sm text-gray-500">Showing <span> 4 </span> of 40</p>
      </div>

      <div class="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 tablet:grid-cols-3 pc:grid-cols-4">
        <div v-for="(item, index) in productList" :key="index">
          <ItemProduct
            :itemProduct="item"
            @update:itemProduct="(newValue) => (product = newValue)"
          />
        </div>
      </div>
      <ol class="mt-8 flex justify-center gap-1 text-xs font-medium">
        <li>
          <a
            href="#"
            class="inline-flex size-8 items-center justify-center rounded border border-gray-100"
          >
            <span class="sr-only">Prev Page</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="size-3"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                clip-rule="evenodd"
              />
            </svg>
          </a>
        </li>

        <li>
          <a href="#" class="block size-8 rounded border border-gray-100 text-center leading-8">
            1
          </a>
        </li>

        <li class="block size-8 rounded border-black bg-black text-center leading-8 text-white">
          2
        </li>

        <li>
          <a href="#" class="block size-8 rounded border border-gray-100 text-center leading-8">
            3
          </a>
        </li>

        <li>
          <a href="#" class="block size-8 rounded border border-gray-100 text-center leading-8">
            4
          </a>
        </li>

        <li>
          <a
            href="#"
            class="inline-flex size-8 items-center justify-center rounded border border-gray-100"
          >
            <span class="sr-only">Next Page</span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="size-3"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                clip-rule="evenodd"
              />
            </svg>
          </a>
        </li>
      </ol>
    </div>
    <ProductDetailView v-model="product" />
  </section>
</template>

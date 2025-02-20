<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const newsList = ref([])

const fetchNews = async () => {
  const response = await axios.get('http://127.0.0.1:8000/api/news/')
  newsList.value = response.data
}

const products = [
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
  {
    id: 1,
    name: 'Basic Tee',
    href: '#',
    imageSrc:
      'https://tailwindui.com/plus-assets/img/ecommerce-images/product-page-01-related-product-01.jpg',
    imageAlt: "Front of men's Basic Tee in black.",
    price: '$35',
    color: 'Black',
  },
]

onMounted(fetchNews)
</script>

<template>
  <div class="bg-white">
    <div v-for="news in newsList" :key="news.id" class="news-item">
      <img
        v-if="news.image"
        :src="news.image"
        height="auto"
        width="auto"
        alt="Ảnh tin tức"
        class="news-image"
      />
      <h2>{{ news.title }}</h2>
      <div v-html="news.content"></div>
    </div>
    <div class="mx-auto max-w-2xl px-4 py-16 sm:px-6 sm:py-24 pc:max-w-7xl pc:px-8">
      <h2 class="text-2xl font-bold tracking-tight text-gray-900">Customers also purchased</h2>

      <div class="mt-6 grid grid-cols-1 gap-x-6 gap-y-10 sm:grid-cols-2 pc:grid-cols-4 xl:gap-x-8">
        <div v-for="product in products" :key="product.id" class="group relative">
          <img
            :src="product.imageSrc"
            :alt="product.imageAlt"
            class="aspect-square w-full rounded-md bg-gray-200 object-cover group-hover:opacity-75 pc:aspect-auto pc:h-80"
          />
          <div class="mt-4 flex justify-between">
            <div>
              <h3 class="text-sm text-gray-700">
                <a :href="product.href">
                  <span aria-hidden="true" class="absolute inset-0" />
                  {{ product.name }}
                </a>
              </h3>
              <p class="mt-1 text-sm text-gray-500">{{ product.color }}</p>
            </div>
            <p class="text-sm font-medium text-gray-900">{{ product.price }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.news-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px 0;
}
.news-image {
  width: 100%;
  max-width: 400px;
  height: auto;
}
</style>

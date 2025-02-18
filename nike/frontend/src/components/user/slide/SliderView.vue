<script setup>
// Import Swiper Vue.js components
import { Swiper, SwiperSlide } from 'swiper/vue'
// Import Swiper styles
import 'swiper/css'
import 'swiper/css/effect-fade'
import 'swiper/css/navigation'
import 'swiper/css/pagination'
// import required modules
import { EffectFade, Navigation, Pagination, Autoplay } from 'swiper/modules'
import { reactive, ref } from 'vue'

const modules = [EffectFade, Navigation, Pagination, Autoplay]
const sale = ref({
  text: 'New Style On Sale: Up to 40% Off',
  toText: 'Shop All Our New Markdowns',
  to: '/product/sale'
})
const slides = reactive([
  {
    title: 'Slide 1',
    description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    image: 'src/assets/images/slider_1.jpg'
  },
  {
    title: 'Slide 2',
    description: 'Curabitur eget velit vel nulla faucibus vulputate.',
    image: 'src/assets/images/slider_2.jpg'
  },
  {
    title: 'Slide 3',
    description: 'Proin tincidunt neque vel libero faucibus, at semper arcu fermentum.',
    image: 'src/assets/images/slider_3.jpg'
  },
  {
    title: 'Slide 4',
    description: 'Sed vel elit vel neque pellentesque ultricies vitae quis felis.',
    image: 'src/assets/images/slider_4.jpg'
  }
])
</script>

<template>
  <section>
    <!-- Sale -->
    <div class="bg-[#e5e5e5] py-3 text-center">
      <p class="font-medium">{{ sale.text }}</p>
      <router-link :to="sale.to" class="font-medium underline underline-offset-2">
        {{ sale.toText }}</router-link
      >
    </div>
    <!-- Slide -->
    <div
      class="xl:h-[80vh] h-[60vh] max-w-[100vw] overflow-hidden"
      data-aos="fade-up"
      data-aos-offset="200"
      data-aos-delay="50"
      data-aos-easing="ease-in-out"
    >
      <!-- :autoplay="{
        delay: 20000,
        disableOnInteraction: false
      }" -->
      <swiper
        :style="{
          '--swiper-navigation-color': '#fff',
          '--swiper-pagination-color': '#fff'
        }"
        :spaceBetween="30"
        :effect="'fade'"
        :navigation="true"
        :pagination="{
          clickable: true
        }"
        :loop="true"
        :modules="modules"
        :autoplay="{
          delay: 2000,
          disableOnInteraction: false
        }"
        class="mySwiper"
      >
        <swiper-slide v-for="(item, index) in slides" :key="index">
          <div class="flex h-full w-full justify-center">
            <img loading="lazy" :src="item.image" alt="" width="100%" height="100%" />
            <div class="xl:w-[75%] absolute bottom-7">
              <router-link
                to="/product"
                class="lg:font-semibold group relative isolation-auto z-10 mx-auto flex items-center justify-center gap-2 overflow-hidden rounded-full border-2 border-gray-50 bg-gray-50 px-4 py-2 text-lg shadow-xl backdrop-blur-md before:absolute before:-left-full before:-z-10 before:aspect-square before:w-full before:rounded-full before:bg-emerald-500 before:transition-all before:duration-700 hover:text-gray-50 before:hover:left-0 before:hover:w-full before:hover:scale-150 before:hover:duration-700"
              >
                Shopping Now ...
              </router-link>
            </div>
          </div>
        </swiper-slide>
      </swiper>
    </div>
  </section>
</template>

<style scoped>
.swiper {
  width: 100%;
  height: 100%;
}

.swiper-slide {
  background-position: center;
  background-size: cover;
}

.swiper-slide img {
  display: block;
  object-fit: cover;
}
.swiper-button-prev {
  border: 1px solid red;
  padding: 5px;
  border-radius: 5px;
}
</style>

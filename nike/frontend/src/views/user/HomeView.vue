<script setup>
import SliderView from 'components/user/slide/SliderView.vue'
import PosterView from 'components/user/poster/PosterView.vue'
import RegisterOfferEmailView from 'components/user/offer/RegisterOfferEmailView.vue'
</script>

<template>
  <main>
    <SliderView />
    <!-- Go to shop  -->
    <div
      class="py-5 text-center"
      data-aos="fade-up"
      data-aos-offset="200"
      data-aos-delay="50"
      data-aos-easing="ease-in-out"
    >
      <h1 class="text-8xl font-black tracking-widest">Give sport</h1>
      <div class="mb-16 mt-3 tracking-[5px]">
        Inspire them with gifts designed for championship athletes.
      </div>
      <div>
        <router-link class="btn-hover mx-5 tracking-[3px]" to="/product"
          >Shop <font-awesome-icon :icon="['fas', 'arrow-right']" class="icon ml-3"
        /></router-link>
        <router-link class="btn-hover mx-5 tracking-[3px]" to="/product/kids"
          >Shop Kids <font-awesome-icon :icon="['fas', 'arrow-right']" class="icon ml-3"
        /></router-link>
      </div>
    </div>

    <PosterView />
    <RegisterOfferEmailView />
  </main>
</template>
<style scoped>
.btn-hover:hover .icon {
  transition: all 600ms ease;
  margin-left: 15px;
}
</style>

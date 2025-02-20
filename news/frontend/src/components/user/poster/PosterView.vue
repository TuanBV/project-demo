<script setup>
import { ref } from 'vue'

const quoteList = ref([
  {
    quote: 'I am Groot.',
    author: 'Groot',
    image: 'src/assets/images/air_force_1.png'
  },
  {
    quote: "You'r the head of security and your password is 'password'&nbsp;?",
    author: 'Peter Parker',
    image: 'src/assets/images/air_jordan_1.png'
  },
  {
    quote: "That really is America's ass.",
    author: 'Captain America',
    image: 'src/assets/images/dunks.png'
  },
  {
    quote: 'The hardest choices require the strongest wills.',
    author: 'Thanos',
    image: 'src/assets/images/killshot.png'
  },
  {
    quote: 'Genius, billionaire, playboy, philanthropist.',
    author: 'Tony Stark',
    image: 'src/assets/images/pegasus_41.png'
  },
  {
    quote: 'We never lose our demons. We only learn to live above them.',
    author: 'Ancient One',
    image: 'src/assets/images/v2k.png'
  }
])
</script>
<template>
  <div
    class="container-customer"
    data-aos="fade-up"
    data-aos-offset="200"
    data-aos-delay="50"
    data-aos-easing="ease-in-out"
    data-aos-anchor-placement="top-bottom"
  >
    <router-link
      v-for="(item, index) in quoteList"
      class="item"
      :key="index"
      to="/product"
      :style="{ backgroundImage: `url(${item.image})` }"
    >
    </router-link>
  </div>
</template>
<style scoped>
.container-customer {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 50vh;
  background: #111;

  @media (min-width: 1024px) {
    flex-direction: row;
  }
}

.item {
  position: relative;
  flex: calc(100vw / 6) 1 1;
  background-size: cover;
  overflow: hidden;
  filter: saturate(90%);
  transition: 1s;
}

.item:before {
  content: '';
  position: absolute;
  inset: 0;
  /* background: linear-gradient(0deg, #ffffff00, #00000073); */
}

.item:not(:last-child) {
  /* border-bottom: 1px solid white; */
  animation: borderPulse 5s infinite;

  @media (min-width: 1024px) {
    border-right: 1px solid white;
    border-bottom: none;
  }
}

.item:hover {
  flex-basis: 40%;
  filter: saturate(150%);

  @media (min-width: 1024px) {
    flex-basis: 75%;
  }
}

.item:hover .quote {
  opacity: 1;
  transform: translateX(0);
}

.item:nth-child(1) {
  background-position: 60% 50%;
}

.item:nth-child(2) {
  background-position: 60% 50%;
}

.item:nth-child(3) {
  background-position: 52% 50%;
}
.item:nth-child(4) {
  background-position: 45% 50%;
}

.item:nth-child(5) {
  background-position: 45% 50%;
}

.item:nth-child(6) {
  background-position: 65% 50%;
}

.quote {
  position: absolute;
  color: #fff;
  bottom: 35%;
  left: 5rem;
  width: calc(100% - 10rem);
  opacity: 0;
  transition: 1s;
  transform: translateX(50%);

  @media (min-width: 512px) {
    left: 15%;
    bottom: 55%;
    width: 50vw;
  }
}

@keyframes borderPulse {
  0%,
  100% {
    border-color: rgba(214, 214, 214, 0.6);
  }
  25%,
  75% {
    /* border-color: rgba(204, 204, 255, 0.9); */
    border-color: rgba(214, 214, 214, 0.6);
  }
  50% {
    /* border-color: rgba(204, 204, 255, 0.5); */
    border-color: rgba(214, 214, 214, 0.6);
  }
}
</style>

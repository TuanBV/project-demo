<script setup>
import { ref } from 'vue'

const quoteList = ref([
  { quote: 'I am Groot.', author: 'Groot' },
  {
    quote: "You'r the head of security and your password is 'password'&nbsp;?",
    author: 'Peter Parker'
  },
  { quote: "That really is America's ass.", author: 'Captain America' },
  { quote: 'The hardest choices require the strongest wills.', author: 'Thanos' },
  { quote: 'Genius, billionaire, playboy, philanthropist.', author: 'Tony Stark' },
  { quote: 'We never lose our demons. We only learn to live above them.', author: 'Ancient One' }
])
</script>
<template>
  <div class="container-customer">
    <div class="item" v-for="(item, index) in quoteList" :key="index">
      <div class="quote">
        <p>
          {{ item.quote }}<span>{{ item.author }}</span>
        </p>
      </div>
    </div>
  </div>
</template>
<style scoped>
.container-customer {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
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
  background: linear-gradient(25deg, rgba(0, 0, 0, 0.9), rgba(0, 0, 0, 0));
}

.item:not(:last-child) {
  border-bottom: 1px solid #ccc;
  animation: borderPulse 5s infinite;

  @media (min-width: 1024px) {
    border-right: 1px solid #ccc;
    border-bottom: none;
  }
}

.item:hover {
  flex-basis: 40%;
  filter: saturate(120%);

  @media (min-width: 1024px) {
    flex-basis: 75%;
  }

  .quote {
    opacity: 1;
    transform: translateX(0);
  }
}

.item:nth-child(1) {
  background-image: url('https://cdn.wallpapersafari.com/41/38/ruKsD7.jpg');
  background-position: 72% 35%;
}

.item:nth-child(2) {
  background-image: url('https://fr.web.img6.acsta.net/r_1920_1080/pictures/19/06/03/11/14/3505525.jpg');
  background-position: 60% 8%;
}

.item:nth-child(3) {
  background-image: url('https://images8.alphacoders.com/101/1012160.jpg');
  background-position: 52% 8%;
}

.item:nth-child(4) {
  background-image: url('https://img1.wallspic.com/attachments/originals/6/2/8/5/6/165826-thanos_the_mad-3840x2160.jpg');
  background-position: 45% 8%;
}

.item:nth-child(5) {
  background-image: url('https://c.wallhere.com/photos/df/a3/1920x1080_px_Iron_man_Iron_Man_3_Robert_Downey_Jr_sea_Tony_Stark-514897.jpg!d');
  background-position: 45% 25%;
}

.item:nth-child(6) {
  background-image: url('https://static1.cbrimages.com/wordpress/wp-content/uploads/2019/05/Tilda-Swinton-as-the-Ancient-One-in-Doctor-Strange.jpg');
  background-position: 65% 2%;
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
    bottom: 35%;
    width: 20vw;
  }

  @media (min-width: 1024px) {
    left: 15%;
    bottom: 35%;
    width: 30vw;
  }

  p {
    position: relative;
    display: inline-block;
    margin-bottom: 1.7rem;
    font-size: 1.4rem;
    text-wrap: balance;
    font-style: italic;

    &:before,
    &:after {
      position: absolute;
      font-size: 5.5rem;
      opacity: 0.6;
    }

    &:before {
      content: '“';
      top: 4rem;
      left: -2rem;
      transform: translate(-100%, -100%);
    }

    &:after {
      content: '”';
      bottom: 2rem;
      right: -2rem;
      transform: translate(100%, 100%);
    }
  }

  span {
    position: absolute;
    bottom: -2rem;
    right: 0;
    text-align: right;
    font-size: 1.2rem;
    font-weight: bold;
    transform: translate(4rem, 100%);

    &:before {
      content: '—';
      margin-right: 0.7rem;
    }
  }
}

@keyframes borderPulse {
  0%,
  100% {
    border-color: rgba(204, 204, 204, 1);
  }
  25%,
  75% {
    border-color: rgba(204, 204, 255, 0.9);
  }
  50% {
    border-color: rgba(204, 204, 255, 0.5);
  }
}
</style>

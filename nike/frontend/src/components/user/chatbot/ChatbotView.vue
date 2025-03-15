<script setup>
import { ref, nextTick, watch } from 'vue'

// State cho chatbot
const messages = ref([{ text: 'Xin chào! Mình có thể giúp gì cho bạn?', isUser: false }])
const newMessage = ref('')
const chatBody = ref(null)
const isChatOpen = ref(false)

// Send message
const sendMessage = () => {
  if (newMessage.value.trim() === '') return

  messages.value.push({ text: newMessage.value, isUser: true })
  messages.value.push({
    text: 'Mình đang xử lý yêu cầu của bạn...',
    isUser: false
  })

  newMessage.value = ''

  nextTick(() => {
    chatBody.value.scrollTop = chatBody.value.scrollHeight
  })
}
watch(isChatOpen, () => {
  console.log(isChatOpen.value)
})
</script>

<template>
  <div>
    <!-- Icon chatbot -->
    <button
      v-if="!isChatOpen"
      @click.prevent="isChatOpen = !isChatOpen"
      class="fixed bottom-10 right-10 rounded-full bg-[#51A7BF] p-3 text-[#DAF4FF] shadow-lg hover:bg-[#30869e]"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512" class="h-8 w-8">
        <path
          fill="#ffffff"
          d="M88.2 309.1c9.8-18.3 6.8-40.8-7.5-55.8C59.4 230.9 48 204 48 176c0-63.5 63.8-128 160-128s160 64.5 160 128s-63.8 128-160 128c-13.1 0-25.8-1.3-37.8-3.6c-10.4-2-21.2-.6-30.7 4.2c-4.1 2.1-8.3 4.1-12.6 6c-16 7.2-32.9 13.5-49.9 18c2.8-4.6 5.4-9.1 7.9-13.6c1.1-1.9 2.2-3.9 3.2-5.9zM208 352c114.9 0 208-78.8 208-176S322.9 0 208 0S0 78.8 0 176c0 41.8 17.2 80.1 45.9 110.3c-.9 1.7-1.9 3.5-2.8 5.1c-10.3 18.4-22.3 36.5-36.6 52.1c-6.6 7-8.3 17.2-4.6 25.9C5.8 378.3 14.4 384 24 384c43 0 86.5-13.3 122.7-29.7c4.8-2.2 9.6-4.5 14.2-6.8c15.1 3 30.9 4.5 47.1 4.5zM432 480c16.2 0 31.9-1.6 47.1-4.5c4.6 2.3 9.4 4.6 14.2 6.8C529.5 498.7 573 512 616 512c9.6 0 18.2-5.7 22-14.5c3.8-8.8 2-19-4.6-25.9c-14.2-15.6-26.2-33.7-36.6-52.1c-.9-1.7-1.9-3.4-2.8-5.1C622.8 384.1 640 345.8 640 304c0-94.4-87.9-171.5-198.2-175.8c4.1 15.2 6.2 31.2 6.2 47.8l0 .6c87.2 6.7 144 67.5 144 127.4c0 28-11.4 54.9-32.7 77.2c-14.3 15-17.3 37.6-7.5 55.8c1.1 2 2.2 4 3.2 5.9c2.5 4.5 5.2 9 7.9 13.6c-17-4.5-33.9-10.7-49.9-18c-4.3-1.9-8.5-3.9-12.6-6c-9.5-4.8-20.3-6.2-30.7-4.2c-12.1 2.4-24.8 3.6-37.8 3.6c-61.7 0-110-26.5-136.8-62.3c-16 5.4-32.8 9.4-50 11.8C279 439.8 350 480 432 480z"
        />
      </svg>
    </button>

    <!-- Chatbot window -->
    <div
      v-if="isChatOpen"
      class="md:w-96 fixed bottom-10 right-10 z-[99] w-80 overflow-hidden rounded-lg bg-white shadow-2xl"
    >
      <div class="flex justify-between bg-[#51A7BF] p-3">
        <h3 class="text-lg font-semibold text-[#DAF4FF]">Chatbot Hỗ Trợ</h3>
        <button
          @click="isChatOpen = !isChatOpen"
          class="text-[#DAF4FF] hover:scale-125 hover:text-gray-200"
        >
          <svg
            class="h-6 w-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
      <div class="h-[350px] overflow-y-auto p-4" ref="chatBody">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="[
            'my-2 max-w-[80%] rounded-lg p-3',
            message.isUser
              ? 'ml-auto bg-[#51A7BF] text-right text-[#DAF4FF]'
              : 'mr-auto bg-gray-200 text-left text-black'
          ]"
        >
          {{ message.text }}
        </div>
      </div>
      <div class="flex border-t border-gray-300 p-2">
        <input
          v-model="newMessage"
          @keypress.enter="sendMessage"
          type="text"
          placeholder="Nhập tin nhắn..."
          class="flex-1 rounded-l-md border-none bg-gray-100 p-2 outline-none"
        />
        <button
          @click="sendMessage"
          class="rounded-r-md bg-[#51A7BF] px-4 py-2 text-[#DAF4FF] hover:bg-[#30869e] hover:text-white"
        >
          Gửi
        </button>
      </div>
    </div>
  </div>
</template>

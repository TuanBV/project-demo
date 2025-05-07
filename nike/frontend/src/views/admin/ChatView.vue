<script setup>
import { onMounted, reactive, watch } from 'vue'
import { isEqual } from 'lodash'
const listChat = reactive([
  {
    name: 'Person 1',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 2',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 3',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 4',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 5',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 6',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 7',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 8',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 9',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
  {
    name: 'Person 10',
    last_text: 'oke ....',
    image: 'assets/images/air_force_1.png',
  },
])

const currentChat = reactive({
  name: '',
  last_text: '',
  image: '',
})

onMounted(() => {
  Object.assign(currentChat, listChat[0])
})

watch(currentChat, () => {
  console.log(currentChat)
})
</script>
<template>
  <div>
    <h1 class="border-b pb-3 text-2xl font-medium tracking-wider">Chat Management</h1>
    <div class="flex">
      <!-- Sidebar -->
      <aside class="block w-64 overflow-y-auto border-r bg-[#F9FBFF]">
        <div class="p-4 text-xl font-semibold">Đoạn chat</div>
        <div class="p-2 text-sm">
          <input
            type="text"
            placeholder="Tìm kiếm trên Messenger"
            class="w-full rounded border px-3 py-2 placeholder-gray-400 focus:outline-none"
          />
        </div>
        <div class="max-h-[calc(100vh-80px)] overflow-y-auto">
          <div
            class="mx-2 mt-1 flex cursor-pointer items-center rounded p-2"
            v-for="(item, index) in listChat"
            :key="index"
            @click.prevent="Object.assign(currentChat, item)"
            :class="{ 'bg-gray-200': isEqual(item, currentChat) }"
          >
            <img
              src="assets/images/air_force_1.png"
              class="mr-2 h-8 w-8 rounded-full border border-red-500"
              alt="Avatar"
              width="auto"
              height="auto"
            />
            <div>
              <div class="text-sm font-medium">{{ item.name }}</div>
              <div class="text-xs text-gray-400">{{ item.last_text }}</div>
            </div>
          </div>
          <!-- More contacts -->
        </div>
      </aside>

      <!-- Chat area -->
      <main class="flex flex-1 flex-col">
        <!-- Header -->
        <div class="flex items-center justify-between border-b p-4">
          <div class="text-lg font-semibold">Bùi Hoàng</div>
          <div class="flex space-x-2 text-purple-400">
            <!-- Information of user -->
            <button>ℹ️</button>
          </div>
        </div>

        <!-- Messages -->
        <div class="flex-1 space-y-2 overflow-y-auto p-4">
          <!-- Message from friend -->
          <div class="flex items-start space-x-2">
            <img
              src="assets/images/air_force_1.png"
              class="h-7 w-7 rounded-full border border-red-500"
            />
            <div class="space-y-1">
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">Uhm</div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">Dẹt</div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">Vào chỗ khác</div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">
                Làm chính thức thì tầm 9tr
              </div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">Văn phòng</div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">Nhưng đi đi lại lại suốt</div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">
                Chứ không phải kiểu ngồi 1 chỗ
              </div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">
                Đi ca thì lương mới được vậy
              </div>
              <div class="max-w-sm rounded-xl bg-gray-700 px-3 py-2">
                Chứ đi hành chính thì 7tr thôi 😆
              </div>
            </div>
          </div>

          <!-- Message from user -->
          <div class="mt-4 flex flex-col items-end space-y-1 text-white">
            <div class="max-w-sm rounded-xl bg-blue-600 px-3 py-2">Mà làm ở đâu</div>
            <div class="max-w-sm rounded-xl bg-blue-600 px-3 py-2">Lại về đấy à</div>
            <div class="max-w-sm rounded-xl bg-blue-600 px-3 py-2">Văn phòng k</div>
            <div class="max-w-sm rounded-xl bg-blue-600 px-3 py-2">Hay dưới nhà máy</div>
            <div class="max-w-sm rounded-xl bg-blue-600 px-3 py-2">Vp mà phải cày đêm à</div>
            <div class="max-w-sm rounded-xl bg-blue-600 px-3 py-2">Chán vc</div>
          </div>
        </div>

        <!-- Input -->
        <div class="flex items-center p-4">
          <input
            type="text"
            placeholder="Aa"
            class="flex-1 rounded border bg-gray-800 px-3 py-2 text-white placeholder-gray-400 focus:outline-none"
          />
          <button class="ml-2 text-lg text-blue-500">👍</button>
        </div>
      </main>
    </div>
  </div>
</template>

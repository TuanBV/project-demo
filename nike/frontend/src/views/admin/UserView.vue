<script setup>
import { onMounted, ref, watch } from 'vue'
import userService from 'service/user.service'
import ToastUtil from 'utility/toast'
import AddUserView from 'components/admin/modal/AddUserView.vue'

// 1) ======= INITIALIZATION ========

// 2) ======= VARIABLE REF ========
const users = ref([])
const isAddUser = ref(false)
// 3) ======= METHOD/FUNCTION ========
const getList = async () => {
  const res = await userService.getList()
  if (res) {
    users.value = res.item
  }
}
const edit = async (userId) => {
  console.log(userId)
}
const statusUser = async (userId, nameUser, status) => {
  const res = await userService.statusUser(userId, status ? 1 : 0)
  if (res) {
    await getList()
    ToastUtil.success((status ? 'Inactive' : 'Active') + ' user successfully : ' + nameUser)
    return
  }
  ToastUtil.error('Change status error : ' + nameUser)
}
// 4) ======= VUE JS LIFECYCLE ========
watch(isAddUser, async () => {
  await getList()
})
onMounted(async () => {
  await getList()
})
</script>

<template>
  <div>
    <div class="flex justify-between">
      <h1 class="text-2xl font-medium tracking-wider">List account</h1>
      <button
        @click.prevent="isAddUser = true"
        class="flex cursor-pointer items-center justify-center gap-2 rounded-md bg-green-500 px-3 py-2 font-medium text-white duration-300 hover:scale-105"
      >
        <font-awesome-icon :icon="['fas', 'add']" class="group h-4 w-4" />
        <span>Add User</span>
      </button>
    </div>

    <div class="overflow-hidden rounded-xl shadow-xl">
      <table class="mt-5 w-full table-fixed">
        <thead>
          <tr class="bg-gray-100">
            <th class="w-1/6 px-6 py-4 text-left font-bold uppercase text-gray-600">Name</th>
            <th class="w-1/6 px-6 py-4 text-left font-bold uppercase text-gray-600">Email</th>
            <th class="w-1/6 px-6 py-4 text-left font-bold uppercase text-gray-600">Phone</th>
            <th class="w-1/6 px-6 py-4 text-left font-bold uppercase text-gray-600">Status</th>
            <th class="w-1/6 px-6 py-4 text-left font-bold uppercase text-gray-600">Action</th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr class="border-b border-gray-300" v-for="(item, index) in users" :key="index">
            <td class="border-b border-gray-200 px-6 py-4">{{ item.username }}</td>
            <td class="truncate border-b border-gray-200 px-6 py-4">{{ item.email }}</td>
            <td class="border-b border-gray-200 px-6 py-4">555-555-5555</td>
            <td class="border-b border-gray-200 px-6 py-4">
              <span
                class="rounded-full px-2 py-1 text-xs text-white"
                :class="item.flg_del ? 'bg-red-500' : 'bg-green-500'"
                >{{ item.flg_del ? 'Inactive' : 'Active' }}</span
              >
            </td>
            <td class="flex items-center gap-4 border-gray-200 px-6 py-4">
              <button
                @click.prevent="edit(item.user_id)"
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon :icon="['fas', 'edit']" class="group h-4 w-4 text-green-500" />
                <span class="text-sm font-semibold text-green-500">Edit</span>
              </button>
              <button
                @click.prevent="statusUser(item.user_id, item.username, !item.flg_del)"
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon
                  :icon="['fas', 'power-off']"
                  class="group h-4 w-4"
                  :class="item.flg_del ? 'text-green-500' : 'text-red-500'"
                />
                <span
                  class="text-sm font-semibold"
                  :class="item.flg_del ? 'text-green-500' : 'text-red-500'"
                  >{{ item.flg_del ? 'On' : 'Off' }}</span
                >
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AddUserView v-model="isAddUser" />
  </div>
</template>

<script setup>
// import { defineAsyncComponent, onMounted, ref, watch } from 'vue'
import { ref } from 'vue'
import ConfirmPopup from 'components/ConfirmPopup.vue'
// import saleService from 'service/sale.service'
// import ToastUtil from 'utility/toast'

const categories = ref([])
const refConfirmPopup = ref({
  isVisible: false,
  message: '',
  confirmAction: null
})
const childSale = ref({
  isModalSale: false,
  saleId: ''
})
// const getList = async () => {
//   const res = await saleService.getList()
//   if (res) {
//     categories.value = res.item
//   }
// }

// const ModalSale = defineAsyncComponent(() => {
//   return import('components/admin/modal/ModalSale.vue')
// })

// const deleteSale = async (saleId) => {
//   const res = await saleService.delete(saleId)
//   if (res) {
//     await getList()
//     ToastUtil.success('Delete sale successfully')
//   }
// }

// const activeSale = async (saleId) => {
//   const res = await saleService.active(saleId)
//   if (res) {
//     await getList()
//     ToastUtil.success('Active sale successfully')
//   }
// }

// const confirmPopup = (title, methodAction) => {
//   refConfirmPopup.value.isVisible = true
//   refConfirmPopup.value.message = title
//   refConfirmPopup.value.confirmAction = methodAction
// }

// watch(childSale.value, async () => {
//   if (!childSale.value.isModalSale) await getList()
// })

// onMounted(async () => {
//   await getList()
// })
</script>
<template>
  <div>
    <h1 class="mb-5 flex items-center gap-2 border-b pb-3 text-2xl font-medium tracking-wider">
      <img loading="lazy" src="../../assets/sale.svg" alt="" height="20px" width="20px" srcset="" />
      Sale Management
      <img loading="lazy" src="../../assets/sale.svg" alt="" height="20px" width="20px" srcset="" />
    </h1>

    <div class="mb-3 flex items-center justify-between">
      <div class="text-base font-medium">Sale List</div>
      <button
        @click.prevent="childSale.isModalSale = true"
        class="flex cursor-pointer items-center justify-center rounded-md bg-green-500 px-3 py-2 font-medium text-white duration-300 hover:scale-105"
      >
        <font-awesome-icon :icon="['fas', 'add']" class="group h-4 w-4" />
        <span>Add Sale Program</span>
      </button>
    </div>
    <div class="overflow-hidden rounded-xl shadow-xl">
      <table class="w-full table-fixed">
        <thead>
          <tr class="bg-gray-100">
            <th class="w-1/12 px-6 py-4 text-left font-bold uppercase text-gray-600">STT</th>
            <th class="w-3/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Name</th>
            <th class="w-2/12 px-6 py-4 text-left font-bold uppercase text-gray-600">Image</th>
            <th class="w-2/12 px-6 py-4 text-center font-bold uppercase text-gray-600">
              Start Date
            </th>
            <th class="w-2/12 px-6 py-4 text-center font-bold uppercase text-gray-600">End Date</th>
            <th class="w-2/12 px-6 py-4 text-center font-bold uppercase text-gray-600"></th>
          </tr>
        </thead>
        <tbody class="bg-white">
          <tr
            v-for="(item, index) in categories"
            :key="index"
            class="border-b border-gray-300"
            :class="item.flg_del ? 'bg-gray-200' : ''"
          >
            <td class="truncate px-6 py-4">{{ index + 1 }}</td>
            <td class="px-6 py-4">{{ item.name }}</td>
            <td class="flex items-center justify-center gap-4 border-gray-200 px-6 py-4">
              <button
                v-if="!item.flg_del"
                @click.prevent="(childSale.saleId = item.id), (childSale.isModalSale = true)"
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon :icon="['fas', 'edit']" class="group h-4 w-4 text-green-500" />
                <span class="text-sm font-semibold text-green-500">Edit</span>
              </button>
              <button
                v-if="!item.flg_del"
                @click.prevent="
                  confirmPopup('Bạn muốn xóa danh mục ' + item.name + ' ?', () => {
                    deleteSale(item.id), (refConfirmPopup.isVisible = false)
                  })
                "
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon
                  :icon="['fas', 'power-off']"
                  class="group h-4 w-4 text-red-500"
                />
                <span class="text-sm font-semibold text-red-500">Delete</span>
              </button>
              <button
                v-else
                @click.prevent="
                  confirmPopup('Bạn muốn thêm lại danh mục ' + item.name + ' ?', () => {
                    activeSale(item.id), (refConfirmPopup.isVisible = false)
                  })
                "
                class="flex gap-2 text-gray-600 duration-200 hover:scale-110 hover:cursor-pointer"
              >
                <font-awesome-icon
                  :icon="['fas', 'power-off']"
                  class="group h-4 w-4 text-yellow-600"
                />
                <span class="text-sm font-semibold text-yellow-600">Active</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Modal sale -->
    <ModalSale v-model="childSale" />
    <!-- Confirm popup -->
    <ConfirmPopup
      :isVisible="refConfirmPopup.isVisible"
      :message="refConfirmPopup.message"
      :accept="refConfirmPopup.confirmAction"
      @cancel="() => (refConfirmPopup.isVisible = false)"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
// import ConfirmPopup from 'components/ConfirmPopup.vue'
import settingService from 'service/setting.service'
import ToastUtil from 'utility/toast'
// 1) ======= INITIALIZATION ========
// 2) ======= VARIABLE REF ========
const setting = ref({
  email: '',
  number_phone: '',
  address: '',
  info: '',
  fb_link: '',
  ig_link: '',
  tt_link: '',
  tw_link: ''
})
// 3) ======= METHOD/FUNCTION ========
const getNewSetting = async () => {
  const res = await settingService.getNewSetting()
  if (res) {
    setting.value = res
  }
}
const saveSetting = async () => {
  const res = await settingService.save(setting.value)
  if (res) {
    ToastUtil.success('Save setting successfully!')
    return
  }
  ToastUtil.error('Save setting failed!')
}
// 4) ======= VUE JS LIFECYCLE ========
onMounted(async () => {
  await getNewSetting()
})
</script>

<template>
  <div>
    <h1 class="mb-5 flex items-center gap-2 border-b pb-3 text-2xl font-medium tracking-wider">
      <font-awesome-icon :icon="['fas', 'gear']" class="h-5 w-5" />
      Setting Management
    </h1>
    <!-- About company -->
    <div class="mx-auto w-full py-2">
      <div class="mb-3 text-xl">About Company</div>
      <div class="flex items-center justify-center">
        <div class="mx-auto w-full bg-white">
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="email" class="col-span-1 text-base">
              Email contact <span class="text-red-500"></span
            ></label>
            <input
              type="text"
              name="email"
              v-model="setting.email"
              placeholder="Type email contact ..."
              class="col-span-3 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="number-phone" class="col-span-1 text-base">
              Number phone <span class="text-red-500"></span
            ></label>
            <input
              type="text"
              name="number-phone"
              v-model="setting.number_phone"
              placeholder="Type number phone ..."
              class="col-span-3 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="address" class="col-span-1 text-base">
              Address <span class="text-red-500"></span
            ></label>
            <input
              type="text"
              name="address"
              v-model="setting.address"
              placeholder="Type address ..."
              class="col-span-3 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="info" class="col-span-1 text-base">
              Info <span class="text-red-500"></span
            ></label>
            <textarea
              type="text"
              name="info"
              v-model="setting.info"
              placeholder="Type about company ..."
              class="col-span-5 max-h-60 min-h-60 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            ></textarea>
          </div>
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="fb-link" class="col-span-1 text-base">
              Facebook <span class="text-red-500"></span
            ></label>
            <input
              type="text"
              name="fb-link"
              v-model="setting.fb_link"
              placeholder="Type facebook link ..."
              class="col-span-3 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="ig-link" class="col-span-1 text-base">
              Instagram <span class="text-red-500"></span
            ></label>
            <input
              type="text"
              name="ig-link"
              v-model="setting.ig_link"
              placeholder="Type instagram link ..."
              class="col-span-3 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="tt-link" class="col-span-1 text-base">
              Tik tok <span class="text-red-500"></span
            ></label>
            <input
              type="text"
              name="tt-link"
              v-model="setting.tt_link"
              placeholder="Type tiktok link ..."
              class="col-span-3 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-4 grid grid-cols-9 items-center">
            <label for="tw-link" class="col-span-1 text-base">
              Twitter <span class="text-red-500"></span
            ></label>
            <input
              type="text"
              name="tw-link"
              v-model="setting.tw_link"
              placeholder="Type twitter link ..."
              class="col-span-3 rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div>
            <button
              @click.prevent="saveSetting"
              class="hover:shadow-form rounded-md bg-green-500 px-8 py-2 text-center text-base font-semibold text-white outline-none hover:bg-green-600"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Modal setting -->
    <!-- <ModalSetting v-model="childSetting" /> -->
    <!-- Confirm popup -->
    <!-- <ConfirmPopup
      :isVisible="refConfirmPopup.isVisible"
      :message="refConfirmPopup.message"
      :accept="refConfirmPopup.confirmAction"
      @cancel="() => (refConfirmPopup.isVisible = false)"
    /> -->
  </div>
</template>

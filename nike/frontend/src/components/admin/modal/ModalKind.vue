<script setup>
import { ref, watch } from 'vue'
import kindService from 'service/kind.service'
import useValidate from 'composables/validate'
import KindSchema from 'schemas/admin/kind'
import ToastUtil from 'utility/toast'

const { validate, errors } = useValidate()
const childKind = defineModel()
const kind = ref({
  name: ''
})

const addKind = async () => {
  const isValid = validate(KindSchema, kind.value)
  if (!isValid) return
  const res = await kindService.add(kind.value)
  if (res) {
    ToastUtil.success('Added kind successfully !!!')
    childKind.value.isModalKind = false
    childKind.value.kindId = ''
  }
}
const updateKind = async () => {
  const isValid = validate(KindSchema, kind.value)
  if (!isValid) return
  const res = await kindService.update(childKind.value.kindId, kind.value)
  if (res) {
    ToastUtil.success('Update kind successfully !!!')
    childKind.value.isModalKind = false
    childKind.value.kindId = ''
  }
}

watch(childKind.value, async () => {
  kind.value.name = ''
  if (childKind.value.kindId) {
    const res = await kindService.getByKindId(childKind.value.kindId)
    if (res) {
      kind.value.name = res.name
      // Populate form data with fetched data
    }
  }
  if (!childKind.value.isModalKind) childKind.value.kindId = ''
  errors.value = []
})
</script>

<template>
  <div
    v-if="childKind.isModalKind"
    class="fixed left-0 top-0 z-[999] flex h-full w-[100vw] items-center justify-center bg-black bg-opacity-35"
    @click.self="childKind.isModalKind = !childKind.isModalKind"
  >
    <div
      class="h-[80%] w-[80%] overflow-y-auto overflow-x-hidden rounded-lg bg-white p-5 shadow-2xl pc:h-auto pc:w-[45%]"
    >
      <div class="mb-5 flex items-start justify-between border-b pb-2">
        <h1 class="text-3xl font-medium">Add Kind</h1>
        <button class="float-end" @click="childKind.isModalKind = false">
          <font-awesome-icon :icon="['fas', 'close']" />
        </button>
      </div>
      <div class="mx-auto h-full w-full py-2">
        <div class="flex items-center justify-center">
          <div class="mx-auto w-full bg-white">
            <div class="mb-4">
              <label for="phone" class="mb-2 block text-base font-medium">
                Kind name <span class="text-red-500">(*)</span></label
              >
              <input
                type="text"
                name="Name"
                v-model="kind.name"
                placeholder="Type kind name"
                class="w-full rounded-md border border-[#e0e0e0] bg-white px-3 py-2 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
              <p v-if="errors.name" class="mt-2 text-sm italic text-red-500">
                {{ errors.name }}
              </p>
            </div>
            <div>
              <button
                v-if="childKind.kindId"
                @click.prevent="updateKind"
                class="hover:shadow-form w-full rounded-md bg-green-500 px-8 py-2 text-center text-base font-semibold text-white outline-none hover:bg-green-600"
              >
                Update
              </button>
              <button
                v-else
                @click.prevent="addKind"
                class="hover:shadow-form w-full rounded-md bg-green-500 px-8 py-2 text-center text-base font-semibold text-white outline-none hover:bg-green-600"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

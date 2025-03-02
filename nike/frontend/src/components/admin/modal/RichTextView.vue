<script setup>
import { onMounted, ref, defineModel, defineAsyncComponent, watch, nextTick, markRaw } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'

const quill = ref(null)
const editor = ref(null)
const content = defineModel()
const imageList = ref({
  flag: false,
  images: []
})

const ImageList = defineAsyncComponent(() => {
  return import('components/admin/modal/ImageList.vue')
})

// Insert element at cursor position
const insertElementAtCursor = (text) => {
  if (!quill.value) return
  quill.value.insertEmbed(quill.value.getLength(), 'image', text)
}

onMounted(() => {
  quill.value = markRaw(
    new Quill(editor.value, {
      theme: 'snow',
      modules: {
        toolbar: [
          [{ header: '1' }, { header: '2' }, { font: [] }],
          [{ list: 'ordered' }, { list: 'bullet' }],
          ['bold', 'italic', 'underline'],
          ['link'],
          [{ align: [] }],
          ['image']
        ]
      },
      debug: false,
      passive: true
    })
  )
  nextTick(() => {
    const toolbar = quill.value.getModule('toolbar')
    const imageButton = toolbar.container.querySelector('.ql-image')

    // Delete button upload image default
    imageButton.remove()

    // Create button upload image
    const customImageButton = document.createElement('button')
    customImageButton.innerHTML = '<i class="fa-solid fa-image"></i>'
    customImageButton.classList.add('ql-image')

    toolbar.container.appendChild(customImageButton)

    // Add event listeners
    customImageButton.addEventListener('click', () => (imageList.value.flag = true))

    quill.value.on('text-change', (delta, oldDelta, source) => {
      content.value = quill.value.root.innerHTML
    })
  })
})

watch(imageList.value.flag, () => {
  if (!imageList.value.flag) {
    insertElementAtCursor('https://img.icons8.com/?size=256&id=wNxEqErpHetl&format=png')
  }
})
</script>

<template>
  <div>
    <div ref="editor" class="rich-text"></div>
    <ImageList v-model="imageList" />
  </div>
</template>

<style scoped>
.ql-container.ql-snow {
  border: 1px solid #e5e7eb !important;
  border-bottom-right-radius: 6px !important;
  border-bottom-left-radius: 6px !important;
}
</style>

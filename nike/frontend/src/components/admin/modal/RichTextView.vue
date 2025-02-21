<script setup>
import { onMounted, ref, defineModel, watch, nextTick } from 'vue'
import ImageList from 'components/admin/modal/ImageList.vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'

const quill = ref(null)
const editor = ref(null)
const content = defineModel()
const isImageList = ref(false)

// Insert element at cursor position
const insertElementAtCursor = (text) => {
  if (!quill.value) return
  // Get cursor position
  // const range = quill.value.getSelection()
  // const index = range ? range.index : 0
  // // Insert element at cursor position
  quill.value.insertEmbed(quill.value.getLength(), 'image', text)
  // quill.value.setSelection(1)

  // setTimeout(() => {
  //   const imgs = document.querySelectorAll('.ql-editor img')
  //   imgs.forEach((img) => img.classList.add('img-add'))
  // }, 50)
}
watch(content, () => {
  console.log(quill.value)
})

onMounted(() => {
  quill.value = new Quill(editor.value, {
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
    passive: true
  })
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
    customImageButton.addEventListener('click', () => (isImageList.value = true))

    quill.value.on('text-change', (delta, oldDelta, source) => {
      content.value = quill.value.root.innerHTML
    })
  })
})

watch(isImageList, () => {
  if (!isImageList.value) {
    insertElementAtCursor('https://img.icons8.com/?size=256&id=wNxEqErpHetl&format=png')
  }
})
</script>

<template>
  <div>
    <div ref="editor"></div>
    <ImageList v-model="isImageList" />
  </div>
</template>

<style scoped>
div[ref='editor'] {
  min-height: 200px;
  max-height: 400px;
}
button.ql-image {
  background-color: #4caf50;
  color: white;
  padding: 5px 10px;
  border: none;
  cursor: pointer;
  margin-right: 10px;
}
</style>

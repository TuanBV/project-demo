<script setup>
import { onMounted, ref, defineModel, defineAsyncComponent, watch, nextTick, markRaw } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'
// 1) ======= INITIALIZATION ========
// 2) ======= VARIABLE REF ========
const quill = ref(null)
const editor = ref(null)
const content = defineModel()
const lengthContent = ref(0)
const imageList = ref({
  flag: false,
  images: []
})
const imgListOld = ref([])

// 3) ======= METHOD/FUNCTION ========
// Lazy loading
const ImageList = defineAsyncComponent(() => {
  return import('components/admin/modal/ImageList.vue')
})

function arrayDifferenceWithCount(arr1, arr2) {
  const freqMap = arr2.reduce((acc, num) => {
    acc[num] = (acc[num] || 0) + 1
    return acc
  }, {})

  return arr1.filter((num) => {
    if (freqMap[num]) {
      freqMap[num]--
      return false
    }
    return true
  })
}

// Insert element at cursor position
const insertElementAtCursor = (text) => {
  if (!quill.value) return
  quill.value.insertEmbed(quill.value.getLength(), 'image', text)
}
// 4) ======= VUE JS LIFECYCLE ========
onMounted(() => {
  // Init quill
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
  // Actions that occur after Vue re-renders the interface
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
      lengthContent.value = quill.value.getText().trim().split(/\s+/).length
      if (lengthContent.value <= 1000) {
        // Event when change text then get new content
        content.value = quill.value.root.innerHTML
      }
    })
  })
})

watch(imageList.value, () => {
  if (
    !imageList.value.flag &&
    arrayDifferenceWithCount(imageList.value.images, imgListOld.value).length
  ) {
    arrayDifferenceWithCount(imageList.value.images, imgListOld.value).forEach((item) => {
      insertElementAtCursor('http://localhost:8000/' + item.path)
    })
  }
  if (imgListOld.value != imageList.value.images) {
    imgListOld.value = [...imageList.value.images]
  }
})
</script>

<template>
  <div>
    <div>
      <div ref="editor" class="rich-text"></div>
      <ImageList v-model="imageList" />
    </div>
    <p v-if="lengthContent > 1000" class="mt-1 text-xs leading-4 text-red-500">
      Max length of content is 1000 wordsf.
    </p>
  </div>
</template>

<style scoped>
.ql-container.ql-snow {
  border: 1px solid #e5e7eb !important;
  border-bottom-right-radius: 6px !important;
  border-bottom-left-radius: 6px !important;
}
</style>

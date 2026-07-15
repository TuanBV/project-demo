<script setup>
import { onMounted, ref, defineAsyncComponent, watch, nextTick, markRaw } from 'vue'
import { MAX_POST } from 'utility/const'
import { API_BASE_URL } from 'utility/env'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'
// 1) ======= INITIALIZATION ========
// ==> 1.1) state and getters
const Image = Quill.import('formats/image')
// ==> 1.2) actions
// Custom method insertEmbed image and style align center
class CenteredImage extends Image {
  static create(value) {
    const node = super.create(value)
    node.setAttribute('src', value)
    node.classList.add('m-auto')
    return node
  }
}
// ==> 1.3) Others
// Register class
CenteredImage.blotName = 'image'
CenteredImage.tagName = 'IMG'
Quill.register(CenteredImage, true)

// 2) ======= VARIABLE REF ========
const content = defineModel()
const props = defineProps(['errorContent'])
const emit = defineEmits(['update'])
const quill = ref(null)
const editor = ref(null)
const imgListOld = ref([])
const lengthContent = ref(0)
const imageList = ref({
  flag: false,
  images: [],
})

// 3) ======= METHOD/FUNCTION ========
// Lazy loading
const ImageList = defineAsyncComponent(() => {
  return import('components/admin/modal/ImageList.vue')
})

// Check difference between 2 array
function arrayDifferenceWithCount(arr1, arr2) {
  const freqMap = arr2.reduce((acc, num) => {
    acc[num] = (acc[num] || 0) + 1
    return acc
  }, {})

  return arr1.filter(num => {
    if (freqMap[num]) {
      freqMap[num]--
      return false
    }
    return true
  })
}

// Insert element at cursor position
const insertElementAtCursor = text => {
  if (!quill.value) return
  const index = quill.value.getLength()
  // Insert image
  quill.value.insertEmbed(index, 'image', text)
  quill.value.insertText(index + 1, '\n')
  // Add style for element
  quill.value.formatLine(index + 1, 1, { align: 'center' })
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
          ['image'],
        ],
      },
      debug: false,
      passive: true,
    })
  )
  // Set value for quill
  quill.value.root.innerHTML = content.value

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
      if (lengthContent.value <= MAX_POST) {
        // Event when change text then get new content
        content.value = quill.value.root.innerHTML
      }
    })
  })
})

// Check change image
watch(imageList.value, () => {
  if (
    !imageList.value.flag &&
    arrayDifferenceWithCount(imageList.value.images, imgListOld.value).length
  ) {
    arrayDifferenceWithCount(imageList.value.images, imgListOld.value).forEach(item => {
      insertElementAtCursor(API_BASE_URL + '/' + item.path)
    })
  }
  if (imgListOld.value != imageList.value.images) {
    imgListOld.value = [...imageList.value.images]
  }
})

// Watch lengthContent
watch(lengthContent, () => {
  if (lengthContent.value > MAX_POST) {
    emit('update', true)
  }
})
</script>

<template>
  <div>
    <div>
      <div ref="editor" class="rich-text"></div>
      <ImageList v-model="imageList" />
    </div>
    <p v-if="lengthContent > MAX_POST" class="mt-1 text-xs leading-4 text-red-500">
      Max length of content is {{ MAX_POST }} word.
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

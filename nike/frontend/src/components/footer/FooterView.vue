<script setup>
import AuthorView from 'components/footer/AuthorView.vue'
import IconSocialMedia from 'components/footer/IconSocialMedia.vue'
</script>
<template>
  <footer class="bg-white text-base">
    <div class="mx-auto max-w-full overflow-hidden border-t-[1px] p-10">
      <div class="mx-auto grid max-w-[1300px] grid-cols-1 gap-8 pb-10 pc:grid-cols-3">
        <div class="grid grid-cols-1">
          <div class="text-teal-600">
            <img src="assets/logo.svg" alt="" srcset="" width="70px" height="70px" />
          </div>

          <p class="mt-4 text-gray-500">
            Lorem ipsum dolor, sit amet consectetur adipisicing elit. Esse non cupiditate quae nam
            molestias.
          </p>
          <!-- Social media -->
          <ul class="mt-8 flex items-center gap-6">
            <IconSocialMedia>
              <template #default="{ item }">
                <a
                  :href="item.link"
                  rel="noreferrer"
                  target="_blank"
                  class="text-gray-700 transition hover:opacity-75"
                >
                  <span class="sr-only">{{ item.name }}</span>
                  <img :src="item.icon" alt="" height="20px" width="20px" srcset="" />
                </a>
              </template>
            </IconSocialMedia>
          </ul>
        </div>

        <div class="grid grid-cols-1 gap-8 tablet:grid-cols-2 pc:col-span-2 pc:grid-cols-4">
          <div>
            <p class="font-medium text-gray-900">Services</p>

            <ul class="mt-6 space-y-4">
              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> 1on1 Coaching </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Company Review </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Accounts Review </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> HR Consulting </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> SEO Optimisation </a>
              </li>
            </ul>
          </div>

          <div>
            <p class="font-medium text-gray-900">Company</p>

            <ul class="mt-6 space-y-4">
              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> About </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Meet the Team </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Accounts Review </a>
              </li>
            </ul>
          </div>

          <div>
            <p class="font-medium text-gray-900">Helpful Links</p>

            <ul class="mt-6 space-y-4">
              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Contact </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> FAQs </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Live Chat </a>
              </li>
            </ul>
          </div>

          <div>
            <p class="font-medium text-gray-900">Legal</p>

            <ul class="mt-6 space-y-4">
              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Accessibility </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Returns Policy </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75"> Refund Policy </a>
              </li>

              <li>
                <a href="#" class="text-gray-700 transition hover:opacity-75">
                  Hiring Statistics
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <AuthorView />
    </div>
  </footer>
</template>

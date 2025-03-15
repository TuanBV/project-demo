<script setup>
import AuthorView from 'components/user/footer/AuthorView.vue'
import IconSocialMedia from 'components/user/footer/IconSocialMedia.vue'
</script>
<template>
  <footer class="bg-white text-base">
    <div class="mx-auto max-w-full overflow-hidden border-t-[1px] p-10">
      <div class="mx-auto grid max-w-[1300px] grid-cols-1 gap-8 pb-10 pc:grid-cols-3">
        <div class="grid grid-cols-1">
          <div class="text-teal-600">
            <img loading="lazy" src="assets/logo.svg" alt="" srcset="" width="70px" height="70px" />
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
                  :href="item"
                  rel="noreferrer"
                  target="_blank"
                  class="text-gray-700 transition hover:opacity-75"
                >
                  <span class="sr-only">{{ item.name }}</span>
                  <img
                    v-if="item.includes('fb')"
                    loading="lazy"
                    src="../../../assets/facebook.svg"
                    alt=""
                    height="20px"
                    width="20px"
                    srcset=""
                  />
                  <img
                    v-if="item.includes('tt')"
                    loading="lazy"
                    src="../../../assets/tiktok.svg"
                    alt=""
                    height="20px"
                    width="20px"
                    srcset=""
                  />
                  <img
                    v-if="item.includes('ig')"
                    loading="lazy"
                    src="../../../assets/instagram.svg"
                    alt=""
                    height="20px"
                    width="20px"
                    srcset=""
                  />
                  <img
                    v-if="item.includes('tw')"
                    loading="lazy"
                    src="../../../assets/twitter.svg"
                    alt=""
                    height="20px"
                    width="20px"
                    srcset=""
                  />
                </a>
              </template>
            </IconSocialMedia>
          </ul>
        </div>

        <div class="grid grid-cols-1 gap-8 tablet:grid-cols-2 pc:col-span-2 pc:grid-cols-4">
          <div>
            <p class="font-medium text-gray-900">Services</p>

            <div class="mt-6 space-y-4">
              <div>
                <router-link to="coaching" class="text-gray-700 transition hover:opacity-75">
                  1on1 Coaching
                </router-link>
              </div>
              <div>
                <router-link to="company-review" class="text-gray-700 transition hover:opacity-75">
                  Company Review
                </router-link>
              </div>
              <div>
                <router-link to="account-review" class="text-gray-700 transition hover:opacity-75">
                  Accounts Review
                </router-link>
              </div>
              <div>
                <router-link to="hr" class="text-gray-700 transition hover:opacity-75">
                  HR Consulting
                </router-link>
              </div>
            </div>
          </div>

          <div>
            <p class="font-medium text-gray-900">Company</p>
            <div class="mt-6 space-y-4">
              <div>
                <router-link class="text-gray-700 transition hover:opacity-75" to="about"
                  >About us</router-link
                >
              </div>
              <div>
                <router-link class="text-gray-700 transition hover:opacity-75" to="meet-team"
                  >Meet the Team</router-link
                >
              </div>
              <div>
                <router-link class="text-gray-700 transition hover:opacity-75" to="account-review"
                  >Accounts Review</router-link
                >
              </div>
            </div>
          </div>

          <div>
            <p class="font-medium text-gray-900">Helpful Links</p>

            <div class="mt-6 space-y-4">
              <div>
                <router-link to="contact-us" class="text-gray-700 transition hover:opacity-75">
                  Contact
                </router-link>
              </div>

              <div>
                <router-link to="faqs" class="text-gray-700 transition hover:opacity-75">
                  FAQs
                </router-link>
              </div>

              <div>
                <router-link to="live-chat" class="text-gray-700 transition hover:opacity-75">
                  Live Chat
                </router-link>
              </div>
            </div>
          </div>
          <div>
            <p class="font-medium text-gray-900">Legal</p>
            <div class="mt-6 space-y-4">
              <div>
                <router-link to=" accessibility" class="text-gray-700 transition hover:opacity-75">
                  Accessibility
                </router-link>
              </div>
              <div>
                <router-link to="return-policy" class="text-gray-700 transition hover:opacity-75">
                  Returns Policy
                </router-link>
              </div>
              <div>
                <router-link to="refund-policy" class="text-gray-700 transition hover:opacity-75">
                  Refund Policy
                </router-link>
              </div>
              <div>
                <router-link
                  to="hiring-statistics"
                  class="text-gray-700 transition hover:opacity-75"
                >
                  Hiring Statistics
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
      <AuthorView />
    </div>
  </footer>
</template>

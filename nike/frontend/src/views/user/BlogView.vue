<template>
  <!-- component -->
  <div class="max-w-screen-xl mx-auto">
    <main class="mt-10">
      <div class="md:flex md:space-x-2 lg:p-0 block px-2">
        <a class="md:mb-0 relative mb-4 inline-block w-full rounded" style="height: 24em" href="#">
          <div
            class="absolute bottom-0 left-0 z-10 h-full w-full"
            style="background-image: linear-gradient(180deg, transparent, rgba(0, 0, 0, 0.7))"
          ></div>
          <img
            loading="lazy"
            src="https://images.unsplash.com/photo-1493770348161-369560ae357d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2100&q=80"
            class="absolute left-0 top-0 z-0 h-full w-full rounded object-cover"
          />
          <div class="absolute bottom-0 left-0 z-20 p-4">
            <span
              class="mb-2 inline-flex items-center justify-center bg-red-500 px-4 py-1 text-gray-200"
              >Nutrition</span
            >
            <h2 class="text-4xl font-semibold leading-tight text-gray-100">
              Pellentesque a consectetur velit, ac molestie ipsum. Donec sodales, massa et auctor.
            </h2>
            <div class="mt-3 flex">
              <img
                loading="lazy"
                src="https://randomuser.me/api/portraits/men/97.jpg"
                class="mr-2 h-10 w-10 rounded-full object-cover"
              />
              <div>
                <p class="text-sm font-semibold text-gray-200">Mike Sullivan</p>
                <p class="text-xs font-semibold text-gray-400">14 Aug</p>
              </div>
            </div>
          </div>
        </a>
      </div>

      <div class="lg:flex lg:space-x-2 lg:p-0 mb-10 mt-10 block px-2">
        <!-- post cards -->
        <div class="lg:w-2/3 w-full">
          <div class="lg:flex mb-10 w-full rounded">
            <div
              class="lg:w-48 h-48 flex-none overflow-hidden bg-cover text-center opacity-75"
              style="
                background-image: url('https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2100&q=80');
              "
              title="deit is very important"
            ></div>
            <div class="flex flex-col justify-between rounded bg-white px-4 leading-normal">
              <div>
                <div class="md:mt-0 mb-2 mt-3 text-2xl font-medium text-gray-700">
                  Suspendisse varius justo eu risus laoreet fermentum non aliquam dolor
                </div>
                <p class="text-base text-gray-700">
                  Mauris porttitor, velit at tempus vulputate, odio turpis facilisis dui, vitae
                  eleifend odio ipsum at odio. Phasellus luctus scelerisque felis eget suscipit.
                </p>
              </div>
              <div class="mt-3 flex">
                <img
                  loading="lazy"
                  src="https://randomuser.me/api/portraits/men/86.jpg"
                  class="mr-2 h-10 w-10 rounded-full object-cover"
                />
                <div>
                  <p class="text-sm font-semibold capitalize text-gray-700">eduard franz</p>
                  <p class="text-xs text-gray-600">14 Aug</p>
                </div>
              </div>
            </div>
          </div>

          <div class="lg:flex mb-10 w-full rounded">
            <div
              class="lg:w-48 h-48 flex-none overflow-hidden bg-cover text-center opacity-75"
              style="
                background-image: url('https://images.unsplash.com/photo-1515003197210-e0cd71810b5f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2100&q=80');
              "
              title="deit is very important"
            ></div>
            <div class="flex flex-col justify-between rounded bg-white px-4 leading-normal">
              <div>
                <div class="md:mt-0 mb-2 mt-3 text-2xl font-medium text-gray-700">
                  Integer commodo, sapien ut vulputate viverra
                </div>
                <p class="text-base text-gray-700">
                  Nam malesuada aliquet metus, ac commodo augue mollis sit amet. Nam bibendum risus
                  sit amet metus semper consectetur. Proin consequat ullamcorper eleifend. Nam
                  bibendum risus sit amet metus semper consectetur.
                </p>
              </div>
              <div class="mt-3 flex">
                <img
                  loading="lazy"
                  src="https://randomuser.me/api/portraits/women/54.jpg"
                  class="mr-2 h-10 w-10 rounded-full object-cover"
                />
                <div>
                  <p class="text-sm font-semibold capitalize text-gray-700">Serenity Hughes</p>
                  <p class="text-xs text-gray-600">14 Aug</p>
                </div>
              </div>
            </div>
          </div>

          <div class="lg:flex mb-10 w-full rounded">
            <div
              class="lg:w-48 h-48 flex-none overflow-hidden bg-cover text-center opacity-75"
              style="
                background-image: url('https://images.unsplash.com/photo-1512621776951-a57141f2eefd?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=2100&q=80');
              "
              title="deit is very important"
            ></div>
            <div class="flex flex-col justify-between rounded bg-white px-4 leading-normal">
              <div>
                <div class="md:mt-0 mb-2 mt-3 text-2xl font-medium text-gray-700">
                  Suspendisse varius justo eu risus laoreet fermentum non aliquam dolor
                </div>
                <p class="text-base text-gray-700">
                  Mauris porttitor, velit at tempus vulputate, odio turpis facilisis dui, vitae
                  eleifend odio ipsum at odio. Phasellus luctus scelerisque felis eget suscipit.
                </p>
              </div>
              <div class="mt-3 flex">
                <img
                  loading="lazy"
                  src="https://randomuser.me/api/portraits/men/86.jpg"
                  class="mr-2 h-10 w-10 rounded-full object-cover"
                />
                <div>
                  <p class="text-sm font-semibold capitalize text-gray-700">eduard franz</p>
                  <p class="text-xs text-gray-600">14 Aug</p>
                </div>
              </div>
            </div>
          </div>

          <div class="lg:flex-row mt-10 w-full flex-col justify-between rounded">
            <nav
              aria-label="Pagination"
              class="lg:mt-0 mt-8 flex items-center justify-center text-gray-600"
            >
              <a href="#" class="mr-4 rounded p-2 hover:bg-gray-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 19l-7-7 7-7"
                  />
                </svg>
              </a>
              <a href="#" class="rounded px-4 py-2 hover:bg-gray-100"> 1 </a>
              <a
                href="#"
                class="rounded bg-gray-200 px-4 py-2 font-medium text-gray-900 hover:bg-gray-100"
              >
                2
              </a>
              <a href="#" class="rounded px-4 py-2 hover:bg-gray-100"> 3 </a>
              <a href="#" class="rounded px-4 py-2 hover:bg-gray-100"> ... </a>
              <a href="#" class="rounded px-4 py-2 hover:bg-gray-100"> 9 </a>
              <a href="#" class="ml-4 rounded p-2 hover:bg-gray-100">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </a>
            </nav>
          </div>
        </div>

        <!-- right advertisement -->
        <div class="lg:w-1/3 w-full space-y-2 px-3">
          <!-- <img loading="lazy" src="assets/images/banner_advertisement.jpg" alt="advertisement" srcset="" /> -->
          <!-- <img loading="lazy" src="assets/images/banner_advertisement.jpg" alt="advertisement" srcset="" /> -->
        </div>
      </div>
    </main>
    <!-- main ends here -->
  </div>
</template>

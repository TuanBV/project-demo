<template>
  <div class="absolute left-0 top-0 z-[999] h-[100vh] w-[100vw] bg-green-400">
    <div class="tablet:grid tablet:grid-cols-3 overflow-hidden rounded-lg shadow-2xl">
      <img
        loading="lazy"
        alt=""
        src="https://images.unsplash.com/photo-1611510338559-2f463335092c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=928&q=80"
        class="tablet:h-full h-32 w-full object-cover"
      />

      <div class="tablet:col-span-2 pc:p-8 p-4 text-center sm:p-6">
        <p class="text-sm font-semibold uppercase tracking-widest">Run with the pack</p>

        <h2 class="mt-6 font-black uppercase">
          <span class="pc:text-6xl text-4xl font-black sm:text-5xl"> Get 20% off </span>

          <span class="mt-2 block text-sm">On your next order over $50</span>
        </h2>

        <a
          class="mt-8 inline-block w-full bg-black py-4 text-sm font-bold uppercase tracking-widest text-white"
          href="#"
        >
          Get Discount
        </a>

        <p class="mt-8 text-xs font-medium uppercase text-gray-400">
          Offer valid until 24th March, 2021 *
        </p>
      </div>
    </div>
  </div>
</template>

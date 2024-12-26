<template>
  <section class="flex min-h-screen items-center justify-center border-red-500 bg-gray-200">
    <div class="flex max-w-3xl rounded-2xl bg-gray-100 p-5 shadow-lg">
      <div class="md:w-1/2 px-5">
        <h2 class="text-2xl font-bold text-[#002D74]">Forgot Password</h2>
        <p class="mt-4 text-sm text-[#002D74]">If you forgot an account, please input email</p>
        <form class="mt-6" action="#" method="POST">
          <div>
            <label class="block text-gray-700">Email Address</label>
            <input
              type="email"
              name=""
              id=""
              placeholder="Enter Email Address"
              class="mt-2 w-full rounded-lg border bg-gray-200 px-4 py-3 focus:border-blue-500 focus:bg-white focus:outline-none"
              autofocus
              required
            />
          </div>

          <button
            type="submit"
            class="mt-6 block w-full rounded-lg bg-blue-500 px-4 py-3 font-medium text-white hover:bg-blue-400 focus:bg-blue-400"
          >
            Send email
          </button>
        </form>

        <div class="mt-7 grid grid-cols-3 items-center text-gray-500">
          <hr class="border-gray-500" />
          <p class="text-center text-sm">OR</p>
          <hr class="border-gray-500" />
        </div>

        <div class="mt-3 flex items-center justify-center text-sm">
          <router-link
            to="/sign-in"
            class="ml-3 rounded-xl border border-blue-400 bg-white px-5 py-2 font-medium duration-300 hover:scale-110"
          >
            Sign In
          </router-link>
          <router-link
            to="/sign-up"
            class="ml-3 rounded-xl border border-blue-400 bg-white px-5 py-2 font-medium duration-300 hover:scale-110"
          >
            Sign Up
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

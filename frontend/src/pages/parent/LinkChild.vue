<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-400 via-purple-400 to-pink-300 flex items-center justify-center p-4">
    <FloatingDecorativeElements />
    <div class="w-full max-w-md p-8 space-y-6 bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20">
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-800">Link Your Child</h2>
        <p class="mt-2 text-gray-600">Enter the unique key to connect with your child's account.</p>
      </div>
      <form @submit.prevent="linkChild" class="space-y-6">
        <div>
          <label for="child-key" class="text-sm font-medium text-gray-700 sr-only">Child's Unique Key</label>
          <div class="relative">
            <input
              id="child-key"
              v-model="childKey"
              type="text"
              required
              class="w-full px-4 py-3 text-lg text-gray-700 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-all"
              placeholder="e.g., 1A3-X3Z"
            />
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.623 5.913M15 7a2 2 0 00-2-2M4.377 16.913A6 6 0 0112 4.087M15 7a2 2 0 00-2 2m0 0A2 2 0 0111 7m-6 10a2 2 0 012-2m-2 2a2 2 0 00-2 2m2-2a2 2 0 012 2m-2-2a2 2 0 002-2m-2 2a2 2 0 012-2m-2 2a2 2 0 002-2" /></svg>
            </div>
          </div>
        </div>
        <div>
          <button
            type="submit"
            class="w-full px-4 py-3 font-bold text-white bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transform hover:scale-105 transition-all duration-200 shadow-lg"
          >
            <span class="text-lg">Link Account</span>
          </button>
        </div>
      </form>
      <div class="text-center mt-4">
        <router-link to="/parent/home" class="text-sm text-gray-600 hover:text-blue-500 transition-colors">Back to Dashboard</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FloatingDecorativeElements from "@/components/partials/FloatingDecorativeElements.vue";

const childKey = ref('');

const linkChild = () => {
  // Handle the logic for linking the child using the childKey
  console.log('Linking child with key:', childKey.value);
};
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
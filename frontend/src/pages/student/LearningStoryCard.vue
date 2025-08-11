<template>
  <div class="bg-white rounded-[20px] shadow-lg overflow-hidden border border-gray-200 flex flex-col transform hover:scale-102 transition-all duration-300 ease-in-out">
    <div class="p-5 flex-grow">
      <div class="flex items-start gap-4 mb-3">
        <div class="text-4xl">{{ story.emoji }}</div> <!-- Larger emoji for prominence -->
        <div class="flex-1">
          <h3 class="text-xl font-bold text-gray-900 mb-1">{{ story.title }}</h3>
          <p class="text-gray-700 text-sm leading-snug">{{ story.description }}</p>
        </div>
      </div>
    </div>
    <div class="p-5 bg-gray-50 border-t border-gray-200 flex flex-col space-y-3">
      <div class="flex justify-between items-center w-full">
        <button class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-xl shadow hover:bg-blue-700 transition-colors duration-200 text-sm font-medium">
          Watch Lesson
        </button>
        <button class="inline-flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-xl shadow hover:bg-green-700 transition-colors duration-200 text-sm font-medium">
          Mark as Complete
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  story: {
    type: Object,
    required: true,
    validator: (value) => {
      return (
        typeof value.id === 'number' &&
        typeof value.title === 'string' &&
        typeof value.description === 'string' &&
        typeof value.emoji === 'string' &&
        typeof value.topic === 'string'
      );
    },
  },
});
</script>

<style scoped>
/* Scoped styles specific to the card if needed, otherwise Tailwind handles most of it. */
</style>

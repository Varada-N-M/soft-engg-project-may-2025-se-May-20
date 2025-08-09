<template>
  <div
    class="bg-gradient-to-br from-orange-50 to-yellow-50 p-6 rounded-2xl shadow-sm border border-orange-100 transition-transform hover:scale-[1.02] cursor-pointer"
  >
    <div class="flex items-start gap-4">
      <div class="text-3xl mt-1">{{ story.emoji }}</div>
      <div class="flex-1">
        <h3 class="font-bold text-gray-900 text-lg mb-1">{{ story.title }}</h3>
        <p class="text-sm text-gray-700 mb-3 leading-snug">{{ story.description }}</p>
        <div class="flex justify-between items-center">
          <span class="text-xs bg-orange-100 text-orange-600 font-semibold px-3 py-1 rounded-full">
            {{ story.topic }}
          </span>
          <button class="text-orange-500 hover:text-orange-600 font-medium text-sm">
            Read Story →
          </button>
        </div>
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
  },
});
</script>
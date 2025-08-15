<template>
  <div class="bg-white rounded-3xl p-6 shadow-lg transform transition-transform hover:scale-101 cursor-pointer relative overflow-hidden">
    <div class="absolute inset-0 rounded-3xl"></div>

    <div class="relative z-10 text-center">
      <div class="w-24 h-24 mx-auto rounded-full flex items-center justify-center text-5xl mb-4 text-white shadow-xl">
        {{ badge.emoji }}
      </div>

      <h3 class="font-bold text-gray-900 text-xl mb-1">{{ badge.name }}</h3>
      <p class="text-sm text-gray-700 mb-3">{{ badge.description }}</p>

      <div class="inline-flex items-center bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-xs font-semibold">
        <span class="mr-1">⭐</span>
        +{{ badge.xpReward }} XP
      </div>

      <p v-if="badge.earnedDate" class="text-xs text-gray-500 mt-2">
        Earned on {{ formatDate(badge.earnedDate) }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  badge: {
    type: Object,
    required: true,
  },
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};
</script>
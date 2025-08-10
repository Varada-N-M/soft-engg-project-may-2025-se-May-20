<template>
  <div
    class="flex items-center gap-4 p-4 rounded-xl transition-colors cursor-pointer"
    :class="getSubjectClass(lesson.subject)"
  >
    <div
      class="text-white rounded-lg p-3 text-lg"
      :class="getSubjectBgClass(lesson.subject)"
    >
      {{ getSubjectEmoji(lesson.subject) }}
    </div>
    <div class="flex-1">
      <h3 class="font-semibold text-gray-800">{{ lesson.lesson }}</h3>
      <p class="text-gray-600 text-sm">{{ lesson.activity }}</p>
      <p class="text-xs text-gray-500 mt-1">{{ formatDate(lesson.created_at) }} • {{ lesson.subject }}</p>
    </div>
    <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
    </svg>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
// import { formatDate, getSubjectClass, getSubjectBgClass, getSubjectEmoji } from '@/utils/helpers'; // Assuming you move these functions

defineProps({
  lesson: Object,
});
</script>
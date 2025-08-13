<!-- LifeLessonCard.vue -->
<template>
  <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-200 flex flex-col transform hover:scale-101 transition-all duration-300 ease-in-out">
    <div class="p-5 flex-grow">
      <h3 class="text-xl font-bold text-gray-900 mb-2">{{ lesson.title }}</h3>
      <p class="text-gray-700 text-sm mb-4 flex-grow">{{ lesson.description }}</p>
    </div>
    <div class="p-5 bg-gray-50 border-t border-gray-200 flex flex-col space-y-3">
      <a
        :href="lesson.youtubeLink"
        target="_blank"
        rel="noopener noreferrer"
        class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-xl shadow hover:bg-blue-700 transition-colors duration-200 text-sm font-medium"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
          <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
          <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
        </svg>
        Watch Lesson
      </a>
      <button
        @click="markComplete"
        :disabled="lesson.completed"
        class="w-full px-4 py-2 rounded-xl shadow-md transition-colors duration-200 text-sm font-medium"
        :class="{
          'bg-green-600 text-white hover:bg-green-700': !lesson.completed,
          'bg-green-600 text-white cursor-not-allowed': lesson.completed
        }"
      >
        {{ lesson.completed ? 'Lesson Completed!' : 'Mark as Complete' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  lesson: {
    type: Object,
    required: true,
    validator: (value) => {
      return (
        typeof value.id === 'number' &&
        typeof value.title === 'string' &&
        typeof value.description === 'string' &&
        typeof value.youtubeLink === 'string' &&
        typeof value.completed === 'boolean'
      );
    },
  },
});

const emit = defineEmits(['lesson-completed']);

const markComplete = () => {
  if (!props.lesson.completed) {
    emit('lesson-completed', props.lesson.id);
  }
};
</script>

<style scoped>
/* Scoped styles specific to the card if needed, otherwise Tailwind handles most of it. */
</style>
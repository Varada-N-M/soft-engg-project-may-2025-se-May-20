<!-- LifeLessonCard.vue -->
<template>
  <div class="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 transform hover:scale-101">
    <!-- Lesson Title -->
    <div class="mb-4">
      <h3 class="text-lg font-bold text-gray-900 leading-tight">
        {{ lesson.skill_name || lesson.title }}
      </h3>
    </div>

    <!-- Action Buttons -->
    <div class="flex gap-3">
      <!-- Watch Lesson Button -->
      <button 
        @click="watchLesson"
        class="flex-1 bg-blue-500 text-white px-4 py-2.5 rounded-[15px] font-medium hover:bg-blue-600 transition-colors duration-200 flex items-center justify-center gap-2"
        :disabled="!lesson.video_url"
        :class="{ 'opacity-50 cursor-not-allowed': !lesson.video_url }"
      >
        <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
          <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
        </svg>
        Watch Lesson
      </button>

      <!-- Mark Complete Button -->
      <button 
        @click="toggleComplete"
        class="px-4 py-2.5 rounded-[15px] font-medium transition-colors duration-200 flex items-center justify-center"
        :class="lesson.completed 
          ? 'bg-gray-100 text-gray-600 hover:bg-gray-200' 
          : 'bg-green-500 text-white hover:bg-green-600'"
      >
        <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>
        </svg>
      </button>
    </div>

    <!-- No Video Warning -->
    <div v-if="!lesson.video_url" class="mt-3 p-2 bg-yellow-50 rounded-lg border border-yellow-200">
      <p class="text-yellow-700 text-xs text-center">No video available for this lesson</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

// Props
const props = defineProps({
  lesson: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['lesson-completed'])

// Methods
const watchLesson = () => {
  if (props.lesson.video_url) {
    // Open video in new tab
    window.open(props.lesson.video_url, '_blank')
  } else {
    alert('No video available for this lesson')
  }
}

const toggleComplete = () => {
  emit('lesson-completed', props.lesson.id)
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
<template>
  <div class="mt-6 text-center">
    <p class="text-xs text-gray-500 mb-2">Sign in as a different user type? </p>
    <div class="flex justify-center space-x-4">
      <router-link
          v-if="activeLink!=='student'"
          to="/student/login"
          class="text-xs text-blue-600 hover:text-blue-800 transition-colors"
      >
        👶🏻 Student
      </router-link>
      <router-link
          v-if="activeLink!=='parent'"
          to="/parent/login"
          class="text-xs text-pink-600 hover:text-pink-800 transition-colors"
      >
        👨‍👩‍👧‍👦 Parent
      </router-link>
      <router-link
          v-if="activeLink!=='teacher'"
          to="/teacher/login"
          class="text-xs text-teal-600 hover:text-teal-800 transition-colors"
      >
        👨‍🏫 Teacher
      </router-link>
    </div>
  </div>
</template>
<script setup>
import {defineProps} from 'vue'

const props = defineProps({
  activeLink: {
    default: '',
    // accepted values

    type: String,

  }
})
</script>
<style scoped>

.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

</style>
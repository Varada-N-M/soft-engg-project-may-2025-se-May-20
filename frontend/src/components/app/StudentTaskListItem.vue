<script setup lang="ts">

import {ChevronRightIcon} from "lucide-vue-next";

defineProps({
  lesson: {}
})
</script>

<template>
  <div class="w-12 h-12 rounded-full flex items-center justify-center text-2xl mr-4"
       :style="{ backgroundColor: lesson.color }">
    {{ lesson.emoji }}
  </div>
  <div class="flex-1">
    <h4 class="font-semibold text-gray-800">{{ lesson.title }}</h4>
    <p class="text-sm text-gray-600">{{ lesson.description }}</p>
    <div class="mt-2">
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div class="bg-blue-500 h-2 rounded-full transition-all duration-500"
             :style="{ width: `${lesson.progress}%` }"></div>
      </div>
      <p class="text-xs text-gray-500 mt-1">{{ lesson.progress }}% complete</p>
    </div>
  </div>
  <ChevronRightIcon class="w-5 h-5 text-gray-400"/>
</template>

<style scoped>

</style>
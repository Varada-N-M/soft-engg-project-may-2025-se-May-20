<template>
  <div
    class="p-4 rounded-xl border-2 transition-all duration-200 cursor-pointer"
    :class="activity.completed ? 'border-green-300 bg-green-50' : 'border-gray-200 bg-gray-50 hover:border-blue-300'"
    @click="$emit('toggle', activity.id)"
  >
    <div class="flex items-start justify-between mb-2">
      <div class="text-2xl">{{ activity.emoji }}</div>
      <div class="text-xl" :class="activity.completed ? 'text-green-500' : 'text-gray-400'">
        {{ activity.completed ? '✅' : '⭕' }}
      </div>
    </div>
    <h3 class="font-semibold text-gray-800 mb-1">{{ activity.title }}</h3>
    <p class="text-sm text-gray-600 mb-2">{{ activity.description }}</p>
    <div class="flex justify-between items-center text-xs">
      <span class="text-gray-500">{{ activity.category }}</span>
      <span class="bg-orange-100 text-orange-600 px-2 py-1 rounded-full">+{{ activity.xp }} XP</span>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  activity: Object,
});
</script>
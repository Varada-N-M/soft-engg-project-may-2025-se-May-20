<template>
  <div class="bg-white rounded-2xl p-6 shadow-md justify-center">
    <div class="text-center">
      <p class="text-gray-600 text-sm font-medium mb-1">{{ label }}</p>
      <h3 class="text-4xl font-bold text-orange-500">
        <span v-if="loading">...</span>
        <span v-else>{{ value ?? 0 }}</span>
      </h3>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

defineProps({
  icon: String,
  label: String,
  value: [Number, String],
  unit: {
    type: String,
    default: '',
  },
  loading: {
    type: Boolean,
    default: false,
  },
});
</script>
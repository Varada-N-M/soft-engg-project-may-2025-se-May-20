<template>
  <div class="bg-white rounded-2xl p-6 shadow-md">
    <div class="flex items-center justify-between mb-3">
      <div>
        <p class="text-gray-600 text-sm font-medium">{{ label }}</p>
        <h3 class="text-3xl font-bold text-orange-500">
          <span v-if="loading">...</span>
          <span v-else>{{ value ?? 0 }}</span>
        </h3>
      </div>
      <div class="text-4xl">{{ icon }}</div>
    </div>
    <p v-if="unit" class="text-gray-500 text-sm">{{ unit }}</p>
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
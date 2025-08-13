<template>
  <div class="progress-chart">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-800">{{ title }}</h3>
      <p v-if="description" class="text-sm text-gray-600">{{ description }}</p>
    </div>
    
    <!-- Simple Progress Bar for now -->
    <div class="space-y-3">
      <div v-for="(item, index) in data" :key="index" class="flex items-center space-x-3">
        <div class="flex-1">
          <div class="flex justify-between items-center mb-1">
            <span class="text-sm font-medium text-gray-700">{{ item.label }}</span>
            <span class="text-sm text-gray-500">{{ item.value }}{{ showPercentage ? '%' : '' }}</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 rounded-full transition-all duration-300"
              :class="getProgressColor(item.value, item.max)"
              :style="`width: ${getProgressWidth(item.value, item.max)}%`"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Stats -->
    <div v-if="showSummary" class="mt-4 p-3 bg-gray-50 rounded-lg">
      <div class="text-sm text-gray-600">
        Total: {{ totalCompleted }}/{{ totalPossible }} 
        ({{ Math.round((totalCompleted / totalPossible) * 100) }}%)
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  data: {
    type: Array,
    required: true,
    // Expected format: [{ label: 'Skills', value: 15, max: 20 }]
  },
  showPercentage: {
    type: Boolean,
    default: false
  },
  showSummary: {
    type: Boolean,
    default: false
  }
})

const totalCompleted = computed(() => {
  return props.data.reduce((sum, item) => sum + item.value, 0)
})

const totalPossible = computed(() => {
  return props.data.reduce((sum, item) => sum + item.max, 0)
})

const getProgressWidth = (value, max) => {
  if (max === 0) return 0
  return Math.min((value / max) * 100, 100)
}

const getProgressColor = (value, max) => {
  const percentage = max === 0 ? 0 : (value / max) * 100
  
  if (percentage >= 80) {
    return 'bg-green-500'
  } else if (percentage >= 60) {
    return 'bg-blue-500'
  } else if (percentage >= 40) {
    return 'bg-yellow-500'
  } else {
    return 'bg-red-500'
  }
}
</script>

<style scoped>
.progress-chart {
  @apply bg-white p-4 rounded-lg border border-gray-200;
}
</style>
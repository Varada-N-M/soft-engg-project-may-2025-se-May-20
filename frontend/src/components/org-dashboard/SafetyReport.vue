<template>
  <div class="space-y-4">
    <div v-for="(value, key) in data" :key="key" class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-3 h-3 rounded-full" :class="getStatusColor(value)"></div>
        <span class="text-sm font-medium text-gray-700 capitalize">
          {{ key.replace(/([A-Z])/g, ' $1').trim() }}
        </span>
      </div>
      <span class="text-sm font-semibold text-gray-900">{{ value }}%</span>
    </div>
    <div class="mt-4 p-3 bg-yellow-50 rounded-lg">
      <div class="flex items-center">
        <AlertTriangle class="w-4 h-4 text-yellow-600 mr-2" />
        <span class="text-sm text-yellow-800">
          First Aid training needs improvement
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AlertTriangle } from 'lucide-vue-next'

interface SafetyData {
  emergencyKnowledge: number
  firstAidBasics: number
  contactInformation: number
  safetyProtocols: number
}

defineProps<{
  data: SafetyData
}>()

const getStatusColor = (value: number) => {
  if (value >= 80) return 'bg-green-500'
  if (value >= 60) return 'bg-yellow-500'
  return 'bg-red-500'
}
</script>

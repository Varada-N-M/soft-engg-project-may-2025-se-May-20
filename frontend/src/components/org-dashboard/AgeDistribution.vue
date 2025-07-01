<template>
  <div class="space-y-4">
    <div v-for="item in data" :key="item.age" class="space-y-2">
      <div class="flex justify-between items-center">
        <span class="text-sm font-medium text-gray-700">Age {{ item.age }}</span>
        <span class="text-sm text-gray-500">{{ item.count }} ({{ item.percentage }}%)</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-purple-600 h-2 rounded-full"
          :style="{ width: `${item.percentage}%` }"
        ></div>
      </div>
    </div>
    <div class="mt-4 text-center">
      <p class="text-sm text-gray-600">
        Most active age group: <span class="font-semibold">12-13 years</span>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface AgeItem {
  age: string
  count: number
  percentage: number
}

defineProps<{
  data: AgeItem[]
}>()
</script>

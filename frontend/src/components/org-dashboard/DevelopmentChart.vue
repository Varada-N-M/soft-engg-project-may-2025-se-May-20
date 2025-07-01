<template>
  <div class="space-y-4">
    <div v-for="item in data" :key="item.skill" class="space-y-2">
      <div class="flex justify-between items-center">
        <span class="text-sm font-medium text-gray-700">{{ item.skill }}</span>
        <span class="text-sm text-gray-500">{{ item.progress }}% / {{ item.target }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div 
          class="bg-blue-600 h-2 rounded-full relative"
          :style="{ width: `${item.progress}%` }"
        >
          <div 
            class="absolute top-0 right-0 w-1 h-2 bg-red-400 rounded-full"
            :style="{ right: `${100 - item.target}%` }"
            v-if="item.target > item.progress"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface DevelopmentItem {
  skill: string
  progress: number
  target: number
}

defineProps<{
  data: DevelopmentItem[]
}>()
</script>

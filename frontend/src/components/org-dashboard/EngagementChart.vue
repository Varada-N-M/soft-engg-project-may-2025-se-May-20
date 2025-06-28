<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center text-sm text-gray-600">
      <span>Engagement Rate</span>
      <span>Task Completions</span>
    </div>
    <div class="h-48 flex items-end justify-between space-x-1">
      <div 
        v-for="(item, index) in data" 
        :key="index"
        class="flex flex-col items-center space-y-1 flex-1"
      >
        <div class="w-full flex flex-col items-center space-y-1">
          <div 
            class="w-full bg-blue-200 rounded-t"
            :style="{ height: `${(item.engagement / 100) * 120}px` }"
          ></div>
          <div 
            class="w-full bg-green-200 rounded-t"
            :style="{ height: `${(item.completions / 100) * 80}px` }"
          ></div>
        </div>
        <span class="text-xs text-gray-500">
          {{ new Date(item.date).getDate() }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface EngagementItem {
  date: string
  engagement: number
  completions: number
}

defineProps<{
  data: EngagementItem[]
}>()
</script>

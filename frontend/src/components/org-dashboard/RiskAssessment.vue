<template>
  <div class="space-y-4">
    <div class="grid grid-cols-2 gap-4">
      <div class="text-center p-3 bg-green-50 rounded-lg">
        <div class="text-2xl font-bold text-green-600">{{ data.lowRisk }}</div>
        <div class="text-sm text-green-700">Low Risk</div>
      </div>
      <div class="text-center p-3 bg-yellow-50 rounded-lg">
        <div class="text-2xl font-bold text-yellow-600">{{ data.mediumRisk }}</div>
        <div class="text-sm text-yellow-700">Medium Risk</div>
      </div>
      <div class="text-center p-3 bg-orange-50 rounded-lg">
        <div class="text-2xl font-bold text-orange-600">{{ data.highRisk }}</div>
        <div class="text-sm text-orange-700">High Risk</div>
      </div>
      <div class="text-center p-3 bg-red-50 rounded-lg">
        <div class="text-2xl font-bold text-red-600">{{ data.criticalRisk }}</div>
        <div class="text-sm text-red-700">Critical</div>
      </div>
    </div>
    <div class="mt-4 p-3 bg-red-50 rounded-lg" v-if="data.criticalRisk > 0">
      <div class="flex items-center">
        <AlertTriangle class="w-4 h-4 text-red-600 mr-2" />
        <span class="text-sm text-red-800">
          {{ data.criticalRisk }} children require immediate attention
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AlertTriangle } from 'lucide-vue-next'

interface RiskData {
  lowRisk: number
  mediumRisk: number
  highRisk: number
  criticalRisk: number
}

defineProps<{
  data: RiskData
}>()
</script>

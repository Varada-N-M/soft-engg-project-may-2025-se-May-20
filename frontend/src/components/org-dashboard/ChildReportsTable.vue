<template>
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Child
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Age
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Engagement
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Skills Completed
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Well-being
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Risk Level
          </th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Last Active
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        <tr v-for="report in reports" :key="report.id" class="hover:bg-gray-50">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-blue-600">
                  {{ report.name.split(' ').map(n => n[0]).join('') }}
                </span>
              </div>
              <div class="ml-3">
                <div class="text-sm font-medium text-gray-900">{{ report.name }}</div>
                <div class="text-sm text-gray-500">ID: {{ report.id }}</div>
              </div>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ report.age }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <div class="w-16 bg-gray-200 rounded-full h-2 mr-2">
                <div 
                  class="bg-blue-600 h-2 rounded-full"
                  :style="{ width: `${report.engagement}%` }"
                ></div>
              </div>
              <span class="text-sm text-gray-900">{{ report.engagement }}%</span>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
            {{ report.skillsCompleted }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <Heart class="w-4 h-4 text-red-500 mr-1" />
              <span class="text-sm text-gray-900">{{ report.wellbeingScore }}</span>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap">
            <span 
              class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
              :class="getRiskLevelClass(report.riskLevel)"
            >
              {{ report.riskLevel }}
            </span>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ formatDate(report.lastActive) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { Heart } from 'lucide-vue-next'

interface ChildReport {
  id: string
  name: string
  age: number
  engagement: number
  skillsCompleted: number
  wellbeingScore: number
  lastActive: string
  riskLevel: string
}

defineProps<{
  reports: ChildReport[]
}>()

const getRiskLevelClass = (level: string) => {
  switch (level.toLowerCase()) {
    case 'low':
      return 'bg-green-100 text-green-800'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800'
    case 'high':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}
</script>

<template>
  <div class="progress-summary">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-800">Progress Overview</h3>
      <p v-if="studentName" class="text-sm text-gray-600">{{ studentName }}</p>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <!-- XP Points -->
      <div class="stat-card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-purple-100 text-sm">Total XP</p>
            <p class="text-2xl font-bold">{{ formatNumber(summary.xp_points || 0) }}</p>
          </div>
          <div class="text-3xl">⭐</div>
        </div>
      </div>

      <!-- Streak -->
      <div class="stat-card bg-gradient-to-br from-orange-500 to-orange-600 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-orange-100 text-sm">Current Streak</p>
            <p class="text-2xl font-bold">{{ summary.streak || 0 }}</p>
          </div>
          <div class="text-3xl">🔥</div>
        </div>
      </div>

      <!-- Skills Completed -->
      <div class="stat-card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-blue-100 text-sm">Skills</p>
            <p class="text-2xl font-bold">{{ summary.completed_skills || 0 }}/{{ summary.total_skills || 0 }}</p>
          </div>
          <div class="text-3xl">📚</div>
        </div>
      </div>

      <!-- Badges Earned -->
      <div class="stat-card bg-gradient-to-br from-green-500 to-green-600 text-white">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-green-100 text-sm">Badges</p>
            <p class="text-2xl font-bold">{{ summary.total_badges || 0 }}</p>
          </div>
          <div class="text-3xl">🏆</div>
        </div>
      </div>
    </div>

    <!-- Weekly Progress (if available) -->
    <div v-if="weeklyStats" class="weekly-progress">
      <h4 class="font-semibold text-gray-700 mb-3">This Week</h4>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div class="mini-stat-card">
          <div class="text-lg font-bold text-gray-800">{{ weeklyStats.habits_completed || 0 }}</div>
          <div class="text-xs text-gray-500">Habits Done</div>
        </div>
        <div class="mini-stat-card">
          <div class="text-lg font-bold text-gray-800">{{ weeklyStats.skills_completed || 0 }}</div>
          <div class="text-xs text-gray-500">Skills Learned</div>
        </div>
        <div class="mini-stat-card">
          <div class="text-lg font-bold text-gray-800">{{ weeklyStats.badges_earned || 0 }}</div>
          <div class="text-xs text-gray-500">Badges Earned</div>
        </div>
        <div class="mini-stat-card">
          <div class="text-lg font-bold text-gray-800">{{ weeklyStats.todos_completed || 0 }}</div>
          <div class="text-xs text-gray-500">Tasks Done</div>
        </div>
      </div>
    </div>

    <!-- Progress Indicators -->
    <div v-if="showProgress" class="mt-6">
      <div class="space-y-3">
        <!-- Skills Progress -->
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-gray-700">Skills Mastery</span>
          <span class="text-sm text-gray-500">{{ getSkillsPercentage() }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div 
            class="h-2 bg-blue-500 rounded-full transition-all duration-500"
            :style="`width: ${getSkillsPercentage()}%`"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  summary: {
    type: Object,
    required: true,
    default: () => ({})
  },
  studentName: {
    type: String,
    default: ''
  },
  weeklyStats: {
    type: Object,
    default: null
  },
  showProgress: {
    type: Boolean,
    default: true
  }
})

const formatNumber = (num) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const getSkillsPercentage = () => {
  const total = props.summary.total_skills || 0
  const completed = props.summary.completed_skills || 0
  if (total === 0) return 0
  return Math.round((completed / total) * 100)
}
</script>

<style scoped>
@reference '@/css/index.css';
.progress-summary {
  @apply bg-white p-4 rounded-lg border border-gray-200;
}

.stat-card {
  @apply p-4 rounded-lg shadow-sm;
}

.mini-stat-card {
  @apply p-3 bg-gray-50 rounded-lg text-center;
}

.weekly-progress {
  @apply pt-4 border-t border-gray-100;
}
</style>
<template>
  <TeacherNavbar/>
  <div class="class-analytics-page">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Class Analytics</h1>
          <p class="text-gray-600">Overview of your class performance and progress</p>
        </div>
        <button
            @click="refreshData"
            :disabled="loading"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
        >
          <svg v-if="loading" class="w-4 h-4 animate-spin mr-2 inline" fill="none" stroke="currentColor"
               viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          {{ loading ? 'Loading...' : 'Refresh' }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && !analyticsData" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"/>
        </svg>
        <span class="text-red-800">{{ error }}</span>
      </div>
    </div>

    <!-- No Students State -->
    <div v-else-if="analyticsData && analyticsData.total_students === 0" class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">👨‍🏫</div>
      <h3 class="text-lg font-semibold text-gray-800 mb-2">No Students Yet</h3>
      <p class="text-gray-600 mb-4">Start by adding students to your class to see analytics</p>
      <router-link
          to="/teacher/add-student"
          class="inline-flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        Add Students
      </router-link>
    </div>

    <!-- Main Content -->
    <div v-else-if="analyticsData" class="space-y-6">
      <!-- Class Overview Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div class="stat-card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-100 text-sm">Total Students</p>
              <p class="text-3xl font-bold">{{ analyticsData.total_students }}</p>
            </div>
            <div class="text-4xl">👨‍🎓</div>
          </div>
        </div>

        <div class="stat-card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-100 text-sm">Total Class XP</p>
              <p class="text-3xl font-bold">{{ formatNumber(analyticsData.class_overview.total_xp || 0) }}</p>
            </div>
            <div class="text-4xl">⭐</div>
          </div>
        </div>

        <div class="stat-card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100 text-sm">Average XP</p>
              <p class="text-3xl font-bold">{{ formatNumber(analyticsData.class_overview.average_xp || 0) }}</p>
            </div>
            <div class="text-4xl">📊</div>
          </div>
        </div>

        <div class="stat-card bg-gradient-to-br from-yellow-500 to-yellow-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-yellow-100 text-sm">Total Badges</p>
              <p class="text-3xl font-bold">{{ analyticsData.class_overview.total_badges || 0 }}</p>
            </div>
            <div class="text-4xl">🏆</div>
          </div>
        </div>
      </div>

      <!-- Top Performers & Skills Summary -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Top Performers -->
        <div class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Top Performers</h3>

          <div v-if="analyticsData.top_performers.length === 0" class="text-center py-8">
            <p class="text-gray-500">No performance data available yet</p>
          </div>

          <div v-else class="space-y-4">
            <div
                v-for="(student, index) in analyticsData.top_performers"
                :key="student.student_id"
                class="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg"
            >
              <div class="flex-shrink-0">
                <div
                    class="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm"
                    :class="getRankColor(index)"
                >
                  {{ index + 1 }}
                </div>
              </div>
              <div class="flex-1">
                <div class="font-medium text-gray-800">{{ student.name }}</div>
                <div class="text-sm text-gray-500">
                  {{ formatNumber(student.xp_points) }} XP • {{ student.streak }} day streak
                </div>
              </div>
              <button
                  @click="viewStudentProgress(student.student_id)"
                  class="text-blue-500 hover:text-blue-600 text-sm font-medium"
              >
                View Progress
              </button>
            </div>
          </div>
        </div>

        <!-- Skills Summary -->
        <div class="bg-white rounded-lg border border-gray-200 p-6">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">Skills Progress</h3>

          <div v-if="Object.keys(analyticsData.skills_summary || {}).length === 0" class="text-center py-8">
            <p class="text-gray-500">No skills data available yet</p>
          </div>

          <div v-else class="space-y-4">
            <div
                v-for="(skillData, skillType) in analyticsData.skills_summary"
                :key="skillType"
                class="skill-summary-item"
            >
              <div class="flex justify-between items-center mb-2">
                <span class="font-medium text-gray-700 capitalize">{{ skillType }}</span>
                <span class="text-sm text-gray-500">
                  {{ skillData.completed }}/{{ skillData.total }}
                </span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div
                    class="h-2 bg-blue-500 rounded-full transition-all duration-300"
                    :style="`width: ${skillData.completion_rate || 0}%`"
                ></div>
              </div>
              <div class="text-xs text-gray-400 mt-1">
                {{ Math.round(skillData.completion_rate || 0) }}% completion rate
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white rounded-lg border border-gray-200 p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <router-link
              to="/teacher/students"
              class="action-card"
          >
            <div class="text-2xl mb-2">👥</div>
            <div class="font-medium">Manage Students</div>
            <div class="text-sm text-gray-500">Add or remove students</div>
          </router-link>

          <router-link
              to="/teacher/lesson-updates"
              class="action-card"
          >
            <div class="text-2xl mb-2">📚</div>
            <div class="font-medium">Lesson Updates</div>
            <div class="text-sm text-gray-500">Create lesson plans</div>
          </router-link>

          <button
              @click="exportData"
              class="action-card text-left"
          >
            <div class="text-2xl mb-2">📊</div>
            <div class="font-medium">Export Data</div>
            <div class="text-sm text-gray-500">Download class report</div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import api from '@/plugins/axios.ts'
import TeacherNavbar from "@/components/app/TeacherNavbar.vue";

const router = useRouter()

const loading = ref(true)
const error = ref('')
const analyticsData = ref(null)

const fetchAnalytics = async () => {
  try {
    loading.value = true
    error.value = ''

    const response = await api.get('/api/teacher/class/analytics')
    analyticsData.value = response.data

  } catch (err) {
    console.error('Error fetching class analytics:', err)
    error.value = err.response?.data?.error || 'Failed to load class analytics'
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchAnalytics()
}

const formatNumber = (num) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const getRankColor = (index) => {
  const colors = ['bg-yellow-500', 'bg-gray-400', 'bg-orange-500', 'bg-blue-500', 'bg-green-500']
  return colors[index] || 'bg-gray-500'
}

const viewStudentProgress = (studentId) => {
  router.push(`/teacher/student-progress/${studentId}`)
}

const exportData = () => {
  // TODO: Implement data export functionality
  alert('Export functionality coming soon!')
}

onMounted(() => {
  fetchAnalytics()
})
</script>

<style scoped>
@reference '@/css/index.css';
.class-analytics-page {
  @apply p-6 min-h-screen bg-gray-50;
}

.stat-card {
  @apply p-6 rounded-lg shadow-sm;
}

.skill-summary-item {
  @apply p-3 bg-gray-50 rounded-lg;
}

.action-card {
  @apply p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer block;
}
</style>
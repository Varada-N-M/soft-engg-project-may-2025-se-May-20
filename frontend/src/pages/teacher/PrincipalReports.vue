<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <TeacherNavbar/>
    <div class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Admin Teacher Dashboard</h1>
            <p class="text-gray-600 mt-1">Organization Statistics & Reports</p>
          </div>
          <div class="flex items-center space-x-4">
            <Button @click="refreshData" :disabled="isLoading" variant="outline">
              <RefreshCw class="w-4 h-4 mr-2" :class="{ 'animate-spin': isLoading }"/>
              Refresh
            </Button>
            <span class="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">Last updated: {{
                lastUpdated
              }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Loading State -->
      <div v-if="isLoading && !statsData" class="flex items-center justify-center py-20">
        <div class="text-center">
          <Loader class="w-8 h-8 animate-spin mx-auto mb-4"/>
          <p class="text-gray-600">Loading organization statistics...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-6">
        <div class="flex items-center">
          <AlertCircle class="w-5 h-5 text-red-600 mr-2"/>
          <p class="text-red-800">{{ error }}</p>
        </div>
      </div>

      <!-- Stats Dashboard -->
      <div v-else-if="statsData" class="space-y-8">
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card class="p-6">
            <div class="flex items-center">
              <Users class="w-8 h-8 text-blue-600"/>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Students</p>
                <p class="text-2xl font-bold text-gray-900">{{ statsData.summary.total_students.toLocaleString() }}</p>
              </div>
            </div>
          </Card>

          <Card class="p-6">
            <div class="flex items-center">
              <GraduationCap class="w-8 h-8 text-green-600"/>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Teachers</p>
                <p class="text-2xl font-bold text-gray-900">{{ statsData.summary.total_teachers.toLocaleString() }}</p>
              </div>
            </div>
          </Card>

          <Card class="p-6">
            <div class="flex items-center">
              <Heart class="w-8 h-8 text-pink-600"/>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Parents</p>
                <p class="text-2xl font-bold text-gray-900">{{ statsData.summary.total_parents.toLocaleString() }}</p>
              </div>
            </div>
          </Card>

          <Card class="p-6">
            <div class="flex items-center">
              <Building class="w-8 h-8 text-purple-600"/>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Total Schools</p>
                <p class="text-2xl font-bold text-gray-900">{{ statsData.summary.total_schools.toLocaleString() }}</p>
              </div>
            </div>
          </Card>
        </div>

        <!-- Engagement Metrics -->
        <Card class="p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-6">Engagement Metrics</h2>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-blue-50 rounded-lg p-4">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm font-medium text-blue-800">Habit Completion Rate</p>
                <CheckCircle class="w-5 h-5 text-blue-600"/>
              </div>
              <p class="text-2xl font-bold text-blue-900">{{ statsData.engagement_metrics.habit_completion_rate }}%</p>
              <p class="text-sm text-blue-700">{{
                  statsData.engagement_metrics.total_habit_completions.toLocaleString()
                }} of {{ statsData.engagement_metrics.total_habits.toLocaleString() }}</p>
            </div>

            <div class="bg-green-50 rounded-lg p-4">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm font-medium text-green-800">Skill Completion Rate</p>
                <BookOpen class="w-5 h-5 text-green-600"/>
              </div>
              <p class="text-2xl font-bold text-green-900">{{ statsData.engagement_metrics.skill_completion_rate }}%</p>
              <p class="text-sm text-green-700">{{ statsData.engagement_metrics.total_skills_learned.toLocaleString() }}
                of {{ statsData.engagement_metrics.total_skills.toLocaleString() }}</p>
            </div>

            <div class="bg-yellow-50 rounded-lg p-4">
              <div class="flex items-center justify-between mb-2">
                <p class="text-sm font-medium text-yellow-800">Todo Completion Rate</p>
                <Target class="w-5 h-5 text-yellow-600"/>
              </div>
              <p class="text-2xl font-bold text-yellow-900">{{ statsData.engagement_metrics.todo_completion_rate }}%</p>
              <p class="text-sm text-yellow-700">{{
                  statsData.engagement_metrics.total_todos_completed.toLocaleString()
                }} of {{ statsData.engagement_metrics.total_todos.toLocaleString() }}</p>
            </div>
          </div>
        </Card>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Class Distribution Chart -->
          <Card class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Class Distribution</h3>
            <BarChart
                v-if="classChartData.length > 0"
                :data="classChartData"
                index="class"
                :categories="['student_count']"
                :colors="['#3b82f6']"
                :height="300"
            />
            <p v-else class="text-gray-500 text-center py-8">No class data available</p>
          </Card>

          <!-- Popular Skills Chart -->
          <Card class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Popular Skills</h3>
            <DonutChart
                v-if="skillsChartData.length > 0"
                :data="skillsChartData"
                index="skill_name"
                :category="'learned_count'"
                :height="300"
                type="pie"
                :colors="['#63b2ff', '#ff81c4', '#bfff6e', '#ffcc93', '#F0E6FF', '#E6FFF3', '#FFE6E6', '#E6E6FF', '#F3F3E6', '#E6F0FF']"

            />
            <p v-else class="text-gray-500 text-center py-8">No skills data available</p>
          </Card>
        </div>

        <!-- Habit Categories & Gender Distribution -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Habit Categories -->
          <Card class="p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Habit Categories</h3>
            <DonutChart
                v-if="habitCategoriesData.length > 0"
                :data="habitCategoriesData"
                index="category"
                category="count"
                :height="300"
                :colors="['#E6F3FF', '#FFE6F3', '#F3FFE6', '#FFF3E6', '#F0E6FF', '#E6FFF3', '#FFE6E6', '#E6E6FF', '#F3F3E6', '#E6F0FF']"
            />
            <p v-else class="text-gray-500 text-center py-8">No habit data available</p>
          </Card>

          <!-- Gender Distribution -->
          <Card class="p-6 pb-12">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Gender Distribution</h3>
            <DonutChart
                v-if="genderChartData.length > 0"
                :data="genderChartData"
                category="count"
                index="gender"
                type="pie"
                :show-legend="true"
                :show-tooltip="true"
            />
            <p v-else class="text-gray-500 text-center py-8">No gender data available</p>
          </Card>
        </div>

        <!-- Habit Completion Trends -->
        <Card class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Habit Completion Trends (Last 7 Days)</h3>
          <AreaChart
              v-if="habitTrendsData.length > 0"
              :data="habitTrendsData"
              index="date"
              :categories="['completions']"
              :colors="['#10b981']"
              :height="300"
          />
          <p v-else class="text-gray-500 text-center py-8">No trend data available</p>
        </Card>

        <!-- Top Performing Students -->
        <Card class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Top Performing Students</h3>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">School</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">XP Points
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Streak</th>
              </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="(student, index) in statsData.top_performers.students" :key="student.child_id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                      <span
                          v-if="index < 3"
                          :class="index === 0 ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-100 text-gray-800'"
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      >
                        {{ index + 1 }}
                      </span>
                    <span v-else class="text-sm text-gray-900">{{ index + 1 }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ student.name }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ student.class || 'N/A' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ student.school || 'N/A' }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{
                    student.xp_points.toLocaleString()
                  }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ student.streak }}</td>
              </tr>
              </tbody>
            </table>
            <p v-if="statsData.top_performers.students.length === 0" class="text-gray-500 text-center py-8">No student
              data available</p>
          </div>
        </Card>

        <!-- Recent Activity -->
        <Card class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-4">Recent Lesson Updates</h3>
          <div class="space-y-4">
            <div
                v-for="lesson in statsData.recent_activity.lessons"
                :key="lesson.created_at"
                class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
            >
              <div>
                <h4 class="font-medium text-gray-900">{{ lesson.lesson }}</h4>
                <p class="text-sm text-gray-600">{{ lesson.subject }} - Class {{ lesson.class }} - {{ lesson.day }}</p>
                <p class="text-xs text-gray-500">by {{ lesson.teacher }}</p>
              </div>
              <div class="text-right">
                <p class="text-sm text-gray-500">{{ formatDate(lesson.created_at) }}</p>
              </div>
            </div>
            <p v-if="statsData.recent_activity.lessons.length === 0" class="text-gray-500 text-center py-8">No recent
              lessons</p>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue'
import {useRouter} from 'vue-router'
import axios from '@/plugins/axios.js'
import {
  Users, GraduationCap, Heart, Building, RefreshCw,
  Loader, AlertCircle, CheckCircle, BookOpen, Target
} from 'lucide-vue-next'
import {Card} from '@/components/ui/card/index.js'
import {Button} from '@/components/ui/button/index.js'
import {BarChart} from '@/components/ui/chart-bar/index.ts'
import {DonutChart} from '@/components/ui/chart-donut/index.ts'
import {AreaChart} from '@/components/ui/chart-area/index.ts'
import TeacherNavbar from "@/components/app/TeacherNavbar.vue";

const router = useRouter()
const isLoading = ref(false)
const error = ref(null)
const statsData = ref(null)
const lastUpdated = ref('')

// Check if user is actually a principal
onMounted(() => {
  const userType = localStorage.getItem('user_type')
  if (userType !== 'principal') {
    router.push('/teacher/dashboard')
    return
  }

  fetchStats()
})

const fetchStats = async () => {
  isLoading.value = true
  error.value = null

  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      router.push('/teacher/login')
      return
    }

    const response = await axios.get('/api/organization/stats', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    statsData.value = response.data
    lastUpdated.value = new Date().toLocaleTimeString()
  } catch (err) {
    console.error('Failed to fetch stats:', err)
    error.value = err.response?.data?.error || 'Failed to load statistics'

    if (err.response?.status === 401 || err.response?.status === 403) {
      localStorage.clear()
      router.push('/teacher/login')
    }
  } finally {
    isLoading.value = false
  }
}

const refreshData = () => {
  fetchStats()
}

// Computed properties for chart data
const classChartData = computed(() => {
  if (!statsData.value?.demographics?.class_distribution) return []
  return statsData.value.demographics.class_distribution.map(item => ({
    class: `Class ${item.class}`,
    student_count: item.student_count
  }))
})

const skillsChartData = computed(() => {
  if (!statsData.value?.popular_content?.skills) return []
  return statsData.value.popular_content.skills.slice(0, 8) // Top 8 skills
})

const habitCategoriesData = computed(() => {
  if (!statsData.value?.popular_content?.habit_categories) return []
  return statsData.value.popular_content.habit_categories
})

const genderChartData = computed(() => {
  if (!statsData.value?.demographics?.gender_distribution) return []
  return statsData.value.demographics.gender_distribution
})

const habitTrendsData = computed(() => {
  if (!statsData.value?.trends?.habit_completions_7_days) return []
  return statsData.value.trends.habit_completions_7_days.map(item => ({
    date: new Date(item.date).toLocaleDateString('en-US', {month: 'short', day: 'numeric'}),
    completions: item.completions
  })).reverse() // Show oldest to newest
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>
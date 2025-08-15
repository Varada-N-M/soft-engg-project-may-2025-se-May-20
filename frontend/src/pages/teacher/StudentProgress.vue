<template>
    <TeacherNavbar/>
  <div class="student-progress-page">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center space-x-4 mb-4">
        <button 
          @click="goBack" 
          class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div>
          <h1 class="text-2xl font-bold text-gray-800">Student Progress</h1>
          <p class="text-gray-600">Detailed progress tracking and analytics</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        <span class="text-red-800">{{ error }}</span>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else-if="studentData">
      <!-- Progress Summary -->
      <ProgressSummary 
        :summary="progressSummary"
        :student-name="`${studentData.student.first_name} ${studentData.student.last_name}`"
        class="mb-6"
      />

      <!-- Tabs -->
      <div class="mb-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              @click="activeTab = tab.id"
              class="py-2 px-1 border-b-2 font-medium text-sm transition-colors"
              :class="{
                'border-blue-500 text-blue-600': activeTab === tab.id,
                'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300': activeTab !== tab.id
              }"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <SkillProgressCard :skills-by-type="studentData.skills_by_type || {}" />
          <BadgeGallery :badges="studentData.badges || []" />
        </div>

        <!-- Skills Tab -->
        <div v-else-if="activeTab === 'skills'">
          <SkillProgressCard 
            :skills-by-type="studentData.skills_by_type || {}" 
            class="mb-6"
          />
          
          <!-- Detailed Skills List -->
          <div class="bg-white rounded-lg border border-gray-200 p-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">All Skills</h3>
            <div v-if="!studentData.skills_by_type || Object.keys(studentData.skills_by_type).length === 0" class="text-center py-8">
              <p class="text-gray-500">No skills data available</p>
            </div>
            <div v-else class="space-y-6">
              <div v-for="(skills, type) in studentData.skills_by_type" :key="type">
                <h4 class="font-medium text-gray-700 capitalize mb-3">{{ type }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  <div 
                    v-for="skill in skills" 
                    :key="skill.skill_id"
                    class="skill-item"
                    :class="{
                      'bg-green-50 border-green-200': skill.is_completed,
                      'bg-gray-50 border-gray-200': !skill.is_completed
                    }"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="text-lg">
                        {{ skill.is_completed ? '✅' : '⭕' }}
                      </div>
                      <div class="flex-1">
                        <div class="font-medium text-sm">{{ skill.skill_name }}</div>
                        <div class="text-xs text-gray-500">+{{ skill.skill_xp }} XP</div>
                        <div v-if="skill.completion_date" class="text-xs text-gray-400">
                          Completed: {{ formatDate(skill.completion_date) }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Habits Tab -->
        <div v-else-if="activeTab === 'habits'">
          <HabitCalendar :habits="studentData.habits || []" />
        </div>

        <!-- Badges Tab -->
        <div v-else-if="activeTab === 'badges'">
          <BadgeGallery :badges="studentData.badges || []" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/plugins/axios.ts'
import ProgressSummary from '@/components/progress/ProgressSummary.vue'
import SkillProgressCard from '@/components/progress/SkillProgressCard.vue'
import BadgeGallery from '@/components/progress/BadgeGallery.vue'
import HabitCalendar from '@/components/progress/HabitCalendar.vue'
import TeacherNavbar from "@/components/app/TeacherNavbar.vue";

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const studentData = ref(null)
const activeTab = ref('overview')

const tabs = [
  { id: 'overview', label: 'Overview' },
  { id: 'skills', label: 'Skills' },
  { id: 'habits', label: 'Habits' },
  { id: 'badges', label: 'Badges' }
]

const progressSummary = computed(() => {
  if (!studentData.value) return {}
  
  return {
    xp_points: studentData.value.student.xp_points,
    streak: studentData.value.student.streak,
    total_skills: studentData.value.total_skills,
    completed_skills: studentData.value.completed_skills,
    total_badges: studentData.value.total_badges
  }
})

const fetchStudentProgress = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const studentId = route.params.studentId
    
    // Fetch main progress data
    const progressResponse = await api.get(`/api/teacher/students/${studentId}/progress`)
    
    // Fetch detailed skills data
    const skillsResponse = await api.get(`/api/teacher/students/${studentId}/skills`)
    
    // Fetch habits data
    const habitsResponse = await api.get(`/api/teacher/students/${studentId}/habits`)
    
    // Fetch badges data
    const badgesResponse = await api.get(`/api/teacher/students/${studentId}/badges`)
    
    studentData.value = {
      ...progressResponse.data,
      skills_by_type: skillsResponse.data.skills_by_type,
      habits: habitsResponse.data.habits,
      badges: badgesResponse.data.badges
    }
    
  } catch (err) {
    console.error('Error fetching student progress:', err)
    error.value = err.response?.data?.error || 'Failed to load student progress data'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/teacher/students')
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchStudentProgress()
})
</script>

<style scoped>
@reference '@/css/index.css';

.student-progress-page {
  @apply p-6 min-h-screen bg-gray-50;
}

.skill-item {
  @apply p-3 border rounded-lg transition-colors;
}

.tab-content {
  @apply min-h-96;
}
</style>
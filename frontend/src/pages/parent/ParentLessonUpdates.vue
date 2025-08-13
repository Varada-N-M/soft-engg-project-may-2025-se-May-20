<template>
  <div class="min-h-screen bg-gray-100 page-font">
    <!-- Parent Navbar -->
    <ParentNavbar page-title="Lesson Updates" />

    <!-- Main Content -->
    <div>

      <!-- Page Content -->
      <div class="p-6 ">
        <!-- Header with Back Button -->
        <div class="bg-white rounded-[20px] p-6 mb-6 shadow">
          <div class="flex items-center gap-4 mb-4">
            <router-link 
              to="/parent/home"
              class="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
              Back to Dashboard
            </router-link>
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Lesson Updates from Teachers</h1>
          <p class="text-gray-600">Stay updated with your children's latest learning progress and lesson activities.</p>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="bg-white rounded-[20px] p-8 shadow text-center">
          <div class="flex items-center justify-center">
            <svg class="animate-spin -ml-1 mr-3 h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-lg text-gray-600">Loading lesson updates...</span>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-white rounded-[20px] p-8 shadow">
          <div class="text-center">
            <svg class="mx-auto h-12 w-12 text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L5.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
            </svg>
            <h3 class="text-lg font-semibold text-gray-800 mb-2">Error Loading Lesson Updates</h3>
            <p class="text-gray-600 mb-4">{{ error }}</p>
            <button 
              @click="loadLessonUpdates" 
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>

        <!-- No Data State -->
        <div v-else-if="lessonUpdates.length === 0" class="bg-white rounded-[20px] p-8 shadow text-center">
          <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
          <h3 class="text-xl font-semibold text-gray-800 mb-2">No Lesson Updates Available</h3>
          <p class="text-gray-600 mb-6">There are currently no lesson updates from your children's teachers.</p>
          <router-link 
            to="/parent/children" 
            class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            View My Children
          </router-link>
        </div>

        <!-- Lesson Updates by Child -->
        <div v-else class="space-y-6">
          <div v-for="child in lessonUpdates" :key="child.child_id" class="bg-white rounded-[20px] shadow">
            <!-- Child Header -->
            <div class="bg-gradient-to-r from-green-500 to-teal-600 text-white p-6 rounded-t-[20px]">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-2xl font-bold">{{ child.child_name }}</h2>
                  <p class="text-green-100">Class {{ child.class_level }} • {{ child.school_name }}</p>
                </div>
                <div class="flex items-center space-x-4">
                  <div class="text-center">
                    <div class="text-xl font-bold">{{ child.xp_points || 0 }}</div>
                    <div class="text-xs text-green-100">XP Points</div>
                  </div>
                  <div class="text-center">
                    <div class="text-xl font-bold">{{ child.streak || 0 }}</div>
                    <div class="text-xs text-green-100">Day Streak</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Lessons -->
            <div class="p-6">
              <h3 class="text-lg font-semibold text-gray-800 mb-4">Recent Lesson Updates</h3>
              
              <div v-if="child.recent_lessons && child.recent_lessons.length > 0" class="space-y-4">
                <div 
                  v-for="lesson in child.recent_lessons" 
                  :key="lesson.id" 
                  class="border border-gray-200 rounded-[15px] p-4 hover:shadow-md transition-shadow"
                >
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-center gap-3">
                      <div :class="getSubjectColor(lesson.subject)" class="p-2 rounded-lg">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getSubjectIcon(lesson.subject)"></path>
                        </svg>
                      </div>
                      <div>
                        <h4 class="font-semibold text-gray-800">{{ lesson.lesson }}</h4>
                        <p class="text-sm text-gray-600">{{ lesson.subject }} • {{ lesson.day }}</p>
                      </div>
                    </div>
                    <div class="text-right">
                      <p class="text-xs text-gray-500 mb-1">by {{ lesson.teacher_name }}</p>
                      <p class="text-xs text-gray-400">{{ formatDate(lesson.created_at) }}</p>
                    </div>
                  </div>

                  <div class="mb-3">
                    <p class="text-sm text-gray-700">{{ lesson.activity }}</p>
                  </div>
                </div>
              </div>

              <div v-else class="text-center py-8 text-gray-500">
                <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
                <p>No recent lesson updates for {{ child.child_name }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Refresh Button -->
        <div class="mt-8 text-center">
          <button 
            @click="loadLessonUpdates" 
            class="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            Refresh Updates
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ParentNavbar from "@/components/partials/ParentNavbar.vue"
import api from '@/plugins/axios.ts'

// Reactive data
const lessonUpdates = ref([])
const isLoading = ref(false)
const error = ref(null)

// Load lesson updates
const loadLessonUpdates = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await api.get('/api/parent/children/lesson-updates')
    lessonUpdates.value = response.data.children_with_lessons || []
  } catch (err) {
    console.error('Error fetching lesson updates:', err)
    error.value = 'Failed to load lesson updates'
  } finally {
    isLoading.value = false
  }
}

const getSubjectColor = (subject) => {
  const colors = {
    'Math': 'bg-blue-500',
    'Mathematics': 'bg-blue-500',
    'Science': 'bg-green-500',
    'Reading': 'bg-purple-500',
    'English': 'bg-purple-500',
    'Language Arts': 'bg-pink-500',
    'History': 'bg-orange-500',
    'Social Studies': 'bg-orange-500',
    'Art': 'bg-red-500',
    'Computers': 'bg-indigo-500'
  }
  return colors[subject] || 'bg-gray-500'
}

const getSubjectIcon = (subject) => {
  const icons = {
    'Math': 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    'Mathematics': 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    'Science': 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547A8.014 8.014 0 004 21h16a8.014 8.014 0 00-.244-5.572zM8 3a5 5 0 015 5v5H8V8a5 5 0 015-5z',
    'Reading': 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    'English': 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    'Language Arts': 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z',
    'History': 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
    'Social Studies': 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
    'Art': 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM7 3H5a2 2 0 00-2 2v12a4 4 0 004 4h2a2 2 0 002-2V5a2 2 0 00-2-2z',
    'Computers': 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z'
  }
  return icons[subject] || 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Initialize data on component mount
onMounted(() => {
  loadLessonUpdates()
})
</script>

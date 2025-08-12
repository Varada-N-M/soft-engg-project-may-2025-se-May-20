<template>
  <div class="min-h-screen bg-gray-100 flex page-font">
    <!-- Parent Navbar -->
    <ParentNavbar :page-title="getPageTitle()" />

    <!-- Main Content -->
    <div class="flex-1 lg:ml-64">
      <!-- Mobile Header Spacing -->
      <div class="h-16 lg:h-0"></div>

      <!-- Page Content -->
      <div class="p-6">
        <!-- Dashboard Page -->
        <div v-if="currentPage === 'dashboard'">
          <!-- Header -->
          <div class="bg-white rounded-[20px] p-6 mb-6 shadow">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">
              <span v-if="linkedChildren.length === 1">{{ linkedChildren[0].first_name }}'s Progress Report</span>
              <span v-else-if="linkedChildren.length > 1">Children's Progress Report</span>
              <span v-else>Parent Dashboard</span>
            </h1>
            <p class="text-gray-600">
              <span v-if="linkedChildren.length === 1">{{ linkedChildren.length }} child linked</span>
              <span v-else-if="linkedChildren.length > 1">{{ linkedChildren.length }} children linked</span>
              <span v-else>No children linked yet</span>
              • Stay updated with their learning journey
            </p>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-blue-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">Recent</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">{{ getTotalLessonUpdates() }}</h3>
              <p class="text-gray-600 text-sm">Recent Lessons</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-yellow-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded-full">Combined</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">{{ getTotalXPPoints() }}</h3>
              <p class="text-gray-600 text-sm">Total XP Points</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-purple-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">Linked</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">{{ linkedChildren.length }}</h3>
              <p class="text-gray-600 text-sm">Children</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-orange-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded-full">Best</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">{{ getHighestStreak() }}</h3>
              <p class="text-gray-600 text-sm">Day Streak</p>
            </div>
          </div>

          <!-- Children Overview -->
          <div class="bg-white rounded-[20px] p-6 shadow mb-6" v-if="linkedChildren.length > 0">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Your Children</h2>
            <div class="space-y-3">
              <div v-for="child in linkedChildren" :key="child.child_id" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-lg">
                    {{ child.first_name?.[0]?.toUpperCase() }}
                  </div>
                  <div>
                    <h4 class="font-semibold text-gray-800">{{ child.first_name }} {{ child.last_name }}</h4>
                    <p class="text-sm text-gray-600">{{ child.school_name }} • Class {{ child.class }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <div class="flex items-center space-x-4">
                    <div class="text-center">
                      <div class="text-lg font-bold text-yellow-600">{{ child.xp_points || 0 }}</div>
                      <div class="text-xs text-gray-500">XP Points</div>
                    </div>
                    <div class="text-center">
                      <div class="text-lg font-bold text-orange-600">{{ child.streak || 0 }}</div>
                      <div class="text-xs text-gray-500">Day Streak</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-[20px] p-6 shadow mb-6">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Recent Lesson Updates</h2>
            
            <!-- Loading state for lesson updates -->
            <div v-if="isLoading" class="text-center py-8">
              <svg class="animate-spin h-8 w-8 text-blue-600 mx-auto mb-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p class="text-gray-600">Loading lesson updates...</p>
            </div>
            
            <!-- Show recent lesson updates preview -->
            <div v-else-if="lessonUpdates.length > 0" class="space-y-3">
              <div v-for="child in lessonUpdates.slice(0, 2)" :key="child.child_id" class="border-l-4 border-blue-500 pl-4">
                <h4 class="font-semibold text-gray-800">{{ child.child_name }}</h4>
                <p class="text-sm text-gray-600">{{ child.recent_lessons.length }} recent lessons</p>
                <div v-if="child.recent_lessons.length > 0" class="mt-1">
                  <p class="text-xs text-gray-500">Latest: {{ child.recent_lessons[0].lesson }} - {{ child.recent_lessons[0].subject }}</p>
                </div>
              </div>
              
              <router-link 
                to="/parent/lesson-updates"
                class="block w-full mt-4 bg-blue-100 hover:bg-blue-200 text-blue-700 font-medium py-2 px-4 rounded-lg transition-colors text-center"
              >
                View All Lesson Updates →
              </router-link>
            </div>
            
            <!-- No updates state -->
            <div v-else class="text-center py-8 text-gray-500">
              <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
              <p class="mb-4">No lesson updates available</p>
              <router-link 
                to="/parent/children" 
                class="text-blue-600 hover:text-blue-800 underline"
              >
                Check your linked children →
              </router-link>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <router-link 
              to="/parent/lesson-updates"
              class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-8 rounded-[20px] shadow-lg transition-colors flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
              </svg>
              View Lesson Updates
            </router-link>
            <router-link 
              to="/parent/children"
              class="bg-purple-500 hover:bg-purple-600 text-white font-medium py-3 px-8 rounded-[20px] shadow-lg transition-colors flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
              Manage Children
            </router-link>
          </div>
        </div>


        <!-- SafeSteps Page -->
        <div v-else-if="currentPage === 'safesteps'" class="bg-white rounded-[20px] p-6 shadow">
          <div class="text-center py-12">
            <!-- <div class="bg-green-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5-6a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div> -->
            <h2 class="text-2xl font-bold text-gray-800 mb-2">SafeSteps</h2>
            <p class="text-gray-600 mb-4">Monitor Alex's online safety and digital wellness while learning.</p>
            <p class="text-gray-500">coming soon...</p>
          </div>
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
const currentPage = ref('dashboard')
const linkedChildren = ref([])
const lessonUpdates = ref([])
const isLoading = ref(false)
const error = ref(null)

// Methods
const getPageTitle = () => {
  switch (currentPage.value) {
    case 'dashboard':
      return 'Dashboard'
    case 'lessons':
      return 'Lessons'
    case 'lesson-updates':
      return 'Lesson Updates'
    case 'safesteps':
      return 'SafeSteps'
    default:
      return 'Parent Portal'
  }
}


// API Methods
const fetchLinkedChildren = async () => {
  try {
    const response = await api.get('/api/parent/linked-children')
    linkedChildren.value = response.data.linked_children || []
  } catch (err) {
    console.error('Error fetching linked children:', err)
    error.value = 'Failed to load children data'
  }
}

const fetchLessonUpdates = async () => {
  try {
    const response = await api.get('/api/parent/children/lesson-updates')
    lessonUpdates.value = response.data.children_with_lessons || []
  } catch (err) {
    console.error('Error fetching lesson updates:', err)
    error.value = 'Failed to load lesson updates'
  }
}

const loadDashboardData = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    await Promise.all([
      fetchLinkedChildren(),
      fetchLessonUpdates()
    ])
  } catch (err) {
    console.error('Error loading dashboard data:', err)
    error.value = 'Failed to load dashboard data'
  } finally {
    isLoading.value = false
  }
}

// Dashboard stats computed methods
const getTotalLessonUpdates = () => {
  return lessonUpdates.value.reduce((total, child) => {
    return total + (child.recent_lessons ? child.recent_lessons.length : 0)
  }, 0)
}

const getTotalXPPoints = () => {
  return linkedChildren.value.reduce((total, child) => {
    return total + (child.xp_points || 0)
  }, 0)
}

const getHighestStreak = () => {
  if (linkedChildren.value.length === 0) return 0
  return Math.max(...linkedChildren.value.map(child => child.streak || 0))
}



// Initialize data on component mount
onMounted(() => {
  loadDashboardData()
})
</script>



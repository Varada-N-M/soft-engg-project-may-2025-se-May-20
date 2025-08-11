<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <!-- Navbar -->
    <TeacherNavbar />

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-8 shadow-xl border border-white/20">
          <div class="flex flex-col md:flex-row items-center justify-between">
            <div>
              <h2 class="text-3xl font-bold text-gray-800 mb-4">Welcome to Your Dashboard</h2>
              <p class="text-gray-600 text-lg">Manage your classes, track student progress, and create engaging lessons.</p>
            </div>
            <div class="text-8xl">🎓</div>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-blue-600">{{ stats.totalLessons }}</p>
              <p class="text-sm text-gray-600">Total Lessons</p>
            </div>
            <div class="text-4xl">📚</div>
          </div>
        </div>
        
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-green-600">{{ stats.totalStudents }}</p>
              <p class="text-sm text-gray-600">Students</p>
            </div>
            <div class="text-4xl">👥</div>
          </div>
        </div>
        
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-purple-600">{{ stats.uniqueSubjects }}</p>
              <p class="text-sm text-gray-600">Subjects</p>
            </div>
            <div class="text-4xl">📖</div>
          </div>
        </div>
        
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-orange-600">{{ stats.thisWeekLessons }}</p>
              <p class="text-sm text-gray-600">This Week</p>
            </div>
            <div class="text-4xl">📅</div>
          </div>
        </div>
      </div>

      <!-- Navigation Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <!-- Lesson Updates -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer" @click="navigateTo('/teacher/lesson-updates')">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">📝</div>
            <div class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm font-semibold">
              {{ stats.totalLessons }} lessons
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Lesson Updates</h3>
          <p class="text-gray-600 mb-4">Create, edit, and manage your daily lesson updates for students.</p>
          <div class="flex items-center text-blue-600 font-semibold group-hover:text-blue-700">
            <span>Manage Lessons</span>
            <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>

        <!-- Add Students -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer" @click="navigateTo('/teacher/add-student')">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">👥</div>
            <div class="bg-green-100 text-green-600 px-3 py-1 rounded-full text-sm font-semibold">
              {{ stats.totalStudents }} students
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Manage Students</h3>
          <p class="text-gray-600 mb-4">Add new students to your classes and manage your student roster.</p>
          <div class="flex items-center text-green-600 font-semibold group-hover:text-green-700">
            <span>Add Students</span>
            <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>

        <!-- Survey Reports -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer" @click="navigateTo('/teacher/survey-report')">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">📊</div>
            <div class="bg-purple-100 text-purple-600 px-3 py-1 rounded-full text-sm font-semibold">
              Reports
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Survey Reports</h3>
          <p class="text-gray-600 mb-4">View and analyze student survey responses and feedback.</p>
          <div class="flex items-center text-purple-600 font-semibold group-hover:text-purple-700">
            <span>View Reports</span>
            <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>

        <!-- Class Performance -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer opacity-60">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">📈</div>
            <div class="bg-orange-100 text-orange-600 px-3 py-1 rounded-full text-sm font-semibold">
              Coming Soon
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Class Performance</h3>
          <p class="text-gray-600 mb-4">Track student progress and class performance metrics.</p>
          <div class="flex items-center text-orange-600 font-semibold">
            <span>Coming Soon</span>
          </div>
        </div>

        <!-- Teaching Resources -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer opacity-60">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">📚</div>
            <div class="bg-red-100 text-red-600 px-3 py-1 rounded-full text-sm font-semibold">
              Coming Soon
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Teaching Resources</h3>
          <p class="text-gray-600 mb-4">Access curriculum guides, teaching materials, and resources.</p>
          <div class="flex items-center text-red-600 font-semibold">
            <span>Coming Soon</span>
          </div>
        </div>

        <!-- Communication Hub -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer opacity-60">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">💬</div>
            <div class="bg-teal-100 text-teal-600 px-3 py-1 rounded-full text-sm font-semibold">
              Coming Soon
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Communication Hub</h3>
          <p class="text-gray-600 mb-4">Message parents and collaborate with other teachers.</p>
          <div class="flex items-center text-teal-600 font-semibold">
            <span>Coming Soon</span>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div v-if="recentLessons.length > 0" class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
        <h3 class="text-xl font-bold text-gray-800 mb-6">Recent Lesson Updates</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="lesson in recentLessons.slice(0, 6)"
            :key="lesson.id"
            class="bg-gray-50 rounded-2xl p-4 border border-gray-200"
          >
            <div class="flex items-center mb-2 flex-wrap gap-2">
              <span class="inline-block px-2 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-semibold">{{ lesson.subject }}</span>
              <span class="inline-block px-2 py-1 rounded-full bg-purple-100 text-purple-700 text-xs font-semibold">Class {{ lesson.class }}</span>
            </div>
            <h4 class="font-bold text-gray-800 text-sm mb-2">{{ lesson.lesson }}</h4>
            <p class="text-xs text-gray-600">{{ lesson.day }}</p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="bg-white/90 backdrop-blur-sm rounded-3xl p-12 shadow-xl border border-white/20 text-center">
        <div class="text-6xl mb-4">🎯</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Ready to get started?</h3>
        <p class="text-gray-600 mb-6">Create your first lesson update to begin engaging with your students.</p>
        <button
          @click="navigateTo('/teacher/lesson-updates')"
          class="px-6 py-3 bg-gradient-to-r from-blue-500 to-green-500 text-white rounded-lg hover:from-blue-600 hover:to-green-600 transition-colors font-semibold"
        >
          Create Lesson Update
        </button>
      </div>
    </main>

    <!-- Floating decorative elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div class="absolute top-20 left-10 w-8 h-8 bg-blue-200 rounded-full opacity-20 animate-bounce"></div>
      <div class="absolute top-40 right-20 w-6 h-6 bg-purple-200 rounded-full opacity-20 animate-bounce" style="animation-delay: 0.5s"></div>
      <div class="absolute bottom-32 left-20 w-10 h-10 bg-green-200 rounded-full opacity-20 animate-bounce" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 right-10 w-7 h-7 bg-orange-200 rounded-full opacity-20 animate-bounce" style="animation-delay: 1.5s"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import TeacherNavbar from '@/components/app/TeacherNavbar.vue'

const router = useRouter()
const teacherName = ref('Teacher')
const lessons = ref([])
const students = ref([])
const loading = ref(false)
const error = ref('')

const goHome = () => {
  router.push('/teacher/dashboard')
}

const navigateTo = (path: string) => {
  router.push(path)
}

const logout = () => {
  // Clear any stored tokens/session data
  localStorage.removeItem('token')
  sessionStorage.clear()
  router.push('/')
}

// Computed stats
const stats = computed(() => ({
  totalLessons: lessons.value.length,
  totalStudents: students.value.length,
  uniqueSubjects: [...new Set(lessons.value.map((l: any) => l.subject))].length,
  thisWeekLessons: lessons.value.filter((l: any) => {
    // Simple week filter - could be enhanced with proper date logic
    return true // For now, show all lessons
  }).length
}))

const recentLessons = computed(() => {
  return lessons.value
    .sort((a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 6)
})

// Fetch teacher data
const fetchTeacherData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Fetch lessons

    const token = localStorage.getItem('access_token') 
    

    const lessonsResponse = await axios.get('http://localhost:5000/api/teacher/lesson-updates', {
    headers: {
    Authorization: `Bearer ${token}`
  }
})
    console.log('Raw API response:', lessonsResponse.data)
    lessons.value = lessonsResponse.data.lessons || []
    

    
    // Set teacher name from localStorage or token if available
    const storedName = localStorage.getItem('teacherName')
    if (storedName) {
      teacherName.value = storedName
    }
    
  } catch (err) {
    console.error('Error fetching teacher data:', err)
    error.value = 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
}

// Load data on component mount
onMounted(() => {
  fetchTeacherData()
})
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
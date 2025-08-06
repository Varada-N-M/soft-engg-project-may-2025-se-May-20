<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300">
    <!-- Header -->
    <header class="bg-white/90 backdrop-blur-sm shadow-lg sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <!-- Back Arrow -->
            <button
              @click="goHome"
              class="p-2 text-gray-600 hover:text-gray-800 transition-colors rounded-lg hover:bg-gray-100"
            >
              <ArrowLeftIcon class="w-6 h-6" />
            </button>
            <h1 class="text-xl font-bold text-gray-800 font-fancy">📚 Lesson Updates</h1>
          </div>
          <div class="flex items-center space-x-6">
            <div class="text-center">
              <p class="text-2xl font-bold text-blue-600">{{ lessons.length }}</p>
              <p class="text-xs text-gray-600">Updates</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-green-600">{{ uniqueTeachers.length }}</p>
              <p class="text-xs text-gray-600">Teachers</p>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Overview Section -->
      <div class="mb-8" v-if="!isLoading && !errorMessage">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
          <div class="flex flex-col md:flex-row items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-bold text-gray-800 mb-2">Recent Lesson Updates</h2>
              <p class="text-gray-600" v-if="lessons.length > 0">{{ lessons.length }} lesson updates from your teachers</p>
              <p class="text-gray-600" v-else>No lesson updates available</p>
            </div>
            <div class="text-6xl animate-bounce">📚</div>
          </div>
          
          <!-- Teachers and Subjects Info -->
          <div v-if="lessons.length > 0">
            <div class="mb-4">
              <h3 class="text-sm font-semibold text-gray-700 mb-2">Teachers:</h3>
              <div class="flex flex-wrap gap-2">
                <span v-for="teacher in uniqueTeachers" :key="teacher" class="inline-flex items-center px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-medium">
                  👨‍🏫 {{ teacher }}
                </span>
              </div>
            </div>
            
            <div>
              <h3 class="text-sm font-semibold text-gray-700 mb-2">Subjects Covered:</h3>
              <div class="flex flex-wrap gap-2">
                <span v-for="subject in uniqueSubjects" :key="subject" class="inline-flex items-center px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-medium">
                  {{ subject }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-16">
        <div class="text-6xl mb-4 animate-spin">🔄</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Loading lesson updates...</h3>
        <p class="text-gray-600">Please wait while we fetch your lesson updates</p>
      </div>

      <!-- Error State -->
      <div v-else-if="errorMessage" class="text-center py-16">
        <div class="text-6xl mb-4">❌</div>
        <h3 class="text-xl font-bold text-red-600 mb-2">Oops! Something went wrong</h3>
        <p class="text-gray-600 mb-6">{{ errorMessage }}</p>
        <button
          @click="fetchLessonUpdates()"
          class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-xl hover:from-blue-600 hover:to-purple-600 transition-all duration-200 shadow-lg"
        >
          🔄 Try Again
        </button>
      </div>

      <!-- Lessons Grid -->
      <div v-else-if="lessons.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="lesson in lessons"
          :key="lesson.lesson_id"
          class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 relative overflow-hidden"
        >
          <!-- Decorative Icon -->
          <div class="absolute -top-4 -right-4 text-5xl opacity-20 select-none pointer-events-none">
            <span v-if="lesson.subject === 'Math'">🧮</span>
            <span v-else-if="lesson.subject === 'English'">📖</span>
            <span v-else-if="lesson.subject === 'Science'">🔬</span>
            <span v-else-if="lesson.subject === 'Social Studies'">🌍</span>
            <span v-else-if="lesson.subject === 'Technology'">💻</span>
            <span v-else>📚</span>
          </div>
          <div class="relative z-10">
            <!-- Header with day and subject -->
            <div class="flex items-center mb-3">
              <span class="inline-block px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-semibold mr-2">{{ lesson.day }}</span>
              <span class="inline-block px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-semibold">{{ lesson.subject }}</span>
            </div>
            
            <!-- Lesson title -->
            <h3 class="font-bold text-gray-800 mb-2 text-lg leading-tight">{{ lesson.lesson }}</h3>
            
            <!-- Summary -->
            <p class="text-sm text-gray-600 mb-4 leading-relaxed">{{ lesson.summary || 'No summary provided' }}</p>
            
            <!-- Teacher and date info -->
            <div class="border-t border-gray-200 pt-3 mt-4">
              <div class="flex items-center justify-between text-xs text-gray-500">
                <span v-if="lesson.teacher_name" class="flex items-center">
                  👨‍🏫 {{ lesson.teacher_name }}
                </span>
                <span v-else class="flex items-center">
                  👨‍🏫 Teacher
                </span>
                <span>{{ formatDate(lesson.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="text-6xl mb-4">📚</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">No lesson updates yet</h3>
        <p class="text-gray-600 mb-4">Your teachers haven't posted any lesson updates yet.</p>
        <p class="text-sm text-gray-500">Check back later for updates from your teachers!</p>
      </div>
    </main>

    <!-- Floating decorative elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div class="absolute top-20 left-10 w-8 h-8 bg-yellow-300 rounded-full opacity-20 animate-bounce"></div>
      <div class="absolute top-40 right-20 w-6 h-6 bg-pink-300 rounded-full opacity-20 animate-bounce" style="animation-delay: 0.5s"></div>
      <div class="absolute bottom-32 left-20 w-10 h-10 bg-orange-300 rounded-full opacity-20 animate-bounce" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 right-10 w-7 h-7 bg-cyan-300 rounded-full opacity-20 animate-bounce" style="animation-delay: 1.5s"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from 'lucide-vue-next'
import api from '../../plugins/axios'

const router = useRouter()
const goHome = () => {
  router.push('/student/home')
}

// Reactive data
const lessons = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

// API function to fetch lesson updates
const fetchLessonUpdates = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await api.get('/api/child/lesson-updates')
    
    if (response.data.lesson_updates) {
      // Transform backend data to match frontend structure
      lessons.value = response.data.lesson_updates.map(update => ({
        lesson_id: update.lesson_id,
        lesson: update.lesson,
        summary: update.summary,
        created_at: update.created_at,
        teacher_name: update.teacher_name,
        // Extract day from created_at date
        day: getDayFromDate(update.created_at),
        // Extract subject from lesson name (simple heuristic)
        subject: getSubjectFromLesson(update.lesson)
      }))
    } else {
      lessons.value = []
    }
  } catch (error) {
    console.error('Error fetching lesson updates:', error)
    if (error.response && error.response.data && error.response.data.message) {
      // Handle case where no teachers are linked to child
      errorMessage.value = error.response.data.message
    } else {
      errorMessage.value = 'Failed to load lesson updates. Please try again.'
    }
    lessons.value = []
  } finally {
    isLoading.value = false
  }
}

// Helper function to get day from date string
const getDayFromDate = (dateString) => {
  try {
    const date = new Date(dateString)
    const options = { weekday: 'long' }
    return date.toLocaleDateString('en-US', options)
  } catch (error) {
    return 'Unknown'
  }
}

// Helper function to determine subject from lesson name
const getSubjectFromLesson = (lessonName) => {
  const lesson = lessonName.toLowerCase()
  if (lesson.includes('math') || lesson.includes('fraction') || lesson.includes('number') || lesson.includes('arithmetic')) {
    return 'Math'
  } else if (lesson.includes('english') || lesson.includes('grammar') || lesson.includes('writing') || lesson.includes('reading')) {
    return 'English'
  } else if (lesson.includes('science') || lesson.includes('experiment') || lesson.includes('biology') || lesson.includes('chemistry') || lesson.includes('physics')) {
    return 'Science'
  } else if (lesson.includes('social') || lesson.includes('history') || lesson.includes('geography') || lesson.includes('community')) {
    return 'Social Studies'
  } else if (lesson.includes('computer') || lesson.includes('technology') || lesson.includes('coding')) {
    return 'Technology'
  } else {
    return 'General'
  }
}

// Helper function to format date
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(today.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return 'Today'
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday'
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }
  } catch (error) {
    return 'Unknown'
  }
}

// Computed properties
const uniqueSubjects = computed(() => {
  const set = new Set(lessons.value.map(l => l.subject))
  return Array.from(set)
})

const uniqueTeachers = computed(() => {
  const set = new Set(lessons.value.filter(l => l.teacher_name).map(l => l.teacher_name))
  return Array.from(set)
})

// Mount lifecycle
onMounted(async () => {
  await fetchLessonUpdates()
})
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>

<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <!-- Header -->
    <header class="max-w-4xl mx-auto mb-8 text-center">
      <router-link to="/student/home" class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">Lesson Updates 📚</h1>
      <p class="text-lg text-gray-600 font-medium">
        You have <span class="text-blue-500 font-bold">{{ lessons.length }}</span> updates from
        <span class="text-green-500 font-bold">{{ uniqueTeachers.length }}</span> teachers.
      </p>
    </header>

    <main class="max-w-6xl mx-auto">
      <!-- Loading State -->
      <div v-if="isLoading" class="text-center py-20">
        <p class="text-lg text-gray-600">Loading lesson updates...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="errorMessage" class="text-center py-20">
        <p class="text-lg text-red-500 font-medium">{{ errorMessage }}</p>
        <button
          @click="fetchLessonUpdates()"
          class="mt-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-102 transition-all duration-200 flex items-center mx-auto"
        >
          🔄 Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="lessons.length === 0" class="text-center py-20">
        <div class="text-6xl mb-4">✨</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">No Lesson Updates Yet!</h2>
        <p class="text-gray-600">Your teachers haven’t posted any updates. Check back soon!</p>
      </div>

      <div v-if="!isLoading && !errorMessage && lessons.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="lesson in lessons"
          :key="lesson.lesson_id"
          class="bg-white rounded-3xl p-6 shadow-lg border-2 border-gray-200 transition-transform hover:scale-102 cursor-default"
        >
          <!-- Header -->
          <div class="flex items-center mb-4">
            <div class="text-3xl mr-3">{{ getEmojiForSubject(lesson.subject) }}</div>
            <div>
              <h3 class="font-bold text-gray-800 text-lg">{{ lesson.lesson }}</h3>
              <p class="text-sm text-gray-600">{{ lesson.teacher_name || 'Teacher' }}</p>
            </div>
          </div>

          <!-- Summary -->
          <p class="text-gray-700 mb-4 text-sm leading-relaxed">{{ lesson.summary || 'No summary provided.' }}</p>

          <!-- Footer -->
          <div class="flex justify-between items-center text-xs">
            <div class="inline-flex items-center bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full font-semibold">
              {{ lesson.day }}
            </div>
            <div class="text-gray-500">
              {{ formatDate(lesson.created_at) }}
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from 'lucide-vue-next'
import api from '../../plugins/axios'

const router = useRouter()
const lessons = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

// Navigate home
const goHome = () => {
  router.push('/student/home')
}

// Fetch lesson updates
const fetchLessonUpdates = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await api.get('/api/child/lesson-updates')
    
    if (response.data.lesson_updates) {
      lessons.value = response.data.lesson_updates.map(update => ({
        lesson_id: update.lesson_id,
        lesson: update.lesson,
        summary: update.summary,
        created_at: update.created_at,
        teacher_name: update.teacher_name,
        day: getDayFromDate(update.created_at),
        subject: getSubjectFromLesson(update.lesson)
      }))
    } else {
      lessons.value = []
    }
  } catch (error) {
    console.error('Error fetching lesson updates:', error)
    errorMessage.value = error.response?.data?.message || 'Failed to load lesson updates. Please try again.'
    lessons.value = []
  } finally {
    isLoading.value = false
  }
}

// Helpers
const getDayFromDate = (dateString) => {
  try {
    const date = new Date(dateString)
    const options = { weekday: 'long' }
    return date.toLocaleDateString('en-US', options)
  } catch (error) {
    return 'Unknown'
  }
}

const getSubjectFromLesson = (lessonName) => {
  const lesson = lessonName.toLowerCase()
  if (lesson.includes('math') || lesson.includes('fraction') || lesson.includes('number')) return 'Math'
  if (lesson.includes('english') || lesson.includes('grammar') || lesson.includes('reading')) return 'English'
  if (lesson.includes('science') || lesson.includes('biology') || lesson.includes('chemistry')) return 'Science'
  if (lesson.includes('social') || lesson.includes('history') || lesson.includes('geography')) return 'Social Studies'
  if (lesson.includes('computer') || lesson.includes('technology') || lesson.includes('coding')) return 'Technology'
  return 'General'
}

const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(today.getDate() - 1)

    if (date.toDateString() === today.toDateString()) return 'Today'
    if (date.toDateString() === yesterday.toDateString()) return 'Yesterday'
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  } catch (error) {
    return 'Unknown'
  }
}

const getEmojiForSubject = (subject) => {
  switch (subject) {
    case 'Math': return '🧮'
    case 'English': return '📖'
    case 'Science': return '🔬'
    case 'Social Studies': return '🌍'
    case 'Technology': return '💻'
    default: return '📚'
  }
}

// Computed
const uniqueSubjects = computed(() => {
  return Array.from(new Set(lessons.value.map(l => l.subject)))
})

const uniqueTeachers = computed(() => {
  return Array.from(new Set(lessons.value.filter(l => l.teacher_name).map(l => l.teacher_name)))
})

// Lifecycle
onMounted(async () => {
  await fetchLessonUpdates()
})
</script>

<style scoped>
/* No extra styles needed — all utility classes are Tailwind */
</style>
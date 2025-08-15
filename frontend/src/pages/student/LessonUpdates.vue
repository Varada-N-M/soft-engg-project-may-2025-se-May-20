<template>
  <div class="min-h-screen flex font-playfair">
    <aside
      class="w-64 bg-opacity-90 backdrop-blur-sm p-6 fixed left-5 top-3 bottom-3 rounded-[20px] overflow-y-auto z-50 shadow-[0_0_10px_rgba(0,0,0,0.14)] flex flex-col">
      <div class="mb-8">
        <h2 class="text-3xl font-extrabold text-gray-900 font-playfair">My Dashboard</h2>
      </div>
      <nav class="space-y-3">
        <router-link v-for="link in navLinks" :key="link.name" :to="link.path"
          class="flex items-center gap-4 py-2 px-2 rounded-xl text-gray-700 hover:text-yellow-600 transition-colors duration-200 font-medium font-playfair">
          <span class="text-xl">{{ link.icon }}</span> {{ link.name }}
        </router-link>
      </nav>
    </aside>

    <main class="flex-1 ml-64 p-8 overflow-y-auto bg-gray-50">
      <div class="max-w-7xl ml-6">
        <div class="bg-rounded-3xl mb-10">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2">
                My Lesson Updates
              </h1>
              <p class="text-lg text-gray-600 font-medium">
                You have <span class="text-blue-500 font-bold">{{ lessons.length }}</span> updates from
                <span class="text-green-500 font-bold">{{ uniqueTeachers.length }}</span> teachers.
              </p>
            </div>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-20">
          <p class="text-lg text-gray-600">Loading lesson updates...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="errorMessage" class="text-center py-20">
          <p class="text-lg text-red-500 font-medium">{{ errorMessage }}</p>
          <button @click="fetchLessonUpdates()"
            class="mt-4 bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-102 transition-all duration-200 flex items-center mx-auto">
            🔄 Try Again
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="lessons.length === 0" class="text-center py-20">
          <div class="text-6xl mb-4">✨</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">No Lesson Updates Yet!</h2>
          <p class="text-gray-600">Your teachers haven’t posted any updates. Check back soon!</p>
        </div>

        <div v-if="!isLoading && !errorMessage && lessons.length > 0"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="lesson in lessons" :key="lesson.lesson_id"
            class="bg-white rounded-3xl p-6 shadow-lg border-1 border-gray-200 transition-transform hover:scale-102 cursor-default">
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
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/plugins/axios'
import { clearAuthData } from '@/utils/auth';

const router = useRouter()
const lessons = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

const navLinks = ref([
  { name: 'Home', path: '/student/home', icon: '🏠' },
  { name: 'Lesson Updates', path: '/student/lesson-updates', icon: '📚' },
  { name: 'To-do List', path: '/student/todolist', icon: '✔️' },
  { name: 'Habits', path: '/student/habit', icon: '🎯' },
  { name: 'Life Lessons', path: '/student/life-lessons', icon: '📖' },
  { name: 'Journal', path: '/student/journal', icon: '✍️' },
  { name: 'AI Companion', path: '/student/ai-companion', icon: '🤖' },
  { name: 'Badges', path: '/student/badges', icon: '🏅' },
]);

const logout = () => {
  clearAuthData();
  router.push('/');
};

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
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.font-playfair {
  font-family: 'Playfair Display', serif;
}
</style>
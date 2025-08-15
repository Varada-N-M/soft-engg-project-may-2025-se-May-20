<!-- LifeLessonsPage.vue -->
<template>
  <div class="min-h-screen bg-gray-50 p-8 font-inter">
    <!-- Header -->
    <header class="max-w-4xl mx-auto mb-10 text-center">
      <router-link
        to="/student/home"
        class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4 rounded-lg px-3 py-1"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>

      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">Life Lessons 💡</h1>
      <p class="text-lg text-gray-600 font-medium">
        You’ve completed
        <span class="text-green-500 font-bold">{{ completedLessons.length }}</span>
        out of
        <span class="text-blue-500 font-bold">{{ lifeLessons.length }}</span>
        lessons!
      </p>
    </header>

    <main class="max-w-6xl mx-auto">
      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
        <p class="text-gray-600">Loading life lessons...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-20">
        <div class="text-6xl mb-4">⚠️</div>
        <h2 class="text-2xl font-bold text-red-600 mb-2">Error Loading Lessons</h2>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <button
          @click="fetchLifeLessons"
          class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        >
          Try Again
        </button>
      </div>

      <!-- Lessons -->
      <div v-else>
        <!-- To Complete -->
        <section v-if="pendingLessons.length > 0" class="mb-12">
          <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            🚀 Lessons To Complete
            <span class="ml-2 text-sm text-gray-500 font-normal">({{ pendingLessons.length }})</span>
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <LifeLessonCard
              v-for="lesson in pendingLessons"
              :key="lesson.id"
              :lesson="lesson"
              @lesson-completed="markLessonAsComplete"
            />
          </div>
        </section>

        <!-- Completed -->
        <section v-if="completedLessons.length > 0">
          <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            ✅ Completed Lessons
            <span class="ml-2 text-sm text-gray-500 font-normal">({{ completedLessons.length }})</span>
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <LifeLessonCard
              v-for="lesson in completedLessons"
              :key="lesson.id"
              :lesson="lesson"
            />
          </div>
        </section>

        <!-- Empty -->
        <div v-if="lifeLessons.length === 0" class="text-center py-20">
          <div class="text-6xl mb-4">📚</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">No Life Lessons Available Yet</h2>
          <p class="text-gray-600">Check back soon for more inspiring content!</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import LifeLessonCard from './LifeLessonCard.vue'
import api from '@/plugins/axios.ts'

const lifeLessons = ref([])
const loading = ref(false)
const error = ref(null)

const completedLessons = computed(() =>
  lifeLessons.value.filter(lesson => lesson.completed)
)
const pendingLessons = computed(() =>
  lifeLessons.value.filter(lesson => !lesson.completed)
)

const fetchLifeLessons = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await api.get('/api/child/skills')
    const regularSkills = data.skills.filter(skill => skill.skill_type === 'regular')

    lifeLessons.value = regularSkills.map(skill => ({
      id: skill.id,
      title: skill.skill_name,
      video_url: skill.video_url,
      skill_type: skill.skill_type,
      completed: skill.is_learned || false,
      completionDate: skill.completion_date || null
    }))
  } catch (err) {
    console.error('Error fetching life lessons:', err)
    error.value = 'Failed to load life lessons. Please try again.'
  } finally {
    loading.value = false
  }
}

// ✅ Complete a lesson
const markLessonAsComplete = async (lessonId) => {
  try {
    await api.post(`/api/child/skills/${lessonId}/complete`)
    // Update state locally
    const lesson = lifeLessons.value.find(l => l.id === lessonId)
    if (lesson) {
      lesson.completed = true
      lesson.completionDate = new Date().toISOString()
    }
  } catch (err) {
    console.error(`Error completing lesson ${lessonId}:`, err)
    alert('Failed to complete the lesson. Please try again.')
  }
}

onMounted(() => {
  fetchLifeLessons()
})
</script>


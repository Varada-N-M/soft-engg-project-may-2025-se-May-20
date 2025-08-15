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
      <div class="max-w-7xl ml-5">
        <div class="rounded-3xl p-8 mb-8">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2">Life Lessons</h1>
              <p class="text-lg text-gray-600 font-medium">
                You’ve completed
                <span class="text-green-500 font-bold">{{ completedLessons.length }}</span>
                out of
                <span class="text-blue-500 font-bold">{{ lifeLessons.length }}</span>
                lessons!
              </p>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p class="text-gray-600">Loading life lessons...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="text-center py-20">
          <div class="text-6xl mb-4"></div>
          <h2 class="text-2xl font-bold text-red-600 mb-2">Error Loading Lessons</h2>
          <p class="text-gray-600 mb-4">{{ error }}</p>
          <button @click="fetchLifeLessons"
            class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors">
            Try Again
          </button>
        </div>

        <!-- Lessons -->
        <div v-else>
          <!-- To Complete -->
          <section v-if="pendingLessons.length > 0" class="mb-12 ml-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
              Lessons To Complete
              <span class="ml-2 text-sm text-gray-500 font-normal">({{ pendingLessons.length }})</span>
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6">
              <LifeLessonCard v-for="lesson in pendingLessons" :key="lesson.id" :lesson="lesson"
                @lesson-completed="markLessonAsComplete" />
            </div>
          </section>

          <!-- Completed -->
          <section v-if="completedLessons.length > 0" class="ml-6">
            <h2 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
              Completed Lessons
              <span class="ml-2 text-sm text-gray-500 font-normal">({{ completedLessons.length }})</span>
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6">
              <LifeLessonCard v-for="lesson in completedLessons" :key="lesson.id" :lesson="lesson" />
            </div>
          </section>

          <!-- Empty -->
          <div v-if="lifeLessons.length === 0" class="text-center py-20">
            <div class="text-6xl mb-4">📚</div>
            <h2 class="text-2xl font-bold text-gray-800 mb-2">No Life Lessons Available Yet</h2>
            <p class="text-gray-600">Check back soon for more inspiring content!</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import LifeLessonCard from './LifeLessonCard.vue'
import api from '@/plugins/axios.ts'
import { clearAuthData } from '@/utils/auth';

const router = useRouter();

const lifeLessons = ref([])
const loading = ref(false)
const error = ref(null)

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
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.font-playfair {
  font-family: 'Playfair Display', serif;
}
</style>
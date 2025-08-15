<template>
  <div class="min-h-screen flex">
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
      <div class="max-w-7xl ml-3">
        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2">My Badge Collection 🏆</h1>
              <p class="text-lg text-gray-600 font-medium">
                You've earned <span class="text-yellow-500 font-bold">{{ earnedBadges.length }}</span> badges so far!
                <br />
                <span class="text-blue-500 font-semibold">Total XP:</span> {{ totalXp }}
              </p>
            </div>

            <!-- Buttons (Right Side - Horizontal Row) -->
            <div class="flex space-x-4 min-w-fit font-playfair">
              <router-link to="/student/profile"
                class="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors duration-200 font-medium">
                Profile
              </router-link>

              <button @click="logout"
                class="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-red-100 text-red-700 hover:bg-red-200 transition-colors duration-200 font-medium">
                Logout
              </button>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500 mx-auto mb-4"></div>
          <p class="text-gray-600">Loading badges...</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="text-center py-20">
          <div class="text-6xl mb-4">⚠️</div>
          <h2 class="text-2xl font-bold text-red-600 mb-2">Error Loading Badges</h2>
          <p class="text-gray-600 mb-4">{{ error }}</p>
          <button @click="fetchBadges"
            class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors">
            Try Again
          </button>
        </div>

        <!-- Badge Grid -->
        <div v-else-if="earnedBadges.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <BadgeCard v-for="badge in earnedBadges" :key="badge.id" :badge="badge" />
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-20">
          <div class="text-6xl mb-4">😔</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">No Badges Earned Yet</h2>
          <p class="text-gray-600">Complete activities and challenges to start your collection!</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import BadgeCard from './BadgeCard.vue'
import api from '@/plugins/axios.ts'
import { clearAuthData } from '@/utils/auth';

const router = useRouter();

const badges = ref([])
const totalXp = ref(0)
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

const earnedBadges = computed(() => badges.value.filter(b => b.earned))

const fetchBadges = async () => {
  loading.value = true
  error.value = null
  try {
    const { data } = await api.get('/api/child/badges/earned')
    badges.value = data.badges || []
    totalXp.value = data.total_xp || 0
  } catch (err) {
    console.error('Error fetching badges:', err)
    error.value = 'Failed to load badges. Please try again.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchBadges()
})
</script>
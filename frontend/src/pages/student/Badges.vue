<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <!-- Header -->
    <header class="max-w-4xl mx-auto mb-8 text-center">
      <router-link
        to="/student/home"
        class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>

      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">My Badge Collection 🏆</h1>
      <p class="text-lg text-gray-600 font-medium">
        You've earned <span class="text-yellow-500 font-bold">{{ earnedBadges.length }}</span> badges so far!  
        <br />
        <span class="text-blue-500 font-semibold">Total XP:</span> {{ totalXp }}
      </p>
    </header>

    <main class="max-w-6xl mx-auto">
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
        <button
          @click="fetchBadges"
          class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors"
        >
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
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import BadgeCard from './BadgeCard.vue'
import api from '@/plugins/axios.ts'

const badges = ref([])
const totalXp = ref(0)
const loading = ref(false)
const error = ref(null)

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

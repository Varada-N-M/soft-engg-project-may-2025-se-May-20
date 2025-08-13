<template>
  <div class="badge-gallery">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-800">Badges Earned</h3>
      <p class="text-sm text-gray-600">{{ badges.length }} badges earned</p>
    </div>

    <div v-if="badges.length === 0" class="text-center py-8">
      <div class="text-gray-400 mb-2">
        🏆
      </div>
      <p class="text-gray-500">No badges earned yet</p>
    </div>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div 
        v-for="badge in badges" 
        :key="badge.badge_id"
        class="badge-card group cursor-pointer"
        @click="selectedBadge = badge"
      >
        <div class="bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full w-16 h-16 mx-auto mb-2 flex items-center justify-center text-white text-2xl font-bold group-hover:scale-105 transition-transform">
          🏆
        </div>
        <h4 class="text-sm font-semibold text-center text-gray-800">{{ badge.badge }}</h4>
        <p class="text-xs text-gray-500 text-center">Level {{ badge.level }}</p>
        <p class="text-xs text-gray-400 text-center">{{ formatDate(badge.earned_at) }}</p>
      </div>
    </div>

    <!-- Badge Detail Modal -->
    <div v-if="selectedBadge" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="selectedBadge = null">
      <div class="bg-white rounded-lg p-6 max-w-sm mx-4" @click.stop>
        <div class="text-center">
          <div class="bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-full w-24 h-24 mx-auto mb-4 flex items-center justify-center text-white text-4xl">
            🏆
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">{{ selectedBadge.badge }}</h3>
          <p class="text-gray-600 mb-2">Level {{ selectedBadge.level }}</p>
          <p class="text-sm text-gray-500 mb-4">+{{ selectedBadge.badge_xp }} XP</p>
          <p class="text-xs text-gray-400">Earned on {{ formatDate(selectedBadge.earned_at) }}</p>
          
          <button 
            @click="selectedBadge = null"
            class="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  badges: {
    type: Array,
    required: true,
    default: () => []
  }
})

const selectedBadge = ref(null)

const formatDate = (dateString) => {
  if (!dateString) return 'Unknown'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}
</script>

<style scoped>
@reference '@/css/index.css';
.badge-gallery {
  @apply bg-white p-4 rounded-lg border border-gray-200;
}

.badge-card {
  @apply p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors;
}
</style>
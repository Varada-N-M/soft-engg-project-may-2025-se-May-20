<template>
  <div class="min-h-screen bg-gray-100 page-font">
    <!-- Parent Navbar -->
    <ParentNavbar />
    
    <!-- Main Content -->
    <div class="achievements-page pt-16">
    <!-- Header -->
    <div class="mb-6">
      <div class="flex items-center space-x-4 mb-4">
        <button 
          @click="goBack" 
          class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div>
          <h1 class="text-2xl font-bold text-gray-800">
            {{ achievementsData?.child ? `${achievementsData.child.name}'s Achievements` : 'Achievements & Badges' }}
          </h1>
          <p class="text-gray-600">Celebrate your child's learning milestones</p>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-red-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        <span class="text-red-800">{{ error }}</span>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else-if="achievementsData">
      <!-- Achievement Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8 p-4 rounded-lg border border-gray-200">
        <div class="stat-card bg-gradient-to-br from-yellow-500 to-yellow-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-yellow-100 text-sm">Total Badges</p>
              <p class="text-3xl font-bold">{{ totalBadges }}</p>
            </div>
            <div class="text-4xl">🏆</div>
          </div>
        </div>

        <div class="stat-card bg-gradient-to-br from-purple-500 to-purple-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-100 text-sm">Total XP</p>
              <p class="text-3xl font-bold">{{ formatNumber(achievementsData.child.xp_points || 0) }}</p>
            </div>
            <div class="text-4xl">⭐</div>
          </div>
        </div>

        <div class="stat-card bg-gradient-to-br from-green-500 to-green-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100 text-sm">Current Streak</p>
              <p class="text-3xl font-bold">{{ achievementsData.child.streak || 0 }}</p>
            </div>
            <div class="text-4xl">🔥</div>
          </div>
        </div>

        <div class="stat-card bg-gradient-to-br from-blue-500 to-blue-600 text-white">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-blue-100 text-sm">Recent Achievements</p>
              <p class="text-3xl font-bold">{{ recentBadges }}</p>
            </div>
            <div class="text-4xl">🎉</div>
          </div>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="mb-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button 
              v-for="filter in filters" 
              :key="filter.id"
              @click="activeFilter = filter.id"
              class="py-2 px-1 border-b-2 font-medium text-sm transition-colors"
              :class="{
                'border-blue-500 text-blue-600': activeFilter === filter.id,
                'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300': activeFilter !== filter.id
              }"
            >
              {{ filter.label }}
              <span v-if="filter.count !== undefined" class="ml-1 text-xs bg-gray-200 text-gray-600 px-1.5 py-0.5 rounded-full">
                {{ filter.count }}
              </span>
            </button>
          </nav>
        </div>
      </div>

      <!-- Badges Gallery -->
      <div class="badges-gallery">
        <!-- No badges state -->
        <div v-if="filteredBadges.length === 0" class="text-center py-16">
          <div class="text-gray-400 text-6xl mb-4">🏅</div>
          <h3 class="text-lg font-semibold text-gray-800 mb-2">
            {{ activeFilter === 'all' ? 'No Badges Yet' : `No ${activeFilter} badges` }}
          </h3>
          <p class="text-gray-600">
            {{ activeFilter === 'all' ? 'Keep learning to earn your first badge!' : 'Keep working towards more achievements!' }}
          </p>
        </div>

        <!-- Badges Grid -->
        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div 
            v-for="badge in filteredBadges" 
            :key="badge.badge_id"
            class="badge-card group cursor-pointer"
            @click="selectedBadge = badge"
          >
            <div class="text-center">
              <!-- Badge Icon/Image -->
              <div class="w-20 h-20 mx-auto mb-3 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center text-3xl text-white shadow-lg group-hover:shadow-xl transition-shadow">
                {{ badge.icon || '🏆' }}
              </div>
              
              <!-- Badge Name -->
              <h4 class="font-semibold text-gray-800 text-sm mb-1 group-hover:text-blue-600 transition-colors">
                {{ badge.badge_name }}
              </h4>
              
              <!-- Badge Description -->
              <p class="text-xs text-gray-500 mb-2 line-clamp-2">
                {{ badge.description }}
              </p>
              
              <!-- Badge XP -->
              <div class="text-xs text-blue-600 font-medium">
                +{{ badge.badge_xp }} XP
              </div>
              
              <!-- Earned Date -->
              <div class="text-xs text-gray-400 mt-1">
                {{ formatDate(badge.earned_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Badge Detail Modal -->
      <div 
        v-if="selectedBadge" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        @click="selectedBadge = null"
      >
        <div 
          class="bg-white rounded-lg p-6 max-w-md w-full mx-4"
          @click.stop
        >
          <div class="text-center">
            <div class="w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br from-yellow-400 to-yellow-600 flex items-center justify-center text-4xl text-white shadow-lg">
              {{ selectedBadge.icon || '🏆' }}
            </div>
            
            <h3 class="text-xl font-bold text-gray-800 mb-2">
              {{ selectedBadge.badge_name }}
            </h3>
            
            <p class="text-gray-600 mb-4">
              {{ selectedBadge.description }}
            </p>
            
            <div class="flex justify-center space-x-6 text-sm mb-6">
              <div class="text-center">
                <div class="font-semibold text-blue-600">{{ selectedBadge.badge_xp }} XP</div>
                <div class="text-gray-500">Reward</div>
              </div>
              <div class="text-center">
                <div class="font-semibold text-gray-800">{{ formatDate(selectedBadge.earned_at) }}</div>
                <div class="text-gray-500">Earned</div>
              </div>
            </div>
            
            <button 
              @click="selectedBadge = null"
              class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/plugins/axios.ts'
import ParentNavbar from '@/components/partials/ParentNavbar.vue'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const achievementsData = ref(null)
const activeFilter = ref('all')
const selectedBadge = ref(null)

const filters = computed(() => {
  if (!achievementsData.value?.badges) return []
  
  const badges = achievementsData.value.badges
  const recentDate = new Date()
  recentDate.setDate(recentDate.getDate() - 30)
  
  return [
    { 
      id: 'all', 
      label: 'All Badges', 
      count: badges.length 
    },
    { 
      id: 'recent', 
      label: 'Recent', 
      count: badges.filter(b => new Date(b.earned_at) >= recentDate).length 
    },
    { 
      id: 'skills', 
      label: 'Skills', 
      count: badges.filter(b => b.badge_type === 'skill').length 
    },
    { 
      id: 'habits', 
      label: 'Habits', 
      count: badges.filter(b => b.badge_type === 'habit').length 
    },
    { 
      id: 'special', 
      label: 'Special', 
      count: badges.filter(b => b.badge_type === 'special').length 
    }
  ]
})

const totalBadges = computed(() => {
  return achievementsData.value?.badges?.length || 0
})

const recentBadges = computed(() => {
  if (!achievementsData.value?.badges) return 0
  const recentDate = new Date()
  recentDate.setDate(recentDate.getDate() - 30)
  return achievementsData.value.badges.filter(b => new Date(b.earned_at) >= recentDate).length
})

const filteredBadges = computed(() => {
  if (!achievementsData.value?.badges) return []
  
  const badges = achievementsData.value.badges
  
  switch (activeFilter.value) {
    case 'recent':
      const recentDate = new Date()
      recentDate.setDate(recentDate.getDate() - 30)
      return badges.filter(b => new Date(b.earned_at) >= recentDate)
    case 'skills':
      return badges.filter(b => b.badge_type === 'skill')
    case 'habits':
      return badges.filter(b => b.badge_type === 'habit')
    case 'special':
      return badges.filter(b => b.badge_type === 'special')
    default:
      return badges
  }
})

const fetchAchievements = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const childId = route.params.childId
    
    // Fetch badges and basic child info
    const badgesResponse = await api.get(`/api/parent/children/${childId}/badges`)
    
    achievementsData.value = {
      child: badgesResponse.data.child,
      badges: badgesResponse.data.badges || []
    }
    
  } catch (err) {
    console.error('Error fetching achievements:', err)
    error.value = err.response?.data?.error || 'Failed to load achievements data'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/parent/home')
}

const formatNumber = (num) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchAchievements()
})
</script>

<style scoped>
@reference '@/css/index.css';
.achievements-page {
  @apply p-6 min-h-screen bg-gray-50;
}

.stat-card {
  @apply p-6 rounded-lg shadow-sm;
}

.badges-gallery {
  @apply min-h-96;
}

.badge-card {
  @apply bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300">
    <!-- Header -->
    <header class="bg-white/90 backdrop-blur-sm shadow-lg sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Back Button and Title -->
          <div class="flex items-center space-x-4">
            <router-link
                to="/student/home"
                class="p-2 text-gray-600 hover:text-gray-800 transition-colors rounded-lg hover:bg-gray-100"
            >
              <ArrowLeftIcon class="w-6 h-6" />
            </router-link>
            <div>
              <h1 class="text-xl font-bold text-gray-800 font-fancy">🏆 My Badges</h1>
              <p class="text-sm text-gray-600 hidden sm:block">Collect them all!</p>
            </div>
          </div>

          <!-- Stats Summary -->
          <div class="flex items-center space-x-6">
            <div class="text-center">
              <p class="text-2xl font-bold text-yellow-600">{{ earnedBadges.length }}</p>
              <p class="text-xs text-gray-600">Earned</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-400">{{ totalBadges - earnedBadges.length }}</p>
              <p class="text-xs text-gray-600">To Go</p>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Progress Overview -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
          <div class="flex flex-col md:flex-row items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-bold text-gray-800 mb-2">Badge Collection Progress</h2>
              <p class="text-gray-600">{{ Math.round((earnedBadges.length / totalBadges) * 100) }}% Complete</p>
            </div>
            <div class="text-6xl animate-bounce">🎯</div>
          </div>

          <!-- Progress Bar -->
          <div class="w-full bg-gray-200 rounded-full h-4 mb-4">
            <div
                class="bg-gradient-to-r from-yellow-400 to-orange-500 h-4 rounded-full transition-all duration-1000 ease-out"
                :style="{ width: `${(earnedBadges.length / totalBadges) * 100}%` }"
            ></div>
          </div>

          <!-- Achievement Milestones -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="milestone in milestones" :key="milestone.count"
                 class="text-center p-3 rounded-xl transition-all duration-200"
                 :class="earnedBadges.length >= milestone.count ? 'bg-green-100 border-2 border-green-300' : 'bg-gray-100 border-2 border-gray-200'">
              <div class="text-2xl mb-1">{{ milestone.emoji }}</div>
              <p class="text-sm font-medium text-gray-800">{{ milestone.count }} Badges</p>
              <p class="text-xs text-gray-600">{{ milestone.title }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filter Tabs -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-2 shadow-lg border border-white/20 inline-flex">
          <button
              v-for="filter in filters"
              :key="filter.id"
              @click="activeFilter = filter.id"
              class="px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center space-x-2"
              :class="activeFilter === filter.id
              ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg transform scale-105'
              : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'"
          >
            <span class="text-lg">{{ filter.emoji }}</span>
            <span>{{ filter.name }}</span>
            <span v-if="filter.count" class="bg-white/20 text-xs px-2 py-1 rounded-full">{{ filter.count }}</span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-16">
        <div class="text-6xl mb-4 animate-spin">🎯</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Loading your badges...</h3>
        <p class="text-gray-600">Getting your latest achievements!</p>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="text-center py-16">
        <div class="text-6xl mb-4">😔</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">Oops! Something went wrong</h3>
        <p class="text-gray-600 mb-4">{{ error }}</p>
        <button @click="fetchBadges" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg">
          Try Again
        </button>
      </div>

      <!-- Badges Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
            v-for="badge in filteredBadges"
            :key="badge.id"
            class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 cursor-pointer relative overflow-hidden"
            :class="badge.earned ? 'ring-4 ring-yellow-300' : 'opacity-75'"
            @click="openBadgeModal(badge)"
        >
          <!-- Badge Glow Effect for Earned Badges -->
          <div v-if="badge.earned" class="absolute inset-0 bg-gradient-to-r from-yellow-200/30 to-orange-200/30 rounded-3xl"></div>

          <!-- Badge Content -->
          <div class="relative z-10">
            <!-- Badge Icon -->
            <div class="text-center mb-4">
              <div
                  class="w-20 h-20 mx-auto rounded-full flex items-center justify-center text-4xl mb-3 transition-all duration-300"
                  :class="badge.earned ? 'bg-gradient-to-br from-yellow-400 to-orange-500 shadow-lg animate-pulse' : 'bg-gray-200'"
              >
                {{ badge.emoji }}
              </div>

              <!-- Earned Badge Crown -->
              <div v-if="badge.earned" class="absolute -top-2 left-1/2 transform -translate-x-1/2">
                <div class="text-2xl animate-bounce">👑</div>
              </div>
            </div>

            <!-- Badge Info -->
            <div class="text-center">
              <h3 class="font-bold text-gray-800 mb-2 text-lg">{{ badge.name }}</h3>
              <p class="text-sm text-gray-600 mb-3">{{ badge.description }}</p>

              <!-- Progress Bar for Unearned Badges -->
              <div v-if="!badge.earned && badge.progress !== undefined" class="mb-3">
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                      class="bg-blue-500 h-2 rounded-full transition-all duration-500"
                      :style="{ width: `${badge.progress}%` }"
                  ></div>
                </div>
                <p class="text-xs text-gray-500 mt-1">{{ badge.progress }}% Complete</p>
              </div>

              <!-- Badge Status -->
              <div class="flex items-center justify-center space-x-2">
                <div v-if="badge.earned" class="flex items-center text-green-600">
                  <CheckCircleIcon class="w-4 h-4 mr-1" />
                  <span class="text-sm font-medium">Earned!</span>
                </div>
                <div v-else class="flex items-center text-gray-500">
                  <ClockIcon class="w-4 h-4 mr-1" />
                  <span class="text-sm">{{ badge.requirement }}</span>
                </div>
              </div>

              <!-- Earned Date -->
              <div v-if="badge.earned && (badge.earned_date || badge.earnedDate)" class="mt-2">
                <p class="text-xs text-gray-500">Earned on {{ formatDate(badge.earned_date || badge.earnedDate) }}</p>
              </div>

              <!-- XP Reward -->
              <div class="mt-3 inline-flex items-center bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-xs font-medium">
                <span class="mr-1">⭐</span>
                +{{ badge.xp_reward || badge.xpReward }} XP
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredBadges.length === 0" class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">No badges found</h3>
        <p class="text-gray-600">Try a different filter to see more badges!</p>
      </div>
    </main>

    <!-- Badge Detail Modal -->
    <div v-if="selectedBadge" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl p-8 max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="text-center">
          <!-- Close Button -->
          <button
              @click="selectedBadge = null"
              class="absolute top-4 right-4 p-2 text-gray-500 hover:text-gray-700 transition-colors"
          >
            <XIcon class="w-6 h-6" />
          </button>

          <!-- Badge Icon -->
          <div
              class="w-24 h-24 mx-auto rounded-full flex items-center justify-center text-5xl mb-4"
              :class="selectedBadge.earned ? 'bg-gradient-to-br from-yellow-400 to-orange-500 shadow-lg' : 'bg-gray-200'"
          >
            {{ selectedBadge.emoji }}
          </div>

          <!-- Badge Details -->
          <h2 class="text-2xl font-bold text-gray-800 mb-2">{{ selectedBadge.name }}</h2>
          <p class="text-gray-600 mb-4">{{ selectedBadge.description }}</p>

          <!-- Detailed Requirements -->
          <div class="bg-gray-50 rounded-2xl p-4 mb-4 text-left">
            <h4 class="font-semibold text-gray-800 mb-2">How to earn this badge:</h4>
            <ul class="space-y-1 text-sm text-gray-600">
              <li v-for="req in (selectedBadge.detailed_requirements || selectedBadge.detailedRequirements)" :key="req" class="flex items-start">
                <span class="text-blue-500 mr-2">•</span>
                {{ req }}
              </li>
            </ul>
          </div>

          <!-- Tips -->
          <div v-if="selectedBadge.tips" class="bg-blue-50 rounded-2xl p-4 mb-4 text-left">
            <h4 class="font-semibold text-blue-800 mb-2">💡 Tips:</h4>
            <p class="text-sm text-blue-700">{{ selectedBadge.tips }}</p>
          </div>

          <!-- Status -->
          <div class="flex items-center justify-center space-x-4 mb-4">
            <div class="text-center">
              <p class="text-sm text-gray-500">Status</p>
              <p class="font-medium" :class="selectedBadge.earned ? 'text-green-600' : 'text-gray-600'">
                {{ selectedBadge.earned ? 'Earned ✅' : 'Not Earned' }}
              </p>
            </div>
            <div class="text-center">
              <p class="text-sm text-gray-500">XP Reward</p>
              <p class="font-medium text-yellow-600">+{{ selectedBadge.xp_reward || selectedBadge.xpReward }} XP</p>
            </div>
          </div>

          <!-- Action Button -->
          <button
              v-if="!selectedBadge.earned"
              @click="startBadgeChallenge(selectedBadge)"
              class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-3 px-4 rounded-xl hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200"
          >
            🚀 Start Challenge
          </button>
        </div>
      </div>
    </div>

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
import {
  ArrowLeftIcon,
  CheckCircleIcon,
  ClockIcon,
  XIcon
} from 'lucide-vue-next'
import axios from '@/plugins/axios.js'

// Router
const router = useRouter()

// Reactive data
const activeFilter = ref('all')
const selectedBadge = ref(null)
const loading = ref(false)
const error = ref(null)
const badgesData = ref(null)

// Fetch badges data from API
const fetchBadges = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await axios.get('/api/student/badges')
    badgesData.value = response.data
  } catch (err) {
    console.error('Error fetching badges:', err)
    error.value = err.response?.data?.error || 'Failed to load badges'
    
    // Fallback to static data if API fails
    badgesData.value = {
      badges: [
  // Math Badges
  {
    id: 1,
    name: 'Math Wizard',
    description: 'Master of numbers and calculations',
    emoji: '🧮',
    category: 'math',
    earned: true,
    earnedDate: '2024-01-15',
    xpReward: 100,
    requirement: 'Solve 100 math problems',
    progress: 100,
    detailedRequirements: [
      'Complete 50 addition problems',
      'Complete 30 subtraction problems',
      'Complete 20 multiplication problems'
    ],
    tips: 'Practice a little bit every day to build your math skills!'
  },
  {
    id: 2,
    name: 'Speed Calculator',
    description: 'Lightning fast with numbers',
    emoji: '⚡',
    category: 'math',
    earned: true,
    earnedDate: '2024-01-20',
    xpReward: 75,
    requirement: 'Solve 20 problems in under 2 minutes',
    progress: 100,
    detailedRequirements: [
      'Complete math quiz in under 2 minutes',
      'Maintain 90% accuracy',
      'Use mental math techniques'
    ],
    tips: 'Learn your multiplication tables to solve problems faster!'
  },
  {
    id: 3,
    name: 'Problem Solver',
    description: 'Tackles the toughest math challenges',
    emoji: '🎯',
    category: 'math',
    earned: false,
    xpReward: 150,
    requirement: 'Complete 5 advanced word problems',
    progress: 60,
    detailedRequirements: [
      'Solve 5 multi-step word problems',
      'Show your work clearly',
      'Explain your reasoning'
    ],
    tips: 'Read the problem carefully and identify what you need to find!'
  },

  // Reading Badges
  {
    id: 4,
    name: 'Bookworm',
    description: 'Loves reading and stories',
    emoji: '📚',
    category: 'reading',
    earned: true,
    earnedDate: '2024-01-10',
    xpReward: 80,
    requirement: 'Read 10 books',
    progress: 100,
    detailedRequirements: [
      'Read 10 complete books',
      'Take comprehension quizzes',
      'Write book summaries'
    ],
    tips: 'Choose books that interest you to make reading more fun!'
  },
  {
    id: 5,
    name: 'Speed Reader',
    description: 'Reads with incredible speed',
    emoji: '🏃‍♂️',
    category: 'reading',
    earned: false,
    xpReward: 90,
    requirement: 'Read 200 words per minute',
    progress: 75,
    detailedRequirements: [
      'Complete speed reading test',
      'Maintain good comprehension',
      'Practice daily reading'
    ],
    tips: 'Practice reading aloud to improve your speed and fluency!'
  },
  {
    id: 6,
    name: 'Story Master',
    description: 'Expert at understanding stories',
    emoji: '📖',
    category: 'reading',
    earned: true,
    earnedDate: '2024-01-25',
    xpReward: 85,
    requirement: 'Perfect scores on 5 comprehension tests',
    progress: 100,
    detailedRequirements: [
      'Score 100% on 5 reading tests',
      'Identify main ideas correctly',
      'Answer inference questions'
    ],
    tips: 'Pay attention to details and think about what the author is trying to say!'
  },

  // Science Badges
  {
    id: 7,
    name: 'Young Scientist',
    description: 'Curious about how the world works',
    emoji: '🔬',
    category: 'science',
    earned: true,
    earnedDate: '2024-01-18',
    xpReward: 95,
    requirement: 'Complete 3 experiments',
    progress: 100,
    detailedRequirements: [
      'Complete 3 hands-on experiments',
      'Record observations accurately',
      'Explain scientific concepts'
    ],
    tips: 'Always ask "why" and "how" to discover amazing things!'
  },
  {
    id: 8,
    name: 'Nature Explorer',
    description: 'Loves learning about plants and animals',
    emoji: '🌱',
    category: 'science',
    earned: false,
    xpReward: 70,
    requirement: 'Study 10 different species',
    progress: 40,
    detailedRequirements: [
      'Learn about 5 plants',
      'Learn about 5 animals',
      'Understand their habitats'
    ],
    tips: 'Go outside and observe nature around you!'
  },

  // Achievement Badges
  {
    id: 9,
    name: 'Perfect Week',
    description: 'Completed all activities for a week',
    emoji: '🌟',
    category: 'achievement',
    earned: true,
    earnedDate: '2024-01-22',
    xpReward: 200,
    requirement: 'Complete all daily activities for 7 days',
    progress: 100,
    detailedRequirements: [
      'Complete daily math practice',
      'Complete daily reading',
      'Complete daily science activity',
      'Do this for 7 consecutive days'
    ],
    tips: 'Set a daily routine and stick to it!'
  },
  {
    id: 10,
    name: 'Streak Master',
    description: 'Consistent learner every day',
    emoji: '🔥',
    category: 'achievement',
    earned: false,
    xpReward: 300,
    requirement: 'Maintain 30-day learning streak',
    progress: 23,
    detailedRequirements: [
      'Log in every day for 30 days',
      'Complete at least one activity daily',
      'Maintain consistent progress'
    ],
    tips: 'Even 10 minutes of learning each day counts!'
  },
  {
    id: 11,
    name: 'Helper',
    description: 'Always ready to help classmates',
    emoji: '🤝',
    category: 'social',
    earned: true,
    earnedDate: '2024-01-12',
    xpReward: 60,
    requirement: 'Help 5 classmates with their work',
    progress: 100,
    detailedRequirements: [
      'Assist classmates with difficult problems',
      'Share helpful tips and strategies',
      'Be kind and encouraging'
    ],
    tips: 'Teaching others helps you learn better too!'
  },
  {
    id: 12,
    name: 'Team Player',
    description: 'Great at working with others',
    emoji: '👥',
    category: 'social',
    earned: false,
    xpReward: 80,
    requirement: 'Complete 3 group projects',
    progress: 33,
    detailedRequirements: [
      'Participate in group activities',
      'Contribute ideas and solutions',
      'Support team members'
    ],
    tips: 'Listen to others and share your ideas respectfully!'
        }
      ],
      summary: {
        earned_count: 3,
        total_count: 12,
        completion_percentage: 25.0
      }
    }
  } finally {
    loading.value = false
  }
}

// Computed property to get badges from API data or fallback
const badges = computed(() => {
  return badgesData.value?.badges || []
})

// Computed properties
const earnedBadges = computed(() => badges.value.filter(badge => badge.earned))
const totalBadges = computed(() => badges.value.length)

const filters = computed(() => [
  { id: 'all', name: 'All Badges', emoji: '🏆', count: badges.value.length },
  { id: 'earned', name: 'Earned', emoji: '✅', count: earnedBadges.value.length },
  { id: 'math', name: 'Math', emoji: '🔢', count: badges.value.filter(b => b.category === 'math').length },
  { id: 'reading', name: 'Reading', emoji: '📚', count: badges.value.filter(b => b.category === 'reading').length },
  { id: 'science', name: 'Science', emoji: '🔬', count: badges.value.filter(b => b.category === 'science').length },
  { id: 'achievement', name: 'Achievement', emoji: '🌟', count: badges.value.filter(b => b.category === 'achievement').length },
  { id: 'social', name: 'Social', emoji: '👥', count: badges.value.filter(b => b.category === 'social').length }
])

const filteredBadges = computed(() => {
  if (activeFilter.value === 'all') return badges.value
  if (activeFilter.value === 'earned') return earnedBadges.value
  return badges.value.filter(badge => badge.category === activeFilter.value)
})

const milestones = ref([
  { count: 5, title: 'Getting Started', emoji: '🌱' },
  { count: 10, title: 'Badge Collector', emoji: '🎯' },
  { count: 15, title: 'Super Achiever', emoji: '⭐' },
  { count: 20, title: 'Badge Master', emoji: '👑' }
])

// Methods
const goBack = () => {
  router.go(-1)
}

const openBadgeModal = (badge) => {
  selectedBadge.value = badge
}

const startBadgeChallenge = (badge) => {
  selectedBadge.value = null
  // Navigate to appropriate activity based on badge category
  switch (badge.category) {
    case 'math':
      router.push('/practice/math')
      break
    case 'reading':
      router.push('/practice/reading')
      break
    case 'science':
      router.push('/practice/science')
      break
    default:
      router.push('/practice')
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const transformElements = () => {
  document.querySelectorAll('.transform').forEach((el, index) => {
    setTimeout(() => {
      el.style.transform = 'translateY(0)'
      el.style.opacity = '1'
    }, index * 100)
  })
}

onMounted(async () => {
  // Fetch badges data
  await fetchBadges()
  
  // Add entrance animation
  transformElements()
})
</script>

<style scoped>

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Initial state for entrance animation */
.transform {
  transform: translateY(20px);
  transition: all 0.5s ease-out;
}
</style>

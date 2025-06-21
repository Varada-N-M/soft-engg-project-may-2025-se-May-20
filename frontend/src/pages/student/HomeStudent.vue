<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300">

    <!-- Floating decorative elements -->
    <FloatingDecorativeElements/>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
          <div class="flex flex-col md:flex-row justify-between">
            <div class="text-center md:text-left mb-4 md:mb-0">
              <h2 class="text-3xl font-bold text-gray-800 mb-2">
                Good {{ timeOfDay }}, {{ studentName }}! 🌈
              </h2>
              <p class="text-gray-600">Ready for another amazing day of learning?</p>
            </div>
            <EmojiBounceAnimation align="end" :emojis="['🎮','📚','🏆']"/>

          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- XP Points -->
        <div
            class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 transform hover:scale-105 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">XP Points</p>
              <p class="text-3xl font-bold text-yellow-600">{{ stats.xpPoints }}</p>
            </div>
            <div class="w-12 h-12 bg-yellow-100 rounded-full flex items-center justify-center">
              <span class="text-2xl">⭐</span>
            </div>
          </div>
          <div class="mt-4">
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div class="bg-yellow-500 h-2 rounded-full transition-all duration-500"
                   :style="{ width: `${(stats.xpPoints % 1000) / 10}%` }"></div>
            </div>
            <p class="text-xs text-gray-500 mt-1">{{ 1000 - (stats.xpPoints % 1000) }} XP to next level</p>
          </div>
        </div>

        <!-- Badges Earned -->
        <div
            class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 transform hover:scale-105 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Badges</p>
              <p class="text-3xl font-bold text-purple-600">{{ stats.badges }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center">
              <span class="text-2xl">🏅</span>
            </div>
          </div>
          <p class="text-xs text-green-600 mt-2">+2 this week!</p>
        </div>

        <!-- Streak Days -->
        <div
            class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 transform hover:scale-105 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Streak</p>
              <p class="text-3xl font-bold text-orange-600">{{ stats.streak }}</p>
            </div>
            <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
              <span class="text-2xl">🔥</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-2">days in a row</p>
        </div>

        <!-- Completed Lessons -->
        <div
            class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 transform hover:scale-105 transition-all duration-200">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Lessons</p>
              <p class="text-3xl font-bold text-green-600">{{ stats.completedLessons }}</p>
            </div>
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <span class="text-2xl">📖</span>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-2">completed</p>
        </div>
      </div>

      <!-- Main Dashboard Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column -->
        <div class="lg:col-span-2 space-y-8">
          <!-- Current Lessons -->
          <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-2xl font-bold text-gray-800">📚 Continue Learning</h3>
              <button class="text-blue-600 hover:text-blue-800 text-sm font-medium">View All</button>
            </div>

            <div class="space-y-4">
              <div v-for="lesson in currentLessons" :key="lesson.id"
                   class="flex items-center p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl border border-blue-100 hover:shadow-md transition-all duration-200 cursor-pointer">
                <div class="w-12 h-12 rounded-full flex items-center justify-center text-2xl mr-4"
                     :style="{ backgroundColor: lesson.color }">
                  {{ lesson.emoji }}
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-gray-800">{{ lesson.title }}</h4>
                  <p class="text-sm text-gray-600">{{ lesson.description }}</p>
                  <div class="mt-2">
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-blue-500 h-2 rounded-full transition-all duration-500"
                           :style="{ width: `${lesson.progress}%` }"></div>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">{{ lesson.progress }}% complete</p>
                  </div>
                </div>
                <ChevronRightIcon class="w-5 h-5 text-gray-400"/>
              </div>
            </div>
          </div>

          <!-- Recent Activities -->
          <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
            <h3 class="text-2xl font-bold text-gray-800 mb-6">🎯 Recent Activities</h3>

            <div class="space-y-4">
              <div v-for="activity in recentActivities" :key="activity.id"
                   class="flex items-center p-4 bg-gray-50 rounded-2xl">
                <div class="w-10 h-10 rounded-full flex items-center justify-center text-xl mr-4"
                     :style="{ backgroundColor: activity.color }">
                  {{ activity.emoji }}
                </div>
                <div class="flex-1">
                  <h4 class="font-medium text-gray-800">{{ activity.title }}</h4>
                  <p class="text-sm text-gray-600">{{ activity.description }}</p>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-gray-800">+{{ activity.points }} XP</p>
                  <p class="text-xs text-gray-500">{{ activity.time }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column -->
        <div class="space-y-8">
          <!-- Quick Actions -->
          <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
            <h3 class="text-xl font-bold text-gray-800 mb-4">🚀 Quick Start</h3>

            <div class="grid grid-cols-2 gap-4">
              <button v-for="action in quickActions" :key="action.id"
                      class="p-4 rounded-2xl text-center transition-all duration-200 transform hover:scale-105"
                      :style="{ backgroundColor: action.bgColor }"
                      @click="handleQuickAction(action.id)">
                <div class="text-3xl mb-2">{{ action.emoji }}</div>
                <p class="text-sm font-medium text-gray-800">{{ action.title }}</p>
              </button>
            </div>
          </div>

          <!-- Achievements -->
          <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-xl font-bold text-gray-800">🏆 Latest Badges</h3>
              <router-link to="/student/badges" class="text-purple-600 hover:text-purple-800 text-sm font-medium">View All</router-link>
            </div>

            <div class="space-y-3">
              <div v-for="badge in latestBadges" :key="badge.id"
                   class="flex items-center p-3 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl border border-yellow-100">
                <div class="text-2xl mr-3">{{ badge.emoji }}</div>
                <div>
                  <h4 class="font-medium text-gray-800 text-sm">{{ badge.name }}</h4>
                  <p class="text-xs text-gray-600">{{ badge.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Friends Activity -->
          <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
            <h3 class="text-xl font-bold text-gray-800 mb-4">👥 Friends Activity</h3>

            <div class="space-y-3">
              <div v-for="friend in friendsActivity" :key="friend.id"
                   class="flex items-center p-3 bg-gray-50 rounded-xl">
                <div class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white mr-3"
                     :style="{ backgroundColor: friend.color }">
                  {{ friend.initials }}
                </div>
                <div class="flex-1">
                  <p class="text-sm font-medium text-gray-800">{{ friend.name }}</p>
                  <p class="text-xs text-gray-600">{{ friend.activity }}</p>
                </div>
                <p class="text-xs text-gray-500">{{ friend.time }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Floating Action Button -->
    <button
        class="fixed bottom-6 right-6 w-14 h-14 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-full shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-200 flex items-center justify-center z-40">
      <PlusIcon class="w-6 h-6"/>
    </button>

  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {
  StarIcon,
  BellIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  PlusIcon
} from 'lucide-vue-next'
import EmojiBounceAnimation from "@/components/partials/EmojiBounceAnimation.vue";
import FloatingDecorativeElements from "@/components/partials/FloatingDecorativeElements.vue";

// Router
const router = useRouter()

// Reactive data
const showProfileMenu = ref(false)
const studentName = ref('Alex')
const studentInitials = ref('AK')

// Mock data
const stats = ref({
  xpPoints: 2450,
  badges: 12,
  streak: 7,
  completedLessons: 34
})

const currentLessons = ref([
  {
    id: 1,
    title: 'Math Adventures',
    description: 'Addition and Subtraction Fun',
    progress: 75,
    emoji: '🔢',
    color: '#FFE4B5'
  },
  {
    id: 2,
    title: 'Reading Quest',
    description: 'Story Comprehension',
    progress: 45,
    emoji: '📖',
    color: '#E6F3FF'
  },
  {
    id: 3,
    title: 'Science Lab',
    description: 'Simple Experiments',
    progress: 20,
    emoji: '🔬',
    color: '#F0FFF0'
  }
])

const recentActivities = ref([
  {
    id: 1,
    title: 'Completed Math Quiz',
    description: 'Perfect score on multiplication',
    points: 100,
    time: '2 hours ago',
    emoji: '🎯',
    color: '#FFE4B5'
  },
  {
    id: 2,
    title: 'Reading Badge Earned',
    description: 'Read 5 stories this week',
    points: 50,
    time: '1 day ago',
    emoji: '🏅',
    color: '#E6F3FF'
  },
  {
    id: 3,
    title: 'Science Experiment',
    description: 'Volcano eruption simulation',
    points: 75,
    time: '2 days ago',
    emoji: '🌋',
    color: '#F0FFF0'
  }
])

const quickActions = ref([
  {id: 'practice', title: 'Practice', emoji: '📝', bgColor: '#FFE4E1'},
  {id: 'games', title: 'Games', emoji: '🎮', bgColor: '#E0E6FF'},
  {id: 'quiz', title: 'Quiz', emoji: '🧠', bgColor: '#E6FFE6'},
  {id: 'stories', title: 'Stories', emoji: '📚', bgColor: '#FFF0E6'}
])

const latestBadges = ref([
  {
    id: 1,
    name: 'Math Master',
    description: 'Solved 50 math problems',
    emoji: '🧮'
  },
  {
    id: 2,
    name: 'Speed Reader',
    description: 'Read 10 books this month',
    emoji: '⚡'
  },
  {
    id: 3,
    name: 'Science Star',
    description: 'Completed 5 experiments',
    emoji: '⭐'
  }
])

const friendsActivity = ref([
  {
    id: 1,
    name: 'Emma',
    initials: 'EM',
    activity: 'Completed Science Quiz',
    time: '1h ago',
    color: '#FF6B6B'
  },
  {
    id: 2,
    name: 'Jake',
    initials: 'JK',
    activity: 'Earned Reading Badge',
    time: '3h ago',
    color: '#4ECDC4'
  },
  {
    id: 3,
    name: 'Lily',
    initials: 'LY',
    activity: 'Started Math Adventure',
    time: '5h ago',
    color: '#45B7D1'
  }
])

// Computed properties
const timeOfDay = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return 'morning'
  if (hour < 17) return 'afternoon'
  return 'evening'
})

// Methods
const handleQuickAction = (actionId) => {
  console.log(`Quick action: ${actionId}`)
  // Handle navigation to different sections
  switch (actionId) {
    case 'practice':
      router.push('/practice')
      break
    case 'games':
      router.push('/games')
      break
    case 'quiz':
      router.push('/quiz')
      break
    case 'stories':
      router.push('/stories')
      break
  }
}

const handleLogout = () => {
  // Clear localStorage
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_type')
  localStorage.removeItem('remember_me')

  // Redirect to login
  router.push('/login')
}

// Close profile menu when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showProfileMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)

  // Get student info from localStorage or API
  const userEmail = localStorage.getItem('user_email')
  if (userEmail) {
    const name = userEmail.split('@')[0]
    studentName.value = name.charAt(0).toUpperCase() + name.slice(1)
    studentInitials.value = name.substring(0, 2).toUpperCase()
  }
})
</script>

<style scoped>
@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -30px, 0);
  }
  70% {
    transform: translate3d(0, -15px, 0);
  }
  90% {
    transform: translate3d(0, -4px, 0);
  }
}



.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
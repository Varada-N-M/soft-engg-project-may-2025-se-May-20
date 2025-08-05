<template>
  <div class="min-h-screen flex">
    <aside class="w-64 bg-white bg-opacity-90 backdrop-blur-sm p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.1)] fixed left-0 top-0 h-screen overflow-y-auto">
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-800 mt-15">Student Dashboard</h2>
      </div>
      <nav class="space-y-4">
        <router-link to="/student/home" class="flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-yellow-100 hover:text-yellow-600 transition-colors duration-200">
          <span class="text-xl">🏠</span> Home  
        </router-link>
        <router-link to="/student/badges" class="flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-blue-100 hover:text-blue-600 transition-colors duration-200">
          <span class="text-xl">🏅</span> Badges
        </router-link>
        <router-link to="/student/habit" class="flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-green-100 hover:text-green-600 transition-colors duration-200">
          <span class="text-xl">🎯</span> Habit
        </router-link>
        <router-link to="/student/lesson-updates" class="flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-purple-100 hover:text-purple-600 transition-colors duration-200">
          <span class="text-xl">📚</span> Lesson Updates
        </router-link>
        <router-link to="/student/journal" class="flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-yellow-100 hover:text-yellow-600 transition-colors duration-200">
          <span class="text-xl">✍️</span> Student Journal
        </router-link>
        <router-link to="/student/weekly-report" class="w-full text-left flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-red-100 hover:text-red-600 transition-colors duration-200">
          <span class="text-xl">📊</span> Weekly Report
        </router-link>
        <router-link to="/student/survey" class="w-full text-left flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-green-100 hover:text-green-600 transition-colors duration-200">
          <span class="text-xl">🔍</span> Survey
        </router-link>
      </nav>
    </aside>

    <div class="flex-1 ml-64 p-4 overflow-y-auto">
      <!-- Loading State -->
      <div v-if="loading" class="max-w-6xl mx-auto mt-10 text-center">
        <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-3xl p-12 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
          <div class="text-6xl mb-4">🎯</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Loading your dashboard...</h2>
          <p class="text-gray-600">Getting your latest progress and achievements!</p>
        </div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="max-w-6xl mx-auto mt-10 text-center">
        <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-3xl p-12 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
          <div class="text-6xl mb-4">😔</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Oops! Something went wrong</h2>
          <p class="text-gray-600 mb-4">{{ error }}</p>
          <button @click="fetchDashboardData" class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg">
            Try Again
          </button>
        </div>
      </div>
      
      <div v-else-if="!showWeeklyReport" class="max-w-6xl mx-auto mt-10">
        <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-3xl p-6 mb-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ dashboardData.greeting || 'Welcome! 🌈' }}</h1>
              <p class="text-gray-600">Ready for another amazing day of learning?</p>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
            <div class="flex items-center justify-between mb-3">
              <div>
                <p class="text-gray-600 text-sm font-medium">XP Points</p>
                <h3 class="text-3xl font-bold text-orange-500">{{ dashboardData.stats?.total_xp || 0 }}</h3>
              </div>
              <div class="text-4xl">⭐</div>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2 mb-2">
              <div class="bg-orange-400 h-2 rounded-full" :style="{ width: `${dashboardData.progress?.xp_progress_percent || 0}%` }"></div>
            </div>
            <p class="text-xs text-gray-500">{{ dashboardData.stats?.xp_for_next_level || 0 }} XP to next level</p>
          </div>

          <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
            <div class="flex items-center justify-between mb-3">
              <div>
                <p class="text-gray-600 text-sm font-medium">Badges</p>
                <h3 class="text-3xl font-bold text-purple-500">{{ dashboardData.stats?.total_badges || 0 }}</h3>
              </div>
              <div class="text-4xl">🏅</div>
            </div>
            <p class="text-green-600 text-sm font-medium">+{{ dashboardData.stats?.badges_this_week || 0 }} this week!</p>
          </div>

          <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
            <div class="flex items-center justify-between mb-3">
              <div>
                <p class="text-gray-600 text-sm font-medium">Streak</p>
                <h3 class="text-3xl font-bold text-red-500">{{ dashboardData.stats?.learning_streak || 0 }}</h3>
              </div>
              <div class="text-4xl">🔥</div>
            </div>
            <p class="text-gray-500 text-sm">days in a row</p>
          </div>

          <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
            <div class="flex items-center justify-between mb-3">
              <div>
                <p class="text-gray-600 text-sm font-medium">Lessons</p>
                <h3 class="text-3xl font-bold text-green-500">{{ dashboardData.stats?.lessons_completed || 0 }}</h3>
              </div>
              <div class="text-4xl">📚</div>
            </div>
            <p class="text-gray-500 text-sm">completed</p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                📚 Continue Learning
              </h2>
              <button class="text-blue-500 hover:text-blue-600 font-medium">View All</button>
            </div>

            <div class="space-y-4">
              <div class="flex items-center gap-4 p-4 bg-blue-50 rounded-xl hover:bg-blue-100 transition-colors cursor-pointer">
                <div class="bg-blue-500 text-white rounded-lg p-3 text-sm font-bold">1+1</div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-800">Math Adventures</h3>
                  <p class="text-gray-600 text-sm">Addition and Subtraction Fun</p>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-blue-500 h-2 rounded-full" style="width: 75%"></div>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">75% complete</p>
                </div>
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>

              <div class="flex items-center gap-4 p-4 bg-green-50 rounded-xl hover:bg-green-100 transition-colors cursor-pointer">
                <div class="bg-green-500 text-white rounded-lg p-3 text-lg">📖</div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-800">Reading Quest</h3>
                  <p class="text-gray-600 text-sm">Story Comprehension</p>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-green-500 h-2 rounded-full" style="width: 45%"></div>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">45% complete</p>
                </div>
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>

              <div class="flex items-center gap-4 p-4 bg-purple-50 rounded-xl hover:bg-purple-100 transition-colors cursor-pointer">
                <div class="bg-purple-500 text-white rounded-lg p-3 text-lg">🧪</div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-800">Science Lab</h3>
                  <p class="text-gray-600 text-sm">Simple Experiments</p>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-purple-500 h-2 rounded-full" style="width: 20%"></div>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">20% complete</p>
                </div>
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>

              <div class="flex items-center gap-4 p-4 bg-red-50 rounded-xl hover:bg-red-100 transition-colors cursor-pointer">
                <div class="bg-red-500 text-white rounded-lg p-3 text-lg">🧪</div>
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-800">Rocket Science Lab</h3>
                  <p class="text-gray-600 text-sm">Build an explosion using Cocola & Mentos :) </p>
                  <div class="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div class="bg-red-500 h-2 rounded-full" style="width: 100%"></div>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">100% complete</p>
                </div>
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </div>
            </div>
          </div>

          <div class="space-y-6">
            <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
              <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                🚀 Quick Start
              </h2>
              <div class="grid grid-cols-2 gap-3">
                <div class="bg-red-100 rounded-xl p-4 text-center hover:bg-red-200 transition-colors cursor-pointer">
                  <div class="text-2xl mb-2">✏️</div>
                  <p class="text-sm font-medium text-gray-700">Practice</p>
                </div>
                <div class="bg-blue-100 rounded-xl p-4 text-center hover:bg-blue-200 transition-colors cursor-pointer">
                  <div class="text-2xl mb-2">🎮</div>
                  <p class="text-sm font-medium text-gray-700">Games</p>
                </div>
                <div class="bg-pink-100 rounded-xl p-4 text-center hover:bg-pink-200 transition-colors cursor-pointer">
                  <div class="text-2xl mb-2">🧠</div>
                  <p class="text-sm font-medium text-gray-700">Quiz</p>
                </div>
                <div class="bg-green-100 rounded-xl p-4 text-center hover:bg-green-200 transition-colors cursor-pointer">
                  <div class="text-2xl mb-2">📚</div>
                  <p class="text-sm font-medium text-gray-700">Stories</p>
                </div>
              </div>
            </div>

            <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-bold text-gray-800 flex items-center gap-2">
                  🏆 Latest Badges
                </h2>
                <button class="text-purple-500 hover:text-purple-600 font-medium text-sm">View All</button>
              </div>
              <div class="space-y-3">
                <div class="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                  <div class="text-2xl">🏅</div>
                  <div>
                    <h4 class="font-medium text-gray-800">Math Master</h4>
                    <p class="text-xs text-gray-600">Solved 50 math problems</p>
                  </div>
                </div>
                <div class="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                  <div class="text-2xl">📖</div>
                  <div>
                    <h4 class="font-medium text-gray-800">Story Explorer</h4>
                    <p class="text-xs text-gray-600">Read 10 stories</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/plugins/axios.js'

const showWeeklyReport = ref(false)
const dashboardData = ref({})
const loading = ref(false)
const error = ref(null)

// Fetch dashboard data
const fetchDashboardData = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await axios.get('/api/student/dashboard')
    dashboardData.value = response.data
  } catch (err) {
    console.error('Error fetching dashboard data:', err)
    error.value = err.response?.data?.error || 'Failed to load dashboard data'
    
    // Fallback to static data if API fails
    dashboardData.value = {
      greeting: 'Welcome! 🌈',
      stats: {
        total_xp: 0,
        xp_for_next_level: 500,
        learning_streak: 0,
        total_badges: 0,
        badges_this_week: 0,
        lessons_completed: 0
      },
      progress: {
        xp_progress_percent: 0
      }
    }
  } finally {
    loading.value = false
  }
}

// Load data on component mount
onMounted(() => {
  fetchDashboardData()
})



// Favorite subjects data
const favoriteSubjects = [
  {
    name: 'Mathematics',
    emoji: '🔢',
    description: 'You solved 25 problems this week!',
    progress: 85,
    bgColor: 'bg-blue-100',
    barColor: 'bg-blue-500'
  },
  {
    name: 'Science',
    emoji: '🧪',
    description: 'Completed 3 fun experiments!',
    progress: 70,
    bgColor: 'bg-green-100',
    barColor: 'bg-green-500'
  },
  {
    name: 'Reading',
    emoji: '📖',
    description: 'Read 4 amazing stories!',
    progress: 92,
    bgColor: 'bg-purple-100',
    barColor: 'bg-purple-500'
  }
]

// New skills data
const newSkills = [
  {
    name: 'Multiplication Master',
    emoji: '✖️',
    description: 'You can now multiply numbers up to 8!'
  },
  {
    name: 'Story Detective',
    emoji: '🕵️',
    description: 'Great at finding main ideas in stories!'
  },
  {
    name: 'Science Explorer',
    emoji: '🔬',
    description: 'Understanding how plants grow!'
  },
  {
    name: 'Creative Writer',
    emoji: '✍️',
    description: 'Writing amazing descriptive paragraphs!'
  }
]

// Weekly achievements data
const weeklyAchievements = [
  {
    title: 'Math Champion',
    emoji: '🏆',
    description: 'Solved 50 math problems',
    date: 'Dec 20'
  },
  {
    title: 'Reading Star',
    emoji: '⭐',
    description: 'Read 10 stories this month',
    date: 'Dec 22'
  },
  {
    title: 'Streak Master',
    emoji: '🔥',
    description: '7 days of learning in a row',
    date: 'Dec 24'
  },
  {
    title: 'Science Whiz',
    emoji: '🧬',
    description: 'Completed all experiments',
    date: 'Dec 21'
  },
  {
    title: 'Perfect Score',
    emoji: '💯',
    description: '100% on reading quiz',
    date: 'Dec 23'
  },
  {
    title: 'Helper Hero',
    emoji: '🦸',
    description: 'Helped classmates learn',
    date: 'Dec 19'
  }
]
</script>

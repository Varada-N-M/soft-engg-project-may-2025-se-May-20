<template>
  <div class="min-h-screen bg-gray-100">
    <div class="bg-gradient-to-r from-blue-500 to-purple-600 pb-32">
      <header class="py-10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-white">
            Weekly Report for {{ childName }}
          </h1>
          <p class="text-blue-200">
            Generated on {{ new Date().toLocaleDateString() }}
          </p>
        </div>
      </header>
    </div>

    <main class="-mt-24 pb-8">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Left Column -->
          <div class="lg:col-span-2 space-y-8">
            <!-- Key Metrics -->
            <section class="bg-white rounded-2xl shadow-lg p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-4">Key Metrics</h3>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-6">
                <div class="text-center">
                  <p class="text-3xl font-bold text-yellow-500">{{ stats.xpPoints }}</p>
                  <p class="text-sm text-gray-500">Total XP</p>
                </div>
                <div class="text-center">
                  <p class="text-3xl font-bold text-purple-500">{{ stats.badges }}</p>
                  <p class="text-sm text-gray-500">Badges Earned</p>
                </div>
                <div class="text-center">
                  <p class="text-3xl font-bold text-orange-500">{{ stats.streak }}</p>
                  <p class="text-sm text-gray-500">Current Streak</p>
                </div>
                <div class="text-center">
                  <p class="text-3xl font-bold text-green-500">{{ stats.completedLessons }}</p>
                  <p class="text-sm text-gray-500">Lessons Done</p>
                </div>
              </div>
            </section>

            <!-- Weekly Progress -->
            <section class="bg-white rounded-2xl shadow-lg p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-4">Weekly Progress</h3>
              <div class="space-y-4">
                <div v-for="day in weeklyProgress" :key="day.day" class="flex items-center">
                  <div class="w-16 text-gray-600 font-medium">{{ day.day }}</div>
                  <div class="flex-1 bg-gray-200 rounded-full h-6 mr-4">
                    <div class="bg-blue-500 h-6 rounded-full text-white text-xs flex items-center justify-center"
                         :style="{ width: `${day.xp / 10}%` }">
                      {{ day.xp }} XP
                    </div>
                  </div>
                  <div class="text-sm text-gray-500 w-24 text-right">{{ day.lessons }} lessons</div>
                </div>
              </div>
            </section>

            <!-- Subject Breakdown -->
            <section class="bg-white rounded-2xl shadow-lg p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-4">Subject Breakdown</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
                <div v-for="subject in subjectBreakdown" :key="subject.name"
                     class="p-4 rounded-lg" :style="{ backgroundColor: subject.color }">
                  <div class="flex items-center justify-between">
                    <h4 class="font-bold text-white">{{ subject.name }}</h4>
                    <span class="text-2xl">{{ subject.emoji }}</span>
                  </div>
                  <p class="text-white/80 text-sm mt-2">{{ subject.lessons }} lessons completed</p>
                  <p class="text-white font-bold mt-1">Avg. Score: {{ subject.avgScore }}%</p>
                </div>
              </div>
            </section>
          </div>

          <!-- Right Column -->
          <div class="space-y-8">
            <!-- Recent Achievements -->
            <section class="bg-white rounded-2xl shadow-lg p-6">
              <h3 class="text-xl font-bold text-gray-800 mb-4">Recent Achievements</h3>
              <div class="space-y-3">
                <div v-for="badge in latestBadges" :key="badge.id"
                     class="flex items-center p-3 bg-gray-100 rounded-lg">
                  <div class="text-2xl mr-3">{{ badge.emoji }}</div>
                  <div>
                    <h4 class="font-medium text-gray-800 text-sm">{{ badge.name }}</h4>
                    <p class="text-xs text-gray-600">{{ badge.description }}</p>
                  </div>
                </div>
              </div>
              <button class="mt-4 w-full text-center text-blue-600 hover:text-blue-800 text-sm font-medium">
                View All Badges
              </button>
            </section>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const childName = ref('Alex')

const stats = ref({
  xpPoints: 2450,
  badges: 12,
  streak: 7,
  completedLessons: 34,
})

const weeklyProgress = ref([
  { day: 'Mon', xp: 350, lessons: 3 },
  { day: 'Tue', xp: 500, lessons: 4 },
  { day: 'Wed', xp: 200, lessons: 2 },
  { day: 'Thu', xp: 600, lessons: 5 },
  { day: 'Fri', xp: 450, lessons: 4 },
  { day: 'Sat', xp: 800, lessons: 7 },
  { day: 'Sun', xp: 150, lessons: 1 },
])

const subjectBreakdown = ref([
  { name: 'Math', emoji: '🔢', lessons: 12, avgScore: 88, color: '#3B82F6' },
  { name: 'Reading', emoji: '📖', lessons: 10, avgScore: 92, color: '#8B5CF6' },
  { name: 'Science', emoji: '🔬', lessons: 7, avgScore: 85, color: '#10B981' },
  { name: 'History', emoji: '🏛️', lessons: 5, avgScore: 95, color: '#F59E0B' },
])

const latestBadges = ref([
  {
    id: 1,
    name: 'Math Master',
    description: 'Solved 50 math problems',
    emoji: '🧮',
  },
  {
    id: 2,
    name: 'Speed Reader',
    description: 'Read 10 books this month',
    emoji: '⚡',
  },
  {
    id: 3,
    name: 'Science Star',
    description: 'Completed 5 experiments',
    emoji: '⭐',
  },
  {
    id: 4,
    name: 'Perfect Week',
    description: 'Completed all goals for 7 days',
    emoji: '🎯',
  },
])
</script>

<style scoped>
/* Additional styles if needed */
</style>

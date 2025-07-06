<template>
  <div class="weekly-report-container">
    <div class="bg-white bg-opacity-95 backdrop-blur-sm rounded-3xl p-6 mb-6 shadow-xl mx-6">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Amazing Week, Alex!</h1>
          <p class="text-gray-600">Week of December 18-24, 2023 • You've been incredible!</p>
        </div>
        <button
          @click="$emit('back-to-dashboard')"
          class="bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-4 rounded-xl drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] transition-all duration-200 h-10"
        >
          ← Back to Dashboard
        </button>
      </div>
    </div>

    <div class="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-3xl p-6 mb-6 shadow-xl text-white mx-6">
      <div class="text-center">
        <div class="text-6xl mb-4">🌟</div>
        <h2 class="text-2xl font-bold mb-2">Superstar Achievement!</h2>
        <p class="text-lg opacity-90">You completed 12 lessons this week and earned 2 new badges!</p>
        <div class="flex justify-center gap-4 mt-4">
          <div class="bg-white bg-opacity-20 rounded-full px-4 py-2">
            <span class="text-black">7-day streak! 🔥</span>
          </div>
          <div class="bg-white bg-opacity-20 rounded-full px-4 py-2">
            <span class="text-black">380 XP earned! ⭐</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6 mx-6">
      <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] text-center">
        <div class="text-4xl mb-3">📚</div>
        <h3 class="text-3xl font-bold text-blue-600 mb-1">12</h3>
        <p class="text-gray-600 text-sm">Lessons Completed</p>
        <div class="mt-2 text-green-600 text-xs font-medium">+3 from last week!</div>
      </div>

      <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] text-center">
        <div class="text-4xl mb-3">⏰</div>
        <h3 class="text-3xl font-bold text-purple-600 mb-1">4h 32m</h3>
        <p class="text-gray-600 text-sm">Learning Time</p>
        <div class="mt-2 text-green-600 text-xs font-medium">Great focus!</div>
      </div>

      <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] text-center">
        <div class="text-4xl mb-3">🎯</div>
        <h3 class="text-3xl font-bold text-green-600 mb-1">87%</h3>
        <p class="text-gray-600 text-sm">Average Score</p>
        <div class="mt-2 text-green-600 text-xs font-medium">Excellent work!</div>
      </div>

      <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] text-center">
        <div class="text-4xl mb-3">🏅</div>
        <h3 class="text-3xl font-bold text-orange-600 mb-1">2</h3>
        <p class="text-gray-600 text-sm">New Badges</p>
        <div class="mt-2 text-orange-600 text-xs font-medium">Amazing!</div>
      </div>
    </div>

    <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] mb-6 mx-6">
      <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        📊 Your Daily Learning Journey
      </h2>
      <div class="space-y-4">
        <div v-for="day in weeklyActivity" :key="day.day" class="flex items-center gap-4">
          <div class="w-20 text-sm font-medium text-gray-600">{{ day.day }}</div>
          <div class="flex-1 bg-gray-200 rounded-full h-6 relative">
            <div
              :class="day.color"
              class="h-6 rounded-full flex items-center justify-end pr-3 text-white text-xs font-medium transition-all duration-500"
              :style="{ width: `${day.percentage}%` }"
            >
              {{ day.minutes }}m
            </div>
          </div>
          <div class="flex gap-1">
            <span v-for="starIndex in day.stars" :key="starIndex" class="text-yellow-400">⭐</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6 mx-6">
      <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)]">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          ❤️ Your Favorite Subjects
        </h2>
        <div class="space-y-4">
          <div v-for="subject in favoriteSubjects" :key="subject.name" class="flex items-center gap-4">
            <div :class="subject.bgColor" class="p-3 rounded-xl">
              <div class="text-2xl">{{ subject.emoji }}</div>
            </div>
            <div class="flex-1">
              <h3 class="font-semibold text-gray-800">{{ subject.name }}</h3>
              <p class="text-sm text-gray-600">{{ subject.description }}</p>
              <div class="flex items-center gap-2 mt-1">
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div
                    :class="subject.barColor"
                    class="h-2 rounded-full transition-all duration-500"
                    :style="{ width: `${subject.progress}%` }"
                  ></div>
                </div>
                <span class="text-xs text-gray-500 w-12">{{ subject.progress }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] mx-6">
        <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
          🔓 New Skills Unlocked
        </h2>
        <div class="space-y-3">
          <div v-for="skill in newSkills" :key="skill.name" class="flex items-center gap-3 p-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl">
            <div class="text-2xl">{{ skill.emoji }}</div>
            <div>
              <h4 class="font-medium text-gray-800">{{ skill.name }}</h4>
              <p class="text-xs text-gray-600">{{ skill.description }}</p>
            </div>
            <div class="ml-auto">
              <div class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                New!
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-white bg-opacity-90 backdrop-blur-sm rounded-2xl p-6 drop-shadow-[0_0_12px_rgba(0,0,0,0.15)] mb-6 mx-6">
      <h2 class="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        🏆 This Week's Achievements
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="achievement in weeklyAchievements" :key="achievement.title" class="bg-gradient-to-br from-yellow-100 to-orange-100 rounded-xl p-4 border-2 border-yellow-200">
          <div class="text-center">
            <div class="text-4xl mb-2">{{ achievement.emoji }}</div>
            <h3 class="font-bold text-gray-800 mb-1">{{ achievement.title }}</h3>
            <p class="text-sm text-gray-600">{{ achievement.description }}</p>
            <div class="mt-2 bg-yellow-200 text-yellow-800 px-3 py-1 rounded-full text-xs font-medium inline-block">
              {{ achievement.date }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="bg-gradient-to-r from-pink-400 to-purple-500 rounded-3xl p-6 shadow-xl text-white text-center mx-6 mb-6">
      <div class="text-5xl mb-4">🎉</div>
      <h2 class="text-2xl font-bold mb-2">Keep Up the Amazing Work!</h2>
      <p class="text-lg opacity-90 mb-4">You're doing fantastic, Alex! Your dedication to learning is inspiring.</p>
      <div class="flex justify-center gap-4">
        <button class="text-black bg-white bg-opacity-20 hover:bg-opacity-30 px-6 py-2 rounded-full font-medium transition-all duration-200">
          Set New Goals 🎯
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'; // ref is imported, which is good.

// Emits are used to communicate from child to parent components
// This allows the parent component (e.g., your main dashboard) to know
// when the "Back to Dashboard" button is clicked.
const emit = defineEmits(['back-to-dashboard']);

// Weekly activity data
const weeklyActivity = [
  { day: 'Mon', minutes: 65, percentage: 85, stars: 3, color: 'bg-gradient-to-r from-blue-400 to-blue-600' },
  { day: 'Tue', minutes: 72, percentage: 95, stars: 3, color: 'bg-gradient-to-r from-green-400 to-green-600' },
  { day: 'Wed', minutes: 45, percentage: 60, stars: 2, color: 'bg-gradient-to-r from-yellow-400 to-yellow-600' },
  { day: 'Thu', minutes: 80, percentage: 100, stars: 3, color: 'bg-gradient-to-r from-purple-400 to-purple-600' },
  { day: 'Fri', minutes: 58, percentage: 75, stars: 3, color: 'bg-gradient-to-r from-pink-400 to-pink-600' },
  { day: 'Sat', minutes: 35, percentage: 45, stars: 2, color: 'bg-gradient-to-r from-orange-400 to-orange-600' },
  { day: 'Sun', minutes: 42, percentage: 55, stars: 2, color: 'bg-gradient-to-r from-indigo-400 to-indigo-600' }
];

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
];

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
];

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
];
</script>
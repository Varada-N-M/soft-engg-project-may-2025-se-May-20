<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-purple-600">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <button @click="$router.go(-1)" class="mr-4 p-2 rounded-full hover:bg-gray-100 transition-colors">
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <div class="flex items-center">
              <span class="text-3xl mr-3">🌟</span>
              <div>
                <h1 class="text-2xl font-bold text-gray-800 font-fancy">My Habits</h1>
                <p class="text-gray-600 text-sm">Build amazing habits!</p>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-6 text-gray-800">
            <div class="text-center">
              <div class="text-2xl font-bold">{{ completedToday }}</div>
              <div class="text-sm text-gray-600">Completed</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold">{{ totalHabits }}</div>
              <div class="text-sm text-gray-600">Total</div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Progress Section -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-gray-800">🎯 Daily Progress</h2>
            <div class="flex items-center space-x-2">
              <span class="text-2xl">🔥</span>
              <span class="text-lg font-bold text-orange-600">{{ currentStreak }} day streak!</span>
            </div>
          </div>
          
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>{{ completedToday }} of {{ totalHabits }} habits completed today</span>
              <span>{{ Math.round((completedToday / totalHabits) * 100) }}% Complete</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div 
                class="bg-gradient-to-r from-green-400 to-blue-500 h-3 rounded-full transition-all duration-500"
                :style="{ width: `${(completedToday / totalHabits) * 100}%` }"
              ></div>
            </div>
          </div>

          <!-- Streak Milestones -->
          <div class="grid grid-cols-4 gap-4">
            <div 
              v-for="milestone in streakMilestones" 
              :key="milestone.days"
              class="text-center p-3 rounded-xl transition-all duration-200"
              :class="currentStreak >= milestone.days ? 'bg-green-100 border-2 border-green-300' : 'bg-gray-100 border-2 border-gray-200'"
            >
              <div class="text-2xl mb-1">{{ milestone.emoji }}</div>
              <div class="text-sm font-medium text-gray-800">{{ milestone.days }} Days</div>
              <div class="text-xs text-gray-600">{{ milestone.title }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="mb-8 flex flex-wrap gap-4">
        <button 
          @click="showCreateModal = true"
          class="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center"
        >
          <span class="text-xl mr-2">➕</span>
          Create New Habit
        </button>
        
        <button 
          @click="currentFilter = currentFilter === 'all' ? 'active' : 'all'"
          class="bg-white/90 backdrop-blur-sm text-gray-800 px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center border border-white/20"
        >
          <span class="text-xl mr-2">🔍</span>
          {{ currentFilter === 'all' ? 'Show Active Only' : 'Show All' }}
        </button>
      </div>

      <!-- Category Filters -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-4 shadow-xl border border-white/20">
          <div class="flex flex-wrap gap-3">
            <button
              v-for="category in categories"
              :key="category.id"
              @click="selectedCategory = category.id"
              class="px-4 py-2 rounded-xl font-medium transition-all duration-200 flex items-center"
              :class="selectedCategory === category.id 
                ? 'bg-blue-500 text-white shadow-lg' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            >
              <span class="mr-2">{{ category.emoji }}</span>
              {{ category.name }}
              <span class="ml-2 text-sm opacity-75">{{ getCategoryCount(category.id) }}</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Habits Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="habit in filteredHabits"
          :key="habit.id"
          class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform hover:scale-105 transition-all duration-200"
          :class="habit.completedToday ? 'ring-2 ring-green-400' : ''"
        >
          <!-- Habit Header -->
          <div class="flex items-start justify-between mb-4">
            <div class="flex items-center">
              <div class="text-3xl mr-3">{{ habit.emoji }}</div>
              <div>
                <h3 class="font-bold text-gray-800 text-lg">{{ habit.name }}</h3>
                <p class="text-sm text-gray-600">{{ habit.description }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <button 
                @click="editHabit(habit)"
                class="p-2 rounded-full hover:bg-gray-100 transition-colors"
              >
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Progress Info -->
          <div class="mb-4">
            <div class="flex justify-between text-sm text-gray-600 mb-2">
              <span>{{ habit.currentStreak }} day streak</span>
              <span class="flex items-center">
                <span class="text-yellow-500 mr-1">⭐</span>
                {{ habit.xpReward }} XP
              </span>
            </div>
            
            <!-- Weekly Progress -->
            <div class="flex space-x-1 mb-3">
              <div
                v-for="(day, index) in habit.weeklyProgress"
                :key="index"
                class="flex-1 h-2 rounded-full"
                :class="day ? 'bg-green-400' : 'bg-gray-200'"
              ></div>
            </div>
          </div>

          <!-- Action Button -->
          <button
            @click="toggleHabit(habit)"
            class="w-full py-3 rounded-2xl font-medium transition-all duration-200 flex items-center justify-center"
            :class="habit.completedToday 
              ? 'bg-green-500 text-white shadow-lg' 
              : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg hover:shadow-xl transform hover:scale-105'"
            :disabled="habit.completedToday"
          >
            <span class="text-xl mr-2">{{ habit.completedToday ? '✅' : '🎯' }}</span>
            {{ habit.completedToday ? 'Completed Today!' : 'Mark as Done' }}
          </button>

          <!-- Stats -->
          <div class="mt-4 grid grid-cols-3 gap-4 text-center">
            <div>
              <div class="text-lg font-bold text-blue-600">{{ habit.totalCompleted }}</div>
              <div class="text-xs text-gray-500">Total</div>
            </div>
            <div>
              <div class="text-lg font-bold text-orange-600">{{ habit.currentStreak }}</div>
              <div class="text-xs text-gray-500">Streak</div>
            </div>
            <div>
              <div class="text-lg font-bold text-green-600">{{ habit.bestStreak }}</div>
              <div class="text-xs text-gray-500">Best</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create/Edit Modal -->
      <div v-if="showCreateModal || editingHabit" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-3xl p-6 w-full max-w-md shadow-2xl">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-bold text-gray-800">
              {{ editingHabit ? 'Edit Habit' : 'Create New Habit' }}
            </h3>
            <button 
              @click="closeModal"
              class="p-2 rounded-full hover:bg-gray-100 transition-colors"
            >
              <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>

          <form @submit.prevent="saveHabit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Habit Name</label>
              <input
                v-model="habitForm.name"
                type="text"
                class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Brush my teeth"
                required
              >
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
              <textarea
                v-model="habitForm.description"
                class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Why is this habit important?"
                rows="3"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Choose an Emoji</label>
              <div class="grid grid-cols-6 gap-2">
                <button
                  v-for="emoji in availableEmojis"
                  :key="emoji"
                  type="button"
                  @click="habitForm.emoji = emoji"
                  class="p-3 text-2xl rounded-xl border-2 transition-all duration-200"
                  :class="habitForm.emoji === emoji ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
                >
                  {{ emoji }}
                </button>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                v-model="habitForm.category"
                class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Select a category</option>
                <option v-for="category in categories.slice(1)" :key="category.id" :value="category.id">
                  {{ category.emoji }} {{ category.name }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">XP Reward</label>
              <select
                v-model="habitForm.xpReward"
                class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option :value="10">10 XP - Easy habit</option>
                <option :value="25">25 XP - Medium habit</option>
                <option :value="50">50 XP - Hard habit</option>
              </select>
            </div>

            <div class="flex space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="flex-1 py-3 px-4 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-200"
              >
                {{ editingHabit ? 'Update' : 'Create' }} Habit
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// Reactive data
const showCreateModal = ref(false)
const editingHabit = ref(null)
const currentFilter = ref('all')
const selectedCategory = ref('all')
const currentStreak = ref(7)

// Form data
const habitForm = ref({
  name: '',
  description: '',
  emoji: '🎯',
  category: '',
  xpReward: 25
})

// Categories
const categories = ref([
  { id: 'all', name: 'All Habits', emoji: '🌟' },
  { id: 'health', name: 'Health', emoji: '💪' },
  { id: 'learning', name: 'Learning', emoji: '📚' },
  { id: 'chores', name: 'Chores', emoji: '🏠' },
  { id: 'social', name: 'Social', emoji: '👥' },
  { id: 'creative', name: 'Creative', emoji: '🎨' }
])

// Available emojis for habits
const availableEmojis = ref([
  '🦷', '🚿', '📚', '🏃', '🥗', '💧', '🧘', '🎵', '🎨', '🧹', 
  '🛏️', '🌱', '⚽', '🎯', '📝', '🎮', '🍎', '🚴', '🏊', '🎪'
])

// Streak milestones
const streakMilestones = ref([
  { days: 3, emoji: '🌱', title: 'Getting Started' },
  { days: 7, emoji: '🔥', title: 'On Fire' },
  { days: 21, emoji: '💎', title: 'Diamond' },
  { days: 50, emoji: '👑', title: 'Habit King' }
])

// Sample habits data
const habits = ref([
  {
    id: 1,
    name: 'Brush My Teeth',
    description: 'Keep my teeth clean and healthy',
    emoji: '🦷',
    category: 'health',
    xpReward: 10,
    completedToday: true,
    currentStreak: 7,
    bestStreak: 12,
    totalCompleted: 45,
    weeklyProgress: [true, true, true, true, true, true, true]
  },
  {
    id: 2,
    name: 'Read for 20 Minutes',
    description: 'Improve my reading skills daily',
    emoji: '📚',
    category: 'learning',
    xpReward: 25,
    completedToday: false,
    currentStreak: 5,
    bestStreak: 8,
    totalCompleted: 32,
    weeklyProgress: [true, true, false, true, true, true, false]
  },
  {
    id: 3,
    name: 'Exercise',
    description: 'Stay active and strong',
    emoji: '🏃',
    category: 'health',
    xpReward: 50,
    completedToday: false,
    currentStreak: 3,
    bestStreak: 10,
    totalCompleted: 28,
    weeklyProgress: [false, true, true, true, false, true, false]
  },
  {
    id: 4,
    name: 'Make My Bed',
    description: 'Start the day organized',
    emoji: '🛏️',
    category: 'chores',
    xpReward: 10,
    completedToday: true,
    currentStreak: 4,
    bestStreak: 15,
    totalCompleted: 38,
    weeklyProgress: [true, true, true, true, false, true, true]
  },
  {
    id: 5,
    name: 'Practice Piano',
    description: 'Improve my musical skills',
    emoji: '🎵',
    category: 'creative',
    xpReward: 25,
    completedToday: false,
    currentStreak: 2,
    bestStreak: 6,
    totalCompleted: 18,
    weeklyProgress: [false, true, true, false, false, true, false]
  },
  {
    id: 6,
    name: 'Drink Water',
    description: 'Stay hydrated throughout the day',
    emoji: '💧',
    category: 'health',
    xpReward: 10,
    completedToday: true,
    currentStreak: 6,
    bestStreak: 14,
    totalCompleted: 42,
    weeklyProgress: [true, true, true, true, true, true, false]
  }
])

// Computed properties
const totalHabits = computed(() => habits.value.length)
const completedToday = computed(() => habits.value.filter(h => h.completedToday).length)

const filteredHabits = computed(() => {
  let filtered = habits.value

  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(h => h.category === selectedCategory.value)
  }

  if (currentFilter.value === 'active') {
    filtered = filtered.filter(h => !h.completedToday)
  }

  return filtered
})

// Methods
const getCategoryCount = (categoryId) => {
  if (categoryId === 'all') return habits.value.length
  return habits.value.filter(h => h.category === categoryId).length
}

const toggleHabit = (habit) => {
  if (!habit.completedToday) {
    habit.completedToday = true
    habit.currentStreak += 1
    habit.totalCompleted += 1
    if (habit.currentStreak > habit.bestStreak) {
      habit.bestStreak = habit.currentStreak
    }
    
    // Show XP gained animation (you can implement this)
    showXPGained(habit.xpReward)
  }
}

const showXPGained = (xp) => {
  // Implement XP gained animation/notification
  console.log(`+${xp} XP gained!`)
}

const editHabit = (habit) => {
  editingHabit.value = habit
  habitForm.value = {
    name: habit.name,
    description: habit.description,
    emoji: habit.emoji,
    category: habit.category,
    xpReward: habit.xpReward
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingHabit.value = null
  habitForm.value = {
    name: '',
    description: '',
    emoji: '🎯',
    category: '',
    xpReward: 25
  }
}

const saveHabit = () => {
  if (editingHabit.value) {
    // Update existing habit
    const habit = editingHabit.value
    habit.name = habitForm.value.name
    habit.description = habitForm.value.description
    habit.emoji = habitForm.value.emoji
    habit.category = habitForm.value.category
    habit.xpReward = habitForm.value.xpReward
  } else {
    // Create new habit
    const newHabit = {
      id: Date.now(),
      name: habitForm.value.name,
      description: habitForm.value.description,
      emoji: habitForm.value.emoji,
      category: habitForm.value.category,
      xpReward: habitForm.value.xpReward,
      completedToday: false,
      currentStreak: 0,
      bestStreak: 0,
      totalCompleted: 0,
      weeklyProgress: [false, false, false, false, false, false, false]
    }
    habits.value.push(newHabit)
  }
  
  closeModal()
}

onMounted(() => {
  // Initialize any data or API calls here
})
</script>

<style scoped>
.font-fancy {
  font-family: 'Comic Sans MS', cursive, sans-serif;
}
</style>
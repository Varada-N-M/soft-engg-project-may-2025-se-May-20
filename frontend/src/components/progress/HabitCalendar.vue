<template>
  <div class="habit-calendar">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-800">Habit Tracking</h3>
      <p class="text-sm text-gray-600">{{ habits.length }} habits tracked</p>
    </div>

    <div v-if="habits.length === 0" class="text-center py-8">
      <div class="text-gray-400 mb-2">📅</div>
      <p class="text-gray-500">No habits tracked yet</p>
    </div>

    <div v-else class="space-y-6">
      <div v-for="habit in habits" :key="habit.habit_id" class="habit-section">
        <div class="flex items-center justify-between mb-3">
          <div>
            <h4 class="font-semibold text-gray-700">{{ habit.name }}</h4>
            <p class="text-sm text-gray-500">{{ habit.description }}</p>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium text-gray-600">
              {{ habit.total_completions || 0 }} completions
            </div>
            <div class="text-xs text-gray-400">+{{ habit.habit_xp }} XP each</div>
          </div>
        </div>

        <!-- Calendar grid for last 30 days -->
        <div class="calendar-grid">
          <div class="grid grid-cols-10 gap-1">
            <div 
              v-for="day in getLast30Days()" 
              :key="day.date"
              class="calendar-day"
              :class="getDayClass(day, habit)"
              :title="formatDayTitle(day)"
            >
              <div class="text-xs">{{ day.day }}</div>
            </div>
          </div>
        </div>

        <!-- Legend -->
        <div class="flex items-center space-x-4 mt-2 text-xs text-gray-500">
          <div class="flex items-center space-x-1">
            <div class="w-3 h-3 bg-green-500 rounded"></div>
            <span>Completed</span>
          </div>
          <div class="flex items-center space-x-1">
            <div class="w-3 h-3 bg-gray-300 rounded"></div>
            <span>Not completed</span>
          </div>
          <div class="flex items-center space-x-1">
            <div class="w-3 h-3 bg-gray-100 rounded border"></div>
            <span>No data</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  habits: {
    type: Array,
    required: true,
    default: () => []
  }
})

const getLast30Days = () => {
  const days = []
  const today = new Date()
  
  for (let i = 29; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(today.getDate() - i)
    
    days.push({
      date: date.toISOString().split('T')[0],
      day: date.getDate(),
      dayName: date.toLocaleDateString('en-US', { weekday: 'short' })
    })
  }
  
  return days
}

const getDayClass = (day, habit) => {
  const completion = habit.completion_history?.find(c => c.completion_date === day.date)
  
  if (!completion) {
    return 'bg-gray-100 border border-gray-200'
  }
  
  return completion.is_done 
    ? 'bg-green-500 text-white' 
    : 'bg-gray-300'
}

const formatDayTitle = (day) => {
  return `${day.dayName}, ${new Date(day.date).toLocaleDateString()}`
}
</script>

<style scoped>
@reference '@/css/index.css';
.habit-calendar {
  @apply bg-white p-4 rounded-lg border border-gray-200;
}

.habit-section {
  @apply pb-4 border-b border-gray-100 last:border-b-0;
}

.calendar-grid {
  @apply bg-gray-50 p-2 rounded;
}

.calendar-day {
  @apply w-8 h-8 rounded flex items-center justify-center text-xs font-medium transition-colors cursor-pointer;
}

.calendar-day:hover {
  @apply scale-110;
}
</style>
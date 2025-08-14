<template>
  <div class="skill-progress-card">
    <div class="mb-4">
      <h3 class="text-lg font-semibold text-gray-800">Life Skills Progress</h3>
      <p class="text-sm text-gray-600">{{ totalCompleted }}/{{ totalSkills }} skills completed</p>
    </div>

    <div v-if="Object.keys(skillsByType).length === 0" class="text-center py-8">
      <div class="text-gray-400 mb-2">📚</div>
      <p class="text-gray-500">No skills data available</p>
    </div>

    <div v-else class="space-y-6">
      <div v-for="(skills, skillType) in skillsByType" :key="skillType" class="skill-type-section">
        <div class="flex items-center justify-between mb-3">
          <h4 class="font-semibold text-gray-700 capitalize">{{ skillType }}</h4>
          <span class="text-sm text-gray-500">
            {{ getCompletedCount(skills) }}/{{ skills.length }}
          </span>
        </div>

        <!-- Progress bar for this skill type -->
        <div class="mb-3">
          <div class="w-full bg-gray-200 rounded-full h-2">
            <div 
              class="h-2 bg-blue-500 rounded-full transition-all duration-300"
              :style="`width: ${getProgressPercentage(skills)}%`"
            ></div>
          </div>
        </div>

        <!-- Individual skills list -->
        <div v-if="showDetails" class="grid grid-cols-1 md:grid-cols-2 gap-2">
          <div 
            v-for="skill in skills" 
            :key="skill.skill_id"
            class="flex items-center p-2 bg-gray-50 rounded text-sm"
            :class="{
              'bg-green-50 border border-green-200': skill.is_completed,
              'bg-gray-50': !skill.is_completed
            }"
          >
            <div class="mr-2">
              {{ skill.is_completed ? '✅' : '⭕' }}
            </div>
            <div class="flex-1">
              <div class="font-medium">{{ skill.skill_name }}</div>
              <div class="text-xs text-gray-500">+{{ skill.skill_xp }} XP</div>
            </div>
            <div v-if="skill.is_completed && skill.completion_date" class="text-xs text-gray-400">
              {{ formatDate(skill.completion_date) }}
            </div>
          </div>
        </div>

        <button 
          v-if="skills.length > 6"
          @click="showDetails = !showDetails"
          class="text-sm text-blue-500 hover:text-blue-600 mt-2"
        >
          {{ showDetails ? 'Show Less' : `Show All ${skills.length} Skills` }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  skillsByType: {
    type: Object,
    required: true,
    default: () => ({})
  }
})

const showDetails = ref(false)

const totalSkills = computed(() => {
  return Object.values(props.skillsByType).reduce((sum, skills) => sum + skills.length, 0)
})

const totalCompleted = computed(() => {
  return Object.values(props.skillsByType).reduce((sum, skills) => {
    return sum + skills.filter(skill => skill.is_completed).length
  }, 0)
})

const getCompletedCount = (skills) => {
  return skills.filter(skill => skill.is_completed).length
}

const getProgressPercentage = (skills) => {
  if (skills.length === 0) return 0
  return (getCompletedCount(skills) / skills.length) * 100
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric' 
  })
}
</script>

<style scoped>
@reference '@/css/index.css';
.skill-progress-card {
  @apply bg-white p-4 rounded-lg border border-gray-200;
}

.skill-type-section {
  @apply pb-4 border-b border-gray-100 last:border-b-0;
}
</style>
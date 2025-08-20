<template>
  <div class="min-h-screen bg-gray-100 page-font">
    <!-- Parent Navbar -->
    <ParentNavbar page-title="My Children"/>
    
    <!-- Main Content -->
    <div class="child-progress-page pt-16">
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
            {{ childData?.child ? `${childData.child.name}'s Progress` : 'Child Progress' }}
          </h1>
          <p class="text-gray-600">Detailed progress tracking and learning journey</p>
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
    <div v-else-if="childData">
      <!-- Progress Summary -->
      <ProgressSummary 
        :summary="progressSummary"
        :student-name="`${childData.child.first_name} ${childData.child.last_name}`"
        :weekly-stats="childData.weekly_stats"
        class="mb-6"
      />

      <!-- Tabs -->
      <div class="mb-6">
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8">
            <button 
              v-for="tab in tabs" 
              :key="tab.id"
              @click="activeTab = tab.id"
              class="py-2 px-1 border-b-2 font-medium text-sm transition-colors"
              :class="{
                'border-blue-500 text-blue-600': activeTab === tab.id,
                'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300': activeTab !== tab.id
              }"
            >
              {{ tab.label }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'" class="space-y-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <SkillProgressCard :skills-by-type="childData.skills_by_type || {}" />
            <BadgeGallery :badges="childData.badges || []" />
          </div>
          
          <!-- Weekly Todo Summary -->
          <div v-if="childData.weekly_todos" class="bg-white rounded-lg border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">This Week's Tasks</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="text-center p-4 bg-green-50 rounded-lg">
                <div class="text-3xl font-bold text-green-600">{{ childData.weekly_todos.completed || 0 }}</div>
                <div class="text-sm text-green-700">Completed Tasks</div>
              </div>
              <div class="text-center p-4 bg-blue-50 rounded-lg">
                <div class="text-3xl font-bold text-blue-600">{{ childData.weekly_todos.pending || 0 }}</div>
                <div class="text-sm text-blue-700">Pending Tasks</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Skills Tab -->
        <div v-else-if="activeTab === 'skills'">
          <SkillProgressCard 
            :skills-by-type="childData.skills_by_type || {}" 
            class="mb-6"
          />
          
          <!-- Detailed Skills List -->
          <div class="bg-white rounded-lg border border-gray-200 p-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">All Skills</h3>
            <div v-if="!childData.skills_by_type || Object.keys(childData.skills_by_type).length === 0" class="text-center py-8">
              <p class="text-gray-500">No skills data available</p>
            </div>
            <div v-else class="space-y-6">
              <div v-for="(skills, type) in childData.skills_by_type" :key="type">
                <h4 class="font-medium text-gray-700 capitalize mb-3">{{ type }}</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  <div 
                    v-for="skill in skills" 
                    :key="skill.skill_id"
                    class="skill-item"
                    :class="{
                      'bg-green-50 border-green-200': skill.is_completed,
                      'bg-gray-50 border-gray-200': !skill.is_completed
                    }"
                  >
                    <div class="flex items-center space-x-3">
                      <div class="text-lg">
                        {{ skill.is_completed ? '✅' : '⭕' }}
                      </div>
                      <div class="flex-1">
                        <div class="font-medium text-sm">{{ skill.skill_name }}</div>
                        <div class="text-xs text-gray-500">+{{ skill.skill_xp }} XP</div>
                        <div v-if="skill.completion_date" class="text-xs text-gray-400">
                          Completed: {{ formatDate(skill.completion_date) }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Habits Tab -->
        <div v-else-if="activeTab === 'habits'">
          <HabitCalendar :habits="childData.habits || []" />
        </div>

        <!-- Badges Tab -->
        <div v-else-if="activeTab === 'badges'">
          <BadgeGallery :badges="childData.badges || []" />
        </div>

        <!-- Tasks Tab -->
        <div v-else-if="activeTab === 'tasks'">
          <div class="bg-white rounded-lg border border-gray-200 p-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Weekly Tasks</h3>
            
            <div v-if="!childData.todos || childData.todos.length === 0" class="text-center py-8">
              <div class="text-gray-400 text-6xl mb-4">📝</div>
              <h3 class="text-lg font-semibold text-gray-800 mb-2">No Tasks Yet</h3>
              <p class="text-gray-600">Your child will get weekly tasks from their teacher</p>
            </div>

            <div v-else class="space-y-4">
              <div 
                v-for="todo in childData.todos" 
                :key="todo.todo_id"
                class="p-4 rounded-lg border"
                :class="{
                  'bg-green-50 border-green-200': todo.is_completed,
                  'bg-yellow-50 border-yellow-200': !todo.is_completed
                }"
              >
                <div class="flex items-start space-x-3">
                  <div class="mt-0.5">
                    {{ todo.is_completed ? '✅' : '📋' }}
                  </div>
                  <div class="flex-1">
                    <h4 class="font-medium text-gray-800">{{ todo.task }}</h4>
                    <p v-if="todo.description" class="text-sm text-gray-600 mt-1">{{ todo.description }}</p>
                    <div class="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                      <span>+{{ todo.xp_reward }} XP</span>
                      <span v-if="todo.due_date">Due: {{ formatDate(todo.due_date) }}</span>
                      <span v-if="todo.completion_date" class="text-green-600">
                        Completed: {{ formatDate(todo.completion_date) }}
                      </span>
                    </div>
                  </div>
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/plugins/axios.ts'
import ProgressSummary from '@/components/progress/ProgressSummary.vue'
import SkillProgressCard from '@/components/progress/SkillProgressCard.vue'
import BadgeGallery from '@/components/progress/BadgeGallery.vue'
import HabitCalendar from '@/components/progress/HabitCalendar.vue'
import ParentNavbar from "@/components/partials/ParentNavbar.vue";

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const error = ref('')
const childData = ref(null)
const activeTab = ref('overview')

const tabs = [
  { id: 'overview', label: 'Overview' },
  { id: 'skills', label: 'Skills' },
  { id: 'habits', label: 'Habits' },
  { id: 'badges', label: 'Badges' },
  { id: 'tasks', label: 'Tasks' }
]

const progressSummary = computed(() => {
  if (!childData.value) return {}
  
  return {
    xp_points: childData.value.child?.xp_points || 0,
    streak: childData.value.child?.streak || 0,
    total_skills: childData.value.total_skills || 0,
    completed_skills: childData.value.completed_skills || 0,
    total_badges: childData.value.total_badges || 0
  }
})

const fetchChildProgress = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const childId = route.params.childId
    
    // Fetch all child data in parallel
    const [skillsResponse, habitsResponse, badgesResponse, todosResponse, weeklyResponse] = await Promise.all([
      api.get(`/api/parent/children/${childId}/skills`),
      api.get(`/api/parent/children/${childId}/habits`),
      api.get(`/api/parent/children/${childId}/badges`),
      api.get(`/api/parent/children/${childId}/todos`),
      api.get(`/api/parent/children/${childId}/weekly-report`)
    ])
    
    // Combine all data
    childData.value = {
      child: badgesResponse.data.child, // Get child info from badges API
      total_skills: skillsResponse.data.total_skills,
      completed_skills: skillsResponse.data.completed_skills,
      total_badges: badgesResponse.data.badges?.length || 0,
      skills_by_type: skillsResponse.data.skills_by_type,
      habits: habitsResponse.data.habits,
      badges: badgesResponse.data.badges,
      todos: todosResponse.data.todos,
      weekly_stats: weeklyResponse.data.weekly_stats,
      weekly_todos: {
        completed: todosResponse.data.todos?.filter(t => t.is_completed).length || 0,
        pending: todosResponse.data.todos?.filter(t => !t.is_completed).length || 0
      }
    }
    
  } catch (err) {
    console.error('Error fetching child progress:', err)
    error.value = err.response?.data?.error || 'Failed to load child progress data'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/parent/home')
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
  fetchChildProgress()
})
</script>

<style scoped>
@reference '@/css/index.css';
.child-progress-page {
  @apply p-6 min-h-screen bg-gray-50;
}

.skill-item {
  @apply p-3 border rounded-lg transition-colors;
}

.tab-content {
  @apply min-h-96;
}
</style>
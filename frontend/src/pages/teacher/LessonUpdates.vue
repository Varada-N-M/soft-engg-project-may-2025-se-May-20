<template>
  <div class="min-h-screen ">
    <!-- Navbar -->
    <TeacherNavbar />

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Error Alert -->
      <div v-if="error" class="mb-6">
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg flex items-center justify-between">
          <div class="flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>{{ error }}</span>
          </div>
          <button @click="error = ''" class="text-red-700 hover:text-red-900">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Success Alert -->
      <div v-if="successMessage" class="mb-6">
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg flex items-center justify-between">
          <div class="flex items-center">
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <span>{{ successMessage }}</span>
          </div>
          <button @click="successMessage = ''" class="text-green-700 hover:text-green-900">
            <XIcon class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading && (!lessons || lessons.length === 0)" class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-8 shadow-xl border border-white/20 text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p class="text-gray-600">Loading your lessons...</p>
        </div>
      </div>

      <!-- Filters Section -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
          <h3 class="text-lg font-bold text-gray-800 mb-4">🔍 Filter Lessons</h3>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <!-- Date Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Filter by Created Date</label>
              <input
                v-model="filters.date"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                @change="applyFilters"
              />
            </div>

            <!-- Subject Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Filter by Subject</label>
              <select 
                v-model="filters.subject" 
                @change="applyFilters"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Subjects</option>
                <option value="Math">Math</option>
                <option value="English">English</option>
                <option value="Science">Science</option>
                <option value="Social Studies">Social Studies</option>
                <option value="Computers">Computers</option>
              </select>
            </div>

            <!-- Class Filter -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Filter by Class</label>
              <select 
                v-model="filters.class" 
                @change="applyFilters"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">All Classes</option>
                <option v-for="n in 12" :key="n" :value="n">Class {{ n }}</option>
              </select>
            </div>

            <!-- Clear Filters Button -->
            <div class="flex items-end">
              <button 
                @click="clearFilters"
                class="w-full px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                Clear Filters
              </button>
            </div>
          </div>
          
          <!-- Filter Results Summary -->
          <div class="mt-4 text-sm text-gray-600">
            Showing {{ filteredLessons.length }} of {{ allLessons.length }} lessons
          </div>
        </div>
      </div>

      <!-- Progress Overview -->
      <div v-if="!loading && lessons && lessons.length > 0" class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
          <div class="flex flex-col md:flex-row items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-bold text-gray-800 mb-2">Your Lesson Updates</h2>
              <p class="text-gray-600">{{ filteredLessons?.length || 0 }} lessons found</p>
            </div>
            <div class="text-6xl animate-bounce">🎓</div>
          </div>
          
          <!-- Quick Stats -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div class="text-center p-3 bg-blue-50 rounded-lg">
              <p class="text-2xl font-bold text-blue-600">{{ lessons?.length || 0 }}</p>
              <p class="text-sm text-gray-600">Total Lessons</p>
            </div>
            <div class="text-center p-3 bg-green-50 rounded-lg">
              <p class="text-2xl font-bold text-green-600">{{ uniqueSubjects?.length || 0 }}</p>
              <p class="text-sm text-gray-600">Subjects</p>
            </div>
            <div class="text-center p-3 bg-purple-50 rounded-lg">
              <p class="text-2xl font-bold text-purple-600">{{ uniqueClasses?.length || 0 }}</p>
              <p class="text-sm text-gray-600">Classes</p>
            </div>
          </div>

          <!-- Subjects Covered -->
          <div class="flex flex-wrap gap-2 mt-2">
            <span v-for="subject in uniqueSubjects" :key="subject" class="inline-flex items-center px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-medium">
              {{ subject }}
            </span>
          </div>
        </div>
      </div>

      <!-- Lessons Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(lesson, index) in filteredLessons"
          :key="index"
          class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 relative overflow-hidden group"
        >
          <!-- Action Buttons -->
          <div class="absolute top-3 right-3 flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-20">
            <!-- Edit Button -->
            <button
              @click="editLesson(index)"
              class="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors"
              title="Edit lesson"
            >
              <EditIcon class="w-4 h-4" />
            </button>
            <!-- Delete Button -->
            <button
              @click="deleteLesson(index)"
              class="p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
              title="Delete lesson"
            >
              <Trash2Icon class="w-4 h-4" />
            </button>
          </div>
          
          <!-- Decorative Icon -->
          <div class="absolute -top-4 -right-4 text-5xl opacity-20 select-none pointer-events-none">
            <span v-if="lesson.subject === 'Math'">🧮</span>
            <span v-else-if="lesson.subject === 'English'">📖</span>
            <span v-else-if="lesson.subject === 'Science'">🔬</span>
            <span v-else-if="lesson.subject === 'Social Studies'">🌍</span>
            <span v-else-if="lesson.subject === 'Computers'">💻</span>
            <span v-else>📚</span>
          </div>
          <div class="relative z-10">
            <div class="flex items-center mb-2 flex-wrap gap-2">
              <span class="inline-block px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-semibold">{{ lesson.day }}</span>
              <span class="inline-block px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-semibold">{{ lesson.subject }}</span>
              <span class="inline-block px-3 py-1 rounded-full bg-purple-100 text-purple-700 text-xs font-semibold">Class {{ lesson.class }}</span>
            </div>
            <h3 class="font-bold text-gray-800 mb-2 text-lg">{{ lesson.lesson }}</h3>
            <p class="text-sm text-gray-600 mb-2">{{ lesson.activity }}</p>
            <div class="flex items-center text-xs text-gray-500 mt-2">
              <span class="mr-1">📅</span>
              <span>Created: {{ formatDate(lesson.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && filteredLessons && filteredLessons.length === 0" class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">No lessons found</h3>
        <p class="text-gray-600">No lesson updates available. Click the + button to create your first lesson!</p>
      </div>
    </main>

    <!-- Floating Action Button -->
    <button
      @click="showAddModal = true"
      class="fixed bottom-8 right-8 w-16 h-16 bg-gradient-to-r from-blue-500 to-green-500 text-white rounded-full shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-200 z-50 flex items-center justify-center"
      title="Add new lesson"
    >
      <PlusIcon class="w-8 h-8" />
    </button>

    <!-- Add Lesson Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold text-gray-800">Add New Lesson</h3>
          <button
            @click="showAddModal = false"
            class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XIcon class="w-6 h-6" />
          </button>
        </div>
        
        <form @submit.prevent="addLesson" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Day</label>
            <select v-model="newLesson.day" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="Monday">Monday</option>
              <option value="Tuesday">Tuesday</option>
              <option value="Wednesday">Wednesday</option>
              <option value="Thursday">Thursday</option>
              <option value="Friday">Friday</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
            <select v-model="newLesson.subject" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="Math">Math</option>
              <option value="English">English</option>
              <option value="Science">Science</option>
              <option value="Social Studies">Social Studies</option>
              <option value="Computers">Computers</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Class/Grade</label>
            <select v-model="newLesson.class_" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option v-for="n in 12" :key="n" :value="n">Class {{ n }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Lesson Title</label>
            <input
              v-model="newLesson.lesson"
              type="text"
              placeholder="Enter lesson title"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Activity Description</label>
            <textarea
              v-model="newLesson.activity"
              placeholder="Describe the activity or lesson content"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            ></textarea>
          </div>
          
          <div class="flex space-x-3 pt-4">
            <button
              type="button"
              @click="showAddModal = false"
              class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-green-500 text-white rounded-lg hover:from-blue-600 hover:to-green-600 transition-colors"
            >
              Add Lesson
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit Lesson Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-xl font-bold text-gray-800">Edit Lesson</h3>
          <button
            @click="showEditModal = false"
            class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XIcon class="w-6 h-6" />
          </button>
        </div>
        
        <form @submit.prevent="updateLesson" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Day</label>
            <select v-model="editingLesson.day" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="Monday">Monday</option>
              <option value="Tuesday">Tuesday</option>
              <option value="Wednesday">Wednesday</option>
              <option value="Thursday">Thursday</option>
              <option value="Friday">Friday</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Subject</label>
            <select v-model="editingLesson.subject" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="Math">Math</option>
              <option value="English">English</option>
              <option value="Science">Science</option>
              <option value="Social Studies">Social Studies</option>
              <option value="Computers">Computers</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Class/Grade</label>
            <select v-model="editingLesson.class_" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option v-for="n in 12" :key="n" :value="n">Class {{ n }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Lesson Title</label>
            <input
              v-model="editingLesson.lesson"
              type="text"
              placeholder="Enter lesson title"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Activity Description</label>
            <textarea
              v-model="editingLesson.activity"
              placeholder="Describe the activity or lesson content"
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            ></textarea>
          </div>
          
          <div class="flex space-x-3 pt-4">
            <button
              type="button"
              @click="showEditModal = false"
              class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-green-500 text-white rounded-lg hover:from-blue-600 hover:to-green-600 transition-colors"
            >
              Update Lesson
            </button>
          </div>
        </form>
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

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { PlusIcon, XIcon, Trash2Icon, EditIcon } from 'lucide-vue-next'
import api from '@/plugins/axios'
import TeacherNavbar from '@/components/app/TeacherNavbar.vue'

const router = useRouter()
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingIndex = ref(-1)
const loading = ref(false)
const error = ref('')
const successMessage = ref('')

const lessons = ref([])
const allLessons = ref([]) // Store all lessons for filtering

// Filters
const filters = ref({
  date: new Date().toISOString().split('T')[0], // Today's date by default
  subject: '',
  class: ''
})

const newLesson = ref({
  day: 'Monday',
  subject: 'Math',
  lesson: '',
  activity: '',
  class_: 1
})

const editingLesson = ref({
  id: null,
  day: 'Monday',
  subject: 'Math',
  lesson: '',
  activity: '',
  class_: 1
})

const uniqueSubjects = computed(() => {
  if (!lessons.value || lessons.value.length === 0) return []
  const set = new Set(lessons.value.map(l => l.subject))
  return Array.from(set)
})

const uniqueClasses = computed(() => {
  if (!lessons.value || lessons.value.length === 0) return []
  const set = new Set(lessons.value.map(l => l.class))
  return Array.from(set).sort((a, b) => a - b)
})


// Filter lessons based on current filters
const filteredLessons = computed(() => {
  if (!allLessons.value || allLessons.value.length === 0) return []
  
  return allLessons.value.filter((lesson: any) => {
    // Date filter - filter by created_at date
    if (filters.value.date) {
      const lessonDate = new Date(lesson.created_at).toISOString().split('T')[0]
      if (lessonDate !== filters.value.date) return false
    }
    
    // Subject filter
    if (filters.value.subject && lesson.subject !== filters.value.subject) {
      return false
    }
    
    // Class filter
    if (filters.value.class && lesson.class !== filters.value.class) {
      return false
    }
    
    return true
  })
})

// Apply filters
const applyFilters = () => {
  // Filters are automatically applied through the computed property
  // This function exists for the @change handlers
}

// Clear all filters
const clearFilters = () => {
  filters.value = {
    date: '',
    subject: '',
    class: ''
  }
}

// Auto-hide success/error messages
const showSuccessMessage = (message: string) => {
  successMessage.value = message
  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

// Fetch lessons from API
const fetchLessons = async () => {
  try {
    loading.value = true
    error.value = ''
    const response = await api.get('/api/teacher/lesson-updates')
    lessons.value = response.data.lessons
    allLessons.value = response.data.lessons
    applyFilters()
  } catch (err) {
    console.error('Error fetching lessons:', err)
    error.value = 'Failed to load lessons. Please refresh the page.'
  } finally {
    loading.value = false
  }
}

// Load lessons on component mount
onMounted(() => {
  fetchLessons()
})

const deleteLesson = async (index: number) => {
  const lesson = filteredLessons.value[index]
  if (confirm(`Are you sure you want to delete "${lesson.lesson}"?`)) {
    try {
      loading.value = true
      await api.delete(`/api/teacher/lesson-updates/${lesson.id}`)
      
      // Remove from both arrays
      const originalIndex = lessons.value.findIndex(l => l.id === lesson.id)
      if (originalIndex !== -1) {
        lessons.value.splice(originalIndex, 1)
      }
      const allIndex = allLessons.value.findIndex(l => l.id === lesson.id)
      if (allIndex !== -1) {
        allLessons.value.splice(allIndex, 1)
      }
      
      showSuccessMessage('Lesson deleted successfully!')
    } catch (err) {
      console.error('Error deleting lesson:', err)
      error.value = 'Failed to delete lesson. Please try again.'
    } finally {
      loading.value = false
    }
  }
}

const addLesson = async () => {
  if (newLesson.value.lesson && newLesson.value.activity) {
    try {
      loading.value = true
      error.value = ''
      
      await api.post('/api/teacher/lesson-updates', {
        day: newLesson.value.day,
        subject: newLesson.value.subject,
        lesson: newLesson.value.lesson,
        activity: newLesson.value.activity,
        class_: newLesson.value.class_
      })
      
      // Refresh lessons from API instead of manually adding
      await fetchLessons()
      
      // Reset form
      newLesson.value = {
        day: 'Monday',
        subject: 'Math',
        lesson: '',
        activity: '',
        class_: 1
      }
      
      showAddModal.value = false
      showSuccessMessage('Lesson created successfully!')
    } catch (err) {
      console.error('Error adding lesson:', err)
      error.value = 'Failed to add lesson. Please try again.'
    } finally {
      loading.value = false
    }
  }
}

const editLesson = (index: number) => {
  const lesson = filteredLessons.value[index]
  const originalIndex = lessons.value.findIndex(l => l.id === lesson.id)
  editingIndex.value = originalIndex
  
  editingLesson.value = {
    id: lesson.id,
    day: lesson.day,
    subject: lesson.subject,
    lesson: lesson.lesson,
    activity: lesson.activity,
    class_: lesson.class
  }
  showEditModal.value = true
}

const updateLesson = async () => {
  if (editingLesson.value.lesson && editingLesson.value.activity && editingIndex.value >= 0) {
    try {
      loading.value = true
      error.value = ''
      
      const response = await api.put(`/api/teacher/lesson-updates/${editingLesson.value.id}`, {
        day: editingLesson.value.day,
        subject: editingLesson.value.subject,
        lesson: editingLesson.value.lesson,
        activity: editingLesson.value.activity,
        class_: editingLesson.value.class_
      })
      
      // Update the lesson in both arrays
      const updatedLesson = response.data.lesson
      lessons.value[editingIndex.value] = updatedLesson
      
      // Also update in allLessons array
      const allLessonsIndex = allLessons.value.findIndex(l => l.id === updatedLesson.id)
      if (allLessonsIndex !== -1) {
        allLessons.value[allLessonsIndex] = updatedLesson
      }
      
      // Reset form and close modal
      editingLesson.value = {
        id: null,
        day: 'Monday',
        subject: 'Math',
        lesson: '',
        activity: '',
        class_: 1
      }
      editingIndex.value = -1
      showEditModal.value = false
      showSuccessMessage('Lesson updated successfully!')
    } catch (err) {
      console.error('Error updating lesson:', err)
      error.value = 'Failed to update lesson. Please try again.'
    } finally {
      loading.value = false
    }
  }
}

// Format date helper function
const formatDate = (dateString: string): string => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  } catch (e) {
    return 'Invalid Date'
  }
}
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style> 

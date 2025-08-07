<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300">
    <!-- Header -->
    <header class="bg-white/90 backdrop-blur-sm shadow-lg sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center space-x-4">
            <!-- Back Arrow -->
            <button
              @click="goHome"
              class="p-2 text-gray-600 hover:text-gray-800 transition-colors rounded-lg hover:bg-gray-100"
            >
              <ArrowLeftIcon class="w-6 h-6" />
            </button>
            <h1 class="text-xl font-bold text-gray-800 font-fancy">📚 Lesson Updates (Teacher)</h1>
          </div>
          <div class="flex items-center space-x-6">
            <router-link to="/teacher/add-student" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
              Add Student
            </router-link>
            <div class="text-center">
              <p class="text-2xl font-bold text-blue-600">{{ lessons.length }}</p>
              <p class="text-xs text-gray-600">Lessons</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-green-600">{{ uniqueSubjects.length }}</p>
              <p class="text-xs text-gray-600">Subjects</p>
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
              <h2 class="text-2xl font-bold text-gray-800 mb-2">Weekly Lesson Progress</h2>
              <p class="text-gray-600">{{ Math.round((lessons.length / 10) * 100) }}% Complete</p>
            </div>
            <div class="text-6xl animate-bounce">🎓</div>
          </div>
          <!-- Progress Bar -->
          <div class="w-full bg-gray-200 rounded-full h-4 mb-4">
            <div
              class="bg-gradient-to-r from-blue-400 to-green-400 h-4 rounded-full transition-all duration-1000 ease-out"
              :style="{ width: `${(lessons.length / 10) * 100}%` }"
            ></div>
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
          v-for="(lesson, index) in lessons"
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
            <div class="flex items-center mb-2">
              <span class="inline-block px-3 py-1 rounded-full bg-green-100 text-green-700 text-xs font-semibold mr-2">{{ lesson.day }}</span>
              <span class="inline-block px-3 py-1 rounded-full bg-blue-100 text-blue-700 text-xs font-semibold">{{ lesson.subject }}</span>
            </div>
            <h3 class="font-bold text-gray-800 mb-2 text-lg">{{ lesson.lesson }}</h3>
            <p class="text-sm text-gray-600 mb-3">{{ lesson.activity }}</p>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="lessons.length === 0" class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">No lessons found</h3>
        <p class="text-gray-600">No lesson updates available for this week.</p>
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
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon, PlusIcon, XIcon, Trash2Icon, EditIcon } from 'lucide-vue-next'

const router = useRouter()
const showAddModal = ref(false)
const showEditModal = ref(false)
const editingIndex = ref(-1)

const goHome = () => {
  router.push('/teacher/home')
}

const lessons = ref([
  { day: 'Monday', subject: 'Math', lesson: 'Algebra: Solving for x', activity: 'Explained variables and solved equations on board' },
  { day: 'Monday', subject: 'English', lesson: 'Essay Writing', activity: 'Guided students through brainstorming and outlining' },
  { day: 'Tuesday', subject: 'Science', lesson: 'Photosynthesis', activity: 'Lab experiment with leaves and sunlight' },
  { day: 'Wednesday', subject: 'Social Studies', lesson: 'World War II Overview', activity: 'Timeline activity and group discussion' },
  { day: 'Thursday', subject: 'Computers', lesson: 'Introduction to Coding', activity: 'Scratch programming basics' },
  { day: 'Friday', subject: 'Math', lesson: 'Geometry: Area & Perimeter', activity: 'Hands-on measurement activity' },
])

const newLesson = ref({
  day: 'Monday',
  subject: 'Math',
  lesson: '',
  activity: ''
})

const editingLesson = ref({
  day: 'Monday',
  subject: 'Math',
  lesson: '',
  activity: ''
})

const uniqueSubjects = computed(() => {
  const set = new Set(lessons.value.map(l => l.subject))
  return Array.from(set)
})

const deleteLesson = (index: number) => {
  if (confirm('Are you sure you want to delete this lesson?')) {
    lessons.value.splice(index, 1)
  }
}

const addLesson = () => {
  if (newLesson.value.lesson && newLesson.value.activity) {
    lessons.value.push({
      day: newLesson.value.day,
      subject: newLesson.value.subject,
      lesson: newLesson.value.lesson,
      activity: newLesson.value.activity
    })
    
    // Reset form
    newLesson.value = {
      day: 'Monday',
      subject: 'Math',
      lesson: '',
      activity: ''
    }
    
    showAddModal.value = false
  }
}

const editLesson = (index: number) => {
  editingIndex.value = index
  const lesson = lessons.value[index]
  editingLesson.value = {
    day: lesson.day,
    subject: lesson.subject,
    lesson: lesson.lesson,
    activity: lesson.activity
  }
  showEditModal.value = true
}

const updateLesson = () => {
  if (editingLesson.value.lesson && editingLesson.value.activity && editingIndex.value >= 0) {
    lessons.value[editingIndex.value] = {
      day: editingLesson.value.day,
      subject: editingLesson.value.subject,
      lesson: editingLesson.value.lesson,
      activity: editingLesson.value.activity
    }
    
    // Reset form and close modal
    editingLesson.value = {
      day: 'Monday',
      subject: 'Math',
      lesson: '',
      activity: ''
    }
    editingIndex.value = -1
    showEditModal.value = false
  }
}
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style> 

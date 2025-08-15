<template>
  <div class="min-h-screen bg-gray-50 ">
    <TeacherNavbar/>
    <header class="max-w-6xl mx-auto mb-8">
      <div class="flex items-center justify-end my-4">
        <router-link
          to="/teacher/add-student" 
          class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          Add Student
        </router-link>
      </div>
      
      <div class="text-center">
        <h1 class="text-4xl font-extrabold text-gray-900 mb-2">My Students</h1>
        <p class="text-gray-600">Manage and view your class students</p>
      </div>
    </header>

    <main class="max-w-6xl mx-auto">
      <!-- Loading State -->
      <div v-if="isLoading" class="bg-white rounded-3xl p-8 shadow-lg border border-gray-200 text-center">
        <div class="inline-flex items-center text-lg text-gray-600">
          <svg class="animate-spin -ml-1 mr-3 h-6 w-6 text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading students...
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-white rounded-3xl p-8 shadow-lg border border-gray-200 text-center">
        <div class="text-6xl mb-4">⚠️</div>
        <p class="text-lg text-red-500 font-medium mb-4">{{ error }}</p>
        <button 
          @click="fetchStudents" 
          class="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
        >
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="students.length === 0" class="bg-white rounded-3xl p-12 shadow-lg border border-gray-200 text-center">
        <div class="text-8xl mb-6">👥</div>
        <h3 class="text-2xl font-bold text-gray-900 mb-4">No Students Yet</h3>
        <p class="text-gray-600 mb-6">You haven't added any students to your class yet. Add your first student to get started!</p>
        <router-link 
          to="/teacher/add-student" 
          class="inline-flex items-center px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md font-medium"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          Add Your First Student
        </router-link>
      </div>

      <!-- Students List -->
      <div v-else class="space-y-6">
        <!-- Stats Header -->
        <div class="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg">
                {{ students.length }}
              </div>
              <div>
                <h3 class="text-2xl font-bold text-gray-900">
                  {{ students.length }} {{ students.length === 1 ? 'Student' : 'Students' }}
                </h3>
                <p class="text-gray-600">Currently enrolled in your class</p>
              </div>
            </div>
            <div class="text-4xl">🎓</div>
          </div>
        </div>

        <!-- Search and Filter -->
        <div class="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div class="flex flex-col sm:flex-row gap-4">
            <div class="flex-1">
              <div class="relative">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search students by name or email..."
                  class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            <button 
              @click="fetchStudents"
              class="px-6 py-3 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition-colors font-medium"
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        <!-- Students Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="student in filteredStudents"
            :key="student.student_id"
            class="bg-white rounded-3xl p-6 shadow-lg border border-gray-200 hover:shadow-xl transition-all duration-200 transform hover:scale-105"
          >
            <div class="flex items-center space-x-4 mb-4">
              <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-lg">
                {{ getInitials(student.first_name, student.last_name) }}
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="font-bold text-gray-900 text-lg truncate">
                  {{ student.first_name }} {{ student.last_name }}
                </h3>
                <p class="text-gray-600 text-sm truncate">{{ student.email }}</p>
              </div>
            </div>
            
            <div class="space-y-3">
              <div class="flex items-center text-sm text-gray-600">
                <span class="text-blue-500 mr-2">🆔</span>
                <span>Student ID: {{ student.student_id }}</span>
              </div>
              
              <div class="flex space-x-2 pt-2">
                <router-link 
                  :to="`/teacher/student-progress/${student.student_id}`"
                  class="flex-1 px-3 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm font-medium text-center block"
                >
                  📊 View Progress
                </router-link>
                <button 
                  @click="confirmRemoveStudent(student)"
                  class="px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm font-medium"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination (if needed for large lists) -->
        <div v-if="students.length > itemsPerPage" class="bg-white rounded-3xl p-6 shadow-lg border border-gray-200">
          <div class="flex items-center justify-between">
            <p class="text-sm text-gray-600">
              Showing {{ startIndex + 1 }} to {{ Math.min(endIndex, filteredStudents.length) }} of {{ filteredStudents.length }} students
            </p>
            <div class="flex space-x-2">
              <button
                @click="previousPage"
                :disabled="currentPage === 1"
                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="currentPage >= totalPages"
                class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Remove Student Confirmation Modal -->
    <div v-if="studentToRemove" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl">
        <div class="text-center">
          <div class="text-6xl mb-4">⚠️</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-4">Remove Student</h3>
          <p class="text-gray-600 mb-6">
            Are you sure you want to remove <strong>{{ studentToRemove.first_name }} {{ studentToRemove.last_name }}</strong> from your class?
            This action cannot be undone.
          </p>
          <div class="flex space-x-4">
            <button
              @click="studentToRemove = null"
              class="flex-1 px-4 py-3 bg-gray-200 text-gray-800 rounded-xl hover:bg-gray-300 transition-colors font-medium"
            >
              Cancel
            </button>
            <button
              @click="removeStudent"
              :disabled="isRemoving"
              class="flex-1 px-4 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ isRemoving ? 'Removing...' : 'Remove Student' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from '@/plugins/axios.js'
import TeacherNavbar from "@/components/app/TeacherNavbar.vue";

// Reactive Data
const students = ref([])
const isLoading = ref(true)
const error = ref(null)
const searchQuery = ref('')
const studentToRemove = ref(null)
const isRemoving = ref(false)

// Pagination
const currentPage = ref(1)
const itemsPerPage = ref(12)

// Computed Properties
const filteredStudents = computed(() => {
  if (!searchQuery.value) return students.value
  
  const query = searchQuery.value.toLowerCase()
  return students.value.filter(student => 
    student.first_name.toLowerCase().includes(query) ||
    student.last_name.toLowerCase().includes(query) ||
    student.email.toLowerCase().includes(query)
  )
})

const totalPages = computed(() => Math.ceil(filteredStudents.value.length / itemsPerPage.value))
const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage.value)
const endIndex = computed(() => startIndex.value + itemsPerPage.value)

// Methods
const fetchStudents = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await axios.get('/api/teacher/linked-students')
    students.value = response.data.students || []
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load students. Please try again.'
    console.error('API Error (fetchStudents):', err)
  } finally {
    isLoading.value = false
  }
}

const getInitials = (firstName, lastName) => {
  if (!firstName && !lastName) return 'S'
  const firstInitial = firstName ? firstName.charAt(0).toUpperCase() : ''
  const lastInitial = lastName ? lastName.charAt(0).toUpperCase() : ''
  return `${firstInitial}${lastInitial}`
}

const confirmRemoveStudent = (student) => {
  studentToRemove.value = student
}

const removeStudent = async () => {
  if (!studentToRemove.value) return
  
  isRemoving.value = true
  
  try {
    await axios.delete(`/api/teacher/remove-student/${studentToRemove.value.student_id}`)
    
    // Remove student from local list
    students.value = students.value.filter(s => s.student_id !== studentToRemove.value.student_id)
    
    // Close modal
    studentToRemove.value = null
  } catch (err) {
    console.error('Failed to remove student:', err)
    alert(err.response?.data?.message || 'Failed to remove student. Please try again.')
  } finally {
    isRemoving.value = false
  }
}

// Pagination Methods
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

// Lifecycle Hook
onMounted(() => {
  fetchStudents()
})
</script>

<style scoped>
/* Additional custom styles if needed */
.transform {
  transition: transform 0.2s ease-in-out;
}

/* Custom scrollbar for the modal */
.modal-content::-webkit-scrollbar {
  width: 4px;
}

.modal-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}
</style>
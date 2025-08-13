<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
    <!-- Navbar -->
    <TeacherNavbar />

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-8 shadow-xl border border-white/20">
          <div class="flex flex-col md:flex-row items-center justify-between">
            <div>
              <h2 class="text-3xl font-bold text-gray-800 mb-4">Welcome to Your Dashboard</h2>
              <p class="text-gray-600 text-lg">Manage your classes, track student progress, and create engaging lessons.</p>
            </div>
            <div class="text-8xl">🎓</div>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-blue-600">{{ stats.totalLessons }}</p>
              <p class="text-sm text-gray-600">Total Lessons</p>
            </div>
            <div class="text-4xl">📚</div>
          </div>
        </div>
        
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-green-600">{{ stats.totalStudents }}</p>
              <p class="text-sm text-gray-600">Students</p>
            </div>
            <div class="text-4xl">👥</div>
          </div>
        </div>
        
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-purple-600">{{ stats.uniqueSubjects }}</p>
              <p class="text-sm text-gray-600">Subjects</p>
            </div>
            <div class="text-4xl">📖</div>
          </div>
        </div>
        
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-xl border border-white/20">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-3xl font-bold text-orange-600">{{ stats.thisWeekLessons }}</p>
              <p class="text-sm text-gray-600">This Week</p>
            </div>
            <div class="text-4xl">📅</div>
          </div>
        </div>
      </div>

      <!-- Principal School Profile Section -->
      <div v-if="isPrincipal" class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-8 shadow-xl border border-white/20">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-bold text-gray-800 flex items-center">
              <span class="text-3xl mr-3">👑</span>
              School Profile
            </h3>
            <div class="bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 px-4 py-2 rounded-full text-sm font-semibold">
              Principal Dashboard
            </div>
          </div>

          <!-- School Info -->
          <div v-if="schoolInfo" class="mb-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl">
            <h4 class="text-xl font-bold text-gray-800 mb-2">{{ schoolInfo.school_name }}</h4>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="text-center">
                <div class="text-3xl font-bold text-blue-600">{{ schoolStats.totalStudents }}</div>
                <div class="text-sm text-gray-600">Total Students</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-green-600">{{ schoolStats.totalTeachers }}</div>
                <div class="text-sm text-gray-600">Teachers</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-purple-600">{{ schoolStats.activeClasses }}</div>
                <div class="text-sm text-gray-600">Active Classes</div>
              </div>
            </div>
          </div>

          <!-- Teachers Management -->
          <div class="bg-white rounded-2xl p-6 border border-gray-200">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-lg font-bold text-gray-800">Teachers Management</h4>
              <button 
                @click="refreshTeachers"
                :disabled="loadingTeachers"
                class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                <span v-if="loadingTeachers">Loading...</span>
                <span v-else>Refresh</span>
              </button>
            </div>

            <div v-if="loadingTeachers" class="text-center py-8">
              <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p class="text-gray-600 mt-2">Loading teachers...</p>
            </div>

            <div v-else-if="teachers.length === 0" class="text-center py-8">
              <div class="text-6xl mb-4">👨‍🏫</div>
              <p class="text-gray-600">No teachers found in your school yet.</p>
            </div>

            <div v-else class="space-y-3">
              <div 
                v-for="teacher in teachers" 
                :key="teacher.teacher_id"
                class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div class="flex items-center space-x-4">
                  <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                    {{ teacher.first_name?.[0]?.toUpperCase() || 'T' }}
                  </div>
                  <div>
                    <h5 class="font-semibold text-gray-800">
                      {{ teacher.first_name }} {{ teacher.last_name }}
                    </h5>
                    <p class="text-sm text-gray-600">{{ teacher.email }}</p>
                    <p class="text-xs text-gray-500">Subject: {{ teacher.subject }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <button
                    @click="viewTeacher(teacher)"
                    class="bg-gray-100 text-gray-600 px-3 py-1 rounded-lg hover:bg-gray-200 transition-colors text-sm"
                  >
                    View
                  </button>
                  <button
                    @click="confirmRemoveTeacher(teacher)"
                    class="bg-red-100 text-red-600 px-3 py-1 rounded-lg hover:bg-red-200 transition-colors text-sm"
                  >
                    Remove
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <!-- Lesson Updates -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer" @click="navigateTo('/teacher/lesson-updates')">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">📝</div>
            <div class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm font-semibold">
              {{ stats.totalLessons }} lessons
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Lesson Updates</h3>
          <p class="text-gray-600 mb-4">Create, edit, and manage your daily lesson updates for students.</p>
          <div class="flex items-center text-blue-600 font-semibold group-hover:text-blue-700">
            <span>Manage Lessons</span>
            <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>

        <!-- Add Students -->
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 group cursor-pointer" @click="navigateTo('/teacher/students')">
          <div class="flex items-center justify-between mb-4">
            <div class="text-5xl group-hover:scale-110 transition-transform duration-300">👥</div>
            <div class="bg-green-100 text-green-600 px-3 py-1 rounded-full text-sm font-semibold">
              {{ stats.totalStudents }} students
            </div>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Manage Students</h3>
          <p class="text-gray-600 mb-4">Add new students to your classes and manage your student roster.</p>
          <div class="flex items-center text-green-600 font-semibold group-hover:text-green-700">
            <span>Manage Students</span>
            <svg class="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </div>
        </div>

      </div>


      <!-- Teacher Detail Modal -->
      <div v-if="selectedTeacher" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="closeModal">
        <div class="bg-white rounded-3xl p-8 max-w-md w-full mx-4 shadow-2xl" @click.stop>
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-2xl font-bold text-gray-800">Teacher Details</h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
          </div>
          
          <div class="space-y-4">
            <div class="flex items-center space-x-4">
              <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-xl">
                {{ selectedTeacher.first_name?.[0]?.toUpperCase() || 'T' }}
              </div>
              <div>
                <h4 class="text-xl font-bold text-gray-800">{{ selectedTeacher.first_name }} {{ selectedTeacher.last_name }}</h4>
                <p class="text-gray-600">{{ selectedTeacher.subject }} Teacher</p>
              </div>
            </div>
            
            <div class="space-y-2">
              <div class="p-3 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600">Email Address</p>
                <p class="font-semibold">{{ selectedTeacher.email }}</p>
              </div>
              
              <div class="p-3 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600">Subject</p>
                <p class="font-semibold">{{ selectedTeacher.subject }}</p>
              </div>
              
              <div class="p-3 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600">Teacher ID</p>
                <p class="font-semibold">#{{ selectedTeacher.teacher_id }}</p>
              </div>
              
              <div class="p-3 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600">Joined Date</p>
                <p class="font-semibold">{{ formatDate(selectedTeacher.created_at) }}</p>
              </div>
            </div>
            
            <div class="flex space-x-3 pt-4">
              <button 
                @click="closeModal"
                class="flex-1 bg-gray-100 text-gray-600 py-3 rounded-lg hover:bg-gray-200 transition-colors font-semibold"
              >
                Close
              </button>
              <button 
                @click="confirmRemoveTeacher(selectedTeacher)"
                class="flex-1 bg-red-100 text-red-600 py-3 rounded-lg hover:bg-red-200 transition-colors font-semibold"
              >
                Remove Teacher
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
    </main>

    <!-- Floating decorative elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div class="absolute top-20 left-10 w-8 h-8 bg-blue-200 rounded-full opacity-20 animate-bounce"></div>
      <div class="absolute top-40 right-20 w-6 h-6 bg-purple-200 rounded-full opacity-20 animate-bounce" style="animation-delay: 0.5s"></div>
      <div class="absolute bottom-32 left-20 w-10 h-10 bg-green-200 rounded-full opacity-20 animate-bounce" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 right-10 w-7 h-7 bg-orange-200 rounded-full opacity-20 animate-bounce" style="animation-delay: 1.5s"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/plugins/axios'
import TeacherNavbar from '@/components/app/TeacherNavbar.vue'

const router = useRouter()
const teacherName = ref('Teacher')
const lessons = ref([])
const students = ref([])
const loading = ref(false)
const error = ref('')

// Principal-specific data
const isPrincipal = ref(false)
const teachers = ref([])
const schoolInfo = ref(null)
const loadingTeachers = ref(false)
const selectedTeacher = ref(null)
const schoolStats = ref({
  totalStudents: 0,
  totalTeachers: 0,
  activeClasses: 0
})

const goHome = () => {
  router.push('/teacher/dashboard')
}

const navigateTo = (path: string) => {
  router.push(path)
}

const logout = () => {
  // Clear any stored tokens/session data
  localStorage.removeItem('token')
  sessionStorage.clear()
  router.push('/')
}

// Computed stats
const stats = computed(() => ({
  totalLessons: lessons.value.length,
  totalStudents: students.value.length,
  uniqueSubjects: [...new Set(lessons.value.map((l: any) => l.subject))].length,
  thisWeekLessons: lessons.value.filter((l: any) => {
    // Simple week filter - could be enhanced with proper date logic
    return true // For now, show all lessons
  }).length
}))


// Check if user is principal
const checkUserRole = () => {
  const userType = localStorage.getItem('user_type')
  isPrincipal.value = userType === 'principal'
}

// Fetch teachers for principals
const fetchTeachers = async () => {
  if (!isPrincipal.value) return
  
  try {
    loadingTeachers.value = true
    const response = await axios.get('/principal/teachers')
    
    teachers.value = response.data.teachers || []
    schoolInfo.value = {
      school_name: response.data.school_name,
      school_id: response.data.school_id
    }
    
    // Update school stats
    schoolStats.value.totalTeachers = teachers.value.length
    schoolStats.value.activeClasses = [...new Set(teachers.value.map(t => t.subject))].length
    
  } catch (err) {
    console.error('Error fetching teachers:', err)
    error.value = 'Failed to load teachers data'
  } finally {
    loadingTeachers.value = false
  }
}

// Refresh teachers list
const refreshTeachers = () => {
  fetchTeachers()
}

// View teacher details
const viewTeacher = (teacher: any) => {
  selectedTeacher.value = teacher
}

// Close modal
const closeModal = () => {
  selectedTeacher.value = null
}

// Format date
const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

// Confirm teacher removal
const confirmRemoveTeacher = (teacher: any) => {
  if (confirm(`Are you sure you want to remove ${teacher.first_name} ${teacher.last_name} from your school?`)) {
    removeTeacher(teacher.teacher_id)
    closeModal()
  }
}

// Remove teacher
const removeTeacher = async (teacherId: number) => {
  try {
    await axios.delete(`/principal/teachers/${teacherId}`)
    
    // Remove from local array
    teachers.value = teachers.value.filter(t => t.teacher_id !== teacherId)
    schoolStats.value.totalTeachers = teachers.value.length
    
    alert('Teacher removed successfully!')
  } catch (err) {
    console.error('Error removing teacher:', err)
    alert('Failed to remove teacher. Please try again.')
  }
}

// Fetch teacher data
const fetchTeacherData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    // Check user role first
    checkUserRole()
    
    // Fetch lessons and students in parallel
    const [lessonsResponse, studentsResponse] = await Promise.all([
      axios.get('/api/teacher/lesson-updates'),
      axios.get('/api/teacher/linked-students')
    ])
    
    lessons.value = lessonsResponse.data.lessons || []
    students.value = studentsResponse.data.students || []
    
    // Set teacher name from localStorage or token if available
    const storedName = localStorage.getItem('teacherName')
    if (storedName) {
      teacherName.value = storedName
    }
    
    // If principal, also fetch teachers
    if (isPrincipal.value) {
      await fetchTeachers()
    }
    
  } catch (err) {
    console.error('Error fetching teacher data:', err)
    error.value = 'Failed to load dashboard data'
  } finally {
    loading.value = false
  }
}

// Load data on component mount
onMounted(() => {
  fetchTeacherData()
})
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
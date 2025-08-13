<template>
  <div class="min-h-screen bg-gray-50 ">
    <TeacherNavbar/>
    <header class="max-w-4xl mx-auto mb-8 text-center mt-5">
      <h1 class="text-4xl font-extrabold text-gray-900 mb-3">My Profile</h1>
    </header>

    <main class="max-w-4xl mx-auto bg-white rounded-3xl p-8 shadow-lg border border-gray-200">
      <div v-if="isLoading" class="text-center py-20">
        <div class="inline-flex items-center text-lg text-gray-600">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading profile data...
        </div>
      </div>
      
      <div v-else-if="error" class="text-center py-20">
        <div class="text-6xl mb-4">⚠️</div>
        <p class="text-lg text-red-500 font-medium">{{ error }}</p>
        <button 
          @click="fetchTeacherProfile" 
          class="mt-4 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
        >
          Try Again
        </button>
      </div>
      
      <div v-else class="space-y-8">
        <!-- Profile Header -->
        <div class="flex items-center space-x-6 pb-6 border-b border-gray-100">
          <div class="w-24 h-24 rounded-full bg-gradient-to-br from-green-500 to-teal-500 flex items-center justify-center text-4xl font-bold text-white shadow-lg">
            {{ getInitials(profile.first_name, profile.last_name) }}
          </div>
          <div>
            <h2 class="text-3xl font-bold text-gray-900">{{ profile.first_name }} {{ profile.last_name }}</h2>
            <p class="text-gray-600 flex items-center mt-1">
              📧 {{ profile.email }}
            </p>
            <p class="text-sm text-gray-500 mt-1">Member since: {{ formatDate(profile.created_at) }}</p>
            <div class="flex items-center mt-2 space-x-4">
              <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                👨‍🏫 Teacher
              </span>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                📚 {{ profile.subject }}
              </span>
            </div>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div class="bg-green-50 rounded-2xl p-5 flex items-center space-x-4 shadow-sm border border-green-200">
            <div class="text-4xl">🆔</div>
            <div>
              <p class="text-sm text-green-700 font-medium">Teacher ID</p>
              <p class="text-2xl font-bold text-green-800">{{ profile.teacher_id }}</p>
            </div>
          </div>
          
          <div class="bg-blue-50 rounded-2xl p-5 flex items-center space-x-4 shadow-sm border border-blue-200">
            <div class="text-4xl">🏫</div>
            <div>
              <p class="text-sm text-blue-700 font-medium">School ID</p>
              <p class="text-2xl font-bold text-blue-800">{{ profile.school_id }}</p>
            </div>
          </div>
          
          <div class="bg-purple-50 rounded-2xl p-5 flex items-center space-x-4 shadow-sm border border-purple-200">
            <div class="text-4xl">👥</div>
            <div>
              <p class="text-sm text-purple-700 font-medium">Students</p>
              <p class="text-2xl font-bold text-purple-800">{{ studentCount }}</p>
            </div>
          </div>
        </div>

        <!-- Professional Details -->
        <div class="space-y-4">
          <h3 class="text-xl font-bold text-gray-800 border-b pb-2 mb-4">Professional Details</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">👤 First Name</p>
              <p class="font-medium text-gray-800">{{ profile.first_name }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">👤 Last Name</p>
              <p class="font-medium text-gray-800">{{ profile.last_name }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">📧 Email Address</p>
              <p class="font-medium text-gray-800">{{ profile.email }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">📚 Subject</p>
              <p class="font-medium text-gray-800">{{ profile.subject }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">🆔 Teacher ID</p>
              <p class="font-medium text-gray-800">{{ profile.teacher_id }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">🏫 School ID</p>
              <p class="font-medium text-gray-800">{{ profile.school_id }}</p>
            </div>
          </div>
        </div>

        <!-- Account Information -->
        <div class="space-y-4">
          <h3 class="text-xl font-bold text-gray-800 border-b pb-2 mb-4">Account Information</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">🔑 User ID</p>
              <p class="font-medium text-gray-800">{{ profile.user_id }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">📅 Account Created</p>
              <p class="font-medium text-gray-800">{{ formatDate(profile.created_at) }}</p>
            </div>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="space-y-4">
          <h3 class="text-xl font-bold text-gray-800 border-b pb-2 mb-4">Quick Actions</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <router-link 
              to="/teacher/lesson-updates" 
              class="flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white p-4 rounded-xl hover:from-blue-600 hover:to-blue-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
            >
              <span class="text-2xl">📚</span>
              <span class="font-medium">Lesson Updates</span>
            </router-link>
            
            <router-link 
              to="/teacher/add-student" 
              class="flex items-center justify-center space-x-2 bg-gradient-to-r from-green-500 to-green-600 text-white p-4 rounded-xl hover:from-green-600 hover:to-green-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
            >
              <span class="text-2xl">👥</span>
              <span class="font-medium">Add Student</span>
            </router-link>
            

            <router-link 
              to="/teacher/dashboard" 
              class="flex items-center justify-center space-x-2 bg-gradient-to-r from-teal-500 to-teal-600 text-white p-4 rounded-xl hover:from-teal-600 hover:to-teal-700 transition-all shadow-md hover:shadow-lg transform hover:scale-105"
            >
              <span class="text-2xl">🏠</span>
              <span class="font-medium">Dashboard</span>
            </router-link>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '@/plugins/axios.js'
import TeacherNavbar from "@/components/app/TeacherNavbar.vue";

// Reactive Data
const profile = ref(null)
const isLoading = ref(true)
const error = ref(null)
const studentCount = ref(0)

// Methods
const fetchTeacherProfile = async () => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await axios.get('/api/teacher/profile')
    profile.value = response.data
    
    // Fetch student count
    await fetchStudentCount()
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load profile. Please try again.'
    console.error('API Error (fetchTeacherProfile):', err)
  } finally {
    isLoading.value = false
  }
}

const fetchStudentCount = async () => {
  try {
    const response = await axios.get('/api/teacher/linked-students')
    studentCount.value = response.data.students?.length || 0
  } catch (err) {
    console.error('Failed to fetch student count:', err)
    studentCount.value = 0
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) {
      return 'Invalid Date'
    }
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  } catch (e) {
    console.error("Error formatting date:", dateString, e)
    return 'Invalid Date'
  }
}

const getInitials = (firstName, lastName) => {
  if (!firstName && !lastName) return 'T'
  const firstInitial = firstName ? firstName.charAt(0).toUpperCase() : ''
  const lastInitial = lastName ? lastName.charAt(0).toUpperCase() : ''
  return `${firstInitial}${lastInitial}`
}

// Lifecycle Hook
onMounted(() => {
  fetchTeacherProfile()
})
</script>

<style scoped>
/* Additional custom styles if needed */
.transform {
  transition: transform 0.2s ease-in-out;
}
</style>
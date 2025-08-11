<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
    <div class="max-w-md w-full">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="font-fancy text-5xl font-bold text-gray-800 mb-2">
          CoolKids
        </h1>
        <p class="text-lg text-gray-600">Teacher Registration</p>
      </div>

      <!-- Signup Form -->
      <div class="bg-white rounded-3xl shadow-2xl p-8 border border-gray-100">
        <div class="text-center mb-6">
          <h2 class="text-2xl font-bold text-gray-800 mb-2">Join Our Platform</h2>
          <p class="text-gray-600">Create your teacher account to get started</p>
        </div>

        <form @submit.prevent="handleSignup" class="space-y-5">
          <!-- Name Fields -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700 mb-2">
                First Name *
              </label>
              <input
                id="firstName"
                v-model="formData.first_name"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                :class="{ 'border-red-500': errors.first_name }"
                placeholder="John"
              />
              <p v-if="errors.first_name" class="text-red-500 text-xs mt-1">{{ errors.first_name }}</p>
            </div>
            
            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700 mb-2">
                Last Name *
              </label>
              <input
                id="lastName"
                v-model="formData.last_name"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                :class="{ 'border-red-500': errors.last_name }"
                placeholder="Doe"
              />
              <p v-if="errors.last_name" class="text-red-500 text-xs mt-1">{{ errors.last_name }}</p>
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address *
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              :class="{ 'border-red-500': errors.email }"
              placeholder="john.doe@school.edu"
            />
            <p v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</p>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password *
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full px-4 py-3 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                :class="{ 'border-red-500': errors.password }"
                placeholder="Create a strong password"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464M9.878 9.878l-1.414-1.414M14.12 14.12l1.414 1.414M14.12 14.12L15.536 15.536M14.12 14.12l1.414-1.414"></path>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
              </button>
            </div>
            <p v-if="errors.password" class="text-red-500 text-xs mt-1">{{ errors.password }}</p>
            
            <!-- Password Strength Indicator -->
            <div v-if="formData.password" class="mt-2">
              <div class="flex items-center space-x-2">
                <div class="flex-1 bg-gray-200 rounded-full h-2">
                  <div 
                    class="h-2 rounded-full transition-all duration-300"
                    :class="passwordStrengthColor"
                    :style="{ width: `${passwordStrengthPercent}%` }"
                  ></div>
                </div>
                <span class="text-xs font-medium" :class="passwordStrengthColor.replace('bg-', 'text-')">
                  {{ passwordStrengthText }}
                </span>
              </div>
            </div>
          </div>

          <!-- Subject -->
          <div>
            <label for="subject" class="block text-sm font-medium text-gray-700 mb-2">
              Subject *
            </label>
            <select
              id="subject"
              v-model="formData.subject"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              :class="{ 'border-red-500': errors.subject }"
            >
              <option value="">Select your subject</option>
              <option v-for="subject in subjects" :key="subject.value" :value="subject.value">
                {{ subject.label }}
              </option>
            </select>
            <p v-if="errors.subject" class="text-red-500 text-xs mt-1">{{ errors.subject }}</p>
          </div>

          <!-- School -->
          <div>
            <label for="school" class="block text-sm font-medium text-gray-700 mb-2">
              School *
            </label>
            <select
              id="school"
              v-model="formData.school_id"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              :class="{ 'border-red-500': errors.school_id }"
            >
              <option value="">Select your school</option>
              <option v-for="school in schools" :key="school.id" :value="school.id">
                {{ school.name }}
              </option>
            </select>
            <p v-if="errors.school_id" class="text-red-500 text-xs mt-1">{{ errors.school_id }}</p>
          </div>

          <!-- Terms and Conditions -->
          <div class="flex items-start">
            <input
              id="terms"
              v-model="acceptTerms"
              type="checkbox"
              required
              class="mt-1 w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <label for="terms" class="ml-3 text-sm text-gray-600">
              I agree to the <a href="#" class="text-blue-600 hover:text-blue-800 underline">Terms of Service</a> 
              and <a href="#" class="text-blue-600 hover:text-blue-800 underline">Privacy Policy</a>
            </label>
          </div>

          <!-- Error Message -->
          <div v-if="generalError" class="bg-red-50 border border-red-200 rounded-xl p-4">
            <div class="flex items-center">
              <svg class="w-5 h-5 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="text-red-700 text-sm">{{ generalError }}</p>
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isLoading || !acceptTerms"
            class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-lg"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-5-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
              </svg>
              Create Teacher Account
            </span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating Account...
            </span>
          </button>
        </form>

        <!-- Login Link -->
        <div class="text-center mt-6 pt-6 border-t border-gray-200">
          <p class="text-gray-600">
            Already have an account? 
            <router-link to="/login" class="text-blue-600 hover:text-blue-800 font-medium underline">
              Sign in here
            </router-link>
          </p>
        </div>
      </div>

      <!-- Success Modal -->
      <div v-if="showSuccess" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-3xl p-8 max-w-md w-full text-center shadow-2xl">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-gray-800 mb-2">Welcome to CoolKids!</h3>
          <p class="text-gray-600 mb-6">Your teacher account has been created successfully.</p>
          <button
            @click="goToDashboard"
            class="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-105"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/plugins/axios'

const router = useRouter()

const isLoading = ref(false)
const showSuccess = ref(false)
const showPassword = ref(false)
const acceptTerms = ref(false)
const generalError = ref('')

const formData = reactive({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  subject: '',
  school_id: ''
})

const errors = reactive({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  subject: '',
  school_id: ''
})

const subjects = [
  { value: 'mathematics', label: '📊 Mathematics' },
  { value: 'science', label: '🔬 Science' },
  { value: 'english', label: '📚 English Language Arts' },
  { value: 'history', label: '🏛️ History' },
  { value: 'geography', label: '🌍 Geography' },
  { value: 'art', label: '🎨 Art' },
  { value: 'music', label: '🎵 Music' },
  { value: 'physical_education', label: '⚽ Physical Education' },
  { value: 'computer_science', label: '💻 Computer Science' },
  { value: 'foreign_language', label: '🌐 Foreign Language' },
  { value: 'special_education', label: '🤝 Special Education' },
  { value: 'other', label: '📝 Other' }
]


const schools = ref([])

onMounted(async () => {
  try {
    const token = localStorage.getItem('token') 
    const response = await axios.get('/api/admin/schools', {
    })
    schools.value = response.data
  } catch (error) {
    console.error('Error fetching schools:', error)
  }
})

// Password strength calculation
const passwordStrength = computed(() => {
  const password = formData.password
  if (!password) return 0
  
  let score = 0
  
  // Length check
  if (password.length >= 8) score += 25
  if (password.length >= 12) score += 25
  
  // Character variety checks
  if (/[a-z]/.test(password)) score += 10
  if (/[A-Z]/.test(password)) score += 10
  if (/[0-9]/.test(password)) score += 15
  if (/[^A-Za-z0-9]/.test(password)) score += 15
  
  return Math.min(score, 100)
})

const passwordStrengthPercent = computed(() => passwordStrength.value)

const passwordStrengthColor = computed(() => {
  const strength = passwordStrength.value
  if (strength < 30) return 'bg-red-500'
  if (strength < 60) return 'bg-yellow-500'
  if (strength < 80) return 'bg-blue-500'
  return 'bg-green-500'
})

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  if (strength < 30) return 'Weak'
  if (strength < 60) return 'Fair'
  if (strength < 80) return 'Good'
  return 'Strong'
})

const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
  
  let isValid = true
  
  // Email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(formData.email)) {
    errors.email = 'Please enter a valid email address'
    isValid = false
  }
  
  // Password validation
  if (formData.password.length < 8) {
    errors.password = 'Password must be at least 8 characters long'
    isValid = false
  }
  
  // Name validation
  if (formData.first_name.trim().length < 2) {
    errors.first_name = 'First name must be at least 2 characters'
    isValid = false
  }
  
  if (formData.last_name.trim().length < 2) {
    errors.last_name = 'Last name must be at least 2 characters'
    isValid = false
  }
  
  // Subject validation
  if (!formData.subject) {
    errors.subject = 'Please select a subject'
    isValid = false
  }
  
  // School validation
  if (!formData.school_id) {
    errors.school_id = 'Please select a school'
    isValid = false
  }
  
  return isValid
}

const handleSignup = async () => {
  generalError.value = ''
  
  if (!validateForm()) {
    return
  }
  
  isLoading.value = true
  
  try {
    const response = await axios.post('/api/teacher/register', {
      email: formData.email,
      password: formData.password,
      first_name: formData.first_name,
      last_name: formData.last_name,
      subject: formData.subject,
      school_id: parseInt(formData.school_id)
    })
    
    // Store tokens in localStorage
    localStorage.setItem('access_token', response.data.access_token)
    localStorage.setItem('refresh_token', response.data.refresh_token)
    localStorage.setItem('user_email', response.data.user_email)
    localStorage.setItem('user_role', response.data.role)
    
    showSuccess.value = true
    
  } catch (error: any) {
    console.error('Signup error:', error)
    
    if (error.response?.data?.error) {
      generalError.value = error.response.data.error
    } else if (error.response?.status === 409) {
      generalError.value = 'An account with this email already exists'
    } else if (error.response?.status === 404) {
      generalError.value = 'Selected school not found'
    } else {
      generalError.value = 'An error occurred during registration. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}

const goToDashboard = () => {
  router.push('/teacher/dashboard')
}
</script>

<style scoped>
/* Custom animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

/* Enhanced focus styles */
input:focus,
select:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Custom checkbox styling */
input[type="checkbox"]:checked {
  background-color: #3b82f6;
  border-color: #3b82f6;
}

/* Smooth transitions */
* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Button hover effects */
button:hover:not(:disabled) {
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* Loading spinner animation */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
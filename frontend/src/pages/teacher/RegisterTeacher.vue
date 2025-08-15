<template>
  <div class="min-h-screen bg-gray-50">
    <GuestNavbar/>
    <div class="flex items-center justify-center p-4 pt-16">
      <div class="w-full max-w-2xl">
        <!-- Main registration card -->
        <Card class="bg-white border shadow-sm p-8">
          <!-- App logo and title -->
          <div class="text-center mb-8">
            <div class="w-16 h-16 bg-slate-900 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <GraduationCapIcon class="w-8 h-8 text-white"/>
            </div>
            <h1 class="text-2xl font-semibold text-gray-900 mb-2">Create Teacher Account</h1>
            <p class="text-gray-600 text-sm">Join our teaching community</p>
          </div>

          <!-- Response Alert -->
          <div v-if="response" class="mb-6 p-4 rounded-lg border-2" :class="alertClasses">
            <div class="flex items-center">
              <CheckCircleIcon v-if="response.success" class="h-5 w-5 mr-2"
                               :class="response.success ? 'text-green-600' : 'text-red-600'"/>
              <AlertCircleIcon v-else class="h-5 w-5 mr-2"
                               :class="response.success ? 'text-green-600' : 'text-red-600'"/>
              <p :class="response.success ? 'text-green-800' : 'text-red-800'">{{ response.message }}</p>
            </div>
          </div>

          <!-- Role Toggle -->
          <div class="mb-6">
            <div class="flex items-center justify-center space-x-1 bg-gray-100 rounded-lg p-1">
              <button
                  type="button"
                  @click="formData.role = 'teacher'"
                  :class="formData.role === 'teacher' 
                    ? 'bg-white text-gray-900 shadow-sm' 
                    : 'text-gray-600 hover:text-gray-900'"
                  class="flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all duration-200"
              >
                Teacher
              </button>
              <button
                  type="button"
                  @click="formData.role = 'principal'"
                  :class="formData.role === 'principal' 
                    ? 'bg-white text-gray-900 shadow-sm' 
                    : 'text-gray-600 hover:text-gray-900'"
                  class="flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all duration-200"
              >
                Admin Teacher
              </button>
            </div>
          </div>

          <!-- Registration form -->
          <form @submit.prevent="handleSubmit" class="space-y-5">
            <!-- Name Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <label for="firstName" class="block text-sm font-medium text-gray-700">
                  First Name *
                </label>
                <Input
                    id="firstName"
                    v-model="formData.first_name"
                    type="text"
                    placeholder="Your first name"
                    class="h-10"
                    :class="getInputClasses('first_name')"
                    required
                />
                <p v-if="errors.first_name" class="text-xs text-red-500">{{ errors.first_name }}</p>
              </div>

              <div class="space-y-2">
                <label for="lastName" class="block text-sm font-medium text-gray-700">
                  Last Name *
                </label>
                <Input
                    id="lastName"
                    v-model="formData.last_name"
                    type="text"
                    placeholder="Your last name"
                    class="h-10"
                    :class="getInputClasses('last_name')"
                    required
                />
                <p v-if="errors.last_name" class="text-xs text-red-500">{{ errors.last_name }}</p>
              </div>
            </div>

            <!-- Email -->
            <div class="space-y-2">
              <label for="email" class="block text-sm font-medium text-gray-700">
                Email Address *
              </label>
              <Input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  placeholder="your.email@school.edu"
                  class="h-10"
                  :class="getInputClasses('email')"
                  required
              />
              <p class="text-xs text-gray-500">This will be your login email</p>
              <p v-if="errors.email" class="text-xs text-red-500">{{ errors.email }}</p>
            </div>

            <!-- Subject and School -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <label for="subject" class="block text-sm font-medium text-gray-700">
                  Subject *
                </label>
                <Select
                    id="subject"
                    v-model="formData.subject"
                    :class="getInputClasses('subject')"
                    required
                >
                  <SelectTrigger class="w-full h-10">
                    <SelectValue placeholder="Select your subject"></SelectValue>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Math">Mathematics</SelectItem>
                    <SelectItem value="English">English</SelectItem>
                    <SelectItem value="Science">Science</SelectItem>
                    <SelectItem value="Social Studies">Social Studies</SelectItem>
                    <SelectItem value="Computers">Computer Science</SelectItem>
                    <SelectItem value="Art">Art</SelectItem>
                    <SelectItem value="Music">Music</SelectItem>
                    <SelectItem value="Physical Education">Physical Education</SelectItem>
                  </SelectContent>
                </Select>
                <p v-if="errors.subject" class="text-xs text-red-500">{{ errors.subject }}</p>
              </div>

              <div class="space-y-2">
                <label for="school" class="block text-sm font-medium text-gray-700">
                  School *
                </label>
                
                <!-- Teacher: Select from existing schools -->
                <Select
                    v-if="formData.role === 'teacher'"
                    id="school_id"
                    v-model="formData.school_id"
                    :class="getInputClasses('school_id')"
                    required
                >
                  <SelectTrigger class="w-full h-10">
                    <SelectValue placeholder="Select your school"></SelectValue>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem v-if="isLoadingSchools" disabled value="loading">Loading schools...</SelectItem>
                    <SelectItem v-else-if="schools.length === 0" disabled value="no-schools">No schools available
                    </SelectItem>
                    <SelectItem
                        v-else
                        v-for="school in schools"
                        :key="school.school_id"
                        :value="school.school_id.toString()"
                    >
                      {{ school.name }}
                    </SelectItem>
                  </SelectContent>
                </Select>
                
                <!-- Principal: Enter new school name -->
                <div v-else class="space-y-3">
                  <Input
                      id="school_name"
                      v-model="formData.school_name"
                      type="text"
                      placeholder="Enter your school name"
                      class="h-10"
                      :class="getInputClasses('school_name')"
                      required
                  />
                  <Input
                      id="school_address"
                      v-model="formData.school_address"
                      type="text"
                      placeholder="School address (optional)"
                      class="h-10"
                      :class="getInputClasses('school_address')"
                  />
                  <Input
                      id="school_phone"
                      v-model="formData.school_phone"
                      type="tel"
                      placeholder="School phone number (optional)"
                      class="h-10"
                      :class="getInputClasses('school_phone')"
                  />
                </div>
                
                <p v-if="formData.role === 'teacher'" class="text-xs text-gray-500">Select the school you work at</p>
                <p v-else class="text-xs text-gray-500">Enter the name of your school to create it</p>
                <p v-if="errors.school_id" class="text-xs text-red-500">{{ errors.school_id }}</p>
                <p v-if="errors.school_name" class="text-xs text-red-500">{{ errors.school_name }}</p>
              </div>
            </div>

            <!-- Password -->
            <div class="space-y-2">
              <label for="password" class="block text-sm font-medium text-gray-700">
                Password *
              </label>
              <div class="relative">
                <Input
                    id="password"
                    v-model="formData.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Create a strong password"
                    class="h-10 pr-10"
                    :class="getInputClasses('password')"
                    required
                />
                <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  <EyeIcon v-if="showPassword" class="w-4 h-4"/>
                  <EyeOffIcon v-else class="w-4 h-4"/>
                </button>
              </div>
              <p v-if="errors.password" class="text-xs text-red-500">{{ errors.password }}</p>

              <!-- Password strength indicator -->
              <div v-if="formData.password" class="mt-2">
                <div class="flex space-x-1">
                  <div
                      v-for="i in 4"
                      :key="i"
                      class="h-1 flex-1 rounded-full transition-colors"
                      :class="getPasswordStrengthColor(i)"
                  ></div>
                </div>
                <p class="text-xs mt-1" :class="passwordStrengthTextColor">
                  {{ passwordStrengthText }}
                </p>
              </div>
            </div>

            <!-- Role info section -->
            <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h4 class="font-medium text-gray-900 mb-3 text-center">
                As a {{ formData.role === 'principal' ? 'Principal' : 'Teacher' }}, you'll be able to:
              </h4>
              <div class="grid grid-cols-2 gap-2 text-sm text-gray-700">
                <div class="flex items-center">
                  <span class="text-slate-600 mr-2">✓</span>
                  Manage lesson updates
                </div>
                <div class="flex items-center">
                  <span class="text-slate-600 mr-2">✓</span>
                  Track student progress
                </div>
                <div class="flex items-center">
                  <span class="text-slate-600 mr-2">✓</span>
                  Add and manage students
                </div>
                <div v-if="formData.role === 'principal'" class="flex items-center">
                  <span class="text-slate-600 mr-2">✓</span>
                  Manage teachers
                </div>
                <div class="flex items-center">
                  <span class="text-slate-600 mr-2">✓</span>
                  View survey reports
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <Button
                type="submit"
                :disabled="isLoading || !isFormValid"
                class="w-full bg-slate-900 text-white font-medium py-2.5 px-4 rounded-md hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
            <span v-if="!isLoading" class="flex items-center justify-center">
              Create Account
            </span>
              <span v-else class="flex items-center justify-center">
              <Loader class="animate-spin mr-2 w-4 h-4"/>
              Creating Account...
            </span>
            </Button>
          </form>

          <!-- Login link -->
          <div class="mt-6 text-center">
            <p class="text-sm text-gray-600">
              Already have an account?
              <router-link
                  to="/teacher/login"
                  class="font-medium text-slate-900 hover:text-slate-700 transition-colors"
              >
                Sign in here
              </router-link>
            </p>
          </div>

          <sign-in-links active-link="teacher"/>

        </Card>

        <!-- Footer text -->
        <div class="text-center mt-6">
          <p class="text-gray-600 text-sm">
            Ready to inspire and educate young minds?
          </p>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import {ref, computed, watch, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {GraduationCapIcon, EyeIcon, EyeOffIcon, Loader, CheckCircleIcon, AlertCircleIcon} from 'lucide-vue-next'
import axios from '@/plugins/axios.js'
import {Input} from "@/components/ui/input/index.js";
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from "@/components/ui/select/index.js";
import {Button} from "@/components/ui/button/index.js";
import SignInLinks from "@/components/partials/SignInLinks.vue";
import {Card} from "@/components/ui/card/index.js";
import GuestNavbar from "@/components/app/GuestNavbar.vue";

// Router
const router = useRouter()

// Reactive data
const formData = ref({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  subject: '',
  school_id: '',
  school_name: '',
  school_address: '',
  school_phone: '',
  role: 'teacher'
})

const showPassword = ref(false)
const isLoading = ref(false)
const response = ref(null)
const errors = ref({})
const schools = ref([])
const isLoadingSchools = ref(false)

// Password strength calculation
const passwordStrength = computed(() => {
  const password = formData.value.password
  let strength = 0

  if (password.length >= 6) strength++
  if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++
  if (password.match(/\d/)) strength++
  if (password.match(/[^a-zA-Z\d]/)) strength++

  return strength
})

const passwordStrengthText = computed(() => {
  const strength = passwordStrength.value
  const texts = ['Too weak 😟', 'Weak 😐', 'Good 😊', 'Strong 💪', 'Super strong! 🦸‍♂️']
  return texts[strength] || texts[0]
})

const passwordStrengthTextColor = computed(() => {
  const strength = passwordStrength.value
  const colors = ['text-red-500', 'text-orange-500', 'text-yellow-500', 'text-green-500', 'text-green-600']
  return colors[strength] || colors[0]
})

const isFormValid = computed(() => {
  const baseValid = formData.value.first_name &&
      formData.value.last_name &&
      formData.value.email &&
      formData.value.subject &&
      formData.value.password &&
      passwordStrength.value >= 2 &&
      Object.keys(errors.value).length === 0
  
  if (formData.value.role === 'teacher') {
    return baseValid &&
        formData.value.school_id &&
        formData.value.school_id !== 'loading' &&
        formData.value.school_id !== 'no-schools'
  } else {
    return baseValid && formData.value.school_name
  }
})

const alertClasses = computed(() => {
  if (!response.value) return ''
  return response.value.success
      ? 'border-green-200 bg-green-50'
      : 'border-red-200 bg-red-50'
})

// Methods
const getPasswordStrengthColor = (index) => {
  const strength = passwordStrength.value
  if (index <= strength) {
    const colors = ['bg-red-400', 'bg-orange-400', 'bg-yellow-400', 'bg-green-400', 'bg-green-500']
    return colors[strength - 1] || 'bg-gray-200'
  }
  return 'bg-gray-200'
}

const getInputClasses = (field) => {
  const baseClasses = 'focus:border-slate-400 focus:ring-slate-400'
  const errorClasses = errors.value[field] ? 'border-red-400 focus:border-red-400 focus:ring-red-400' : 'border-gray-300'
  return `${baseClasses} ${errorClasses}`
}

const handleSubmit = async () => {
  isLoading.value = true
  response.value = null
  errors.value = {}

  try {
    let apiData
    
    if (formData.value.role === 'principal') {
      // For principals, send school data with registration
      apiData = {
        email: formData.value.email,
        password: formData.value.password,
        first_name: formData.value.first_name,
        last_name: formData.value.last_name,
        subject: formData.value.subject,
        role: 'principal',
        school_name: formData.value.school_name,
        school_address: formData.value.school_address,
        school_phone: formData.value.school_phone
      }
    } else {
      // For teachers, register with existing school
      apiData = {
        email: formData.value.email,
        password: formData.value.password,
        first_name: formData.value.first_name,
        last_name: formData.value.last_name,
        subject: formData.value.subject,
        school_id: parseInt(formData.value.school_id),
        role: 'teacher'
      }
    }

    // Single API call for both teachers and principals
    const apiResponse = await axios.post('/api/teacher/register', apiData)

    if (apiResponse.data) {
      const accountType = formData.value.role === 'principal' ? 'Principal' : 'Teacher'
      response.value = {
        success: true,
        message: `${accountType} account created successfully! Welcome to EduMaster! 🎉`,
        data: apiResponse.data
      }

      // Store tokens and user info
      localStorage.setItem('access_token', apiResponse.data.access_token)
      localStorage.setItem('refresh_token', apiResponse.data.refresh_token)
      localStorage.setItem('user_email', apiResponse.data.user_email)
      localStorage.setItem('user_type', formData.value.role)

      // Redirect to teacher dashboard
      setTimeout(() => {
        router.push('/teacher/dashboard')
      }, 1000)
    }
  } catch (error) {
    let errorMessage = 'Registration failed. Please try again.'
    if (error.response) {
      errorMessage = error.response.data.error || error.response.data.message

      // Handle specific field errors if they exist
      if (error.response.data.details) {
        errors.value = error.response.data.details
      }
    } else if (error.request) {
      errorMessage = 'Network error. Please check your connection and try again.'
    }
    response.value = {
      success: false,
      message: errorMessage
    }
  } finally {
    isLoading.value = false
  }
}

// Fetch schools from API
const fetchSchools = async () => {
  isLoadingSchools.value = true
  try {
    // Use axios without authentication for public endpoint
    const apiResponse = await axios.get('/api/schools')
    schools.value = apiResponse.data.schools || []
  } catch (error) {
    console.error('Failed to fetch schools:', error)
    schools.value = []
  } finally {
    isLoadingSchools.value = false
  }
}

// Clear errors when user starts typing
watch(formData, (newData, oldData) => {
  Object.keys(newData).forEach(key => {
    if (newData[key] !== oldData[key] && errors.value[key]) {
      delete errors.value[key]
    }
  })
}, {deep: true})

// Load schools on component mount
onMounted(() => {
  fetchSchools()
})
</script>

<style scoped>
</style>
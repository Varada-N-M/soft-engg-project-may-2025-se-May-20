<template>
  <div class="bg-gradient-to-br from-blue-400 via-purple-400 to-teal-300">
    <GuestNavbar/>
    <div
        class="min-h-screen  flex items-center justify-center p-4">
      <!-- Floating decorative elements -->
      <FloatingDecorativeElements/>

      <div class="w-full max-w-2xl">
        <!-- Main registration card -->
        <Card class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <!-- Decorative top wave -->
          <div
              class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-t-3xl"></div>

          <!-- App logo and title -->
          <div class="relative z-10 text-center  pt-4">
            <div
                class="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
              <GraduationCapIcon class="w-10 h-10 text-white"/>
            </div>
            <p class="text-gray-600 text-sm">Join Our Teaching Community - Create Your Teacher Account</p>
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

          <!-- Registration form -->
          <form @submit.prevent="handleSubmit" class="space-y-5">
            <!-- Name Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="firstName" class="block text-sm font-semibold text-gray-700 mb-2">
                  👤 First Name *
                </label>
                <Input
                    id="firstName"
                    v-model="formData.first_name"
                    type="text"
                    placeholder="Your first name"
                    :class="getInputClasses('first_name')"
                    required
                />
                <p v-if="errors.first_name" class="text-xs text-red-500 mt-1">{{ errors.first_name }}</p>
              </div>

              <div>
                <label for="lastName" class="block text-sm font-semibold text-gray-700 mb-2">
                  👤 Last Name *
                </label>
                <Input
                    id="lastName"
                    v-model="formData.last_name"
                    type="text"
                    placeholder="Your last name"
                    :class="getInputClasses('last_name')"
                    required
                />
                <p v-if="errors.last_name" class="text-xs text-red-500 mt-1">{{ errors.last_name }}</p>
              </div>
            </div>

            <!-- Email -->
            <div>
              <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">
                📧 Email Address *
              </label>
              <Input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  placeholder="your.email@school.edu"
                  :class="getInputClasses('email')"
                  required
              />
              <p class="text-xs text-gray-500 mt-1">This will be your login email</p>
              <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
            </div>

            <!-- Subject and School -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label for="subject" class="block text-sm font-semibold text-gray-700 mb-2">
                  📚 Subject *
                </label>
                <Select
                    id="subject"
                    v-model="formData.subject"
                    :class="getInputClasses('subject')"
                    required
                >
                  <SelectTrigger class="w-full">
                    <SelectValue placeholder="Select your subject"></SelectValue>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Math">🔢 Mathematics</SelectItem>
                    <SelectItem value="English">📖 English</SelectItem>
                    <SelectItem value="Science">🔬 Science</SelectItem>
                    <SelectItem value="Social Studies">🌍 Social Studies</SelectItem>
                    <SelectItem value="Computers">💻 Computer Science</SelectItem>
                    <SelectItem value="Art">🎨 Art</SelectItem>
                    <SelectItem value="Music">🎵 Music</SelectItem>
                    <SelectItem value="Physical Education">⚽ Physical Education</SelectItem>
                  </SelectContent>
                </Select>
                <p v-if="errors.subject" class="text-xs text-red-500 mt-1">{{ errors.subject }}</p>
              </div>

              <div>
                <label for="school_id" class="block text-sm font-semibold text-gray-700 mb-2">
                  🏫 School *
                </label>
                <Select
                    id="school_id"
                    v-model="formData.school_id"
                    :class="getInputClasses('school_id')"
                    required
                >
                  <SelectTrigger class="w-full">
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
                <p v-if="errors.school_id" class="text-xs text-red-500 mt-1">{{ errors.school_id }}</p>
              </div>
            </div>

            <!-- Password -->
            <div>
              <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
                🔒 Password *
              </label>
              <div class="relative">
                <Input
                    id="password"
                    v-model="formData.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Create a strong password"
                    :class="getInputClasses('password')"
                    required
                />
                <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  <EyeIcon v-if="showPassword" class="w-5 h-5"/>
                  <EyeOffIcon v-else class="w-5 h-5"/>
                </button>
              </div>
              <p v-if="errors.password" class="text-xs text-red-500 mt-1">{{ errors.password }}</p>

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

            <!-- Teacher info section -->
            <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-4 border border-blue-200">
              <h4 class="font-semibold text-gray-800 mb-2 flex items-center justify-center">
                🌟 As a Teacher, You'll Be Able To:
              </h4>
              <div class="grid grid-cols-2 gap-2 text-xs text-gray-700">
                <div class="flex items-center">
                  <span class="text-blue-500 mr-1">✓</span>
                  Manage lesson updates
                </div>
                <div class="flex items-center">
                  <span class="text-blue-500 mr-1">✓</span>
                  Track student progress
                </div>
                <div class="flex items-center">
                  <span class="text-blue-500 mr-1">✓</span>
                  Add and manage students
                </div>
                <div class="flex items-center">
                  <span class="text-blue-500 mr-1">✓</span>
                  View survey reports
                </div>
              </div>
            </div>

            <!-- Submit Button -->
            <Button
                type="submit"
                :disabled="isLoading || !isFormValid"
                class="w-full bg-gradient-to-r from-blue-500 to-purple-500 text-white font-bold py-4 px-4 rounded-xl hover:from-blue-600 hover:to-purple-600 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-lg"
            >
            <span v-if="!isLoading" class="flex items-center justify-center">
              🎓 Create Teacher Account!
            </span>
              <span v-else class="flex items-center justify-center">
              <Loader class="animate-spin mr-2"/>
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
                  class="font-semibold text-blue-600 hover:text-blue-800 transition-colors"
              >
                Sign in here
              </router-link>
            </p>
          </div>

          <sign-in-links active-link="teacher"/>

          <emoji-bounce-animation :emojis="['🎓','📚','👨‍🏫','⭐']"/>

        </Card>

        <!-- Footer text -->
        <div class="text-center mt-6">
          <p class="text-white text-sm opacity-80">
            Ready to inspire and educate young minds? 🌟
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
import EmojiBounceAnimation from "@/components/partials/EmojiBounceAnimation.vue";
import SignInLinks from "@/components/partials/SignInLinks.vue";
import FloatingDecorativeElements from "@/components/partials/FloatingDecorativeElements.vue";
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
  school_id: ''
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
  return formData.value.first_name &&
      formData.value.last_name &&
      formData.value.email &&
      formData.value.subject &&
      formData.value.school_id &&
      formData.value.school_id !== 'loading' &&
      formData.value.school_id !== 'no-schools' &&
      formData.value.password &&
      passwordStrength.value >= 2 &&
      Object.keys(errors.value).length === 0
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
  const baseClasses = 'focus:border-blue-400'
  const errorClasses = errors.value[field] ? 'border-red-400' : 'border-gray-200'
  return `${baseClasses} ${errorClasses}`
}

const handleSubmit = async () => {
  isLoading.value = true
  response.value = null
  errors.value = {}

  try {
    const apiData = {
      email: formData.value.email,
      password: formData.value.password,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      subject: formData.value.subject,
      school_id: parseInt(formData.value.school_id)
    }

    const apiResponse = await axios.post('/api/teacher/register', apiData)

    if (apiResponse.data) {
      response.value = {
        success: true,
        message: 'Teacher account created successfully! Welcome to CoolKids! 🎉',
        data: apiResponse.data
      }

      // Store tokens and user info
      localStorage.setItem('access_token', apiResponse.data.access_token)
      localStorage.setItem('refresh_token', apiResponse.data.refresh_token)
      localStorage.setItem('user_email', apiResponse.data.user_email)
      localStorage.setItem('user_type', 'teacher')

      // Redirect to teacher dashboard
      setTimeout(() => {
        router.push('/teacher/dashboard')
      }, 1000)
    }
  } catch (error) {
    let errorMessage = 'Registration failed. Please try again.'
    if (error.response) {
      errorMessage = error.response.data.error

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
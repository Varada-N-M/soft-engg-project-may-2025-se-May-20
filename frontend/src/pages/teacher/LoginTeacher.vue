<template>
  <div class="bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-400">
    <GuestNavbar/>
    <div
        class="min-h-screen  flex items-center justify-center p-4">
      <!-- Floating decorative elements -->
      <FloatingDecorativeElements/>

      <div class="w-full max-w-md">
        <!-- Main login card -->
        <Card class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <!-- Decorative top wave -->
          <div
              class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-t-3xl"></div>

          <!-- App logo and title -->
          <div class="relative z-10 text-center pt-4">
            <div
                class="w-20 h-20 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
              <GraduationCapIcon class="w-10 h-10 text-white"/>
            </div>
            <p class="text-gray-600 text-sm">Teacher Portal - Inspire & Educate</p>
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
            <div class="flex items-center justify-center space-x-1 bg-gray-100 rounded-full p-1">
              <button
                  type="button"
                  @click="formData.role = 'teacher'"
                  :class="formData.role === 'teacher' 
                    ? 'bg-indigo-600 text-white shadow-sm' 
                    : 'text-gray-600 hover:text-indigo-600'"
                  class="flex-1 px-4 py-2 text-sm font-medium rounded-full transition-all duration-200"
              >
                👨‍🏫 Teacher
              </button>
              <button
                  type="button"
                  @click="formData.role = 'principal'"
                  :class="formData.role === 'principal' 
                    ? 'bg-indigo-600 text-white shadow-sm' 
                    : 'text-gray-600 hover:text-indigo-600'"
                  class="flex-1 px-4 py-2 text-sm font-medium rounded-full transition-all duration-200"
              >
                👑 Principal
              </button>
            </div>
          </div>

          <!-- Login form -->
          <form @submit.prevent="handleLogin" class="space-y-6">
            <div class="space-y-4">
              <!-- Username/Email field -->
              <div class="relative">
                <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">
                  👨‍🏫 Email Address
                </label>
                <Input
                    id="email"
                    v-model="formData.email"
                    type="email"
                    placeholder="Enter your professional email"
                    class="w-full px-4 py-6 border-2 placeholder-gray-400 text-lg"
                    :class="getInputClasses('email')"
                    required
                />
                <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
              </div>

              <!-- Password field -->
              <div class="relative">
                <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
                  🔐 Password
                </label>
                <div class="relative">
                  <Input
                      id="password"
                      v-model="formData.password"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="Enter your secure password"
                      class="w-full px-4 py-6 border-2  pr-12 text-lg"
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
              </div>
            </div>

            <!-- Forgot password link -->
            <div class="flex justify-end">
              <router-link 
                to="/user/password/reset" 
                class="text-sm text-indigo-600 hover:text-indigo-800 font-medium transition-colors"
              >
                Forgot your password?
              </router-link>
            </div>

            <!-- Login button -->
            <button
                type="submit"
                :disabled="isLoading"
                class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-bold py-4 px-4 rounded-xl hover:from-indigo-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-lg"
            >
            <span v-if="!isLoading" class="flex items-center justify-center">
                Login
            </span>
              <span v-else class="flex items-center justify-center">
               <Loader class="animate-spin mr-2"/>
              Authenticating...
            </span>
            </button>
          </form>

          <!-- Sign up link -->
          <div class="mt-6 text-center">
            <p class="text-sm text-gray-600">
              New educator at
              <logo/>
              ?
              <a href="/teacher/register" class="font-semibold text-indigo-600 hover:text-indigo-800 transition-colors">
                Join our faculty
              </a>
            </p>
          </div>

          <!-- Other login types -->
          <sign-in-links active-link="teacher"/>

          <!-- Professional elements at bottom -->
          <emoji-bounce-animation :emojis="['📖','🎓','✏️','🏅']"/>
        </Card>

        <!-- Footer text -->
        <div class="text-center mt-6">
          <p class="text-white text-sm opacity-80">
            Empowering minds, shaping futures with EduMaster! 🌟
          </p>
        </div>
      </div>

    </div>
  </div>

</template>

<script setup>
import {computed, ref, watch} from 'vue'
import {useRouter} from 'vue-router'
import {AlertCircleIcon, CheckCircleIcon, EyeIcon, EyeOffIcon, GraduationCapIcon, Loader} from 'lucide-vue-next'
import axios from '@/plugins/axios.js'
import SignInLinks from "@/components/partials/SignInLinks.vue";
import Logo from "@/components/partials/Logo.vue";
import EmojiBounceAnimation from "@/components/partials/EmojiBounceAnimation.vue";
import {Input} from "@/components/ui/input/index.js";
import FloatingDecorativeElements from "@/components/partials/FloatingDecorativeElements.vue";
import {Card} from "@/components/ui/card/index.js";
import GuestNavbar from "@/components/app/GuestNavbar.vue";

// Router
const router = useRouter()

// Reactive data
const formData = ref({
  email: '',
  password: '',
  role: 'teacher',
  rememberMe: false
})

const showPassword = ref(false)
const isLoading = ref(false)
const response = ref(null)
const errors = ref({})
const showHelp = ref(false)

// Computed properties
const alertClasses = computed(() => {
  if (!response.value) return ''
  return response.value.success
      ? 'border-green-200 bg-green-50'
      : 'border-red-200 bg-red-50'
})

// Methods
const getInputClasses = (field) => {
  const baseClasses = 'focus:border-indigo-400'
  const errorClasses = errors.value[field] ? 'border-red-400' : 'border-gray-200'
  return `${baseClasses} ${errorClasses}`
}

const validateForm = () => {
  const newErrors = {}

  if (!formData.value.email) {
    newErrors.email = 'Please enter your email address'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
    newErrors.email = 'Please enter a valid email address'
  }

  if (!formData.value.password) {
    newErrors.password = 'Please enter your password'
  } else if (formData.value.password.length < 6) {
    newErrors.password = 'Password must be at least 6 characters'
  }

  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

const handleLogin = async () => {
  if (!validateForm()) return

  isLoading.value = true
  response.value = null

  try {
    const loginData = {
      email: formData.value.email,
      password: formData.value.password,
      role_type: formData.value.role === 'principal' ? 'principal' : 'teacher'
    }

    const apiResponse = await axios.post('/api/login', loginData)

    if (apiResponse.data) {
      // Store tokens in localStorage
      localStorage.setItem('access_token', apiResponse.data.access_token)
      localStorage.setItem('refresh_token', apiResponse.data.refresh_token)
      localStorage.setItem('user_email', apiResponse.data.user)
      localStorage.setItem('user_type', formData.value.role)

      response.value = {
        success: true,
        message: apiResponse.data.message || 'Welcome back, educator! Ready to inspire? 🎓'
      }

      // Redirect to teacher dashboard after a short delay
      setTimeout(() => {
        router.push('/teacher/dashboard')
      }, 500)
    }
  } catch (error) {
    console.error('Login error:', error)

    let errorMessage = 'Authentication failed. Please verify your credentials.'

    if (error.response) {
      // Server responded with error status
      if (error.response.status === 401) {
        errorMessage = 'Invalid email or password. Please check your credentials and try again.'
      } else if (error.response.status === 422) {
        errorMessage = 'Please verify your email and password format.'
      } else if (error.response.status === 403) {
        errorMessage = 'Access denied. Please contact your administrator.'
      } else if (error.response.data && error.response.data.message) {
        errorMessage = error.response.data.message
      }
    } else if (error.request) {
      // Network error
      errorMessage = 'Connection error. Please check your network and try again.'
    }

    response.value = {
      success: false,
      message: errorMessage
    }
  } finally {
    isLoading.value = false
  }
}

// Clear errors when user starts typing
const clearErrors = () => {
  if (errors.value.email && formData.value.email) {
    delete errors.value.email
  }
  if (errors.value.password && formData.value.password) {
    delete errors.value.password
  }
}

// Watch for form changes to clear errors
watch(formData, clearErrors, {deep: true})
</script>
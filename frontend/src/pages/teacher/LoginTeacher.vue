<template>
  <div class="min-h-screen bg-gray-50">
    <GuestNavbar/>
    <div class="flex items-center justify-center p-4 pt-16">
      <div class="w-full max-w-md">
        <!-- Main login card -->
        <Card class="bg-white border shadow-sm p-8">
          <!-- App logo and title -->
          <div class="text-center mb-8">
            <div class="w-16 h-16 bg-slate-900 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <GraduationCapIcon class="w-8 h-8 text-white"/>
            </div>
            <h1 class="text-2xl font-semibold text-gray-900 mb-2">Teacher Portal</h1>
            <p class="text-gray-600 text-sm">Sign in to your account</p>
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

          <!-- Login form -->
          <form @submit.prevent="handleLogin" class="space-y-6">
            <div class="space-y-4">
              <!-- Username/Email field -->
              <div class="space-y-2">
                <label for="email" class="block text-sm font-medium text-gray-700">
                  Email Address
                </label>
                <Input
                    id="email"
                    v-model="formData.email"
                    type="email"
                    placeholder="Enter your email"
                    class="w-full h-10"
                    :class="getInputClasses('email')"
                    required
                />
                <p v-if="errors.email" class="text-xs text-red-500">{{ errors.email }}</p>
              </div>

              <!-- Password field -->
              <div class="space-y-2">
                <label for="password" class="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <div class="relative">
                  <Input
                      id="password"
                      v-model="formData.password"
                      :type="showPassword ? 'text' : 'password'"
                      placeholder="Enter your password"
                      class="w-full h-10 pr-10"
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
              </div>
            </div>

            <!-- Forgot password link -->
            <div class="flex justify-end">
              <router-link 
                to="/user/password/reset" 
                class="text-sm text-slate-600 hover:text-slate-900 font-medium transition-colors"
              >
                Forgot your password?
              </router-link>
            </div>

            <!-- Login button -->
            <button
                type="submit"
                :disabled="isLoading"
                class="w-full bg-slate-900 text-white font-medium py-2.5 px-4 rounded-md hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-500 focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
            <span v-if="!isLoading" class="flex items-center justify-center">
                Sign In
            </span>
              <span v-else class="flex items-center justify-center">
               <Loader class="animate-spin mr-2 w-4 h-4"/>
              Signing in...
            </span>
            </button>
          </form>

          <!-- Sign up link -->
          <div class="mt-6 text-center">
            <p class="text-sm text-gray-600">
              New to the platform?
              <a href="/teacher/register" class="font-medium text-slate-900 hover:text-slate-700 transition-colors">
                Create an account
              </a>
            </p>
          </div>

          <!-- Other login types -->
          <sign-in-links active-link="teacher"/>
        </Card>

        <!-- Footer text -->
        <div class="text-center mt-6">
          <p class="text-gray-600 text-sm">
            Empowering education through technology
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
import {Input} from "@/components/ui/input/index.js";
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

// Computed properties
const alertClasses = computed(() => {
  if (!response.value) return ''
  return response.value.success
      ? 'border-green-200 bg-green-50'
      : 'border-red-200 bg-red-50'
})

// Methods
const getInputClasses = (field) => {
  const baseClasses = 'focus:border-slate-400 focus:ring-slate-400'
  const errorClasses = errors.value[field] ? 'border-red-400 focus:border-red-400 focus:ring-red-400' : 'border-gray-300'
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
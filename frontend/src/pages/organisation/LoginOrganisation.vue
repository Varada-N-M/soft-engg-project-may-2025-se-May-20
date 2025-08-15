<template>
  <div
      class="min-h-screen bg-gradient-to-br from-blue-400 via-purple-400 to-indigo-300 flex items-center justify-center p-4">
    <!-- Floating decorative elements -->
    <FloatingDecorativeElements/>

    <div class="w-full max-w-md">
      <!-- Main login card -->
      <Card class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
        <!-- Decorative top wave -->
        <div
            class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-t-3xl"></div>

        <!-- App logo and title -->
        <div class="relative z-10 text-center mb-8 pt-4">
          <div
              class="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
            <BuildingIcon class="w-10 h-10 text-white"/>
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2 font-fancy">GrowWise</h1>
          <p class="text-gray-600 text-sm">Organization Login - Admin Access</p>
        </div>

        <!-- Response Alert -->
        <div v-if="response" class="mb-6 p-4 rounded-lg border-2" :class="alertClasses">
          <div class="flex items-center">
            <CheckCircleIcon v-if="response.success" class="h-5 w-5 mr-2"
                             :class="response.success ? 'text-green-600' : 'text-red-600'"/>
            <AlertCircleIcon v-else class="h-5 w-5 mr-2" :class="response.success ? 'text-green-600' : 'text-red-600'"/>
            <p :class="response.success ? 'text-green-800' : 'text-red-800'">{{ response.message }}</p>
          </div>
        </div>

        <!-- Login form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-4">
            <!-- Email field -->
            <div class="relative">
              <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">
                📧 Organization Email
              </label>
              <input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  placeholder="admin@yourorganization.com"
                  class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400"
                  :class="getInputClasses('email')"
                  required
              />
              <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
            </div>

            <!-- Password field -->
            <div class="relative">
              <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
                🔒 Password
              </label>
              <div class="relative">
                <input
                    id="password"
                    v-model="formData.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Enter your password"
                    class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 pr-12"
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


          <!-- Login button -->
          <button
              type="submit"
              :disabled="isLoading"
              class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-3 px-4 rounded-xl hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              🏢 Sign In to Organization
            </span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing In...
            </span>
          </button>
        </form>

        <!-- Sign up link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Don't have an organization account?
            <router-link
                to="/org/register"
                class="font-semibold text-blue-600 hover:text-blue-800 transition-colors"
            >
              Register your organization
            </router-link>
          </p>
        </div>

        <!-- Other login types -->
        <sign-in-links active-link="org"/>

      </Card>

      <!-- Footer text -->
      <div class="text-center mt-6">
        <p class="text-white text-sm opacity-80">
          Empowering educational institutions to deliver exceptional learning experiences
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, watch, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {BuildingIcon, EyeIcon, EyeOffIcon, CheckCircleIcon, AlertCircleIcon} from 'lucide-vue-next'
import axios from '@/plugins/axios.js'
import SignInLinks from "@/components/partials/SignInLinks.vue";
import FloatingDecorativeElements from "@/components/partials/FloatingDecorativeElements.vue";
import {Card} from "@/components/ui/card/index.js";

// Router
const router = useRouter()

// Reactive data
const formData = ref({
  email: '',
  password: '',
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
  const baseClasses = 'focus:border-blue-400'
  const errorClasses = errors.value[field] ? 'border-red-400' : 'border-gray-200'
  return `${baseClasses} ${errorClasses}`
}

const validateForm = () => {
  const newErrors = {}

  if (!formData.value.email) {
    newErrors.email = 'Email is required'
  } else if (!/\S+@\S+\.\S+/.test(formData.value.email)) {
    newErrors.email = 'Email is invalid'
  }

  if (!formData.value.password) {
    newErrors.password = 'Password is required'
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
      role_type: 'organization'
    }

    const apiResponse = await axios.post('/api/login', loginData)

    if (apiResponse.data) {
      // Store tokens in localStorage
      localStorage.setItem('access_token', apiResponse.data.access_token)
      localStorage.setItem('refresh_token', apiResponse.data.refresh_token)
      localStorage.setItem('user_email', apiResponse.data.user)
      localStorage.setItem('user_type', 'organization')


      response.value = {
        success: true,
        message: apiResponse.data.message || 'Login successful! Welcome back! 🎉'
      }

      // Redirect to organization dashboard after a short delay
      setTimeout(() => {
        router.push('/org/home')
      }, 500)
    }
  } catch (error) {
    console.error('Login error:', error)

    let errorMessage = 'Login failed. Please try again.'

    if (error.response) {
      // Server responded with error status
      if (error.response.status === 401) {
        errorMessage = 'Invalid email or password. Please check your credentials.'
      } else if (error.response.status === 422) {
        errorMessage = 'Please check your email and password format.'
      } else if (error.response.data && error.response.data.message) {
        errorMessage = error.response.data.message
      }
    } else if (error.request) {
      // Network error
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

<style scoped>


.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}


</style>

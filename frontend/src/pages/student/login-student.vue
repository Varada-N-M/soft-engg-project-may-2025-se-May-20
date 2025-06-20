<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300 flex items-center justify-center p-4">
    <!-- Floating decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-16 h-16 bg-yellow-300 rounded-full opacity-60 animate-bounce"></div>
      <div class="absolute top-40 right-20 w-12 h-12 bg-pink-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 0.5s"></div>
      <div class="absolute bottom-32 left-20 w-20 h-20 bg-orange-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 right-10 w-14 h-14 bg-cyan-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 1.5s"></div>
      <div class="absolute top-1/2 left-4 w-10 h-10 bg-red-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 2s"></div>
    </div>

    <div class="w-full max-w-md">
      <!-- Main login card -->
      <div class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
        <!-- Decorative top wave -->
        <div class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-green-500 to-blue-500 rounded-t-3xl"></div>

        <!-- App logo and title -->
        <div class="relative z-10 text-center mb-8 pt-4">
          <div class="w-20 h-20 bg-gradient-to-br from-green-500 to-blue-500 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
            <StarIcon class="w-10 h-10 text-white" />
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2 font-fancy">CoolKids</h1>
          <p class="text-gray-600 text-sm">Student Login - Let's Learn & Play!</p>
        </div>

        <!-- Response Alert -->
        <div v-if="response" class="mb-6 p-4 rounded-lg border-2" :class="alertClasses">
          <div class="flex items-center">
            <CheckCircleIcon v-if="response.success" class="h-5 w-5 mr-2" :class="response.success ? 'text-green-600' : 'text-red-600'" />
            <AlertCircleIcon v-else class="h-5 w-5 mr-2" :class="response.success ? 'text-green-600' : 'text-red-600'" />
            <p :class="response.success ? 'text-green-800' : 'text-red-800'">{{ response.message }}</p>
          </div>
        </div>

        <!-- Login form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-4">
            <!-- Username/Email field -->
            <div class="relative">
              <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">
                👤 Username or Email
              </label>
              <input
                  id="email"
                  v-model="formData.email"
                  type="text"
                  placeholder="Enter your username or email"
                  class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 text-lg"
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
                    class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 pr-12 text-lg"
                    :class="getInputClasses('password')"
                    required
                />
                <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 focus:outline-none"
                >
                  <EyeIcon v-if="showPassword" class="w-5 h-5" />
                  <EyeOffIcon v-else class="w-5 h-5" />
                </button>
              </div>
              <p v-if="errors.password" class="text-xs text-red-500 mt-1">{{ errors.password }}</p>
            </div>
          </div>

          <!-- Remember me and help -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                  id="remember"
                  v-model="formData.rememberMe"
                  type="checkbox"
                  class="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 rounded focus:ring-green-500"
              />
              <label for="remember" class="ml-2 text-sm text-gray-700">
                Remember me
              </label>
            </div>
            <button
                type="button"
                @click="showHelp = true"
                class="text-sm text-green-600 hover:text-green-800 transition-colors"
            >
              Need help? 🤔
            </button>
          </div>

          <!-- Login button -->
          <button
              type="submit"
              :disabled="isLoading"
              class="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white font-bold py-4 px-4 rounded-xl hover:from-green-600 hover:to-blue-600 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none text-lg"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              🚀 Let's Start Learning!
            </span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Getting Ready...
            </span>
          </button>
        </form>

        <!-- Fun motivational section -->
        <div class="mt-6 p-4 bg-gradient-to-r from-yellow-50 to-green-50 rounded-xl border border-yellow-200">
          <h4 class="font-semibold text-gray-800 mb-2 flex items-center justify-center">
            🌟 Ready for an Adventure?
          </h4>
          <div class="grid grid-cols-2 gap-2 text-xs text-gray-700">
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Fun games & quizzes
            </div>
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Earn cool badges
            </div>
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Learn new things
            </div>
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Beat your scores
            </div>
          </div>
        </div>
        <!-- Sign up link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            New to CoolKids ?
            <a href="/student/register" class="font-semibold text-purple-600 hover:text-purple-800 transition-colors">
              Create an account
            </a>
          </p>
        </div>
        <!-- Other login types -->
        <sign-in-links active-link="student"/>

        <!-- Fun characters at bottom -->
        <div class="mt-6 flex justify-center space-x-4">
          <div class="text-2xl animate-bounce" style="animation-delay: 0s">🎮</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.2s">📚</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.4s">🏆</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.6s">⭐</div>
        </div>
      </div>

      <!-- Footer text -->
      <div class="text-center mt-6">
        <p class="text-white text-sm opacity-80">
          Learning is fun when you're with CoolKids! 🌈
        </p>
      </div>
    </div>

    <!-- Help Modal -->
    <div v-if="showHelp" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl p-6 max-w-sm w-full">
        <div class="text-center mb-4">
          <div class="w-16 h-16 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full mx-auto mb-3 flex items-center justify-center">
            <span class="text-2xl">🤗</span>
          </div>
          <h3 class="text-lg font-bold text-gray-800">Need Help?</h3>
        </div>

        <div class="space-y-3 text-sm text-gray-700">
          <div class="flex items-start space-x-2">
            <span class="text-blue-500">💡</span>
            <p>Ask your teacher or parent for your username and password</p>
          </div>
          <div class="flex items-start space-x-2">
            <span class="text-green-500">📞</span>
            <p>Call your school if you forgot your login details</p>
          </div>
          <div class="flex items-start space-x-2">
            <span class="text-purple-500">🎯</span>
            <p>Make sure you're typing carefully - no extra spaces!</p>
          </div>
        </div>

        <button
            @click="showHelp = false"
            class="w-full mt-4 bg-gradient-to-r from-blue-500 to-green-500 text-white py-2 rounded-lg font-medium hover:from-blue-600 hover:to-green-600 transition-all"
        >
          Got it! 👍
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, ref, watch} from 'vue'
import {useRouter} from 'vue-router'
import {AlertCircleIcon, CheckCircleIcon, EyeIcon, EyeOffIcon, StarIcon} from 'lucide-vue-next'
import axios from '@/plugins/axios.js'
import SignInLinks from "@/components/partials/sign-in-links.vue";

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
  const baseClasses = 'focus:border-green-400'
  const errorClasses = errors.value[field] ? 'border-red-400' : 'border-gray-200'
  return `${baseClasses} ${errorClasses}`
}

const validateForm = () => {
  const newErrors = {}

  if (!formData.value.email) {
    newErrors.email = 'Please enter your username or email'
  }

  if (!formData.value.password) {
    newErrors.password = 'Please enter your password'
  } else if (formData.value.password.length < 4) {
    newErrors.password = 'Password must be at least 4 characters'
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
      password: formData.value.password
    }

    const apiResponse = await axios.post('/api/login', loginData)

    if (apiResponse.data) {
      // Store tokens in localStorage
      localStorage.setItem('access_token', apiResponse.data.access_token)
      localStorage.setItem('refresh_token', apiResponse.data.refresh_token)
      localStorage.setItem('user_email', apiResponse.data.user)
      localStorage.setItem('user_type', 'student')

      // Store remember me preference
      if (formData.value.rememberMe) {
        localStorage.setItem('remember_me', 'true')
      }

      response.value = {
        success: true,
        message: apiResponse.data.message || 'Welcome back! Ready to learn? 🎉'
      }

      // Redirect to student dashboard after a short delay
      setTimeout(() => {
        router.push('/dashboard')
      }, 1500)
    }
  } catch (error) {
    console.error('Login error:', error)

    let errorMessage = 'Oops! Something went wrong. Please try again.'

    if (error.response) {
      // Server responded with error status
      if (error.response.status === 401) {
        errorMessage = 'Hmm, that username or password doesn\'t look right. Try again! 🤔'
      } else if (error.response.status === 422) {
        errorMessage = 'Please check your username and password.'
      } else if (error.response.data && error.response.data.message) {
        errorMessage = error.response.data.message
      }
    } else if (error.request) {
      // Network error
      errorMessage = 'Having trouble connecting. Check your internet and try again! 📶'
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
watch(formData, clearErrors, { deep: true })
</script>

<style scoped>
@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0,0,0);
  }
  40%, 43% {
    transform: translate3d(0,-30px,0);
  }
  70% {
    transform: translate3d(0,-15px,0);
  }
  90% {
    transform: translate3d(0,-4px,0);
  }
}

.animate-bounce {
  animation: bounce 2s infinite;
}

.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

</style>
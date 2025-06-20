<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-400 via-pink-400 to-orange-300 flex items-center justify-center p-4">
    <!-- Floating decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-16 h-16 bg-yellow-300 rounded-full opacity-60 animate-bounce"></div>
      <div class="absolute top-40 right-20 w-12 h-12 bg-green-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 0.5s"></div>
      <div class="absolute bottom-32 left-20 w-20 h-20 bg-blue-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 right-10 w-14 h-14 bg-red-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 1.5s"></div>
    </div>

    <div class="w-full max-w-md">
      <!-- Main login card -->
      <div class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
        <!-- Decorative top wave -->
        <div class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-blue-400 to-purple-500 rounded-t-3xl"></div>
        
        <!-- App logo and title -->
        <div class="relative z-10 text-center mb-8 pt-4">
          <div class="w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
            <svg class="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">CoolKids</h1>
          <p class="text-gray-600 text-sm">Let's start learning together!</p>
        </div>

        <!-- Login form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-4">
            <!-- Username field -->
            <div class="relative">
              <label for="username" class="block text-sm font-semibold text-gray-700 mb-2">
                👤 Username
              </label>
              <input
                id="username"
                v-model="username"
                type="text"
                placeholder="Enter your username"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400"
                required
              />
            </div>

            <!-- Password field -->
            <div class="relative">
              <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
                🔒 Password
              </label>
              <div class="relative">
                <input
                  id="password"
                  v-model="password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Enter your password"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400 pr-12"
                  required
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                >
                  <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Remember me checkbox -->
          <div class="flex items-center">
            <input
              id="remember"
              v-model="rememberMe"
              type="checkbox"
              class="w-4 h-4 text-purple-600 bg-gray-100 border-gray-300 rounded focus:ring-purple-500"
            />
            <label for="remember" class="ml-2 text-sm text-gray-700">
              Remember me for next time
            </label>
          </div>

          <!-- Login button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 px-4 rounded-xl hover:from-purple-600 hover:to-pink-600 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              🚀 Let's Learn!
            </span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Loading...
            </span>
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center">
          <div class="flex-1 border-t border-gray-200"></div>
          <span class="px-4 text-sm text-gray-500">or</span>
          <div class="flex-1 border-t border-gray-200"></div>
        </div>

        <!-- Social login buttons -->
        <div class="space-y-3">
          <button
            type="button"
            class="w-full flex items-center justify-center px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-colors"
          >
            <svg class="w-5 h-5 mr-3" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </button>

          <button
            type="button"
            class="w-full flex items-center justify-center px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 transition-colors"
          >
            <svg class="w-5 h-5 mr-3" fill="#1877F2" viewBox="0 0 24 24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
            Continue with Facebook
          </button>
        </div>

        <!-- Sign up link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            New to CoolKids?
            <a href="#" class="font-semibold text-purple-600 hover:text-purple-800 transition-colors">
              Create an account
            </a>
          </p>
        </div>

        <!-- Fun characters at bottom -->
        <div class="mt-6 flex justify-center space-x-4">
          <div class="text-2xl animate-bounce" style="animation-delay: 0s">🦄</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.2s">🌟</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.4s">🎨</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.6s">📚</div>
        </div>
      </div>

      <!-- Footer text -->
      <div class="text-center mt-6">
        <p class="text-white text-sm opacity-80">
          Safe, fun, and educational for kids aged 3-12
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Reactive data
const username = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const isLoading = ref(false)

// Methods
const handleLogin = async () => {
  isLoading.value = true
  
  // Simulate login process
  setTimeout(() => {
    console.log('Login attempt:', {
      username: username.value,
      password: password.value,
      rememberMe: rememberMe.value
    })
    isLoading.value = false
    // Here you would typically handle the actual login logic
  }, 2000)
}
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
</style>
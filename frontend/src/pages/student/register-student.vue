<template>
  <div
      class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300 flex items-center justify-center p-4">
    <!-- Floating decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-16 left-8 w-14 h-14 bg-pink-300 rounded-full opacity-60 animate-bounce"></div>
      <div class="absolute top-32 right-16 w-18 h-18 bg-yellow-300 rounded-full opacity-60 animate-bounce"
           style="animation-delay: 0.3s"></div>
      <div class="absolute bottom-40 left-16 w-16 h-16 bg-orange-300 rounded-full opacity-60 animate-bounce"
           style="animation-delay: 0.8s"></div>
      <div class="absolute bottom-24 right-12 w-12 h-12 bg-cyan-300 rounded-full opacity-60 animate-bounce"
           style="animation-delay: 1.2s"></div>
      <div class="absolute top-1/2 left-4 w-10 h-10 bg-red-300 rounded-full opacity-60 animate-bounce"
           style="animation-delay: 1.8s"></div>
    </div>

    <div class="w-full max-w-lg">
      <!-- Main registration card -->
      <div class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
        <!-- Decorative top wave -->
        <div class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-green-400 to-blue-500 rounded-t-3xl"></div>

        <!-- App logo and title -->
        <div class="relative z-10 text-center mb-6 pt-4">
          <div
              class="w-20 h-20 bg-gradient-to-br from-green-400 to-blue-500 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
            <svg class="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Join <span class="font-fancy">CoolKids!</span></h1>
          <p class="text-gray-600 text-sm">Create your account and start your learning adventure!</p>
        </div>

        <!-- Registration form -->
        <form @submit.prevent="handleRegister" class="space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- First Name -->
            <div>
              <label for="firstName" class="block text-sm font-semibold text-gray-700 mb-2">
                👶 First Name
              </label>
              <input
                  id="firstName"
                  v-model="formData.firstName"
                  type="text"
                  placeholder="Your first name"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400"
                  required
              />
            </div>

            <!-- Last Name -->
            <div>
              <label for="lastName" class="block text-sm font-semibold text-gray-700 mb-2">
                👨‍👩‍👧‍👦 Last Name
              </label>
              <input
                  id="lastName"
                  v-model="formData.lastName"
                  type="text"
                  placeholder="Your last name"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400"
                  required
              />
            </div>
          </div>

          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-semibold text-gray-700 mb-2">
              🎮 Username
            </label>
            <input
                id="username"
                v-model="formData.username"
                type="text"
                placeholder="Choose a cool username"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400"
                required
            />
            <p class="text-xs text-gray-500 mt-1">This will be your unique name in CoolKids!</p>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">
              📧 Email Address
            </label>
            <input
                id="email"
                v-model="formData.email"
                type="email"
                placeholder="your.email@example.com"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400"
                required
            />
          </div>

          <!-- Age Selection -->
          <div>
            <label for="age" class="block text-sm font-semibold text-gray-700 mb-2">
              🎂 How old are you?
            </label>
            <select
                id="age"
                v-model="formData.age"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:outline-none transition-colors text-gray-800"
                required
            >
              <option value="">Select your age</option>
              <option v-for="age in ageOptions" :key="age.value" :value="age.value">
                {{ age.label }}
              </option>
            </select>
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
              🔒 Password
            </label>
            <div class="relative">
              <input
                  id="password"
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Create a strong password"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400 pr-12"
                  required
              />
              <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                </svg>
              </button>
            </div>
            <!-- Password strength indicator -->
            <div class="mt-2">
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

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="block text-sm font-semibold text-gray-700 mb-2">
              🔐 Confirm Password
            </label>
            <div class="relative">
              <input
                  id="confirmPassword"
                  v-model="formData.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="Type your password again"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-400 focus:outline-none transition-colors text-gray-800 placeholder-gray-400 pr-12"
                  :class="{ 'border-red-400': formData.confirmPassword && !passwordsMatch }"
                  required
              />
              <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                <svg v-if="showConfirmPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"/>
                </svg>
              </button>
            </div>
            <p v-if="formData.confirmPassword && !passwordsMatch" class="text-xs text-red-500 mt-1">
              Passwords don't match! 😅
            </p>
            <p v-else-if="formData.confirmPassword && passwordsMatch" class="text-xs text-green-500 mt-1">
              Passwords match! ✅
            </p>
          </div>

          <!-- Terms and Privacy -->
          <div class="space-y-3">
            <div class="flex items-start">
              <input
                  id="terms"
                  v-model="formData.agreeToTerms"
                  type="checkbox"
                  class="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 rounded focus:ring-green-500 mt-1"
                  required
              />
              <label for="terms" class="ml-2 text-sm text-gray-700">
                I agree to the
                <a href="#" class="font-semibold text-green-600 hover:text-green-800 transition-colors">Terms of
                  Service</a>
                and
                <a href="#" class="font-semibold text-green-600 hover:text-green-800 transition-colors">Privacy
                  Policy</a>
              </label>
            </div>

            <div class="flex items-start">
              <input
                  id="newsletter"
                  v-model="formData.subscribeNewsletter"
                  type="checkbox"
                  class="w-4 h-4 text-green-600 bg-gray-100 border-gray-300 rounded focus:ring-green-500 mt-1"
              />
              <label for="newsletter" class="ml-2 text-sm text-gray-700">
                Send me fun learning tips and updates! 📚✨
              </label>
            </div>
          </div>

          <!-- Register button -->
          <button
              type="submit"
              :disabled="isLoading || !isFormValid"
              class="w-full bg-gradient-to-r from-green-500 to-blue-500 text-white font-bold py-3 px-4 rounded-xl hover:from-green-600 hover:to-blue-600 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              🎉 Create My Account!
            </span>
            <span v-else class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Creating Account...
            </span>
          </button>
        </form>


        <!-- Login link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Already have an account?
            <router-link to="/student/login"
                         class="font-semibold text-green-600 hover:text-green-800 transition-colors">
              Sign in here
            </router-link>
          </p>
        </div>

        <!-- Fun characters at bottom -->
        <div class="mt-6 flex justify-center space-x-4">
          <div class="text-2xl animate-bounce" style="animation-delay: 0s">🎓</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.2s">🌈</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.4s">🚀</div>
          <div class="text-2xl animate-bounce" style="animation-delay: 0.6s">⭐</div>
        </div>
      </div>

      <!-- Footer text -->
      <div class="text-center mt-6">
        <p class="text-white text-sm opacity-80">
          Join thousands of kids learning and having fun every day!
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed} from 'vue'

// Reactive data
const formData = ref({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  age: '',
  password: '',
  confirmPassword: '',
  agreeToTerms: false,
  subscribeNewsletter: false
})

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)

// Age options for kids
const ageOptions = [
  {value: '3', label: '3 years old 🍼'},
  {value: '4', label: '4 years old 🧸'},
  {value: '5', label: '5 years old 🎨'},
  {value: '6', label: '6 years old 📚'},
  {value: '7', label: '7 years old ✏️'},
  {value: '8', label: '8 years old 🔢'},
  {value: '9', label: '9 years old 🧮'},
  {value: '10', label: '10 years old 🔬'},
  {value: '11', label: '11 years old 🌟'},
  {value: '12', label: '12 years old 🎯'}
]

// Computed properties
const passwordsMatch = computed(() => {
  return formData.value.password === formData.value.confirmPassword
})

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
  return formData.value.firstName &&
      formData.value.lastName &&
      formData.value.username &&
      formData.value.email &&
      formData.value.age &&
      formData.value.password &&
      formData.value.confirmPassword &&
      passwordsMatch.value &&
      formData.value.agreeToTerms &&
      passwordStrength.value >= 2
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

const handleRegister = async () => {
  if (!isFormValid.value) return

  isLoading.value = true

  // Simulate registration process
  setTimeout(() => {
    console.log('Registration attempt:', formData.value)
    isLoading.value = false
    // Here you would typically handle the actual registration logic
  }, 2500)
}
</script>

<style scoped>
@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -30px, 0);
  }
  70% {
    transform: translate3d(0, -15px, 0);
  }
  90% {
    transform: translate3d(0, -4px, 0);
  }
}

.animate-bounce {
  animation: bounce 2s infinite;
}
</style>
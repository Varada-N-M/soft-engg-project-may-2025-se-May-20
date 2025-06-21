<template>
  <div
      class="min-h-screen bg-gradient-to-br from-pink-400 via-purple-400 to-indigo-300 flex items-center justify-center p-4">
    <!-- Floating decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-16 left-8 w-14 h-14 bg-yellow-300 rounded-full opacity-60 animate-bounce"></div>
      <div
          class="absolute top-32 right-16 w-18 h-18 bg-green-300 rounded-full opacity-60 animate-bounce"
          style="animation-delay: 0.3s"
      ></div>
      <div
          class="absolute bottom-40 left-16 w-16 h-16 bg-orange-300 rounded-full opacity-60 animate-bounce"
          style="animation-delay: 0.8s"
      ></div>
      <div
          class="absolute bottom-24 right-12 w-12 h-12 bg-cyan-300 rounded-full opacity-60 animate-bounce"
          style="animation-delay: 1.2s"
      ></div>
      <div
          class="absolute top-1/2 left-4 w-10 h-10 bg-red-300 rounded-full opacity-60 animate-bounce"
          style="animation-delay: 1.8s"
      ></div>
    </div>

    <div class="w-full max-w-lg">
      <!-- Main registration card -->
      <Card class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
        <!-- Decorative top wave -->
        <div
            class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-pink-500 to-purple-600 rounded-t-3xl"></div>

        <!-- App logo and title -->
        <div class="relative z-10 text-center mb-6 pt-4">
          <div
              class="w-20 h-20 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
            <HeartIcon class="w-10 h-10 text-white"/>
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Join as a Parent!</h1>
          <p class="text-gray-600 text-sm">Create your account and support your child's learning journey!</p>
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
                placeholder="your.email@example.com"
                :class="getInputClasses('email')"
                required
            />
            <p class="text-xs text-gray-500 mt-1">This will be your login email and where we'll send updates</p>
            <p v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</p>
          </div>

          <!-- Phone Number -->
          <div>
            <label for="phoneNumber" class="block text-sm font-semibold text-gray-700 mb-2">
              📱 Phone Number *
            </label>
            <Input
                id="phoneNumber"
                v-model="formData.phone_number"
                type="tel"
                placeholder="1234567890"
                :class="getInputClasses('phone_number')"
                required
            />
            <p class="text-xs text-gray-500 mt-1">We'll use this for important notifications about your child</p>
            <p v-if="errors.phone_number" class="text-xs text-red-500 mt-1">{{ errors.phone_number }}</p>
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
                  placeholder="Create a secure password"
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

          <!-- Parent-specific information box -->
          <div class="bg-gradient-to-r from-pink-50 to-purple-50 rounded-xl p-4 border border-pink-200">
            <h4 class="font-semibold text-gray-800 mb-2 flex items-center">
              💝 As a parent, you'll be able to:
            </h4>
            <ul class="text-sm text-gray-700 space-y-1">
              <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Track your child's learning
                progress
              </li>
              <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Receive weekly progress reports
              </li>
              <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Set learning goals and rewards
              </li>
              <li class="flex items-center"><span class="text-green-500 mr-2">✓</span>Connect with teachers and other
                parents
              </li>
            </ul>
          </div>

          <!-- Submit Button -->
          <button
              type="submit"
              :disabled="isLoading || !isFormValid"
              class="w-full bg-gradient-to-r from-pink-500 to-purple-600 text-white font-bold py-4 px-4 rounded-xl hover:from-pink-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              💝 Create Parent Account
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
            Already have a parent account?
            <router-link to="/parent/login" class="font-semibold text-pink-600 hover:text-pink-800 transition-colors">
              Sign in here
            </router-link>
          </p>
        </div>

        <!-- Fun characters at bottom -->
        <EmojiBounceAnimation :emojis="['👨‍👩‍👧‍👦','💕','📚','🌟']"/>

      </Card>

      <!-- Footer text -->
      <div class="text-center mt-6">
        <p class="text-white text-sm opacity-80">
          Join thousands of parents supporting their children's learning journey
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, watch} from 'vue'
import {HeartIcon, EyeIcon, EyeOffIcon, CheckCircleIcon, AlertCircleIcon} from 'lucide-vue-next'
import api from '@/plugins/axios'
import EmojiBounceAnimation from "@/components/partials/EmojiBounceAnimation.vue";
import {Input} from "@/components/ui/input/index.js";

// Reactive data
const formData = ref({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  phone_number: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const response = ref(null)
const errors = ref({})

// Password strength calculation
const passwordStrength = computed(() => {
  const password = formData.value.password
  let strength = 0

  if (password.length >= 8) strength++
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
      formData.value.phone_number &&
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
  const baseClasses = 'focus:border-pink-400'
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
  } else if (formData.value.password.length < 8) {
    newErrors.password = 'Password must be at least 8 characters'
  }

  if (!formData.value.first_name) newErrors.first_name = 'First name is required'
  if (!formData.value.last_name) newErrors.last_name = 'Last name is required'

  if (!formData.value.phone_number) {
    newErrors.phone_number = 'Phone number is required'
  } else if (!/^\d+$/.test(formData.value.phone_number)) {
    newErrors.phone_number = 'Phone number must contain only digits'
  }

  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) return

  isLoading.value = true
  response.value = null

  try {
    const apiData = {
      email: formData.value.email,
      password: formData.value.password,
      first_name: formData.value.first_name,
      last_name: formData.value.last_name,
      phone_number: formData.value.phone_number // keep as string, backend expects string
    }

    const res = await api.post('/api/parent/register', apiData)
    const result = res.data

    response.value = {
      success: true,
      message: result.message || 'Parent account created successfully! Welcome to CooKids! 🎉',
      data: result
    }
    // Optionally, store tokens here: result.access_token, result.refresh_token
    formData.value = {
      email: '',
      password: '',
      first_name: '',
      last_name: '',
      phone_number: ''
    }
    errors.value = {}
  } catch (error) {
    let msg = 'Network error. Please check your connection and try again.'
    if (error.response) {
      msg = error.response.data?.error || error.response.data?.message || msg
    }
    response.value = {
      success: false,
      message: msg
    }
  } finally {
    isLoading.value = false
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
</script>

<style scoped>

</style>
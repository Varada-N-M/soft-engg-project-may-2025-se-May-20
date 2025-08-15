<template>
  <div class="min-h-screen bg-gray-50">
    <GuestNavbar/>
    <div class="flex items-center justify-center p-4 pt-16">
      <div class="w-full max-w-lg">
        <!-- Main registration card -->
        <Card class="bg-white border shadow-sm p-8">
          <!-- App logo and title -->
          <div class="text-center mb-8">
            <div class="w-16 h-16 bg-slate-900 rounded-lg mx-auto mb-4 flex items-center justify-center">
              <HeartIcon class="w-8 h-8 text-white"/>
            </div>
            <h1 class="text-2xl font-semibold text-gray-900 mb-2">Create Parent Account</h1>
            <p class="text-gray-600 text-sm">Join our parent community</p>
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
                  placeholder="your.email@example.com"
                  class="h-10"
                  :class="getInputClasses('email')"
                  required
              />
              <p class="text-xs text-gray-500">This will be your login email</p>
              <p v-if="errors.email" class="text-xs text-red-500">{{ errors.email }}</p>
            </div>

            <!-- Phone Number -->
            <div class="space-y-2">
              <label for="phoneNumber" class="block text-sm font-medium text-gray-700">
                Phone Number *
              </label>
              <Input
                  id="phoneNumber"
                  v-model="formData.phone_number"
                  type="tel"
                  placeholder="1234567890"
                  class="h-10"
                  :class="getInputClasses('phone_number')"
                  required
              />
              <p class="text-xs text-gray-500">For important notifications</p>
              <p v-if="errors.phone_number" class="text-xs text-red-500">{{ errors.phone_number }}</p>
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
                    placeholder="Create a secure password"
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

            <!-- Parent-specific information box -->
            <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h4 class="font-medium text-gray-900 mb-3">
                As a parent, you'll be able to:
              </h4>
              <ul class="text-sm text-gray-700 space-y-2">
                <li class="flex items-center"><span class="text-slate-600 mr-2">✓</span>Track your child's learning progress
                </li>
                <li class="flex items-center"><span class="text-slate-600 mr-2">✓</span>Receive weekly progress reports
                </li>
                <li class="flex items-center"><span class="text-slate-600 mr-2">✓</span>Set learning goals and rewards
                </li>
                <li class="flex items-center"><span class="text-slate-600 mr-2">✓</span>Connect with teachers
                </li>
              </ul>
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
              <router-link to="/parent/login" class="font-medium text-slate-900 hover:text-slate-700 transition-colors">
                Sign in here
              </router-link>
            </p>
          </div>

        </Card>

        <!-- Footer text -->
        <div class="text-center mt-6">
          <p class="text-gray-600 text-sm">
            Join our parent community
          </p>
        </div>
      </div>
    </div>

  </div>

</template>

<script setup>
import {ref, computed, watch} from 'vue'
import {HeartIcon, EyeIcon, EyeOffIcon, CheckCircleIcon, AlertCircleIcon, Loader} from 'lucide-vue-next'
import api from '@/plugins/axios'
import {Input} from "@/components/ui/input/index.js";
import {Button} from "@/components/ui/button/index.js";
import {Card} from "@/components/ui/card/index.js";
import GuestNavbar from "@/components/app/GuestNavbar.vue";

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
  const baseClasses = 'focus:border-slate-400 focus:ring-slate-400'
  const errorClasses = errors.value[field] ? 'border-red-400 focus:border-red-400 focus:ring-red-400' : 'border-gray-300'
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
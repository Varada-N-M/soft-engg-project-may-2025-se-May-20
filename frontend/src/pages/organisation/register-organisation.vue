<template>
  <div
      class="min-h-screen bg-gradient-to-br from-blue-400 via-purple-400 to-pink-300 flex items-center justify-center p-4">
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

    <div class="w-full max-w-2xl">
      <!-- Main registration card -->
      <div class="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
        <!-- Decorative top wave -->
        <div
            class="absolute top-0 left-0 right-0 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-t-3xl"></div>

        <!-- App logo and title -->
        <div class="relative z-10 text-center mb-6 pt-4">
          <div
              class="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full mx-auto mb-4 flex items-center justify-center shadow-lg">
            <BuildingIcon class="w-10 h-10 text-white"/>
          </div>
          <h1 class="text-3xl font-bold text-gray-800 mb-2">Register Your Organization</h1>
          <p class="text-gray-600 text-sm">Join CoolKids and start creating amazing learning experiences for kids!</p>
        </div>

        <!-- Response Alert -->
        <div v-if="response" class="mb-6 p-4 rounded-lg border-2"
             :class="response.success ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'">
          <div class="flex items-center">
            <CheckCircleIcon v-if="response.success" class="h-5 w-5 mr-2"
                             :class="response.success ? 'text-green-600' : 'text-red-600'"/>
            <AlertCircleIcon v-else class="h-5 w-5 mr-2" :class="response.success ? 'text-green-600' : 'text-red-600'"/>
            <p :class="response.success ? 'text-green-800' : 'text-red-800'">{{ response.message }}</p>
          </div>
        </div>

        <!-- Registration form -->
        <form @submit.prevent="handleSubmit" class="space-y-5">
          <!-- Organization Name - Featured prominently -->
          <div>
            <label for="organizationName" class="block text-sm font-semibold text-gray-700 mb-2">
              🏫 Organization Name *
            </label>
            <input
                id="organizationName"
                v-model="formData.organization_name"
                type="text"
                placeholder="e.g., Sunshine Elementary School, ABC Learning Center"
                class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 border-gray-200"
                required
            />
            <p class="text-xs text-gray-500 mt-1">This will be displayed to students and parents</p>
          </div>

          <!-- Administrator Details -->
          <div class="bg-gray-50 rounded-xl p-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              👨‍💼 Administrator Details
            </h3>

            <!-- Name Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label for="firstName" class="block text-sm font-semibold text-gray-700 mb-2">
                  First Name *
                </label>
                <input
                    id="firstName"
                    v-model="formData.first_name"
                    type="text"
                    placeholder="Administrator's first name"
                    class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 border-gray-200"
                    required
                />
              </div>

              <div>
                <label for="lastName" class="block text-sm font-semibold text-gray-700 mb-2">
                  Last Name *
                </label>
                <input
                    id="lastName"
                    v-model="formData.last_name"
                    type="text"
                    placeholder="Administrator's last name"
                    class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 border-gray-200"
                    required
                />
              </div>
            </div>

            <!-- Email -->
            <div class="mb-4">
              <label for="email" class="block text-sm font-semibold text-gray-700 mb-2">
                📧 Email Address *
              </label>
              <input
                  id="email"
                  v-model="formData.email"
                  type="email"
                  placeholder="admin@yourorganization.com"
                  class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 border-gray-200"
                  required
              />
              <p class="text-xs text-gray-500 mt-1">This will be your login email</p>
            </div>

            <!-- Password -->
            <div>
              <label for="password" class="block text-sm font-semibold text-gray-700 mb-2">
                🔒 Password *
              </label>
              <div class="relative">
                <input
                    id="password"
                    v-model="formData.password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Create a secure password"
                    class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 pr-12 border-gray-200"
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
            </div>
          </div>

          <!-- Contact Information -->
          <div class="bg-blue-50 rounded-xl p-4">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              📞 Contact Information
            </h3>

            <!-- Phone Number -->
            <div class="mb-4">
              <label for="phoneNumber" class="block text-sm font-semibold text-gray-700 mb-2">
                📱 Phone Number *
              </label>
              <input
                  id="phoneNumber"
                  v-model="formData.phone_number"
                  type="tel"
                  placeholder="1234567890"
                  class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 border-gray-200"
                  required
              />
              <p class="text-xs text-gray-500 mt-1">Primary contact number for your organization</p>
            </div>

            <!-- Address -->
            <div>
              <label for="address" class="block text-sm font-semibold text-gray-700 mb-2">
                🏠 Organization Address *
              </label>
              <textarea
                  id="address"
                  v-model="formData.address"
                  rows="3"
                  placeholder="Enter your organization's full address"
                  class="w-full px-4 py-3 border-2 rounded-xl focus:outline-none transition-colors text-gray-800 placeholder-gray-400 resize-none border-gray-200"
                  required
              ></textarea>
            </div>
          </div>


          <!-- Submit Button -->
          <button
              type="submit"
              :disabled="isLoading"
              class="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-4 px-4 rounded-xl hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            <span v-if="!isLoading" class="flex items-center justify-center">
              🎉 Register Organization
            </span>
          </button>
        </form>


        <!-- Login link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            Already have an organization account?
            <a href="/org/login" class="font-semibold text-blue-600 hover:text-blue-800 transition-colors">
              Sign in here
            </a>
          </p>
        </div>

      </div>

      <!-- Footer text -->
      <div class="text-center mt-6">
        <p class="text-white text-sm opacity-80">
          Trusted by schools and learning centers worldwide to deliver quality education
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref} from 'vue'
import {BuildingIcon, EyeIcon, EyeOffIcon, CheckCircleIcon, AlertCircleIcon} from 'lucide-vue-next'
import api from '@/plugins/axios'

// Reactive data
const formData = ref({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
  organization_name: '',
  phone_number: '',
  address: ''
})

const showPassword = ref(false)
const isLoading = ref(false)
const response = ref(null)

const handleSubmit = async () => {
  isLoading.value = true
  response.value = null

  // Prepare data as required by backend
  const apiData = {
    email: formData.value.email,
    password: formData.value.password,
    first_name: formData.value.first_name,
    last_name: formData.value.last_name,
    organization_name: formData.value.organization_name,
    phone_number: formData.value.phone_number,
    address: formData.value.address
  }

  try {
    const {data: result} = await api.post('/api/organization/register', apiData)
    response.value = {
      success: true,
      message: result.message || 'Organization registered successfully! Welcome to CoolKids! 🎉',
      data: result
    }

    localStorage.setItem('refreshToken', result.refresh_token)
    localStorage.setItem('accessToken', result.access_token)
    localStorage.setItem('role', result.role)

    this.$router.push('/org/home')

  } catch (error) {
    response.value = {
      success: false,
      message: error.response?.data?.error || error.response?.data?.message || 'Registration failed. Please try again.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

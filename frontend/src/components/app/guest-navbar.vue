<template>
  <header class="bg-white border-b-2 border-gray-200 sticky top-0 z-50">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center space-x-4">
          <router-link to="/" class="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div class="hidden sm:block">
              <h1 class="text-2xl font-black  font-fancy  text-gray-800">
                CoolKids
              </h1>
              <p class="text-xs text-gray-500 -mt-1">Learning Made Fun!</p>
            </div>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <!-- Main Navigation Links -->
<!--          <div class="flex items-center space-x-6">-->
<!--            <router-link-->
<!--                to="/about"-->
<!--                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"-->
<!--                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/about' }"-->
<!--            >-->
<!--              ℹ️ About-->
<!--            </router-link>-->

<!--            <router-link-->
<!--                to="/features"-->
<!--                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"-->
<!--                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/features' }"-->
<!--            >-->
<!--              ✨ Features-->
<!--            </router-link>-->

<!--            <router-link-->
<!--                to="/pricing"-->
<!--                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"-->
<!--                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/pricing' }"-->
<!--            >-->
<!--              💰 Pricing-->
<!--            </router-link>-->

<!--            <router-link-->
<!--                to="/contact"-->
<!--                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"-->
<!--                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/contact' }"-->
<!--            >-->
<!--              📞 Contact-->
<!--            </router-link>-->
<!--          </div>-->

          <!-- Login/Signup Actions -->
          <div class="flex items-center space-x-4">
            <!-- Login Dropdown -->
            <div class="relative">
              <button
                  @click="showLoginMenu = !showLoginMenu"
                  class="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors font-medium"
              >
                <LogInIcon class="w-4 h-4" />
                <span>Sign In</span>
                <ChevronDownIcon class="w-4 h-4" />
              </button>

              <!-- Login Menu Dropdown -->
              <div
                  v-if="showLoginMenu"
                  class="absolute right-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                  @click.stop
              >
                <div class="px-4 py-2 border-b border-gray-100">
                  <h3 class="font-semibold text-gray-800">Choose Your Role</h3>
                  <p class="text-xs text-gray-500 mt-1">Select how you want to sign in</p>
                </div>

                <div class="py-1">
                  <router-link
                      to="/student/login"
                      class="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600 transition-colors"
                      @click="showLoginMenu = false"
                  >
                    <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center mr-3">
                      <span class="text-white text-xs font-bold">👦</span>
                    </div>
                    <div>
                      <p class="font-medium">Student Login</p>
                      <p class="text-xs text-gray-500">Access your learning dashboard</p>
                    </div>
                  </router-link>

                  <router-link
                      to="/parent/login"
                      class="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-pink-50 hover:text-pink-600 transition-colors"
                      @click="showLoginMenu = false"
                  >
                    <div class="w-8 h-8 bg-gradient-to-br from-pink-400 to-red-500 rounded-full flex items-center justify-center mr-3">
                      <span class="text-white text-xs font-bold">👨‍👩‍👧‍👦</span>
                    </div>
                    <div>
                      <p class="font-medium">Parent Login</p>
                      <p class="text-xs text-gray-500">Monitor your child's progress</p>
                    </div>
                  </router-link>

                  <router-link
                      to="/teacher/login"
                      class="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-green-50 hover:text-green-600 transition-colors"
                      @click="showLoginMenu = false"
                  >
                    <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mr-3">
                      <span class="text-white text-xs font-bold">👨‍🏫</span>
                    </div>
                    <div>
                      <p class="font-medium">Teacher Login</p>
                      <p class="text-xs text-gray-500">Manage your classroom</p>
                    </div>
                  </router-link>

                  <router-link
                      to="/org/login"
                      class="flex items-center px-4 py-3 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                      @click="showLoginMenu = false"
                  >
                    <div class="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center mr-3">
                      <span class="text-white text-xs font-bold">🏢</span>
                    </div>
                    <div>
                      <p class="font-medium">Organization Login</p>
                      <p class="text-xs text-gray-500">School & institution access</p>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Get Started Button -->
            <router-link
                to="/"
                class="bg-gradient-to-r from-blue-500 to-pink-500 text-white px-6 py-2 rounded-lg font-medium hover:from-blue-600 hover:to-pink-600 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              🚀 Get Started
            </router-link>
          </div>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden">
          <button
              @click="showMobileMenu = !showMobileMenu"
              class="p-2 rounded-lg text-gray-500 hover:text-blue-600 hover:bg-blue-50 transition-colors"
          >
            <MenuIcon v-if="!showMobileMenu" class="w-6 h-6" />
            <XIcon v-else class="w-6 h-6" />
          </button>
        </div>
      </div>

      <!-- Mobile Navigation Menu -->
      <div
          v-if="showMobileMenu"
          class="md:hidden border-t border-gray-200 bg-white"
      >
        <div class="px-2 pt-2 pb-3 space-y-1">
          <!-- Mobile Navigation Links -->
          <router-link
              to="/about"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/about' }"
              @click="showMobileMenu = false"
          >
            ℹ️ About
          </router-link>

          <router-link
              to="/features"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/features' }"
              @click="showMobileMenu = false"
          >
            ✨ Features
          </router-link>

          <router-link
              to="/pricing"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/pricing' }"
              @click="showMobileMenu = false"
          >
            💰 Pricing
          </router-link>

          <router-link
              to="/contact"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/contact' }"
              @click="showMobileMenu = false"
          >
            📞 Contact
          </router-link>
        </div>

        <!-- Mobile Login Section -->
        <div class="border-t border-gray-200 pt-4 pb-3">
          <div class="px-4 mb-3">
            <h3 class="font-semibold text-gray-800 mb-2">Sign In As:</h3>
          </div>

          <div class="space-y-1 px-2">
            <router-link
                to="/login/student"
                class="flex items-center px-3 py-3 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
                @click="showMobileMenu = false"
            >
              <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center mr-3">
                <span class="text-white text-xs">👦</span>
              </div>
              <div>
                <p class="font-medium">Student</p>
                <p class="text-xs text-gray-500">Access learning dashboard</p>
              </div>
            </router-link>

            <router-link
                to="/login/parent"
                class="flex items-center px-3 py-3 rounded-lg text-base font-medium text-gray-700 hover:text-pink-600 hover:bg-pink-50"
                @click="showMobileMenu = false"
            >
              <div class="w-8 h-8 bg-gradient-to-br from-pink-400 to-red-500 rounded-full flex items-center justify-center mr-3">
                <span class="text-white text-xs">👨‍👩‍👧‍👦</span>
              </div>
              <div>
                <p class="font-medium">Parent</p>
                <p class="text-xs text-gray-500">Monitor child's progress</p>
              </div>
            </router-link>

            <router-link
                to="/login/teacher"
                class="flex items-center px-3 py-3 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
                @click="showMobileMenu = false"
            >
              <div class="w-8 h-8 bg-gradient-to-br from-green-400 to-teal-500 rounded-full flex items-center justify-center mr-3">
                <span class="text-white text-xs">👨‍🏫</span>
              </div>
              <div>
                <p class="font-medium">Teacher</p>
                <p class="text-xs text-gray-500">Manage classroom</p>
              </div>
            </router-link>

            <router-link
                to="/login/organization"
                class="flex items-center px-3 py-3 rounded-lg text-base font-medium text-gray-700 hover:text-indigo-600 hover:bg-indigo-50"
                @click="showMobileMenu = false"
            >
              <div class="w-8 h-8 bg-gradient-to-br from-indigo-400 to-purple-500 rounded-full flex items-center justify-center mr-3">
                <span class="text-white text-xs">🏢</span>
              </div>
              <div>
                <p class="font-medium">Organization</p>
                <p class="text-xs text-gray-500">School & institution</p>
              </div>
            </router-link>
          </div>

          <!-- Mobile Get Started Button -->
          <div class="px-2 mt-4">
            <router-link
                to="/get-started"
                class="block w-full bg-gradient-to-r from-blue-500 to-pink-500 text-white text-center px-6 py-3 rounded-lg font-medium hover:from-blue-600 hover:to-pink-600 transition-all duration-200 shadow-lg"
                @click="showMobileMenu = false"
            >
              🚀 Get Started Free
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Click outside to close dropdowns -->
    <div
        v-if="showLoginMenu"
        class="fixed inset-0 z-40"
        @click="closeAllDropdowns"
    ></div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import {
  BookOpenIcon,
  ChevronDownIcon,
  MenuIcon,
  XIcon,
  LogInIcon
} from 'lucide-vue-next'

// Reactive state
const showMobileMenu = ref(false)
const showLoginMenu = ref(false)

// Methods
const closeAllDropdowns = () => {
  showLoginMenu.value = false
}

// Close dropdowns when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    closeAllDropdowns()
  }
}

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Smooth transitions */
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

/* Active link styles */


/* Hover effects for login options */
.hover\:bg-pink-50:hover {
  background-color: #fdf2f8;
}

.hover\:text-pink-600:hover {
  color: #db2777;
}

.hover\:bg-green-50:hover {
  background-color: #f0fdf4;
}

.hover\:text-green-600:hover {
  color: #16a34a;
}

.hover\:bg-indigo-50:hover {
  background-color: #eef2ff;
}

.hover\:text-indigo-600:hover {
  color: #4f46e5;
}
</style>
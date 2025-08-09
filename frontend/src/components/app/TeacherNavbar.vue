<template>
  <header class="bg-white border-b-2 border-gray-200 sticky top-0 z-50">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center space-x-4">
          <router-link to="/teacher/dashboard" class="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center shadow-lg">
              <span class="text-white text-lg font-bold">👨‍🏫</span>
            </div>
            <div class="hidden sm:block">
              <h1 class="text-2xl font-black font-fancy text-gray-800">
                CoolKids
              </h1>
              <p class="text-xs text-gray-500 -mt-1">Teacher Portal</p>
            </div>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <!-- Main Navigation Links -->
          <div class="flex items-center space-x-6">
            <router-link
                to="/teacher/dashboard"
                class="text-gray-700 hover:text-green-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-green-50"
                :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/dashboard' }"
            >
              📊 Dashboard
            </router-link>

            <router-link
                to="/teacher/lesson-updates"
                class="text-gray-700 hover:text-green-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-green-50"
                :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/lesson-updates' }"
            >
              📚 Lesson Updates
            </router-link>

            <router-link
                to="/teacher/students"
                class="text-gray-700 hover:text-green-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-green-50"
                :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/students' }"
            >
              👥 Manage Students
            </router-link>

            <router-link
                to="/teacher/reports"
                class="text-gray-700 hover:text-green-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-green-50"
                :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/reports' }"
            >
              📈 Reports
            </router-link>
          </div>

          <!-- User Actions -->
          <div class="flex items-center space-x-4">
            <!-- Notifications -->
            <div class="relative">
              <button
                  @click="showNotifications = !showNotifications"
                  class="p-2 text-gray-500 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors relative"
              >
                <BellIcon class="w-5 h-5" />
                <span v-if="notificationCount > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {{ notificationCount }}
                </span>
              </button>

              <!-- Notifications Dropdown -->
              <div
                  v-if="showNotifications"
                  class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                  @click.stop
              >
                <div class="px-4 py-2 border-b border-gray-100">
                  <h3 class="font-semibold text-gray-800">Notifications</h3>
                </div>
                <div class="max-h-64 overflow-y-auto">
                  <div v-for="notification in notifications" :key="notification.id" class="px-4 py-3 hover:bg-gray-50 border-b border-gray-50 last:border-b-0">
                    <div class="flex items-start space-x-3">
                      <div class="text-2xl">{{ notification.emoji }}</div>
                      <div class="flex-1">
                        <p class="text-sm font-medium text-gray-800">{{ notification.title }}</p>
                        <p class="text-xs text-gray-500 mt-1">{{ notification.message }}</p>
                        <p class="text-xs text-gray-400 mt-1">{{ notification.time }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="px-4 py-2 border-t border-gray-100">
                  <button class="text-sm text-green-600 hover:text-green-800 font-medium">
                    View all notifications
                  </button>
                </div>
              </div>
            </div>

            <!-- User Profile Dropdown -->
            <div class="relative">
              <button
                  @click="showUserMenu = !showUserMenu"
                  class="flex items-center space-x-2 p-2 rounded-lg hover:bg-green-50 transition-colors"
              >
                <div class="w-8 h-8 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-bold">{{ userInitials }}</span>
                </div>
                <ChevronDownIcon class="w-4 h-4 text-gray-500" />
              </button>

              <!-- User Menu Dropdown -->
              <div
                  v-if="showUserMenu"
                  class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                  @click.stop
              >
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-800">{{ currentUser.name }}</p>
                  <p class="text-xs text-gray-500">{{ currentUser.email }}</p>
                  <div class="flex items-center mt-2">
                    <div class="flex items-center space-x-1">
                      <span class="text-sm font-medium text-gray-700">Teacher ID: {{ currentUser.teacher_id || 'T001' }}</span>
                    </div>
                  </div>
                </div>

                <div class="py-1">
                  <router-link
                      to="/teacher/profile"
                      class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-green-50 hover:text-green-600"
                      @click="showUserMenu = false"
                  >
                    <UserIcon class="w-4 h-4 mr-3" />
                    My Profile
                  </router-link>

                  <router-link
                      to="/teacher/settings"
                      class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-green-50 hover:text-green-600"
                      @click="showUserMenu = false"
                  >
                    <SettingsIcon class="w-4 h-4 mr-3" />
                    Settings
                  </router-link>

                  <router-link
                      to="/teacher/help"
                      class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-green-50 hover:text-green-600"
                      @click="showUserMenu = false"
                  >
                    <HelpCircleIcon class="w-4 h-4 mr-3" />
                    Help & Support
                  </router-link>
                </div>

                <div class="border-t border-gray-100 py-1">
                  <button
                      @click="handleLogout"
                      class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                  >
                    <LogOutIcon class="w-4 h-4 mr-3" />
                    Sign Out
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden">
          <button
              @click="showMobileMenu = !showMobileMenu"
              class="p-2 rounded-lg text-gray-500 hover:text-green-600 hover:bg-green-50 transition-colors"
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
              to="/teacher/dashboard"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
              :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/dashboard' }"
              @click="showMobileMenu = false"
          >
            📊 Dashboard
          </router-link>

          <router-link
              to="/teacher/lesson-updates"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
              :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/lesson-updates' }"
              @click="showMobileMenu = false"
          >
            📚 Lesson Updates
          </router-link>

          <router-link
              to="/teacher/students"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
              :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/students' }"
              @click="showMobileMenu = false"
          >
            👥 Manage Students
          </router-link>

          <router-link
              to="/teacher/reports"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
              :class="{ 'text-green-600 bg-green-50': $route.path === '/teacher/reports' }"
              @click="showMobileMenu = false"
          >
            📈 Reports
          </router-link>
        </div>

        <!-- Mobile User Section -->
        <div class="border-t border-gray-200 pt-4 pb-3">
          <div class="flex items-center px-5">
            <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center">
              <span class="text-white font-bold">{{ userInitials }}</span>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{{ currentUser.name }}</div>
              <div class="text-sm text-gray-500">{{ currentUser.email }}</div>
              <div class="text-xs text-gray-500 mt-1">ID: {{ currentUser.teacher_id || 'T001' }}</div>
            </div>
          </div>

          <div class="mt-3 space-y-1 px-2">
            <router-link
                to="/teacher/profile"
                class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
                @click="showMobileMenu = false"
            >
              👤 My Profile
            </router-link>

            <router-link
                to="/teacher/settings"
                class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
                @click="showMobileMenu = false"
            >
              ⚙️ Settings
            </router-link>

            <router-link
                to="/teacher/help"
                class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-green-600 hover:bg-green-50"
                @click="showMobileMenu = false"
            >
              ❓ Help & Support
            </router-link>

            <button
                @click="handleLogout"
                class="block w-full text-left px-3 py-2 rounded-lg text-base font-medium text-red-600 hover:bg-red-50"
            >
              🚪 Sign Out
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Click outside to close dropdowns -->
    <div
        v-if="showNotifications || showUserMenu"
        class="fixed inset-0 z-40"
        @click="closeAllDropdowns"
    ></div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  BellIcon,
  ChevronDownIcon,
  MenuIcon,
  XIcon,
  UserIcon,
  SettingsIcon,
  HelpCircleIcon,
  LogOutIcon
} from 'lucide-vue-next'

const router = useRouter()

// Reactive state
const showMobileMenu = ref(false)
const showNotifications = ref(false)
const showUserMenu = ref(false)
const notificationCount = ref(2)

// Mock user data - replace with actual user data from your auth system
const currentUser = ref({
  name: 'Ms. Sarah Johnson',
  email: 'sarah.johnson@school.edu',
  teacher_id: 'T001',
  avatar: null
})

// Mock notifications - replace with actual notifications from your API
const notifications = ref([
  {
    id: 1,
    emoji: '📚',
    title: 'New Student Enrolled',
    message: 'Alex Smith has been added to your Math class',
    time: '15 minutes ago'
  },
  {
    id: 2,
    emoji: '📊',
    title: 'Weekly Report Ready',
    message: 'Your class performance report is available',
    time: '2 hours ago'
  }
])

// Computed properties
const userInitials = computed(() => {
  const names = currentUser.value.name.split(' ')
  return names.map(name => name.charAt(0)).join('').toUpperCase()
})

// Methods
const closeAllDropdowns = () => {
  showNotifications.value = false
  showUserMenu.value = false
}

const handleLogout = () => {
  // Implement logout logic here
  console.log('Logging out...')
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push('/teacher/login')
  closeAllDropdowns()
  showMobileMenu.value = false
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
/* Custom scrollbar for notifications */
.max-h-64::-webkit-scrollbar {
  width: 4px;
}

.max-h-64::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.max-h-64::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.max-h-64::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

/* Smooth transitions */
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
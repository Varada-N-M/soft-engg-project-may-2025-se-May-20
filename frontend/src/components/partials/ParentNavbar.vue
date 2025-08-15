<template>
  <header class="bg-white border-b-2 border-gray-200 sticky top-0 z-50">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center space-x-4">
          <router-link to="/parent/home" class="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center shadow-lg">
              <span class="text-white text-lg font-bold">👨‍👩‍👧‍👦</span>
            </div>
            <div class="hidden sm:block">
              <h1 class="text-2xl font-black font-fancy text-gray-800">
                GrowWise
              </h1>
              <p class="text-xs text-gray-500 -mt-1">Parent Portal</p>
            </div>
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <!-- Main Navigation Links -->
          <div class="flex items-center space-x-6">
            <router-link
                to="/parent/home"
                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"
                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/home' || $route.path === '/parent/home' }"
            >
              📊 Dashboard
            </router-link>

            <router-link
                to="/parent/children"
                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"
                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/children' }"
            >
              👥 My Children
            </router-link>

            <router-link
                to="/parent/lesson-updates"
                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"
                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/lesson-updates' }"
            >
              📚 Lesson Updates
            </router-link>

            <router-link
                to="/parent/link-child"
                class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"
                :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/link-child' }"
            >
              🔗 Link Child
            </router-link>

            <!-- Progress Dropdown -->
            <div class="relative" v-if="hasLinkedChildren">
              <button
                  @click="showProgressMenu = !showProgressMenu"
                  class="flex items-center space-x-1 text-gray-700 hover:text-blue-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"
                  :class="{ 'text-blue-600 bg-blue-50': $route.path.includes('/parent/child-progress') || $route.path.includes('/parent/achievements') }"
              >
                <span>📈 Progress</span>
                <ChevronDownIcon class="w-4 h-4" />
              </button>

              <!-- Progress Menu Dropdown -->
              <div
                  v-if="showProgressMenu"
                  class="absolute left-0 mt-2 w-64 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
                  @click.stop
              >
                <div v-for="child in linkedChildren" :key="child.child_id" class="border-b border-gray-100 last:border-b-0">
                  <div class="px-4 py-2 text-xs font-medium text-gray-500 bg-gray-50">
                    {{ child.first_name }} {{ child.last_name }}
                  </div>
                  <router-link
                      :to="`/parent/child-progress/${child.child_id}`"
                      class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600"
                      @click="showProgressMenu = false"
                  >
                    📊 Progress Details
                  </router-link>
                  <router-link
                      :to="`/parent/achievements/${child.child_id}`"
                      class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600"
                      @click="showProgressMenu = false"
                  >
                    🏆 Achievements
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- User Actions -->
          <div class="flex items-center space-x-4">
            <!-- User Profile Dropdown -->
            <div class="relative">
              <button
                  @click="showUserMenu = !showUserMenu"
                  class="flex items-center space-x-2 p-2 rounded-lg hover:bg-blue-50 transition-colors"
              >
                <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
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
                  <p class="text-sm font-medium text-gray-800">Parent Account</p>
                  <p class="text-xs text-gray-500">{{ userEmail }}</p>
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
              to="/parent/home"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/home' || $route.path === '/parent/home' }"
              @click="showMobileMenu = false"
          >
            📊 Dashboard
          </router-link>

          <router-link
              to="/parent/children"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/children' }"
              @click="showMobileMenu = false"
          >
            👥 My Children
          </router-link>

          <router-link
              to="/parent/lesson-updates"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/lesson-updates' }"
              @click="showMobileMenu = false"
          >
            📚 Lesson Updates
          </router-link>

          <router-link
              to="/parent/link-child"
              class="block px-3 py-2 rounded-lg text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50"
              :class="{ 'text-blue-600 bg-blue-50': $route.path === '/parent/link-child' }"
              @click="showMobileMenu = false"
          >
            🔗 Link Child
          </router-link>

          <!-- Mobile Progress Section -->
          <div v-if="hasLinkedChildren" class="space-y-1">
            <div class="px-3 py-2 text-xs font-medium text-gray-400 uppercase tracking-wide">
              Progress & Analytics
            </div>
            <div v-for="child in linkedChildren" :key="child.child_id" class="ml-4 space-y-1">
              <div class="px-3 py-1 text-xs font-medium text-gray-600">
                {{ child.first_name }} {{ child.last_name }}
              </div>
              <router-link
                  :to="`/parent/child-progress/${child.child_id}`"
                  class="block px-3 py-2 rounded-lg text-sm text-gray-700 hover:text-blue-600 hover:bg-blue-50"
                  @click="showMobileMenu = false"
              >
                📊 Progress Details
              </router-link>
              <router-link
                  :to="`/parent/achievements/${child.child_id}`"
                  class="block px-3 py-2 rounded-lg text-sm text-gray-700 hover:text-blue-600 hover:bg-blue-50"
                  @click="showMobileMenu = false"
              >
                🏆 Achievements
              </router-link>
            </div>
          </div>
        </div>

        <!-- Mobile User Section -->
        <div class="border-t border-gray-200 pt-4 pb-3">
          <div class="flex items-center px-5">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
              <span class="text-white font-bold">{{ userInitials }}</span>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">Parent Account</div>
              <div class="text-sm text-gray-500">{{ userEmail }}</div>
            </div>
          </div>

          <div class="mt-3 space-y-1 px-2">
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
        v-if="showUserMenu || showProgressMenu"
        class="fixed inset-0 z-40"
        @click="closeAllDropdowns"
    ></div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from '@/plugins/axios.ts'
import {
  ChevronDownIcon,
  MenuIcon,
  XIcon,
  LogOutIcon
} from 'lucide-vue-next'

const router = useRouter()

// Reactive state
const showMobileMenu = ref(false)
const showUserMenu = ref(false)
const showProgressMenu = ref(false)
const userEmail = ref('')
const linkedChildren = ref([])

// Computed
const hasLinkedChildren = computed(() => {
  return linkedChildren.value.length > 0
})

const userInitials = computed(() => {
  if (!userEmail.value) return 'P'
  const names = userEmail.value.split('@')[0].split('.')
  return names.map(name => name.charAt(0)).join('').toUpperCase().slice(0, 2)
})

// Methods
const closeAllDropdowns = () => {
  showUserMenu.value = false
  showProgressMenu.value = false
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/parent/login')
  closeAllDropdowns()
  showMobileMenu.value = false
}

const fetchLinkedChildren = async () => {
  try {
    const response = await axios.get('/api/parent/linked-children')
    linkedChildren.value = response.data.linked_children || []
  } catch (error) {
    console.error('Error fetching linked children:', error)
    linkedChildren.value = []
  }
}

// Close dropdowns when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    closeAllDropdowns()
  }
}

// Lifecycle
onMounted(() => {
  userEmail.value = localStorage.getItem('user_email') || 'parent@example.com'
  fetchLinkedChildren()
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
</style>
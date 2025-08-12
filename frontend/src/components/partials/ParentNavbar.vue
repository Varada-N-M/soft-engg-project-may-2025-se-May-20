<template>
  <div>
    <!-- Desktop Sidebar -->
    <div class="w-64 bg-white shadow-lg hidden lg:block fixed h-full">
      <div class="p-6">
        <!-- Logo -->
        <div class="flex items-center gap-3 mb-8">
          <div class="bg-blue-500 p-2 rounded-2xl">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
            </svg>
          </div>
          <div>
            <h2 class="text-lg font-bold text-gray-800">Parent Portal</h2>
            <p class="text-xs text-gray-500">CoolKids Learning</p>
          </div>
        </div>

        <!-- Navigation -->
        <nav class="space-y-2">
          <router-link 
            to="/parent/home"
            :class="isActive('/parent/home') ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h2a2 2 0 012 2v2H8V5z"></path>
            </svg>
            Dashboard
          </router-link>

          <router-link 
            to="/parent/children"
            :class="isActive('/parent/children') ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            My Children
          </router-link>

          <router-link 
            to="/parent/lesson-updates"
            :class="isActive('/parent/lesson-updates') ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
            </svg>
            Lesson Updates
          </router-link>

          <router-link 
            to="/parent/link-child"
            :class="isActive('/parent/link-child') ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
            </svg>
            Link Child
          </router-link>

          <div class="border-t border-gray-200 my-4"></div>

          <!-- User Profile Section -->
          <div class="pt-4">
            <div class="flex items-center gap-3 px-4 py-3 rounded-[15px] bg-gray-50">
              <div class="bg-gray-300 w-8 h-8 rounded-full flex items-center justify-center">
                <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-800 truncate">Parent Account</p>
                <p class="text-xs text-gray-500">{{ userEmail }}</p>
              </div>
            </div>
          </div>

          <!-- Logout Button -->
          <button 
            @click="logout"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            Logout
          </button>
        </nav>
      </div>
    </div>

    <!-- Mobile Sidebar Overlay -->
    <div v-if="sidebarOpen" class="fixed inset-0 bg-black bg-opacity-50 z-50 lg:hidden" @click="sidebarOpen = false">
      <div class="w-64 bg-white h-full shadow-xl" @click.stop>
        <div class="p-6">
          <div class="flex items-center justify-between mb-8">
            <div class="flex items-center gap-3">
              <div class="bg-blue-500 p-2 rounded-2xl">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-lg font-bold text-gray-800">Parent Portal</h2>
                <p class="text-xs text-gray-500">CoolKids Learning</p>
              </div>
            </div>
            <button @click="sidebarOpen = false" class="p-2 hover:bg-gray-100 rounded-[15px]">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <nav class="space-y-2">
            <router-link 
              to="/parent/home"
              @click="sidebarOpen = false"
              :class="isActive('/parent/home') ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'"
              class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h2a2 2 0 012 2v2H8V5z"></path>
              </svg>
              Dashboard
            </router-link>

            <router-link 
              to="/parent/children"
              @click="sidebarOpen = false"
              :class="isActive('/parent/children') ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'"
              class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
              My Children
            </router-link>

            <router-link 
              to="/parent/link-child"
              @click="sidebarOpen = false"
              :class="isActive('/parent/link-child') ? 'bg-blue-500 text-white' : 'text-gray-600 hover:bg-gray-100'"
              class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
              </svg>
              Link Child
            </router-link>

            <div class="border-t border-gray-200 my-4"></div>

            <!-- User Profile Section -->
            <div class="pt-4">
              <div class="flex items-center gap-3 px-4 py-3 rounded-[15px] bg-gray-50">
                <div class="bg-gray-300 w-8 h-8 rounded-full flex items-center justify-center">
                  <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-800 truncate">Parent Account</p>
                  <p class="text-xs text-gray-500">{{ userEmail }}</p>
                </div>
              </div>
            </div>

            <!-- Logout Button -->
            <button 
              @click="logout"
              class="w-full flex items-center gap-3 px-4 py-3 rounded-[15px] text-left text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
              </svg>
              Logout
            </button>
          </nav>
        </div>
      </div>
    </div>

    <!-- Mobile Header -->
    <div class="lg:hidden bg-white shadow-sm p-4 flex items-center justify-between fixed top-0 left-0 right-0 z-40">
      <button @click="sidebarOpen = true" class="p-2">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
        </svg>
      </button>
      <h1 class="text-lg font-semibold">{{ pageTitle }}</h1>
      <div class="w-10"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Props
defineProps<{
  pageTitle?: string
}>()

// State
const sidebarOpen = ref(false)
const userEmail = ref('')

// Computed
const isActive = (path: string) => {
  return route.path === path
}

// Methods
const logout = () => {
  localStorage.clear()
  router.push('/parent/login')
}

// Lifecycle
onMounted(() => {
  userEmail.value = localStorage.getItem('user_email') || 'parent@example.com'
})
</script>

<style scoped>
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style>
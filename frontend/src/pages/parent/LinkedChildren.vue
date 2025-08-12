<template>
  <div class="min-h-screen bg-gray-100 flex page-font">
    <!-- Parent Navbar -->
    <ParentNavbar page-title="My Children"/>

    <!-- Main Content -->
    <div class="flex-1 lg:ml-64">
      <!-- Mobile Header Spacing -->
      <div class="h-16 lg:h-0"></div>

      <div class="p-6">
        <div class="max-w-6xl mx-auto">
          <!-- Header -->
          <div class="bg-white rounded-[20px] p-6 mb-6 shadow">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">My Children</h1>
            <p class="text-gray-600">Monitor your children's learning progress and achievements.</p>
          </div>

          <!-- Loading State -->
          <div v-if="isLoading" class="bg-white rounded-[20px] p-8 shadow text-center">
            <div class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-8 w-8 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span class="text-lg text-gray-600">Loading children...</span>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="bg-white rounded-[20px] p-8 shadow">
            <div class="text-center">
              <svg class="mx-auto h-12 w-12 text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L5.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
              </svg>
              <h3 class="text-lg font-semibold text-gray-800 mb-2">Error Loading Children</h3>
              <p class="text-gray-600 mb-4">{{ error }}</p>
              <button
                  @click="fetchLinkedChildren"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Try Again
              </button>
            </div>
          </div>

          <!-- No Children State -->
          <div v-else-if="linkedChildren.length === 0" class="bg-white rounded-[20px] p-8 shadow text-center">
            <svg class="mx-auto h-16 w-16 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            <h3 class="text-xl font-semibold text-gray-800 mb-2">No Children Linked</h3>
            <p class="text-gray-600 mb-6">You haven't linked any children to your account yet.</p>
            <router-link
                to="/parent/link-child"
                class="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              Link Your First Child
            </router-link>
          </div>

          <!-- Children List -->
          <div v-else class="space-y-6">
            <div
                v-for="child in linkedChildren"
                :key="child.child_id"
                class="bg-white rounded-[20px] p-6 shadow hover:shadow-md transition-shadow"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-4">
                  <!-- Avatar -->
                  <div
                      class="w-16 h-16 bg-violet-300 rounded-full flex items-center justify-center text-white text-xl font-bold">
                    {{ getInitials(child.first_name, child.last_name) }}
                  </div>

                  <!-- Child Info -->
                  <div>
                    <h3 class="text-xl font-bold text-gray-800">
                      {{ child.first_name }} {{ child.last_name }}
                    </h3>
                    <p class="text-gray-600">{{ child.email }}</p>
                    <div class="flex items-center space-x-4 mt-1">
                      <span v-if="child.class" class="text-sm text-gray-500">
                        <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                        </svg>
                        Class {{ child.class }}
                      </span>
                      <span v-if="child.school_name" class="text-sm text-gray-500">
                        <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-4m-5 0H9m0 0H5m0 0H3m2 0v-4a2 2 0 012-2v0a2 2 0 012 2v4"></path>
                        </svg>
                        {{ child.school_name }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Stats -->
                <div class="text-right">
                  <div class="flex items-center space-x-6 mb-2">
                    <!-- XP Points -->
                    <div class="text-center">
                      <div class="text-2xl font-bold text-yellow-600">{{ child.xp_points || 0 }}</div>
                      <div class="text-xs text-gray-500">XP Points</div>
                    </div>

                    <!-- Streak -->
                    <div class="text-center">
                      <div class="text-2xl font-bold text-orange-600">{{ child.streak || 0 }}</div>
                      <div class="text-xs text-gray-500">Day Streak</div>
                    </div>
                  </div>

                  <div class="text-xs text-gray-400">
                    Linked: {{ formatDate(child.linked_at) }}
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="mt-4 pt-4 border-t border-gray-100">
                <div class="flex justify-between items-center">
                  <div class="flex space-x-3">
                    <button
                        class="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm font-medium">
                      View Progress
                    </button>
                    <button
                        class="px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm font-medium">
                      View Achievements
                    </button>
                  </div>

                  <button
                      @click="unlinkChild(child)"
                      class="px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm font-medium"
                  >
                    Unlink
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Add Another Child Button -->
          <div v-if="linkedChildren.length > 0" class="mt-8 text-center">
            <router-link
                to="/parent/link-child"
            >
              <Button>
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                </svg>
                Link Another Child
              </Button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import ParentNavbar from "@/components/partials/ParentNavbar.vue";
import api from '@/plugins/axios.ts';
import {Button} from "@/components/ui/button/index.js";

const linkedChildren = ref([]);
const isLoading = ref(false);
const error = ref(null);

const fetchLinkedChildren = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await api.get('/api/parent/linked-children');
    linkedChildren.value = response.data.linked_children || [];
  } catch (err) {
    console.error('Error fetching linked children:', err);

    if (err.response?.status === 404) {
      linkedChildren.value = [];
    } else if (err.response?.data?.message) {
      error.value = err.response.data.message;
    } else if (err.request) {
      error.value = 'Network error. Please check your connection and try again.';
    } else {
      error.value = 'An unexpected error occurred. Please try again.';
    }
  } finally {
    isLoading.value = false;
  }
};

const unlinkChild = async (child) => {
  if (!confirm(`Are you sure you want to unlink ${child.first_name} ${child.last_name}?`)) {
    return;
  }

  try {
    await api.put(`/api/parent/unlink-child/${child.child_id}`);

    // Remove child from local list
    linkedChildren.value = linkedChildren.value.filter(c => c.child_id !== child.child_id);

    // Show success message (you could add a toast notification here)
    alert(`${child.first_name} ${child.last_name} has been unlinked successfully.`);
  } catch (err) {
    console.error('Error unlinking child:', err);
    const errorMessage = err.response?.data?.message || 'Failed to unlink child. Please try again.';
    alert(errorMessage);
  }
};

const getInitials = (firstName, lastName) => {
  const first = firstName ? firstName.charAt(0).toUpperCase() : '';
  const last = lastName ? lastName.charAt(0).toUpperCase() : '';
  return first + last;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

onMounted(() => {
  fetchLinkedChildren();
});
</script>

<style scoped>
/* Additional styles if needed */
</style>
<template>
  <div class="min-h-screen bg-gray-100 flex page-font">
    <!-- Parent Navbar -->
    <ParentNavbar page-title="Link Child" />
    
    <!-- Main Content -->
    <div class="flex-1 lg:ml-64">
      <!-- Mobile Header Spacing -->
      <div class="h-16 lg:h-0"></div>
      
      <div class="p-6">
        <div class="max-w-2xl mx-auto">
          <!-- Header -->
          <div class="bg-white rounded-[20px] p-6 mb-6 shadow">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Link Your Child</h1>
            <p class="text-gray-600">Enter the unique key to connect with your child's account and monitor their learning progress.</p>
          </div>

          <!-- Form Card -->
          <div class="bg-white rounded-[20px] p-8 shadow">
            <form @submit.prevent="linkChild" class="space-y-6">
              <div>
                <label for="child-key" class="block text-sm font-medium text-gray-700 mb-2">
                  Child's Unique Key
                </label>
                <div class="relative">
                  <input
                    id="child-key"
                    v-model="childKey"
                    type="text"
                    required
                    class="w-full px-4 py-3 text-lg text-gray-700 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-all"
                    placeholder="e.g., 1A3-X3Z"
                  />
                  <div class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.623 5.913M15 7a2 2 0 00-2-2M4.377 16.913A6 6 0 0112 4.087M15 7a2 2 0 00-2 2m0 0A2 2 0 0111 7m-6 10a2 2 0 012-2m-2 2a2 2 0 00-2 2m2-2a2 2 0 012 2m-2-2a2 2 0 002-2m-2 2a2 2 0 012-2m-2 2a2 2 0 002-2" />
                    </svg>
                  </div>
                </div>
                <p class="text-sm text-gray-500 mt-2">
                  Ask your child for their unique account key. This key was provided when they created their account.
                </p>
              </div>

              <div>
                <button
                  type="submit"
                  :disabled="isLinking"
                  class="w-full px-4 py-3 font-bold text-white bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transform hover:scale-105 transition-all duration-200 shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                >
                  <span v-if="!isLinking" class="text-lg">Link Child Account</span>
                  <span v-else class="flex items-center justify-center text-lg">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Linking...
                  </span>
                </button>
              </div>
            </form>

            <!-- Response Message -->
            <div v-if="message" class="mt-6 p-4 rounded-lg border-2" :class="messageClasses">
              <div class="flex items-center">
                <svg v-if="message.success" class="h-5 w-5 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <svg v-else class="h-5 w-5 mr-2 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.464 0L5.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <p :class="message.success ? 'text-green-800' : 'text-red-800'">{{ message.text }}</p>
              </div>
            </div>
          </div>

          <!-- Help Section -->
          <div class="bg-blue-50 border border-blue-200 rounded-[20px] p-6 mt-6">
            <h3 class="text-lg font-semibold text-blue-900 mb-3">Need Help?</h3>
            <div class="space-y-2 text-blue-800">
              <p class="flex items-start gap-2">
                <span class="font-semibold">1.</span>
                Ask your child to log into their CoolKids account
              </p>
              <p class="flex items-start gap-2">
                <span class="font-semibold">2.</span>
                They can find their unique key in their account settings or profile
              </p>
              <p class="flex items-start gap-2">
                <span class="font-semibold">3.</span>
                Enter the exact key here (case-sensitive)
              </p>
              <p class="flex items-start gap-2">
                <span class="font-semibold">4.</span>
                Once linked, you'll be able to monitor their learning progress
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import ParentNavbar from "@/components/partials/ParentNavbar.vue";
import api from '@/plugins/axios.ts';

const childKey = ref('');
const isLinking = ref(false);
const message = ref(null);

const messageClasses = computed(() => {
  if (!message.value) return '';
  return message.value.success
    ? 'border-green-200 bg-green-50'
    : 'border-red-200 bg-red-50';
});

const linkChild = async () => {
  if (!childKey.value.trim()) {
    message.value = {
      success: false,
      text: 'Please enter your child\'s unique key.'
    };
    return;
  }

  isLinking.value = true;
  message.value = null;

  try {
    const response = await api.post('/api/parent/link-child', {
      child_key: childKey.value.trim()
    });

    message.value = {
      success: true,
      text: response.data.message || 'Child account linked successfully! You can now monitor their learning progress.'
    };

    // Clear the form
    childKey.value = '';
    
  } catch (error) {
    console.error('Link child error:', error);
    
    let errorMessage = 'Failed to link child account. Please try again.';
    
    if (error.response) {
      if (error.response.status === 404) {
        errorMessage = 'Invalid child key. Please check the key and try again.';
      } else if (error.response.data && error.response.data.message) {
        errorMessage = error.response.data.message;
      }
    } else if (error.request) {
      errorMessage = 'Network error. Please check your connection and try again.';
    }

    message.value = {
      success: false,
      text: errorMessage
    };
  } finally {
    isLinking.value = false;
  }
};
</script>

<style scoped>

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
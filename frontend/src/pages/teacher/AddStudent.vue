<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300 flex items-center justify-center p-4">
    <FloatingDecorativeElements />
    <div class="w-full max-w-md p-8 space-y-6 bg-white/90 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20">
      <div class="text-center">
        <h2 class="text-3xl font-bold text-gray-800">Add Student</h2>
        <p class="mt-2 text-gray-600">Enter the student's email to add them to your class.</p>
      </div>

      <div v-if="message" :class="['p-4 rounded-xl text-center', messageClass]">
        {{ message }}
      </div>

      <form @submit.prevent="addStudent" class="space-y-6">
        <div>
          <label for="student-email" class="text-sm font-medium text-gray-700 sr-only">Student's Email</label>
          <div class="relative">
            <input
              id="student-email"
              v-model="studentEmail"
              type="email"
              required
              class="w-full px-4 py-3 text-lg text-gray-700 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-all"
              placeholder="student@example.com"
            />
            <div class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>
        <div>
          <button
            type="submit"
            class="w-full px-4 py-3 font-bold text-white bg-gradient-to-r from-green-500 to-blue-600 rounded-xl hover:from-green-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transform hover:scale-105 transition-all duration-200 shadow-lg"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Processing...
            </span>
            <span v-else class="text-lg">Add Student</span>
          </button>
        </div>
      </form>
      <div class="text-center mt-4">
        <router-link to="/teacher/lesson-updates" class="text-sm text-gray-600 hover:text-blue-500 transition-colors">Back to Lesson Updates</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FloatingDecorativeElements from "@/components/partials/FloatingDecorativeElements.vue";
import axios from 'axios';

const studentEmail = ref('');
const isLoading = ref(false);
const message = ref('');
const messageClass = ref('');

const addStudent = async () => {
  if (!studentEmail.value) {
    message.value = 'Please enter a student email';
    messageClass.value = 'bg-red-100 text-red-700';
    return;
  }

  isLoading.value = true;
  message.value = '';

  try {
    const token = localStorage.getItem('token');

    if (!token) {
      message.value = 'You must be logged in to add a student';
      messageClass.value = 'bg-red-100 text-red-700';
      isLoading.value = false;
      return;
    }

    const response = await axios.post(
      '/api/teacher/add-student',
      { student_email: studentEmail.value },
      {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );

    if (response.status === 201) {
      message.value = 'Student added successfully!';
      messageClass.value = 'bg-green-100 text-green-700';
      studentEmail.value = ''; // Clear the input
    }
  } catch (error) {
    console.error('Error adding student:', error);

    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      message.value = error.response.data.message || 'Failed to add student';
      messageClass.value = 'bg-red-100 text-red-700';
    } else if (error.request) {
      // The request was made but no response was received
      message.value = 'No response from server. Please try again.';
      messageClass.value = 'bg-red-100 text-red-700';
    } else {
      // Something happened in setting up the request that triggered an Error
      message.value = 'Error adding student. Please try again.';
      messageClass.value = 'bg-red-100 text-red-700';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>

<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <header class="max-w-4xl mx-auto mb-8 text-center">
      <router-link to="/student/home" class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">My Profile</h1>
    </header>

    <main class="max-w-4xl mx-auto bg-white rounded-3xl p-8 shadow-lg border border-gray-200">
      <div v-if="isLoading" class="text-center py-20">
        <p class="text-lg text-gray-600">Loading profile data...</p>
      </div>
      <div v-else-if="error" class="text-center py-20">
        <p class="text-lg text-red-500 font-medium">{{ error }}</p>
      </div>
      <div v-else class="space-y-6">
        <div class="flex items-center space-x-6 pb-6 border-b border-gray-100">
          <div class="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-5xl font-bold text-blue-600 shadow-inner">
            {{ getInitials(profile.first_name, profile.last_name) }}
          </div>
          <div>
            <h2 class="text-3xl font-bold text-gray-900">{{ profile.first_name }} {{ profile.last_name }}</h2>
            <p class="text-gray-600">{{ profile.email }}</p>
            <p class="text-sm text-gray-500">Member since: {{ formatDate(profile.created_at) }}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="bg-yellow-50 rounded-2xl p-5 flex items-center space-x-4 shadow-sm border border-yellow-200">
            <div class="text-4xl">✨</div>
            <div>
              <p class="text-sm text-yellow-700 font-medium">Total XP Points</p>
              <p class="text-3xl font-bold text-yellow-800">{{ profile.xp_points }}</p>
            </div>
          </div>
        </div>

        <div class="space-y-4">
          <h3 class="text-xl font-bold text-gray-800 border-b pb-2 mb-4">Personal Details</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">Date of Birth</p>
              <p class="font-medium text-gray-800">{{ profile.dob ? formatDate(profile.dob) : 'N/A' }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">Gender</p>
              <p class="font-medium text-gray-800">{{ profile.gender || 'N/A' }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">Class Level</p>
              <p class="font-medium text-gray-800">{{ profile.class_level || 'N/A' }}</p>
            </div>
            <div class="bg-gray-100 p-4 rounded-xl">
              <p class="text-sm text-gray-600">School Name</p>
              <p class="font-medium text-gray-800">{{ profile.school_name || 'N/A' }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// --- Reactive Data ---
const profile = ref(null);
const isLoading = ref(true);
const error = ref(null);

// --- Methods ---
const fetchUserProfile = async () => {
  isLoading.value = true;
  error.value = null;
  const token = localStorage.getItem('access_token');

  if (!token) {
    error.value = 'Authentication required. Please log in.';
    isLoading.value = false;
    return;
  }

  try {
    const response = await axios.get('/api/student/profile', {
      headers: { Authorization: `Bearer ${token}` },
    });
    profile.value = response.data.profile;
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load profile. Please try again.';
    console.error('API Error (fetchUserProfile):', err);
  } finally {
    isLoading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      return 'Invalid Date';
    }
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch (e) {
    console.error("Error formatting date:", dateString, e);
    return 'Invalid Date';
  }
};

const getInitials = (firstName, lastName) => {
  if (!firstName && !lastName) return 'P';
  const firstInitial = firstName ? firstName.charAt(0).toUpperCase() : '';
  const lastInitial = lastName ? lastName.charAt(0).toUpperCase() : '';
  return `${firstInitial}${lastInitial}`;
};

// --- Lifecycle Hook ---
onMounted(() => {
  fetchUserProfile();
});
</script>
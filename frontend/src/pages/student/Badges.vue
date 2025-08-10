<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <header class="max-w-4xl mx-auto mb-8 text-center">
      <router-link to="/student/home" class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">My Badge Collection 🏆</h1>
      <p class="text-lg text-gray-600 font-medium">
        You've earned <span class="text-yellow-500 font-bold">{{ earnedBadges.length }}</span> awesome badges so far! Keep up the great work!
      </p>
    </header>

    <main class="max-w-6xl mx-auto">
      <div v-if="earnedBadges.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <BadgeCard v-for="badge in earnedBadges" :key="badge.id" :badge="badge" />
      </div>
      <div v-else class="text-center py-20">
        <div class="text-6xl mb-4">😔</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">No Badges Earned Yet</h2>
        <p class="text-gray-600">Complete activities and challenges to start your collection!</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import BadgeCard from './BadgeCard.vue';

// --- Reactive Data ---
const allBadges = ref([
  // This is a simplified list. In a real app, you would fetch this from an API.
  {
    id: 1,
    name: 'Math Wizard',
    description: 'Master of numbers and calculations.',
    emoji: '🧮',
    earned: true,
    earnedDate: '2024-01-15',
    xpReward: 100
  },
  {
    id: 2,
    name: 'Bookworm',
    description: 'Loves reading and stories.',
    emoji: '📚',
    earned: true,
    earnedDate: '2024-01-10',
    xpReward: 80
  },
  {
    id: 3,
    name: 'Young Scientist',
    description: 'Curious about how the world works.',
    emoji: '🔬',
    earned: true,
    earnedDate: '2024-01-18',
    xpReward: 95
  },
  {
    id: 4,
    name: 'Perfect Week',
    description: 'Completed all activities for a week.',
    emoji: '🌟',
    earned: true,
    earnedDate: '2024-01-22',
    xpReward: 200
  },
  {
    id: 5,
    name: 'Team Player',
    description: 'Great at working with others.',
    emoji: '👥',
    earned: false,
    earnedDate: null,
    xpReward: 80
  },
  {
    id: 6,
    name: 'Streak Master',
    description: 'Consistent learner every day.',
    emoji: '🔥',
    earned: false,
    earnedDate: null,
    xpReward: 300
  }
]);

const earnedBadges = computed(() => allBadges.value.filter(badge => badge.earned));

</script>
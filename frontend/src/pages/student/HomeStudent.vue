<template>
  <div class="min-h-screen flex">
    <aside class="w-64  bg-opacity-90 backdrop-blur-sm p-6 fixed left-5 top-3 bottom-3 rounded-[20px] overflow-y-auto z-50 shadow-[0_0_10px_rgba(0,0,0,0.14)] flex flex-col">
      <div class="mb-8">
        <h2 class="text-3xl font-extrabold text-gray-900">My Dashboard</h2>
      </div>
      <nav class="space-y-3">
        <router-link
          v-for="link in navLinks"
          :key="link.name"
          :to="link.path"
          class="flex items-center gap-3 py-3 px-4 rounded-xl text-gray-700 hover:bg-yellow-100 hover:text-yellow-600 transition-colors duration-200 font-medium"
        >
          <span class="text-xl">{{ link.icon }}</span> {{ link.name }}
        </router-link>
      </nav>

      <router-link to="/student/profile"
        class="mt-30 flex items-center gap-3 py-3 px-4 rounded-xl bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors duration-200 font-medium justify-center"
      >
        Profile
      </router-link>
      <!-- Logout button at bottom -->
      <button
        @click="logout"
        class="mt-3 flex items-center gap-3 py-3 px-4 rounded-xl bg-red-100 text-red-700 hover:bg-red-200 transition-colors duration-200 font-medium justify-center"
      >
        Logout
      </button>
    </aside>

    <main class="flex-1 ml-64 p-8 overflow-y-auto bg-gray-50">
      <div class="max-w-7xl ml-3">
        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-4xl font-bold text-gray-900 mb-2" v-if="studentProfile">
                Hello, {{ studentProfile.first_name }}! 👋
              </h1>
              <h1 class="text-4xl font-bold text-gray-900 mb-2" v-else>
                Welcome Back.
              </h1>
              <p class="text-gray-600 text-lg">
                Your adventure awaits. Let's make today a great day!
              </p>
            </div>
          </div>
        </div>

        <!-- <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3">
              🎯 Today's Habits
            </h2>
            <router-link
              to="/student/habit"
              class="text-blue-600 hover:text-blue-800 font-semibold"
            >
              View All
            </router-link>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <ActivityCard
              v-for="habit in habits"
              :key="habit.habit_id"
              :activity="{
                id: habit.habit_id,
                emoji: '📌', // you can map categories to emojis if you want
                title: habit.name,
                description: habit.description,
                category: habit.category,
                xp: habit.habit_xp,
                completed: false // replace if you track completion
              }"
              @toggle="toggleHabit(habit.habit_id)"
            />
          </div>
        </div> -->


        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="bg-white rounded-3xl p-8 shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3 mb-6">
              💖 Daily Gratitude
            </h2>
            <div v-if="todaysGratitude" class="bg-pink-50 p-6 rounded-2xl">
              <p class="text-gray-800 italic text-lg leading-relaxed">
                "{{ todaysGratitude }}"
              </p>
              <div class="flex items-center gap-2 mt-4">
                <span class="text-green-500">✅</span>
                <span class="text-sm text-gray-600 font-medium">You completed this today!</span>
              </div>
            </div>
            <div v-else class="text-center py-6">
              <div class="text-5xl mb-4">💭</div>
              <p class="text-gray-700 text-lg mb-4">
                What's one thing you're thankful for today?
              </p>
              <router-link
                to="/student/journal"
                class="bg-pink-500 text-white font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-pink-600 transition-colors inline-block text-center"
              >
                Write Gratitude
              </router-link>
            </div>
          </div>

          <div class="bg-white rounded-3xl p-8 shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3 mb-6">
              🤖 Learn with AI
            </h2>
            <div class="p-6 rounded-2xl">
              <div class="flex items-center gap-3 mb-4">
                <div class="text-lg text-gray-700 font-medium">Meet Rohit!</div>
              </div>
              <p class="text-gray-800 mb-4 leading-relaxed">
                "Hi! I'm here to talk, teach and help you improve your Communication Skills!"
              </p>
              <router-link
                to="/student/ai-companion"
                class="bg-blue-500 text-white font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-blue-600 transition-colors inline-block text-center"
              >
                Chat Now
              </router-link>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3 mb-6">
            🛠️ Weekly Skills Challenge
          </h2>
          <div class="bg-gradient-to-r from-teal-50 to-cyan-50 p-6 rounded-2xl border border-teal-200">
            <div class="flex items-start gap-5">
              <div class="text-5xl">{{ currentLifeSkill.emoji }}</div>
              <div class="flex-1">
                <h5 class="font-bold text-gray-900 text-lg mb-2">{{ currentLifeSkill.title }}</h5>
                <p class="text-gray-700 mb-4">{{ currentLifeSkill.description }}</p>
                <div class="flex items-center gap-4">
                  <a href="https://www.youtube.com/watch?v=byZlWHEZWSM">
                  <button class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-xl shadow hover:bg-blue-700 transition-colors duration-200 text-sm font-medium cursor-pointer">
                    Watch Lesson
                  </button>
                  </a>
                  <button
                  @click="markSkillAsComplete(currentLifeSkill.id)"
                  :class="{ 'bg-green-600 hover:bg-green-700': !isComplete, 'bg-green-500': isComplete }"
                  class="inline-flex items-center justify-center px-4 py-2 text-white rounded-xl shadow transition-colors duration-200 text-sm font-medium"
                  :disabled="isComplete">
                  <span v-if="!isComplete">Mark as Complete</span>
                  <span v-else>Lesson Completed!</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3">
              📖 Life Lessons
            </h2>
            <router-link to="/student/life-lessons" class="text-blue-600 hover:text-blue-800 font-semibold">View All</router-link>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <LearningStoryCard
              v-for="story in learningStories.slice(0, 2)"
              :key="story.id"
              :story="story"
            />
          </div>
        </div>

        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3">
              📚 Recent Lessons
            </h2>
            <router-link to="/student/lesson-updates" class="text-blue-600 hover:text-blue-800 font-semibold">View All</router-link>
          </div>

          <div v-if="isLoading" class="space-y-4">
            <div v-for="i in 3" :key="i" class="animate-pulse flex items-center gap-4 p-4 bg-gray-100 rounded-2xl">
              <div class="bg-gray-200 rounded-lg p-3 h-12 w-12"></div>
              <div class="flex-1">
                <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div class="h-3 bg-gray-200 rounded w-1/2 mb-2"></div>
              </div>
            </div>
          </div>

          <div v-else-if="lessonUpdates.length > 0" class="space-y-4">
            <LessonUpdateCard
              v-for="lesson in lessonUpdates.slice(0, 4)"
              :key="lesson.lesson_id"
              :lesson="lesson"
            />
          </div>

          <div v-else class="text-center py-10">
            <div class="text-5xl mb-4">📚</div>
            <h3 class="text-xl font-medium text-gray-800">No lessons to show yet!</h3>
            <p class="text-gray-500 mt-2">Check back later for updates from your teacher.</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { defineProps,ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { clearAuthData } from '@/utils/auth';

// Import smaller, reusable components (assuming they are created)
import StatCard from './StatCard.vue';
import ActivityCard from './ActivityCard.vue';
import LearningStoryCard from './LearningStoryCard.vue';
import LessonUpdateCard from './LessonUpdateCard.vue';

// Router instance
const router = useRouter();

const habits = ref([])
const studentProfile = ref(null);
const isLoading = ref(true);
const xpPoints = ref(0);
const error = ref(null);

const isComplete = ref(false);

// Logout function
const logout = () => {
  clearAuthData();
  router.push('/');
};

const navLinks = ref([
  { name: 'Home', path: '/student/home', icon: '🏠' },
  { name: 'Habits', path: '/student/habit', icon: '🎯' },
  { name: 'Badges', path: '/student/badges', icon: '🏅' },
  { name: 'Life Lessons', path: '/student/life-lessons', icon: '📖' },
  { name: 'Journal', path: '/student/journal', icon: '✍️' },
  { name: 'To-do List', path: '/student/todolist', icon: '✔️' },
  // { name: 'Activities', path: '/student/daily-activities', icon: '📅' },
  // { name: 'Weekly Challenge', path: '/student/life-skills', icon: '🛠️' },
  { name: 'AI Companion', path: '/student/ai-companion', icon: '🤖' },
  // { name: 'Lesson Updates', path: '/student/lesson-updates', icon: '📚' },
  // { name: 'Weekly Report', path: '/student/weekly-report', icon: '📊' },
]);

const categoryToEmojiMap = {
  reading: '📚',
  health: '💧',
  chores: '🧹',
  sports: '🏃',
  creative: '🎨',
  other: '🎯',
};

const markAsComplete = () => {
  isComplete.value = true;
};

const getEmojiForCategory = (category) => {
  return categoryToEmojiMap[category] || '🎯';
};

const fetchHabits = async () => {
  const token = localStorage.getItem('access_token');
  try {
    const response = await axios.get('/api/child/habits', {
      headers: { Authorization: `Bearer ${token}` },
    });

    habits.value = response.data.habits_created || [];

    const today = new Date().toISOString().split('T')[0];
    habits.value = response.data.habits_created.map(habit => {
      const isCompletedToday = response.data.completed_habits.some(
        c => c.habit_id === habit.habit_id && c.completion_date && c.completion_date.startsWith(today)
      );

      return {
        id: habit.habit_id,
        emoji: getEmojiForCategory(habit.category),
        title: habit.name,
        description: habit.description,
        category: habit.category,
        xp: habit.habit_xp,
        completed: isCompletedToday,
      };
    });
  } catch (err) {
    console.error('Failed to fetch habits:', err);
    // You could show an error message to the user here
  } finally {
    isLoading.value = false;
  }
};

const toggleHabit = async (habitId) => {
  const token = localStorage.getItem('access_token');
  const habitToToggle = habits.value.find(h => h.id === habitId);

  // Prevent multiple clicks and mark as done
  if (habitToToggle && !habitToToggle.completed) {
    try {
      // The backend POST endpoint marks it as complete
      await axios.post(`/api/child/habit/${habitId}/complete`, null, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Update the UI after successful API call
      habitToToggle.completed = true;
      alert(`🎉 You earned +${habitToToggle.xp} XP!`);

    } catch (err) {
      console.error('Failed to complete habit:', err);
      if (err.response && err.response.status === 400) {
        alert('This habit is already completed for today!');
      } else {
        alert('An error occurred. Please try again.');
      }
    }
  }
};

const fetchUserProfile = async () => {
  const token = localStorage.getItem('access_token');
  try {
    // Assuming you have an endpoint like '/api/child/profile'
    const response = await axios.get('/api/child/profile', {
      headers: { Authorization: `Bearer ${token}` },
    });

    xpPoints.value = response.data.xp_points;
  } catch (err) {
    error.value = 'Failed to fetch user profile data.';
    console.error('Failed to fetch user profile:', err);
  }
};

const markSkillAsComplete = async (skillId) => { // Removed ': number' from here
  try {
    await axios.post(`/api/child/skills/${skillId}/complete`); 
    isComplete.value = true
    console.log(`Weekly skill with ID ${skillId} marked as complete`)
  } catch (err) {
    console.error('Error marking skill as complete:', err)
  }
}

const todaysGratitude = ref('');

const currentLifeSkill = ref({
  id: 1,
  title: 'Making a Simple Sandwich',
  description: 'Learn to prepare your own healthy lunch! This week we\'ll practice making sandwich safely.',
  emoji: '🥪'
});

const learningStories = ref([
  { id: 1, title: 'Manage & Save Money', description: 'Learn how to manage & save money',  link:"https://youtu.be/hYbRu_MXI80?feature=shared" },
  { id: 2, title: 'Manage stress & emotions', description: 'Learn how to manage stress & emotions', link: "https://youtu.be/Vs-MyQgfH3A?feature=shared" },
]);

// Dynamic data fetched from API
const lessonUpdates = ref([]);
const badgeCount = ref(0);
const isBadgeCountLoading = ref(true);
const completedSkillsCount = ref(0);
const isCompletedSkillsLoading = ref(true);

const toggleActivity = (activityId) => {
  const activity = todaysActivities.value.find((a) => a.id === activityId);
  if (activity && !activity.completed) {
    activity.completed = true;
  }
};

const fetchData = async (url, loadingRef, dataRef, transform = (d) => d, key = '') => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  loadingRef.value = true;
  try {
    const response = await axios.get(url, { headers: { Authorization: `Bearer ${token}` } });
    dataRef.value = transform(response.data[key] || response.data) || [];
  } catch (err) {
    console.error(`Error fetching data from ${url}:`, err);
  } finally {
    loadingRef.value = false;
  }
};

onMounted(async () => {
  await fetchData('/api/child/profile', isLoading, studentProfile, null, 'profile');

  await Promise.all([
    fetchData('/api/child/lesson-updates', isLoading, lessonUpdates, null, 'lesson_updates'),
    fetchData('/api/child/badge/count', isBadgeCountLoading, badgeCount, (data) => data.badge_count),
    fetchData('/api/child/skills/completed/count', isCompletedSkillsLoading, completedSkillsCount, (data) => data.completed_skills_count),
    fetchHabits(),
    fetchUserProfile()
  ]);
});

</script>
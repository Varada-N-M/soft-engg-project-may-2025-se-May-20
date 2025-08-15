<template>
  <div class="min-h-screen flex font-playfair">
    <aside
      class="w-64 bg-opacity-90 backdrop-blur-sm p-6 fixed left-5 top-3 bottom-3 rounded-[20px] overflow-y-auto z-50 shadow-[0_0_10px_rgba(0,0,0,0.14)] flex flex-col">
      <div class="mb-8">
        <h2 class="text-3xl font-extrabold text-gray-900 font-playfair">My Dashboard</h2>
      </div>
      <nav class="space-y-3">
        <router-link v-for="link in navLinks" :key="link.name" :to="link.path"
          class="flex items-center gap-4 py-2 px-2 rounded-xl text-gray-700 hover:text-yellow-600 transition-colors duration-200 font-medium font-playfair">
          <span class="text-xl">{{ link.icon }}</span> {{ link.name }}
        </router-link>
      </nav>
    </aside>

    <main class="flex-1 ml-64 p-8 overflow-y-auto bg-gray-50">
      <div class="max-w-7xl ml-6">
        <div class="rounded-3xl mb-8">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2">My Habits</h1>
              <p class="text-lg text-gray-600 font-medium">
                You are tracking <span class="text-blue-500 font-bold">{{ habits.length }}</span> habits.
              </p>
            </div>
          </div>
        </div>

        <div class="flex justify-center mb-8">
          <button @click="openCreateModal"
            class="bg-blue-500 text-white px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center font-playfair">
            Create New Habit
          </button>
        </div>

        <div v-if="isLoading" class="text-center py-20">
          <p class="text-lg text-gray-600">Loading habits...</p>
        </div>
        <div v-else-if="error" class="text-center py-20">
          <p class="text-lg text-red-500 font-medium">{{ error }}</p>
        </div>
        <div v-else-if="habits.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="habit in habits" :key="habit.id" @click="openEditModal(habit)"
            class="bg-white rounded-3xl p-6 shadow-lg border-1 transition-transform hover:scale-101 cursor-pointer">
            <div class="flex items-center mb-4">
              <div class="text-3xl mr-3">{{ getEmojiForCategory(habit.category) }}</div>
              <div>
                <h3 class="font-bold text-gray-800 text-lg">{{ habit.name }}</h3>
                <p class="text-sm text-gray-600">{{ habit.description }}</p>
              </div>
            </div>

            <div class="flex justify-between items-center text-xs">
              <div class="inline-flex items-center bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full font-semibold">
                +{{ habit.habit_xp }} XP
              </div>
              <div v-if="habit.completedToday" class="text-lg text-green-600 font-bold">
                Done Today!
              </div>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-20">
          <p class="text-gray-600">Click the button above to create your first habit!</p>
        </div>
      </div>
    </main>

    <div v-if="showModal" class="fixed inset-0 flex bg-black/30 items-center justify-center z-50 p-4 shadow-2xl">
      <div class="bg-white rounded-3xl p-6 w-full max-w-md shadow-2xl">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-gray-800">
            {{ editingHabit ? 'Edit Habit' : 'Create New Habit' }}
          </h3>
          <button @click="closeModal" class="p-2 rounded-full hover:bg-gray-100 transition-colors">
            <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveHabit" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Habit Name</label>
            <input v-model="habitForm.name" type="text"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Read for 15 minutes" required>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea v-model="habitForm.description"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., This helps me learn new things." rows="3"></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
            <select v-model="habitForm.category"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option value="reading">📚 Reading</option>
              <option value="health">💧 Health</option>
              <option value="chores">🧹 Chores</option>
              <option value="sports">🏃 Sports</option>
              <option value="creative">🎨 Creative</option>
              <option value="other">🎯 Other</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">XP Reward</label>
            <select v-model="habitForm.habit_xp"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
              <option :value="10">10 XP - Easy</option>
              <option :value="25">25 XP - Medium</option>
              <option :value="50">50 XP - Hard</option>
            </select>
          </div>

          <div class="flex space-x-3 pt-4">
            <button v-if="editingHabit && !editingHabit.completedToday" type="button" @click="completeHabit(editingHabit.id)"
              class="flex-1 py-3 px-4 rounded-xl bg-green-500 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer">
              Mark as Done
            </button>
            <button v-if="editingHabit" type="button" @click="deleteHabit"
              class="flex-1 py-3 px-4 rounded-xl border border-red-300 text-red-600 bg-red-500 text-white font-medium hover:bg-red-600 transition-colors cursor-pointer">
              Delete
            </button>
            <button type="button" @click="closeModal"
              class="flex-1 py-3 px-4 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors cursor-pointer">
              Cancel
            </button>
            <button type="submit"
              class="flex-1 py-3 px-4 rounded-xl bg-blue-500 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer">
              {{ editingHabit ? 'Update Habit' : 'Create Habit' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/plugins/axios.ts';
import { clearAuthData } from '@/utils/auth';

const router = useRouter();

// --- Reactive Data ---
const showModal = ref(false);
const editingHabit = ref(null);
const habits = ref([]);
const isLoading = ref(true);
const error = ref(null);

const navLinks = ref([
  { name: 'Home', path: '/student/home', icon: '🏠' },
  { name: 'Lesson Updates', path: '/student/lesson-updates', icon: '📚' },
  { name: 'To-do List', path: '/student/todolist', icon: '✔️' },
  { name: 'Habits', path: '/student/habit', icon: '🎯' },
  { name: 'Life Lessons', path: '/student/life-lessons', icon: '📖' },
  { name: 'Journal', path: '/student/journal', icon: '✍️' },
  { name: 'AI Companion', path: '/student/ai-companion', icon: '🤖' },
  { name: 'Badges', path: '/student/badges', icon: '🏅' },
]);

const logout = () => {
  clearAuthData();
  router.push('/');
};

const habitForm = ref({
  id: null,
  name: '',
  description: '',
  category: 'other',
  habit_xp: 25,
});

const categoryToEmojiMap = {
  reading: '📚',
  health: '💧',
  chores: '🧹',
  sports: '🏃',
  creative: '🎨',
  other: '🎯',
};

const getEmojiForCategory = (category) => {
  return categoryToEmojiMap[category] || '🎯';
};

// --- Methods for API Calls ---
const fetchHabits = async () => {
  isLoading.value = true;
  error.value = null;
  const token = localStorage.getItem('access_token');

  try {
    const response = await api.get('/api/child/habit', {
      headers: { Authorization: `Bearer ${token}` }
    });

    const today = new Date().toISOString().split('T')[0];

    if (!response.data.habits_created) {
      habits.value = [];
      return;
    }

    habits.value = response.data.habits_created.map(habit => {
      const isCompletedToday = response.data.completed_habits?.some(
        c => c.habit_id === habit.habit_id && c.completion_date?.startsWith(today)
      );
      return {
        ...habit,
        id: habit.habit_id,
        completedToday: isCompletedToday,
      };
    });
  } catch (err) {
    console.error('API Error:', err);
    error.value = 'Could not load your habits. Please try again.';
  } finally {
    isLoading.value = false;
  }
};


const completeHabit = async (habitId) => {
  const token = localStorage.getItem('access_token');
  try {
    await api.post(`/api/child/habit/${habitId}/complete`, null, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Find the habit in the local list and mark it as completed for today
    const habitToUpdate = habits.value.find(h => h.id === habitId);
    if (habitToUpdate) {
      habitToUpdate.completedToday = true;
    }
    closeModal();
    alert(`🎉 Habit completed! You earned +${habitToUpdate.habit_xp} XP!`);
  } catch (err) {
    console.error('Failed to complete habit:', err);
    if (err.response && err.response.status === 400) {
      alert('This habit has already been completed today!');
    } else {
      alert('An error occurred. Please try again.');
    }
  }
};

const createHabit = async () => {
  const token = localStorage.getItem('access_token');
  try {
    const response = await api.post('/api/child/habit', {
      habit_name: habitForm.value.name,
      habit_description: habitForm.value.description,
      habit_category: habitForm.value.category,
      habit_xp: habitForm.value.habit_xp
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const newHabit = {
      id: response.data.habit_id,
      name: habitForm.value.name,
      description: habitForm.value.description,
      category: habitForm.value.category,
      habit_xp: habitForm.value.habit_xp,
      completedToday: false,
    };
    habits.value.push(newHabit);
    closeModal();
  } catch (err) {
    error.value = 'Failed to create habit.';
    console.error('API Error:', err);
  }
};

const updateHabit = async () => {
  const token = localStorage.getItem('access_token');
  try {
    await api.put(`/api/child/habit/${editingHabit.value.id}`, {
      habit_name: habitForm.value.name,
      habit_description: habitForm.value.description,
      habit_category: habitForm.value.category,
      habit_xp: habitForm.value.habit_xp
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const index = habits.value.findIndex(h => h.id === editingHabit.value.id);
    if (index !== -1) {
      habits.value[index] = { ...habits.value[index], ...habitForm.value };
    }
    closeModal();
  } catch (err) {
    error.value = 'Failed to update habit.';
    console.error('API Error:', err);
  }
};

const deleteHabit = async () => {
  const userConfirmed = confirm(`Are you sure you want to delete the habit "${editingHabit.value.name}"? This action cannot be undone.`);
  if (!userConfirmed) return;

  const token = localStorage.getItem('access_token');
  try {
    await api.delete(`/api/child/habit/${editingHabit.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    habits.value = habits.value.filter(h => h.id !== editingHabit.value.id);
    closeModal();
  } catch (err) {
    error.value = 'Failed to delete habit.';
    console.error('API Error:', err);
  }
};

const saveHabit = () => {
  if (editingHabit.value) {
    updateHabit();
  } else {
    createHabit();
  }
};

// --- Modal and Form Logic ---
const openCreateModal = () => {
  editingHabit.value = null;
  resetForm();
  showModal.value = true;
};

const openEditModal = (habit) => {
  editingHabit.value = habit;
  habitForm.value = { ...habit };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingHabit.value = null;
  resetForm();
};

const resetForm = () => {
  habitForm.value = {
    id: null,
    name: '',
    description: '',
    category: 'other',
    habit_xp: 25,
  };
};

// --- Lifecycle Hook ---
onMounted(() => {
  fetchHabits();
});
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.font-playfair {
  font-family: 'Playfair Display', serif;
}
</style>
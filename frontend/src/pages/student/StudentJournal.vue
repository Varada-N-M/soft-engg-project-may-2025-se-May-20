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
      <div class="max-w-7xl ml-3">
        <div class="rounded-3xl p-8 mb-8">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2">My Journal</h1>
              <p class="text-lg text-gray-600 font-medium">
                Reflect on your progress and capture your thoughts.
              </p>
            </div>
          </div>
        </div>

        <!-- Show "New Entry" button only if logged in -->
        <div v-if="isLoggedIn" class="flex justify-center mb-8">
          <button @click="openCreateModal"
            class="bg-blue-500 text-white px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-102 transition-all duration-200 flex items-center">
            New Journal Entry
          </button>
        </div>

        <!-- Loading, Error, or Content -->
        <div v-if="isLoading" class="text-center py-20">
          <p class="text-lg text-gray-600">Loading journal entries...</p>
        </div>

        <div v-else-if="error" class="text-center py-20">
          <p class="text-lg text-red-500 font-medium">{{ error }}</p>
        </div>

        <!-- Show entries if logged in and has data -->
        <div v-else-if="!isLoggedIn" class="text-center py-20">
          <div class="text-6xl mb-4">🔒</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">You Need to Log In</h2>
          <p class="text-gray-600 mb-4">Please log in to access your learning journal and start writing entries.</p>
          <router-link to="/login"
            class="inline-block mt-2 px-6 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors">
            Go to Login
          </router-link>
        </div>

        <div v-else-if="journalEntries.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="entry in journalEntries" :key="entry.id" @click="openEditModal(entry)"
            class="bg-white rounded-3xl p-6 shadow-lg border border-gray-200 transform transition-transform hover:scale-101 cursor-pointer flex flex-col justify-between">
            <div>
              <p class="font-bold text-lg text-gray-600 mb-4 line-clamp-4">{{ entry.content }}</p>
              <h3 class="text-gray-800 text-sm mb-2">Date: {{ formatDate(entry.date) }}</h3>

            </div>
          </div>
        </div>

        <!-- Empty journal (logged in but no entries) -->
        <div v-else class="text-center py-20">
          <p class="text-gray-600">Start writing to capture your thoughts and ideas!</p>
        </div>
      </div>
    </main>

    <!-- Create/Edit Journal Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl p-6 w-full max-w-md shadow-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-gray-800">
            {{ editingEntry ? 'Edit Entry' : 'New Journal Entry' }}
          </h3>
          <button @click="closeModal" class="p-2 rounded-full hover:bg-gray-100 transition-colors">
            <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveEntry" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Your Journal Entry</label>
            <textarea v-model="journalForm.content"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="What are you grateful for today? What did you learn?" rows="8" required></textarea>
          </div>

          <div class="flex space-x-3 pt-4">
            <button v-if="editingEntry" type="button" @click="deleteEntry"
              class="flex-1 py-3 px-4 rounded-xl border border-red-300 text-white bg-red-500 font-medium hover:bg-red-600 transition-colors cursor-pointer">
              Delete
            </button>
            <button type="button" @click="closeModal"
              class="flex-1 py-3 px-4 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors cursor-pointer">
              Cancel
            </button>
            <button type="submit"
              class="flex-1 py-3 px-4 rounded-xl bg-blue-500 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-200 cursor-pointer">
              {{ editingEntry ? 'Update Entry' : 'Save Entry' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/plugins/axios.ts';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { clearAuthData } from '@/utils/auth';

const router = useRouter();

// --- Reactive Data ---
const showModal = ref(false);
const editingEntry = ref(null);
const journalEntries = ref([]);
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

const journalForm = ref({
  id: null,
  content: '',
});

// --- Check Login Status ---
const token = localStorage.getItem('access_token');
const isLoggedIn = ref(!!token); // true if token exists

// --- Methods ---
const fetchJournalEntries = async () => {
  if (!isLoggedIn.value) {
    error.value = 'Please log in to view your journal.';
    isLoading.value = false;
    return;
  }

  isLoading.value = true;
  error.value = null;

  try {
    const response = await api.get('/api/child/gratitude', {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (response.data.entries) {
      journalEntries.value = response.data.entries.map(entry => ({
        id: entry.entry_id,
        content: entry.gratitude_text,
        date: entry.created_at,
      }));
    } else {
      journalEntries.value = [];
    }
  } catch (err) {
    console.error('Fetch error:', err);
    if (err.response?.status === 401) {
      error.value = 'Session expired. Please log in again.';
      isLoggedIn.value = false;
      localStorage.removeItem('access_token');
    } else {
      error.value = 'Failed to load journal entries.';
    }
  } finally {
    isLoading.value = false;
  }
};

const createEntry = async () => {
  if (!isLoggedIn.value) return;

  try {
    const response = await api.post('/api/child/gratitude', {
      gratitude_text: journalForm.value.content,
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const newEntry = {
      id: response.data.entry_id,
      content: journalForm.value.content,
      date: response.data.created_at,
    };
    journalEntries.value.unshift(newEntry);
    closeModal();
  } catch (err) {
    error.value = 'Failed to create entry.';
    console.error('Create error:', err);
  }
};

const updateEntry = async () => {
  if (!isLoggedIn.value) return;

  try {
    await api.put(`/api/child/gratitude/${editingEntry.value.id}`, {
      gratitude_text: journalForm.value.content,
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const index = journalEntries.value.findIndex(e => e.id === editingEntry.value.id);
    if (index !== -1) {
      journalEntries.value[index].content = journalForm.value.content;
    }
    closeModal();
  } catch (err) {
    error.value = 'Failed to update entry.';
    console.error('Update error:', err);
  }
};

const deleteEntry = async () => {
  if (!isLoggedIn.value) return;

  const confirmed = confirm("Are you sure you want to delete this entry?");
  if (!confirmed) return;

  try {
    await api.delete(`/api/child/gratitude/${editingEntry.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    journalEntries.value = journalEntries.value.filter(e => e.id !== editingEntry.value.id);
    closeModal();
  } catch (err) {
    error.value = 'Failed to delete entry.';
    console.error('Delete error:', err);
  }
};

// --- Modal Logic ---
const openCreateModal = () => {
  if (!isLoggedIn.value) {
    alert('Please log in to create a journal entry.');
    return;
  }
  editingEntry.value = null;
  resetForm();
  showModal.value = true;
};

const openEditModal = (entry) => {
  if (!isLoggedIn.value) return;
  editingEntry.value = entry;
  journalForm.value = { ...entry };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingEntry.value = null;
  resetForm();
};

const resetForm = () => {
  journalForm.value = { id: null, content: '' };
};

const saveEntry = () => {
  if (!isLoggedIn.value) return;
  if (!journalForm.value.content.trim()) return;

  if (editingEntry.value) {
    updateEntry();
  } else {
    createEntry();
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// --- Lifecycle Hook ---
onMounted(() => {
  fetchJournalEntries();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');
.line-clamp-4 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
}

.font-playfair {
  font-family: 'Playfair Display', serif;
}
</style>
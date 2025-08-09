<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <header class="max-w-4xl mx-auto mb-8 text-center">
      <router-link to="/student/home" class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">My Learning Journal 📝</h1>
      <p class="text-lg text-gray-600 font-medium">
        Reflect on your progress and capture your thoughts.
      </p>
    </header>

    <main class="max-w-6xl mx-auto">
      <div class="flex justify-center mb-8">
        <button
          @click="openCreateModal"
          class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center"
        >
          <span class="text-xl mr-2">➕</span>
          New Journal Entry
        </button>
      </div>

      <div v-if="journalEntries.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="entry in journalEntries"
          :key="entry.id"
          @click="openEditModal(entry)"
          class="bg-white rounded-3xl p-6 shadow-lg border border-gray-200 transform transition-transform hover:scale-105 cursor-pointer flex flex-col justify-between"
        >
          <div>
            <h3 class="font-bold text-gray-800 text-lg mb-2">{{ entry.title }}</h3>
            <p class="text-sm text-gray-600 mb-4 line-clamp-4">{{ entry.content }}</p>
          </div>
          <div class="flex items-center text-xs text-gray-500">
            <span class="font-semibold">{{ formatDate(entry.date) }}</span>
            <span class="mx-2">•</span>
            <span class="font-medium">{{ entry.moodEmoji }}</span>
            <span class="ml-1">{{ entry.mood }}</span>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-20">
        <div class="text-6xl mb-4">📖</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">Your Journal is Empty</h2>
        <p class="text-gray-600">Start writing to capture your thoughts and ideas!</p>
      </div>
    </main>

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
            <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
            <input
              v-model="journalForm.title"
              type="text"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="What did you learn today?"
              required
            >
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Your Thoughts</label>
            <textarea
              v-model="journalForm.content"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Describe your day, your feelings, or what you learned."
              rows="6"
              required
            ></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">How are you feeling?</label>
            <div class="flex space-x-2">
              <button
                v-for="mood in availableMoods"
                :key="mood.emoji"
                type="button"
                @click="journalForm.mood = mood.name; journalForm.moodEmoji = mood.emoji"
                class="p-3 text-2xl rounded-xl border-2 transition-all duration-200"
                :class="journalForm.moodEmoji === mood.emoji ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'"
              >
                {{ mood.emoji }}
              </button>
            </div>
          </div>

          <div class="flex space-x-3 pt-4">
            <button
              v-if="editingEntry"
              type="button"
              @click="deleteEntry"
              class="flex-1 py-3 px-4 rounded-xl border border-red-300 text-red-600 font-medium hover:bg-red-50 transition-colors"
            >
              Delete
            </button>
            <button
              type="button"
              @click="closeModal"
              class="flex-1 py-3 px-4 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-200"
            >
              {{ editingEntry ? 'Update Entry' : 'Save Entry' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// --- Reactive Data ---
const showModal = ref(false);
const editingEntry = ref(null);
const journalEntries = ref([]);

// Form data for the modal
const journalForm = ref({
  id: null,
  title: '',
  content: '',
  date: '',
  mood: 'Happy',
  moodEmoji: '😊',
});

// Available moods for the journal entry
const availableMoods = ref([
  { name: 'Happy', emoji: '😊' },
  { name: 'Excited', emoji: '🤩' },
  { name: 'Calm', emoji: '😌' },
  { name: 'Confused', emoji: '🤔' },
  { name: 'Stressed', emoji: '😥' },
  { name: 'Tired', emoji: '😴' },
]);

// --- Methods for Modal and CRUD operations ---
const openCreateModal = () => {
  editingEntry.value = null;
  resetForm();
  showModal.value = true;
};

const openEditModal = (entry) => {
  editingEntry.value = entry;
  journalForm.value = { ...entry }; // Populate form with existing entry data
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingEntry.value = null;
  resetForm();
};

const resetForm = () => {
  journalForm.value = {
    id: null,
    title: '',
    content: '',
    date: '',
    mood: 'Happy',
    moodEmoji: '😊',
  };
};

const saveEntry = () => {
  if (editingEntry.value) {
    // Logic to update an existing journal entry
    const index = journalEntries.value.findIndex(e => e.id === editingEntry.value.id);
    if (index !== -1) {
      journalEntries.value[index] = { ...journalForm.value };
    }
  } else {
    // Logic to create a new journal entry
    const newEntry = {
      id: Date.now(), // Simple unique ID
      ...journalForm.value,
      date: new Date().toISOString().split('T')[0], // Set current date
    };
    journalEntries.value.unshift(newEntry); // Add to the beginning of the array
  }
  closeModal();
};

const deleteEntry = () => {
  if (confirm(`Are you sure you want to delete this journal entry?`)) {
    journalEntries.value = journalEntries.value.filter(e => e.id !== editingEntry.value.id);
    closeModal();
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
  // In a real application, you would fetch journal entries from an API here
  journalEntries.value = [
    {
      id: 1,
      title: 'First Day of School',
      content: 'Today was my first day back at school. I met my new teacher, Ms. Smith, and she seems really nice. We learned about fractions in math and read a new book called "The Starship Adventure." It was a great day!',
      date: '2025-08-01',
      mood: 'Happy',
      moodEmoji: '😊',
    },
    {
      id: 2,
      title: 'Science Project Ideas',
      content: 'I have to come up with a science project idea for next week. I am thinking of either making a volcano with baking soda or building a small robot. I think the robot sounds more challenging but also more fun! I will do some more research tonight.',
      date: '2025-08-05',
      mood: 'Excited',
      moodEmoji: '🤩',
    },
    {
      id: 3,
      title: 'Feeling a bit tired',
      content: 'I stayed up a little too late last night finishing my book. I need to make sure I go to bed earlier so I am not so sleepy in class. I will try to read for only 20 minutes before bed tonight.',
      date: '2025-08-08',
      mood: 'Tired',
      moodEmoji: '😴',
    },
  ];
});
</script>

<style scoped>
/* Tailwind's line-clamp utility for truncating text */
.line-clamp-4 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
}
</style>
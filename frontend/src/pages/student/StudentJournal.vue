<template>
  <div class="min-h-screen bg-gradient-to-br from-green-400 via-blue-400 to-purple-300">
    <!-- Header -->
    <header class="bg-white/90 backdrop-blur-sm shadow-lg sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Back Button and Title -->
          <div class="flex items-center space-x-4">
            <button
                @click="goBack"
                class="p-2 text-gray-600 hover:text-gray-800 transition-colors rounded-lg hover:bg-gray-100"
            >
              <ArrowLeftIcon class="w-6 h-6" />
            </button>
            <div>
              <h1 class="text-xl font-bold text-gray-800 font-fancy">📖 My Journal</h1>
              <p class="text-sm text-gray-600 hidden sm:block">Write about your day!</p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex items-center space-x-3">
            <button
                @click="showCreateModal = true"
                class="bg-gradient-to-r from-green-500 to-blue-500 text-white px-4 py-2 rounded-xl hover:from-green-600 hover:to-blue-600 transition-all duration-200 flex items-center space-x-2 shadow-lg"
            >
              <PlusIcon class="w-4 h-4" />
              <span class="hidden sm:inline">New Entry</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Welcome Section -->
      <div class="mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20">
          <div class="flex flex-col md:flex-row items-center justify-between">
            <div class="text-center md:text-left mb-4 md:mb-0">
              <h2 class="text-2xl font-bold text-gray-800 mb-2">
                {{ getGreeting() }}, {{ studentName }}! 📝
              </h2>
              <p class="text-gray-600">What amazing things happened today?</p>
            </div>
            <div class="flex space-x-4">
              <div class="text-4xl animate-bounce" style="animation-delay: 0s">✨</div>
              <div class="text-4xl animate-bounce" style="animation-delay: 0.2s">📚</div>
              <div class="text-4xl animate-bounce" style="animation-delay: 0.4s">🌟</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 text-center">
          <div class="text-3xl mb-2">📖</div>
          <p class="text-2xl font-bold text-blue-600">{{ journalEntries.length }}</p>
          <p class="text-sm text-gray-600">Total Entries</p>
        </div>

        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 text-center">
          <div class="text-3xl mb-2">🔥</div>
          <p class="text-2xl font-bold text-orange-600">{{ currentStreak }}</p>
          <p class="text-sm text-gray-600">Day Streak</p>
        </div>

        <div class="bg-white/90 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 text-center">
          <div class="text-3xl mb-2">📝</div>
          <p class="text-2xl font-bold text-green-600">{{ totalWords }}</p>
          <p class="text-sm text-gray-600">Words Written</p>
        </div>
      </div>

      <!-- Filter and Sort -->
      <div class="mb-6 flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
        <div class="flex items-center space-x-4">
          <select
              v-model="selectedMood"
              class="px-4 py-2 bg-white/90 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Moods</option>
            <option value="😊">😊 Happy</option>
            <option value="😢">😢 Sad</option>
            <option value="😴">😴 Tired</option>
            <option value="😎">😎 Cool</option>
            <option value="🤔">🤔 Thoughtful</option>
            <option value="😆">😆 Excited</option>
          </select>

          <select
              v-model="sortOrder"
              class="px-4 py-2 bg-white/90 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="newest">Newest First</option>
            <option value="oldest">Oldest First</option>
          </select>
        </div>

        <div class="text-sm text-gray-600">
          {{ filteredEntries.length }} {{ filteredEntries.length === 1 ? 'entry' : 'entries' }} found
        </div>
      </div>

      <!-- Journal Entries Grid -->
      <div v-if="filteredEntries.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
            v-for="entry in filteredEntries"
            :key="entry.id"
            class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl border border-white/20 transform transition-all duration-300 hover:scale-105 cursor-pointer relative overflow-hidden"
            @click="openEntry(entry)"
        >
          <!-- Date Badge -->
          <div class="absolute top-4 right-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white px-3 py-1 rounded-full text-xs font-medium">
            {{ formatDate(entry.date) }}
          </div>

          <!-- Mood Icon -->
          <div class="text-4xl mb-4">{{ entry.mood }}</div>

          <!-- Entry Preview -->
          <h3 class="font-bold text-gray-800 mb-2 text-lg">{{ entry.title }}</h3>
          <p class="text-gray-600 text-sm mb-4 line-clamp-3">{{ entry.content }}</p>

          <!-- Entry Stats -->
          <div class="flex items-center justify-between text-xs text-gray-500">
            <span>{{ entry.wordCount }} words</span>
            <span>{{ formatTime(entry.date) }}</span>
          </div>

          <!-- Weather if available -->
          <div v-if="entry.weather" class="mt-3 flex items-center text-xs text-gray-500">
            <span class="mr-1">🌤️</span>
            {{ entry.weather }}
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="text-6xl mb-4">📝</div>
        <h3 class="text-xl font-bold text-gray-800 mb-2">No journal entries yet</h3>
        <p class="text-gray-600 mb-6">Start writing about your day to create your first entry!</p>
        <button
            @click="showCreateModal = true"
            class="bg-gradient-to-r from-green-500 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-blue-600 transition-all duration-200 shadow-lg"
        >
          ✨ Write My First Entry
        </button>
      </div>
    </main>

    <!-- Create/Edit Entry Modal -->
    <div v-if="showCreateModal || editingEntry" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-800">
            {{ editingEntry ? '✏️ Edit Entry' : '📝 New Journal Entry' }}
          </h2>
          <button
              @click="closeModal"
              class="p-2 text-gray-500 hover:text-gray-700 transition-colors rounded-lg hover:bg-gray-100"
          >
            <XIcon class="w-6 h-6" />
          </button>
        </div>

        <form @submit.prevent="saveEntry" class="space-y-6">
          <!-- Date -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">📅 Date</label>
            <input
                v-model="entryForm.date"
                type="date"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-400 transition-colors"
                required
            />
          </div>

          <!-- Title -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">📖 Title</label>
            <input
                v-model="entryForm.title"
                type="text"
                placeholder="What's today's story about?"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-400 transition-colors"
                required
            />
          </div>

          <!-- Mood -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">😊 How are you feeling?</label>
            <div class="grid grid-cols-3 sm:grid-cols-6 gap-3">
              <button
                  v-for="mood in moods"
                  :key="mood.emoji"
                  type="button"
                  @click="entryForm.mood = mood.emoji"
                  class="p-3 rounded-xl border-2 transition-all duration-200 text-center"
                  :class="entryForm.mood === mood.emoji
                  ? 'border-blue-500 bg-blue-50 scale-110'
                  : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'"
              >
                <div class="text-2xl mb-1">{{ mood.emoji }}</div>
                <div class="text-xs text-gray-600">{{ mood.label }}</div>
              </button>
            </div>
          </div>

          <!-- Weather (Optional) -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">🌤️ Weather (Optional)</label>
            <select
                v-model="entryForm.weather"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-400 transition-colors"
            >
              <option value="">Select weather</option>
              <option value="Sunny">☀️ Sunny</option>
              <option value="Cloudy">☁️ Cloudy</option>
              <option value="Rainy">🌧️ Rainy</option>
              <option value="Snowy">❄️ Snowy</option>
              <option value="Windy">💨 Windy</option>
            </select>
          </div>

          <!-- Content -->
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-2">✍️ What happened today?</label>
            <textarea
                v-model="entryForm.content"
                placeholder="Tell me about your day... What did you learn? What made you happy? What was challenging?"
                rows="8"
                class="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-blue-400 transition-colors resize-none"
                required
            ></textarea>
            <div class="text-xs text-gray-500 mt-1">
              {{ entryForm.content.split(' ').filter(word => word.length > 0).length }} words
            </div>
          </div>

          <!-- Prompts for inspiration -->
          <div class="bg-blue-50 rounded-2xl p-4">
            <h4 class="font-semibold text-blue-800 mb-2">💡 Need inspiration? Try these prompts:</h4>
            <div class="space-y-1 text-sm text-blue-700">
              <button
                  v-for="prompt in writingPrompts"
                  :key="prompt"
                  type="button"
                  @click="addPromptToContent(prompt)"
                  class="block text-left hover:text-blue-900 transition-colors"
              >
                • {{ prompt }}
              </button>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex space-x-4">
            <button
                type="button"
                @click="closeModal"
                class="flex-1 px-6 py-3 border-2 border-gray-200 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
                type="submit"
                :disabled="!entryForm.title || !entryForm.content || !entryForm.mood"
                class="flex-1 bg-gradient-to-r from-green-500 to-blue-500 text-white px-6 py-3 rounded-xl hover:from-green-600 hover:to-blue-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ editingEntry ? '💾 Update Entry' : '✨ Save Entry' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Read Entry Modal -->
    <div v-if="readingEntry" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="flex justify-between items-center mb-6">
          <div class="flex items-center space-x-3">
            <div class="text-3xl">{{ readingEntry.mood }}</div>
            <div>
              <h2 class="text-2xl font-bold text-gray-800">{{ readingEntry.title }}</h2>
              <p class="text-sm text-gray-600">{{ formatFullDate(readingEntry.date) }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <button
                @click="editEntry(readingEntry)"
                class="p-2 text-blue-600 hover:text-blue-800 transition-colors rounded-lg hover:bg-blue-50"
            >
              <EditIcon class="w-5 h-5" />
            </button>
            <button
                @click="deleteEntry(readingEntry.id)"
                class="p-2 text-red-600 hover:text-red-800 transition-colors rounded-lg hover:bg-red-50"
            >
              <TrashIcon class="w-5 h-5" />
            </button>
            <button
                @click="readingEntry = null"
                class="p-2 text-gray-500 hover:text-gray-700 transition-colors rounded-lg hover:bg-gray-100"
            >
              <XIcon class="w-6 h-6" />
            </button>
          </div>
        </div>

        <!-- Entry Content -->
        <div class="space-y-4">
          <div v-if="readingEntry.weather" class="flex items-center text-gray-600">
            <span class="mr-2">🌤️</span>
            <span>Weather: {{ readingEntry.weather }}</span>
          </div>

          <div class="prose prose-lg max-w-none">
            <p class="text-gray-800 leading-relaxed whitespace-pre-wrap">{{ readingEntry.content }}</p>
          </div>

          <div class="flex items-center justify-between text-sm text-gray-500 pt-4 border-t border-gray-200">
            <span>{{ readingEntry.wordCount }} words</span>
            <span>Written at {{ formatTime(readingEntry.date) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Floating decorative elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div class="absolute top-20 left-10 w-8 h-8 bg-yellow-300 rounded-full opacity-20 animate-bounce"></div>
      <div class="absolute top-40 right-20 w-6 h-6 bg-pink-300 rounded-full opacity-20 animate-bounce" style="animation-delay: 0.5s"></div>
      <div class="absolute bottom-32 left-20 w-10 h-10 bg-orange-300 rounded-full opacity-20 animate-bounce" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 right-10 w-7 h-7 bg-cyan-300 rounded-full opacity-20 animate-bounce" style="animation-delay: 1.5s"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowLeftIcon,
  PlusIcon,
  XIcon,
  EditIcon,
  TrashIcon
} from 'lucide-vue-next'

// Router
const router = useRouter()

// Reactive data
const showCreateModal = ref(false)
const editingEntry = ref(null)
const readingEntry = ref(null)
const selectedMood = ref('')
const sortOrder = ref('newest')
const studentName = ref('Alex')

// Form data
const entryForm = ref({
  date: new Date().toISOString().split('T')[0],
  title: '',
  content: '',
  mood: '',
  weather: ''
})

// Mock journal entries
const journalEntries = ref([
  {
    id: 1,
    date: '2024-01-15T10:30:00Z',
    title: 'Amazing Science Experiment!',
    content: 'Today we did a volcano experiment in science class! It was so cool when it erupted with baking soda and vinegar. I learned that chemical reactions can create gas that makes things bubble up. I want to try this at home with mom and dad. The best part was when everyone cheered when my volcano erupted the highest! I felt like a real scientist.',
    mood: '😆',
    weather: 'Sunny',
    wordCount: 65
  },
  {
    id: 2,
    date: '2024-01-14T15:45:00Z',
    title: 'Math Was Tricky Today',
    content: 'We learned about fractions today and it was really hard at first. I didn\'t understand how 1/2 could be the same as 2/4. But then Mrs. Johnson showed us with pizza slices and it made so much sense! Now I think fractions are actually pretty cool. I helped my friend Jake understand it too, which made me feel proud.',
    mood: '🤔',
    weather: 'Cloudy',
    wordCount: 58
  },
  {
    id: 3,
    date: '2024-01-13T09:15:00Z',
    title: 'Reading Adventure',
    content: 'I finished reading "Charlotte\'s Web" today and I cried at the end! Charlotte was such a good friend to Wilbur. It made me think about how important friendship is. I want to be a good friend like Charlotte. Tomorrow I\'m going to start a new book about dragons. Reading makes me feel like I can go anywhere and be anyone!',
    mood: '😢',
    weather: 'Rainy',
    wordCount: 62
  },
  {
    id: 4,
    date: '2024-01-12T14:20:00Z',
    title: 'Art Class Masterpiece',
    content: 'In art class today, I painted a picture of my family at the beach. I used lots of blue for the ocean and yellow for the sun. My little sister looks funny in the painting because I made her head too big, but mom said it shows how much I love her. I can\'t wait to give it to my parents as a surprise!',
    mood: '😊',
    weather: 'Sunny',
    wordCount: 59
  },
  {
    id: 5,
    date: '2024-01-11T16:30:00Z',
    title: 'Playground Fun',
    content: 'Recess was the best part of today! We played tag and I was "it" for most of the time, but I didn\'t mind because everyone was laughing and having fun. Then we played on the swings and tried to see who could swing the highest. I made a new friend named Emma who just moved here from another state. She\'s really nice and likes the same games I do.',
    mood: '😎',
    weather: 'Windy',
    wordCount: 71
  }
])

// Available moods
const moods = [
  { emoji: '😊', label: 'Happy' },
  { emoji: '😢', label: 'Sad' },
  { emoji: '😴', label: 'Tired' },
  { emoji: '😎', label: 'Cool' },
  { emoji: '🤔', label: 'Thoughtful' },
  { emoji: '😆', label: 'Excited' }
]

// Writing prompts
const writingPrompts = [
  'What was the best part of your day?',
  'What did you learn today?',
  'Who made you smile today?',
  'What was challenging for you?',
  'What are you grateful for?',
  'What do you want to remember about today?',
  'How did you help someone today?',
  'What made you laugh?'
]

// Computed properties
const filteredEntries = computed(() => {
  let entries = [...journalEntries.value]

  // Filter by mood
  if (selectedMood.value) {
    entries = entries.filter(entry => entry.mood === selectedMood.value)
  }

  // Sort entries
  entries.sort((a, b) => {
    const dateA = new Date(a.date)
    const dateB = new Date(b.date)
    return sortOrder.value === 'newest' ? dateB - dateA : dateA - dateB
  })

  return entries
})

const currentStreak = computed(() => {
  // Calculate consecutive days with entries
  const today = new Date()
  let streak = 0

  for (let i = 0; i < 30; i++) {
    const checkDate = new Date(today)
    checkDate.setDate(today.getDate() - i)
    const dateString = checkDate.toISOString().split('T')[0]

    const hasEntry = journalEntries.value.some(entry =>
        entry.date.split('T')[0] === dateString
    )

    if (hasEntry) {
      streak++
    } else if (i > 0) {
      break
    }
  }

  return streak
})

const totalWords = computed(() => {
  return journalEntries.value.reduce((total, entry) => total + entry.wordCount, 0)
})

// Methods
const goBack = () => {
  router.go(-1)
}

const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 17) return 'Good afternoon'
  return 'Good evening'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const today = new Date()
  const yesterday = new Date(today)
  yesterday.setDate(today.getDate() - 1)

  if (date.toDateString() === today.toDateString()) {
    return 'Today'
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday'
  } else {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
  }
}

const formatFullDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatTime = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

const openEntry = (entry) => {
  readingEntry.value = entry
}

const editEntry = (entry) => {
  editingEntry.value = entry
  entryForm.value = {
    date: entry.date.split('T')[0],
    title: entry.title,
    content: entry.content,
    mood: entry.mood,
    weather: entry.weather || ''
  }
  readingEntry.value = null
}

const deleteEntry = (entryId) => {
  if (confirm('Are you sure you want to delete this journal entry?')) {
    const index = journalEntries.value.findIndex(entry => entry.id === entryId)
    if (index > -1) {
      journalEntries.value.splice(index, 1)
    }
    readingEntry.value = null
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingEntry.value = null
  entryForm.value = {
    date: new Date().toISOString().split('T')[0],
    title: '',
    content: '',
    mood: '',
    weather: ''
  }
}

const addPromptToContent = (prompt) => {
  if (entryForm.value.content) {
    entryForm.value.content += '\n\n' + prompt + ' '
  } else {
    entryForm.value.content = prompt + ' '
  }
}

const saveEntry = () => {
  const wordCount = entryForm.value.content.split(' ').filter(word => word.length > 0).length

  if (editingEntry.value) {
    // Update existing entry
    const index = journalEntries.value.findIndex(entry => entry.id === editingEntry.value.id)
    if (index > -1) {
      journalEntries.value[index] = {
        ...editingEntry.value,
        ...entryForm.value,
        date: entryForm.value.date + 'T' + new Date().toTimeString().split(' ')[0] + 'Z',
        wordCount
      }
    }
  } else {
    // Create new entry
    const newEntry = {
      id: Date.now(),
      ...entryForm.value,
      date: entryForm.value.date + 'T' + new Date().toTimeString().split(' ')[0] + 'Z',
      wordCount
    }
    journalEntries.value.unshift(newEntry)
  }

  closeModal()
}

onMounted(() => {
  // Get student info from localStorage
  const userEmail = localStorage.getItem('user_email')
  if (userEmail) {
    const name = userEmail.split('@')[0]
    studentName.value = name.charAt(0).toUpperCase() + name.slice(1)
  }
})
</script>

<style scoped>
@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0,0,0);
  }
  40%, 43% {
    transform: translate3d(0,-30px,0);
  }
  70% {
    transform: translate3d(0,-15px,0);
  }
  90% {
    transform: translate3d(0,-4px,0);
  }
}

.animate-bounce {
  animation: bounce 2s infinite;
}

.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

.font-fancy {
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.prose {
  max-width: none;
}

.prose p {
  margin-bottom: 1em;
}
</style>

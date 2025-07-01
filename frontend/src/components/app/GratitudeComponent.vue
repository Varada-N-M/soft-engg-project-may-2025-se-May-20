<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-400 via-cyan-400 to-purple-500 p-4">
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl mb-6">
        <h1 class="font-fancy text-4xl font-bold text-gray-800 text-center mb-2">
          Journal
        </h1>
      </div>

      <!-- Entries by Month -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl mb-6">
        <div v-if="loading && groupedEntries.length === 0" class="text-center py-8">
          <div class="text-4xl mb-4">⏳</div>
          <p class="text-gray-600">Loading your journal entries...</p>
        </div>

        <div v-else-if="groupedEntries.length === 0" class="text-center py-12">
          <div class="text-6xl mb-4">📖</div>
          <h4 class="text-xl font-bold text-gray-700 mb-2">"Ready to Begin?</h4>
          <p class="text-gray-600">Write something you're thankful for and start your journal today!"</p>
        </div>

        <div v-else class="space-y-8">
          <div v-for="monthGroup in groupedEntries" :key="monthGroup.month" class="space-y-4">
            <!-- Month Header -->
            <h2 class="text-2xl font-bold text-gray-800 border-b-2 border-purple-200 pb-2">
              {{ monthGroup.month }}
            </h2>
            
            <!-- Entries for this month -->
            <div class="space-y-4">
              <div
                v-for="entry in monthGroup.entries"
                :key="entry.entry_id"
                class="border-l-4 border-purple-300 pl-4 py-2"
              >
                <div class="flex items-start justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-purple-600 text-lg">{{ getDayOfMonth(entry.created_at) }}</span>
                    <span class="text-sm text-gray-500">{{ getTimeAgo(entry.created_at) }}</span>
                  </div>
                  
                  <div class="flex gap-2">
                    <button
                      @click="startEdit(entry)"
                      class="p-1 text-blue-500 hover:bg-blue-100 rounded transition-colors duration-200"
                      title="Edit entry"
                    >
                      ✏️
                    </button>
                    <button
                      @click="deleteEntry(entry.entry_id)"
                      class="p-1 text-red-500 hover:bg-red-100 rounded transition-colors duration-200"
                      title="Delete entry"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
                
                <p class="text-gray-700 leading-relaxed">{{ entry.gratitude_text }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Section -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-xl">
        <form @submit.prevent="submitEntry" class="flex gap-3">
          <input
            v-model="gratitudeText"
            type="text"
            :placeholder="editingEntry ? 'Update your entry...' : 'How was your day?'"
            class="flex-1 p-4 border-2 border-purple-200 rounded-2xl focus:border-purple-400 focus:outline-none text-gray-700"
            required
          />
          
          <button
            type="submit"
            :disabled="loading || !gratitudeText.trim()"
            class="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-4 rounded-2xl hover:from-purple-600 hover:to-pink-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg min-w-[60px] flex items-center justify-center"
          >
            <svg v-if="!loading" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
            </svg>
            <div v-else class="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          </button>
        </form>
        
        <button
          v-if="editingEntry"
          @click="cancelEdit"
          class="mt-3 w-full py-2 px-4 bg-gray-300 text-gray-700 font-semibold rounded-2xl hover:bg-gray-400 transition-colors duration-200"
        >
          Cancel Edit
        </button>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div
      v-if="message"
      :class="[
        'fixed top-4 right-4 p-4 rounded-2xl shadow-lg z-50 transition-all duration-300',
        messageType === 'success' 
          ? 'bg-green-500 text-white' 
          : 'bg-red-500 text-white'
      ]"
    >
      <div class="flex items-center gap-2">
        <span>{{ messageType === 'success' ? '✅' : '❌' }}</span>
        <span class="font-semibold">{{ message }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '@/plugins/axios'

// Reactive data
const gratitudeText = ref('')
const entries = ref([])
const loading = ref(false)
const message = ref('')
const messageType = ref('success')
const editingEntry = ref(null)

// Computed properties
const groupedEntries = computed(() => {
  const groups = {}
  
  entries.value.forEach(entry => {
    const date = new Date(entry.created_at)
    const monthYear = date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
    
    if (!groups[monthYear]) {
      groups[monthYear] = []
    }
    groups[monthYear].push(entry)
  })
  
  // Convert to array and sort by month (newest first)
  return Object.entries(groups)
    .map(([month, entries]) => ({
      month,
      entries: entries.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    }))
    .sort((a, b) => {
      const dateA = new Date(a.entries[0].created_at)
      const dateB = new Date(b.entries[0].created_at)
      return dateB - dateA
    })
})

// Methods
const showMessage = (msg, type = 'success') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const getDayOfMonth = (dateString) => {
  return new Date(dateString).getDate()
}

const getTimeAgo = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'Today'
  if (diffDays === 2) return 'Yesterday'
  if (diffDays <= 7) return `${diffDays - 1} days ago`
  
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric'
  })
}

const fetchEntries = async () => {
  try {
    loading.value = true
    const response = await axios.get('/gratitude')
    entries.value = response.data.entries || []
  } catch (error) {
    console.error('Error fetching entries:', error)
    showMessage('Failed to load entries', 'error')
  } finally {
    loading.value = false
  }
}

const submitEntry = async () => {
  if (!gratitudeText.value.trim()) return
  
  try {
    loading.value = true
    
    if (editingEntry.value) {
      // Update existing entry
      await axios.put(`/gratitude/${editingEntry.value.entry_id}`, {
        gratitude_text: gratitudeText.value.trim()
      })
      showMessage('Entry updated successfully! 🎉')
      editingEntry.value = null
    } else {
      // Create new entry
      await axios.post('/gratitude', {
        gratitude_text: gratitudeText.value.trim()
      })
      showMessage('New journal entry saved! 📝')
    }
    
    gratitudeText.value = ''
    await fetchEntries()
  } catch (error) {
    console.error('Error saving entry:', error)
    showMessage('Failed to save entry', 'error')
  } finally {
    loading.value = false
  }
}

const startEdit = (entry) => {
  editingEntry.value = entry
  gratitudeText.value = entry.gratitude_text
  // Scroll to input
  window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
}

const cancelEdit = () => {
  editingEntry.value = null
  gratitudeText.value = ''
}

const deleteEntry = async (entryId) => {
  if (!confirm('Are you sure you want to delete this journal entry? 🤔')) return
  
  try {
    loading.value = true
    await axios.delete(`/gratitude/${entryId}`)
    showMessage('Entry deleted successfully! 👋')
    await fetchEntries()
  } catch (error) {
    console.error('Error deleting entry:', error)
    showMessage('Failed to delete entry', 'error')
  } finally {
    loading.value = false
  }
}

// Initialize
onMounted(() => {
  fetchEntries()
})
</script>

<style scoped>
.font-fancy {
  font-family: 'Comic Sans MS', cursive, sans-serif;
}
</style>
<template>
  <div class="min-h-screen bg-gray-50 flex flex-col p-8 font-inter">
    <header class="max-w-4xl mx-auto w-full text-center mb-6">
      <router-link to="/student/home" class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4 rounded-lg px-3 py-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">My AI Companion</h1>
    </header>

    <main class="flex-1 max-w-4xl w-full mx-auto bg-white rounded-[25px] shadow-lg border border-gray-200 flex flex-col overflow-hidden">
      <div class="flex-1 p-6 space-y-4 overflow-y-auto custom-scrollbar">

        <!-- AI Tools Section (Tabs) -->
        <div class="main-content mt-4">
          <div class="tabs flex justify-center space-x-2 mb-6">
            <button
              class="tab px-5 py-2 rounded-xl text-sm font-medium transition-all duration-200"
              :class="{ 'active bg-blue-500 text-white shadow-md': activeTab === 'sentence', 'bg-gray-200 text-gray-700 hover:bg-gray-300': activeTab !== 'sentence' }"
              @click="activeTab = 'sentence'"
            >
              Sentence Improver
            </button>
            <button
              class="tab px-5 py-2 rounded-xl text-sm font-medium transition-all duration-200"
              :class="{ 'active bg-blue-500 text-white shadow-md': activeTab === 'writing', 'bg-gray-200 text-gray-700 hover:bg-gray-300': activeTab !== 'writing' }"
              @click="activeTab = 'writing'"
            >
              Writing Analyzer
            </button>
            <button
              class="tab px-5 py-2 rounded-xl text-sm font-medium transition-all duration-200"
              :class="{ 'active bg-blue-500 text-white shadow-md': activeTab === 'grammar', 'bg-gray-200 text-gray-700 hover:bg-gray-300': activeTab !== 'grammar' }"
              @click="activeTab = 'grammar'"
            >
              Grammar Check
            </button>
          </div>

          <!-- Sentence Improver Tab Content -->
          <div v-show="activeTab === 'sentence'" class="tab-content bg-white p-6 rounded-2xl shadow-inner border border-gray-100">
            <div class="form-group mb-4">
              <label for="sentence-input" class="block text-gray-700 text-sm font-bold mb-2">Enter your sentence:</label>
              <textarea
                id="sentence-input"
                v-model="sentenceInput"
                class="form-control w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
                rows="3"
                placeholder="Example: Yesterday I told her that I have had to go home"
              ></textarea>
            </div>
            <button
              class="btn bg-blue-600 text-white py-3 px-6 rounded-xl shadow-md hover:bg-blue-700 transition-colors duration-200 flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
              @click="improveSentence"
              :disabled="loading || !sentenceInput?.trim()"
            >
              <span v-if="loading" class="spinner mr-2 w-4 h-4 border-2 border-white border-t-transparent rounded-[20px] animate-spin"></span>
              {{ loading ? 'Analyzing...' : 'Improve Sentence' }}
            </button>

            <div v-if="sentenceResults" class="results mt-6 p-4 bg-gray-50 rounded-xl border border-gray-200">
              <div class="result-section mb-4">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">📝 AI Improved Version</h3>
                <div class="improved-text p-3 bg-white border border-gray-200 rounded-lg" v-html="formatAIResponse(sentenceResults.ai_improvement)"></div>
              </div>

              <div v-if="sentenceResults.issues && sentenceResults.issues.length > 0" class="result-section mb-4">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">⚠️ Issues Found</h3>
                <ul class="issues-list list-disc list-inside p-3 bg-white border border-gray-200 rounded-lg">
                  <li v-for="issue in sentenceResults.issues" :key="issue" class="text-red-600 mb-1">{{ issue }}</li>
                </ul>
              </div>

              <div v-if="sentenceResults.suggestions && sentenceResults.suggestions.length > 0" class="result-section mb-4">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">💡 Suggestions</h3>
                <ul class="tips-list list-disc list-inside p-3 bg-white border border-gray-200 rounded-lg">
                  <li v-for="suggestion in sentenceResults.suggestions" :key="suggestion" class="text-green-700 mb-1">{{ suggestion }}</li>
                </ul>
              </div>

              <div v-if="sentenceResults.speaking_tips && sentenceResults.speaking_tips.length > 0" class="result-section mb-4">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">🎤 Speaking Tips</h3>
                <ul class="tips-list list-disc list-inside p-3 bg-white border border-gray-200 rounded-lg">
                  <li v-for="tip in sentenceResults.speaking_tips" :key="tip" class="text-purple-700 mb-1">{{ tip }}</li>
                </ul>
              </div>

              <div class="result-section">
                <h3 class="text-lg font-semibold text-gray-800 mb-2">📊 Analysis</h3>
                <div class="stats flex space-x-4 p-3 bg-white border border-gray-200 rounded-lg">
                  <div class="stat-item text-center">
                    <div class="stat-number text-2xl font-bold text-blue-600">{{ sentenceResults.word_count || 0 }}</div>
                    <div class="stat-label text-gray-600 text-sm">Words</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Chat Messages -->
        <div v-for="message in messages" :key="message.id" class="flex" :class="message.from === 'user' ? 'justify-end' : 'justify-start'">
          <div v-if="message.from === 'user'" class="bg-purple-500 text-white p-4 rounded-3xl max-w-[80%] transform transition-transform duration-300 ease-out">
            <p>{{ message.text }}</p>
          </div>
          <div v-else class="flex items-start">
            <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold text-lg mr-3">🤖</div>
            <div class="bg-gray-100 p-4 rounded-3xl max-w-[80%] transform transition-transform duration-300 ease-out">
              <p class="text-gray-800">{{ message.text }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Message Input -->
      <div class="p-6 border-t border-gray-200 bg-white">
        <form @submit.prevent="sendMessage" class="flex items-center space-x-3">
          <input
            v-model="newMessage"
            type="text"
            placeholder="Type your message here..."
            class="flex-1 px-5 py-3 rounded-2xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-200"
            required
          />
          <button
            type="submit"
            class="bg-blue-500 text-white p-3 rounded-2xl shadow-md hover:bg-blue-600 transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
            </svg>
          </button>
        </form>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Reactive variables for chat functionality
const newMessage = ref('');
const messages = ref([]);

// Reactive variables for AI tools functionality
const activeTab = ref('sentence'); // Default active tab
const sentenceInput = ref(''); // Input for sentence improver
const sentenceResults = ref(null); // Results object for sentence improver
const loading = ref(false); // Loading state for AI operations

// Function to handle sending chat messages
const sendMessage = () => {
  if (newMessage.value.trim() === '') return;

  // Add user's message to the chat
  messages.value.push({
    id: Date.now(),
    from: 'user',
    text: newMessage.value,
  });

  // Simulate an AI response after a short delay
  setTimeout(() => {
    messages.value.push({
      id: Date.now() + 1,
      from: 'ai',
      text: "That's a great question! I'm still learning, but I can tell you more about that topic. What would you like to know?",
    });
  }, 1000);

  // Clear the input field
  newMessage.value = '';
};

// Function to simulate sentence improvement (replace with actual API call)
const improveSentence = () => {
  if (!sentenceInput.value?.trim()) return;

  loading.value = true;
  // Simulate an API call
  setTimeout(() => {
    sentenceResults.value = {
      ai_improvement: "Yesterday, I had to go home, and I informed her about it.",
      issues: ["Redundant phrasing 'I told her that I have had to go home' could be simplified."],
      suggestions: ["Use more concise language.", "Ensure active voice where appropriate."],
      speaking_tips: ["Practice intonation for clarity.", "Maintain a steady pace."],
      word_count: sentenceInput.value.split(/\s+/).filter(word => word.length > 0).length,
    };
    loading.value = false;
  }, 1500);
};

// Function to format AI response (e.g., for highlighting or simple HTML)
const formatAIResponse = (text) => {
  // Simple example: if you wanted to bold certain parts or add specific HTML.
  // For now, it just returns the text as is.
  return text;
};
</script>

<style scoped>
/* Ensure font is Inter */
.font-inter {
  font-family: 'Inter', sans-serif;
}

/* Custom Scrollbar for Chat Window */
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Basic spinner animation */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
</style>
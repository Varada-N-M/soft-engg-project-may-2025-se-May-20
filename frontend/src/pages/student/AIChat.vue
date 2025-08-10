<template>
  <div class="min-h-screen bg-gray-50 flex flex-col p-8">
    <header class="max-w-4xl mx-auto w-full text-center mb-6">
      <router-link to="/student/home" class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">My AI Companion</h1>
    </header>

    <main class="flex-1 max-w-4xl w-full mx-auto bg-white rounded-3xl shadow-lg border border-gray-200 flex flex-col overflow-hidden">
      <div class="flex-1 p-6 space-y-4 overflow-y-auto custom-scrollbar">
        <div class="flex items-start">
          <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold text-lg mr-3">🤖</div>
          <div class="bg-gray-100 p-4 rounded-3xl max-w-[80%]">
            <p class="text-gray-800">Hello there! I'm your learning companion. How can I assist you today?</p>
          </div>
        </div>

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

const newMessage = ref('');
const messages = ref([]);

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
</script>

<style scoped>
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
</style>
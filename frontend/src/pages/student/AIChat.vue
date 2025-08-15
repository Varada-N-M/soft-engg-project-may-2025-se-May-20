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
        <div class="rounded-3xl p-8">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2">
                Meet Rohit!
              </h1>
              <p class="text-gray-600 text-lg">
                Improve your writing and speaking skills with your AI-powered assistant.
              </p>
            </div>
          </div>
        </div>

        <div class="rounded-3xl p-8">
          <div class="tabs">
            <button class="tab" :class="{ 'active': activeTab === 'sentence' }" @click="activeTab = 'sentence'">
              Sentence Improver
            </button>
            <button class="tab" :class="{ 'active': activeTab === 'writing' }" @click="activeTab = 'writing'">
              Writing Analyzer
            </button>
            <button class="tab" :class="{ 'active': activeTab === 'grammar' }" @click="activeTab = 'grammar'">
              Grammar Check
            </button>
          </div>

          <!-- Sentence Improver Tab -->
          <div v-show="activeTab === 'sentence'" class="tab-content">
            <div class="form-group">
              <label for="sentence-input">Enter your sentence:</label>
              <textarea id="sentence-input" v-model="sentenceInput" class="form-control" rows="3"
                placeholder="Start typing your sentence here..."></textarea>
            </div>
            <button class="btn" @click="improveSentence" :disabled="loading || !sentenceInput.trim()">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Analyzing...' : 'Improve Sentence' }}
            </button>

            <div v-if="sentenceResults" class="results">
              <div class="result-section">
                <h3>AI Improved Version :</h3>
                <div class="improved-text" v-html="formatAIResponse(sentenceResults.ai_improvement)"></div>
              </div>

              <div v-if="sentenceResults.issues && sentenceResults.issues.length > 0" class="result-section">
                <h3>Issues Found</h3>
                <ul class="issues-list">
                  <li v-for="issue in sentenceResults.issues" :key="issue">{{ issue }}</li>
                </ul>
              </div>

              <div v-if="sentenceResults.suggestions && sentenceResults.suggestions.length > 0" class="result-section">
                <h3>Suggestions</h3>
                <ul class="tips-list">
                  <li v-for="suggestion in sentenceResults.suggestions" :key="suggestion">{{ suggestion }}</li>
                </ul>
              </div>

              <div v-if="sentenceResults.speaking_tips && sentenceResults.speaking_tips.length > 0"
                class="result-section">
                <h3>Speaking Tips</h3>
                <ul class="tips-list">
                  <li v-for="tip in sentenceResults.speaking_tips" :key="tip">{{ tip }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Writing Analyzer Tab -->
          <div v-show="activeTab === 'writing'" class="tab-content">
            <div class="form-group">
              <label for="writing-type">Writing Type:</label>
              <select id="writing-type" v-model="writingType" class="form-control">
                <option value="general">General</option>
                <option value="story">Story</option>
                <option value="essay">Essay</option>
                <option value="speech">Speech</option>
              </select>
            </div>
            <div class="form-group">
              <label for="writing-input">Your writing:</label>
              <textarea id="writing-input" v-model="writingInput" class="form-control" rows="8"
                placeholder="Paste your story, essay, or any longer text here..."></textarea>
            </div>
            <button class="btn" @click="analyzeWriting" :disabled="loading || !writingInput.trim()">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Analyzing...' : 'Analyze Writing' }}
            </button>

            <div v-if="writingResults" class="results">
              <div class="stats">
                <div class="stat-item">
                  <div class="stat-number">{{ writingResults.analysis?.word_count || 0 }}</div>
                  <div class="stat-label">Words</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ writingResults.analysis?.sentence_count || 0 }}</div>
                  <div class="stat-label">Sentences</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ Math.round(writingResults.analysis?.avg_sentence_length || 0) }}</div>
                  <div class="stat-label">Avg Words/Sentence</div>
                </div>
                <div class="stat-item">
                  <div class="stat-number">{{ writingResults.readability_score || 'N/A' }}</div>
                  <div class="stat-label">Readability</div>
                </div>
              </div>

              <div class="result-section">
                <h3>AI Feedback</h3>
                <div class="improved-text" v-html="formatAIResponse(writingResults.ai_feedback)"></div>
              </div>

              <div v-if="writingResults.analysis?.issues && writingResults.analysis.issues.length > 0"
                class="result-section">
                <h3>Issues to Address</h3>
                <ul class="issues-list">
                  <li v-for="issue in writingResults.analysis.issues.slice(0, 5)" :key="issue">{{ issue }}</li>
                </ul>
              </div>

              <div v-if="writingResults.analysis?.suggestions && writingResults.analysis.suggestions.length > 0"
                class="result-section">
                <h3>Suggestions</h3>
                <ul class="tips-list">
                  <li v-for="suggestion in writingResults.analysis.suggestions.slice(0, 5)" :key="suggestion">
                    {{ 
                    suggestion }}
                  </li>
                </ul>
              </div>

              <div v-if="writingResults.speaking_tips && writingResults.speaking_tips.length > 0"
                class="result-section">
                <h3>Speaking Tips</h3>
                <ul class="tips-list">
                  <li v-for="tip in writingResults.speaking_tips.slice(0, 4)" :key="tip">{{ tip }}</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Grammar Check Tab -->
          <div v-show="activeTab === 'grammar'" class="tab-content">
            <div class="form-group">
              <label for="grammar-input">Text to check:</label>
              <textarea id="grammar-input" v-model="grammarInput" class="form-control" rows="4"
                placeholder="Enter text to check for basic grammar issues..."></textarea>
            </div>
            <button class="btn" @click="checkGrammar" :disabled="loading || !grammarInput.trim()">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? 'Checking...' : 'Check Grammar' }}

            </button>

            <div v-if="grammarResults" class="results">
              <!-- Show AI improved text if available -->
              <div v-if="grammarResults.ai_improved_text" class="result-section">
                <h3>AI Improved Version :</h3>
                <div class="improved-text">{{ grammarResults.ai_improved_text }}</div>
              </div>

              <!-- Show grammar status -->
              <div v-if="grammarResults.is_correct" class="success">
                Great! No major grammar issues found.
              </div>

              <!-- Show grammar issues if any -->
              <div v-if="grammarResults.issues && grammarResults.issues.length > 0" class="result-section">
                <h3>Grammar Issues</h3>
                <ul class="issues-list">
                  <li v-for="issue in grammarResults.issues" :key="issue">{{ issue }}</li>
                </ul>
              </div>

              <!-- Show corrections if any -->
              <div v-if="grammarResults.corrections && grammarResults.corrections.length > 0" class="result-section">
                <h3>Suggested Corrections</h3>
                <div v-for="correction in grammarResults.corrections" :key="correction" class="improved-text">
                  {{ correction }}
                </div>
              </div>

              <!-- Show any other feedback -->
              <div v-if="grammarResults.feedback" class="result-section">
                <h3>Feedback</h3>
                <div class="improved-text">{{ grammarResults.feedback }}</div>
              </div>

              <!-- Vocabulary Suggestions Button -->
              <div class="form-group" style="margin-top: 20px;">
                <button class="btn" @click="getVocabSuggestions" :disabled="loading || !grammarInput.trim()">
                  <span v-if="loading" class="spinner"></span>
                  {{ loading ? 'Loading...' : 'Get Vocabulary Suggestions' }}
                </button>
              </div>

              <!-- Vocabulary Results - Fixed to use grammarResults -->
              <div
                v-if="grammarResults && grammarResults.vocabulary_suggestions && grammarResults.vocabulary_suggestions.length > 0"
                class="result-section">
                <h3>Vocabulary Enhancements</h3>
                <div v-for="suggestion in grammarResults.vocabulary_suggestions" :key="suggestion.original"
                  class="vocab-suggestion">
                  <strong>"{{ suggestion.original }}"</strong> could be replaced with:
                  <div class="vocab-alternatives">
                    <span v-for="alt in suggestion.alternatives" :key="alt" class="vocab-alt">
                      {{ alt }}
                    </span>
                  </div>
                </div>
                <div class="success" v-if="grammarResults.tip">
                   {{ grammarResults.tip }}
                </div>
              </div>

              <div
                v-else-if="grammarResults && grammarResults.vocabulary_suggestions && grammarResults.vocabulary_suggestions.length === 0"
                class="success">
                Your vocabulary looks good! No obvious improvements needed.
              </div>
            </div>
          </div>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="error" style="margin-top: 20px;">
          {{ error }}
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/plugins/axios';
import { clearAuthData } from '@/utils/auth';

const router = useRouter();

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

const activeTab = ref('sentence');
const loading = ref(false);
const error = ref(null);

// Sentence Improver
const sentenceInput = ref('');
const sentenceResults = ref(null);

// Writing Analyzer
const writingInput = ref('');
const writingType = ref('general');
const writingResults = ref(null);

// Speaking Practice
const skillLevel = ref('intermediate');
const focusArea = ref('general');
const speakingResults = ref(null);

// Grammar Check
const grammarInput = ref('');
const grammarResults = ref(null);

const logout = () => {
  clearAuthData();
  router.push('/');
};

onMounted(() => {
  // Set example sentence on load
  sentenceInput.value = '';
});

const improveSentence = async () => {
  if (!sentenceInput.value.trim()) return;

  loading.value = true;
  error.value = null;
  sentenceResults.value = null;

  try {
    const response = await api.post('/api/child/improve-sentence', {
      sentence: sentenceInput.value,
    });

    sentenceResults.value = response.data;
    console.log('Sentence results:', sentenceResults.value);
  } catch (err) {
    console.error('Error improving sentence:', err);
    error.value = err.response?.data?.error || 'An error occurred while improving the sentence.';
  } finally {
    loading.value = false;
  }
};

const analyzeWriting = async () => {
  if (!writingInput.value.trim()) return;

  loading.value = true;
  error.value = null;
  writingResults.value = null;

  try {
    const response = await api.post('/api/child/analyze-writing', {
      text: writingInput.value,
      type: writingType.value,
    });

    writingResults.value = response.data;
    console.log('Writing results:', writingResults.value);
  } catch (err) {
    console.error('Error analyzing writing:', err);
    error.value = err.response?.data?.error || 'An error occurred while analyzing the writing.';
  } finally {
    loading.value = false;
  }
};

const getSpeakingPractice = async () => {
  loading.value = true;
  error.value = null;
  speakingResults.value = null;

  try {
    const response = await api.post('/api/story-starter', {
      level: skillLevel.value,
      focus: focusArea.value,
    });

    speakingResults.value = response.data;
    console.log('Speaking results:', speakingResults.value);
  } catch (err) {
    console.error('Error getting speaking exercises:', err);
    error.value = err.response?.data?.error || 'An error occurred while getting speaking exercises.';
  } finally {
    loading.value = false;
  }
};

const checkGrammar = async () => {
  if (!grammarInput.value.trim()) return;

  loading.value = true;
  error.value = null;
  grammarResults.value = null;

  try {
    const response = await api.post('/api/child/grammar-check', {
      text: grammarInput.value,
    });

    grammarResults.value = response.data;
    console.log('Grammar results:', grammarResults.value);
    console.log('Grammar results keys:', Object.keys(grammarResults.value));
  } catch (err) {
    console.error('Error checking grammar:', err);
    error.value = err.response?.data?.error || 'An error occurred while checking grammar.';
  } finally {
    loading.value = false;
  }
};

const getVocabSuggestions = async () => {
  if (!grammarInput.value.trim()) return;

  loading.value = true;
  error.value = null;

  try {
    const response = await api.post('/api/child/vocabulary-suggestions', {
      text: grammarInput.value,
    });

    if (grammarResults.value) {
      grammarResults.value = {
        ...grammarResults.value,
        vocabulary_suggestions: response.data.vocabulary_suggestions,
        tip: response.data.tip,
      };
    } else {
      grammarResults.value = response.data;
    }

    console.log('Updated grammar results with vocabulary:', grammarResults.value);
  } catch (err) {
    console.error('Error getting vocabulary suggestions:', err);
    error.value = err.response?.data?.error || 'An error occurred while getting vocabulary suggestions.';
  } finally {
    loading.value = false;
  }
};

const formatAIResponse = (text) => {
  if (!text) return '';

  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/#{1,6}\s*(.*?)$/gm, '<strong>$1</strong>');
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap');

.tabs {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 1.5rem;
}

.tab {
  padding: 1rem 1.5rem;
  cursor: pointer;
  background-color: transparent;
  border: none;
  font-weight: 500;
  color: #6b7280;
  transition: color 0.2s ease-in-out, border-bottom-color 0.2s ease-in-out;
}

.tab.active {
  color: #3b82f6;
  border-bottom: 2px solid #3b82f6;
}

.tab-content {
  padding-top: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.form-control:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 1rem;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background-color 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn:hover {
  background-color: #3a7ce6;
  cursor: pointer;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.results {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f9fafb;
  border-radius: 1rem;
}

.result-section {
  margin-bottom: 1.5rem;
}

.result-section h3 {
  color: #374151;
  margin-bottom: 0.75rem;
  font-size: 1.125rem;
  font-weight: 600;
}

.improved-text {
  background-color: #f0f1f3;
  padding: 1rem;
  border-radius: 1rem;
  margin: 0.5rem 0;
  white-space: pre-wrap;
}

.issues-list,
.tips-list {
  list-style: none;
  padding: 0;
}

.issues-list li,
.tips-list li {
  background-color: white;
  margin: 0.5rem 0;
  padding: 0.75rem 1rem;
  border-radius: 1rem;
  border-left: 4px solid #f59e0b;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.tips-list li {
  border-left-color: #10b981;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background-color: white;
  border-radius: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #3b82f6;
}

.stat-label {
  color: #6b7280;
  margin-top: 0.25rem;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.error {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #ef4444;
  margin: 0.5rem 0;
}

.success {
  background-color: #d1fae5;
  color: #065f46;
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid #10b981;
  margin: 0.5rem 0;
}

.exercise-card {
  background-color: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #10b981;
}

.exercise-title {
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.75rem;
}

.select-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.vocab-suggestion {
  background-color: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  margin: 1rem 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #3b82f6;
}

.vocab-alternatives {
  margin-top: 0.5rem;
}

.vocab-alt {
  background-color: #ede9fe;
  padding: 0.25rem 0.5rem;
  margin: 0.125rem;
  border-radius: 9999px;
  display: inline-block;
  font-size: 0.875rem;
}
.font-playfair {
  font-family: 'Playfair Display', serif;
}
</style>
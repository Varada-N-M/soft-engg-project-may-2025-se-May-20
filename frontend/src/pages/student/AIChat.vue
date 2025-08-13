<template>
  <div class="ai-chat-container">
    <div class="container">
      <div class="header">
        <h1>✨ Communication Helper</h1>
        <p>Improve your writing and speaking skills with AI-powered suggestions</p>
      </div>

      <div class="main-content">
        <div class="tabs">
          <button 
            class="tab" 
            :class="{active: activeTab === 'sentence'}" 
            @click="activeTab = 'sentence'"
          >
            Sentence Improver
          </button>
          <button 
            class="tab" 
            :class="{active: activeTab === 'writing'}" 
            @click="activeTab = 'writing'"
          >
            Writing Analyzer
          </button>
          <button 
            class="tab" 
            :class="{active: activeTab === 'grammar'}" 
            @click="activeTab = 'grammar'"
          >
            Grammar Check
          </button>
        </div>

        <!-- Sentence Improver Tab -->
        <div v-show="activeTab === 'sentence'" class="tab-content">
          <div class="form-group">
            <label for="sentence-input">Enter your sentence:</label>
            <textarea 
              id="sentence-input"
              v-model="sentenceInput" 
              class="form-control" 
              rows="3" 
              placeholder="Example: Yesterday I told her that I have had to go home"
            ></textarea>
          </div>
          <button 
            class="btn" 
            @click="improveSentence" 
            :disabled="loading || !sentenceInput.trim()"
          >
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Analyzing...' : 'Improve Sentence' }}
          </button>

          <div v-if="sentenceResults" class="results">
            <div class="result-section">
              <h3>📝 AI Improved Version</h3>
              <div class="improved-text" v-html="formatAIResponse(sentenceResults.ai_improvement)"></div>
            </div>

            <div v-if="sentenceResults.issues && sentenceResults.issues.length > 0" class="result-section">
              <h3>⚠️ Issues Found</h3>
              <ul class="issues-list">
                <li v-for="issue in sentenceResults.issues" :key="issue">{{ issue }}</li>
              </ul>
            </div>

            <div v-if="sentenceResults.suggestions && sentenceResults.suggestions.length > 0" class="result-section">
              <h3>💡 Suggestions</h3>
              <ul class="tips-list">
                <li v-for="suggestion in sentenceResults.suggestions" :key="suggestion">{{ suggestion }}</li>
              </ul>
            </div>

            <div v-if="sentenceResults.speaking_tips && sentenceResults.speaking_tips.length > 0" class="result-section">
              <h3>🎤 Speaking Tips</h3>
              <ul class="tips-list">
                <li v-for="tip in sentenceResults.speaking_tips" :key="tip">{{ tip }}</li>
              </ul>
            </div>

            <div class="result-section">
              <h3>📊 Analysis</h3>
              <div class="stats">
                <div class="stat-item">
                  <div class="stat-number">{{ sentenceResults.word_count || 0 }}</div>
                  <div class="stat-label">Words</div>
                </div>
              </div>
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
            <textarea 
              id="writing-input"
              v-model="writingInput" 
              class="form-control" 
              rows="8" 
              placeholder="Paste your story, essay, or any longer text here..."
            ></textarea>
          </div>
          <button 
            class="btn" 
            @click="analyzeWriting" 
            :disabled="loading || !writingInput.trim()"
          >
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
              <h3>🤖 AI Feedback</h3>
              <div class="improved-text" v-html="formatAIResponse(writingResults.ai_feedback)"></div>
            </div>

            <div v-if="writingResults.analysis?.issues && writingResults.analysis.issues.length > 0" class="result-section">
              <h3>⚠️ Issues to Address</h3>
              <ul class="issues-list">
                <li v-for="issue in writingResults.analysis.issues.slice(0, 5)" :key="issue">{{ issue }}</li>
              </ul>
            </div>

            <div v-if="writingResults.analysis?.suggestions && writingResults.analysis.suggestions.length > 0" class="result-section">
              <h3>💡 Suggestions</h3>
              <ul class="tips-list">
                <li v-for="suggestion in writingResults.analysis.suggestions.slice(0, 5)" :key="suggestion">{{ suggestion }}</li>
              </ul>
            </div>

            <div v-if="writingResults.speaking_tips && writingResults.speaking_tips.length > 0" class="result-section">
              <h3>🎤 Speaking Tips</h3>
              <ul class="tips-list">
                <li v-for="tip in writingResults.speaking_tips.slice(0, 4)" :key="tip">{{ tip }}</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Speaking Practice Tab -->
        <div v-show="activeTab === 'speaking'" class="tab-content">
          <div class="select-group">
            <div class="form-group">
              <label for="skill-level">Skill Level:</label>
              <select id="skill-level" v-model="skillLevel" class="form-control">
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div class="form-group">
              <label for="focus-area">Focus Area:</label>
              <select id="focus-area" v-model="focusArea" class="form-control">
                <option value="general">General</option>
                <option value="pronunciation">Pronunciation</option>
                <option value="fluency">Fluency</option>
                <option value="presentation">Presentation</option>
                <option value="conversation">Conversation</option>
              </select>
            </div>
          </div>
          <button class="btn" @click="getSpeakingPractice" :disabled="loading">
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Loading...' : 'Get Speaking Exercises' }}
          </button>

          <div v-if="speakingResults" class="results">
            <div class="result-section">
              <h3>🎯 Your Focus: {{ speakingResults.focus_area }}</h3>
              <p><strong>Level:</strong> {{ speakingResults.level }} | <strong>Duration:</strong> {{ speakingResults.practice_duration }}</p>
            </div>

            <div v-if="speakingResults.exercises && speakingResults.exercises.length > 0" class="result-section">
              <h3>🏃‍♂️ Practice Exercises</h3>
              <div v-for="(exercise, index) in speakingResults.exercises" :key="index" class="exercise-card">
                <div class="exercise-title">Exercise {{ index + 1 }}</div>
                <div>{{ exercise }}</div>
              </div>
            </div>

            <div v-if="speakingResults.tips && speakingResults.tips.length > 0" class="result-section">
              <h3>💡 Speaking Tips</h3>
              <ul class="tips-list">
                <li v-for="tip in speakingResults.tips" :key="tip">{{ tip }}</li>
              </ul>
            </div>
          </div>
        </div>


        <!-- Grammar Check Tab -->
        <div v-show="activeTab === 'grammar'" class="tab-content">
          <div class="form-group">
            <label for="grammar-input">Text to check:</label>
            <textarea 
              id="grammar-input"
              v-model="grammarInput" 
              class="form-control" 
              rows="4" 
              placeholder="Enter text to check for basic grammar issues..."
            ></textarea>
          </div>
          <button 
            class="btn" 
            @click="checkGrammar" 
            :disabled="loading || !grammarInput.trim()"
          >
            <span v-if="loading" class="spinner"></span>
            {{ loading ? 'Checking...' : 'Check Grammar' }}

          </button>

          <div v-if="grammarResults" class="results">
            <!-- Show AI improved text if available -->
            <div v-if="grammarResults.ai_improved_text" class="result-section">
              <h3>✏️ AI Improved Version</h3>
              <div class="improved-text">{{ grammarResults.ai_improved_text }}</div>
            </div>

            <!-- Show grammar status -->
            <div v-if="grammarResults.is_correct" class="success">
              ✅ Great! No major grammar issues found.
            </div>
            
            <!-- Show grammar issues if any -->
            <div v-if="grammarResults.issues && grammarResults.issues.length > 0" class="result-section">
              <h3>⚠️ Grammar Issues</h3>
              <ul class="issues-list">
                <li v-for="issue in grammarResults.issues" :key="issue">{{ issue }}</li>
              </ul>
            </div>

            <!-- Show corrections if any -->
            <div v-if="grammarResults.corrections && grammarResults.corrections.length > 0" class="result-section">
              <h3>✏️ Suggested Corrections</h3>
              <div v-for="correction in grammarResults.corrections" :key="correction" class="improved-text">
                {{ correction }}
              </div>
            </div>

            <!-- Show any other feedback -->
            <div v-if="grammarResults.feedback" class="result-section">
              <h3>💭 Feedback</h3>
              <div class="improved-text">{{ grammarResults.feedback }}</div>
            </div>

            <!-- Vocabulary Suggestions Button -->
            <div class="form-group" style="margin-top: 20px;">
              <button 
                class="btn" 
                @click="getVocabSuggestions" 
                :disabled="loading || !grammarInput.trim()"
              >
                <span v-if="loading" class="spinner"></span>
                {{ loading ? 'Loading...' : 'Get Vocabulary Suggestions' }}
              </button>
            </div>

            <!-- Vocabulary Results - Fixed to use grammarResults -->
            <div v-if="grammarResults && grammarResults.vocabulary_suggestions && grammarResults.vocabulary_suggestions.length > 0" class="result-section">
              <h3>📚 Vocabulary Enhancements</h3>
              <div v-for="suggestion in grammarResults.vocabulary_suggestions" :key="suggestion.original" class="vocab-suggestion">
                <strong>"{{ suggestion.original }}"</strong> could be replaced with:
                <div class="vocab-alternatives">
                  <span v-for="alt in suggestion.alternatives" :key="alt" class="vocab-alt">
                    {{ alt }}
                  </span>
                </div>
              </div>
              <div class="success" v-if="grammarResults.tip">
                💡 {{ grammarResults.tip }}
              </div>
            </div>
            
            <div v-else-if="grammarResults && grammarResults.vocabulary_suggestions && grammarResults.vocabulary_suggestions.length === 0" class="success">
              ✅ Your vocabulary looks good! No obvious improvements needed.
            </div>
          </div>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="error" style="margin-top: 20px;">
        ❌ {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/plugins/axios'

export default {
  name: 'AIChat',
  
  data() {
    return {
      activeTab: 'sentence',
      loading: false,
      error: null,
      
      // Sentence Improver
      sentenceInput: '',
      sentenceResults: null,
      
      // Writing Analyzer
      writingInput: '',
      writingType: 'general',
      writingResults: null,
      
      // Speaking Practice
      skillLevel: 'intermediate',
      focusArea: 'general',
      speakingResults: null,
      
      // Grammar Check
      grammarInput: '',
      grammarResults: null
      // Removed vocabResults since we're merging into grammarResults
    }
  },
  
  mounted() {
    // Set example sentence on load
    this.sentenceInput = 'Yesterday I told her that I have had to go home'
  },
  
  methods: {
    async improveSentence() {
      if (!this.sentenceInput.trim()) return
      
      this.loading = true
      this.error = null
      this.sentenceResults = null
      
      try {
        const response = await api.post('/api/child/improve-sentence', {
          sentence: this.sentenceInput
        })
        
        this.sentenceResults = response.data
        console.log('Sentence results:', this.sentenceResults)
      } catch (err) {
        console.error('Error improving sentence:', err)
        this.error = err.response?.data?.error || 'An error occurred while improving the sentence.'
      } finally {
        this.loading = false
      }
    },
    
    async analyzeWriting() {
      if (!this.writingInput.trim()) return
      
      this.loading = true
      this.error = null
      this.writingResults = null
      
      try {
        const response = await api.post('/api/child/analyze-writing', {
          text: this.writingInput,
          type: this.writingType
        })
        
        this.writingResults = response.data
        console.log('Writing results:', this.writingResults)
      } catch (err) {
        console.error('Error analyzing writing:', err)
        this.error = err.response?.data?.error || 'An error occurred while analyzing the writing.'
      } finally {
        this.loading = false
      }
    },
    
    async getSpeakingPractice() {
      this.loading = true
      this.error = null
      this.speakingResults = null
      
      try {
        const response = await api.post('/api/story-starter', {
          level: this.skillLevel,
          focus: this.focusArea
        })
        
        this.speakingResults = response.data
        console.log('Speaking results:', this.speakingResults)
      } catch (err) {
        console.error('Error getting speaking exercises:', err)
        this.error = err.response?.data?.error || 'An error occurred while getting speaking exercises.'
      } finally {
        this.loading = false
      }
    },
    
    async checkGrammar() {
      if (!this.grammarInput.trim()) return
      
      this.loading = true
      this.error = null
      this.grammarResults = null
      
      try {
        const response = await api.post('/api/child/grammar-check', {
          text: this.grammarInput
        })
        
        this.grammarResults = response.data
        console.log('Grammar results:', this.grammarResults)
        console.log('Grammar results keys:', Object.keys(this.grammarResults))
      } catch (err) {
        console.error('Error checking grammar:', err)
        this.error = err.response?.data?.error || 'An error occurred while checking grammar.'
      } finally {
        this.loading = false
      }
    },
    
    // Fixed getVocabSuggestions method
    async getVocabSuggestions() {
      if (!this.grammarInput.trim()) return
      
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/api/child/vocabulary-suggestions', {
          text: this.grammarInput
        })
        
        // Fix: Merge vocabulary data into existing grammarResults
        if (this.grammarResults) {
          this.grammarResults = {
            ...this.grammarResults,
            vocabulary_suggestions: response.data.vocabulary_suggestions,
            tip: response.data.tip
          }
        } else {
          // If no grammar results exist, create them
          this.grammarResults = response.data
        }
        
        console.log('Updated grammar results with vocabulary:', this.grammarResults)
      } catch (err) {
        console.error('Error getting vocabulary suggestions:', err)
        this.error = err.response?.data?.error || 'An error occurred while getting vocabulary suggestions.'
      } finally {
        this.loading = false
      }
    },
    
    formatAIResponse(text) {
      if (!text) return ''
      
      // Simple formatting for better readability
      return text
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/#{1,6}\s*(.*?)$/gm, '<strong>$1</strong>')
    }
  }
}
</script>

<style scoped>
.ai-chat-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.main-content {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  overflow: hidden;
}

.tabs {
  display: flex;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.tab {
  flex: 1;
  padding: 20px;
  text-align: center;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 500;
}

.tab.active {
  background: white;
  border-bottom: 3px solid #667eea;
  color: #667eea;
}

.tab:hover {
  background: #e9ecef;
}

.tab-content {
  padding: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #495057;
}

.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  resize: vertical;
}

.form-control:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.btn {
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.results {
  margin-top: 30px;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 15px;
  border-left: 5px solid #667eea;
}

.result-section {
  margin-bottom: 20px;
}

.result-section h3 {
  color: #495057;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.improved-text {
  background: #d4edda;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #28a745;
  margin: 10px 0;
  font-style: italic;
  white-space: pre-wrap;
}

.issues-list, .tips-list {
  list-style: none;
  padding: 0;
}

.issues-list li, .tips-list li {
  background: white;
  margin: 8px 0;
  padding: 12px 15px;
  border-radius: 8px;
  border-left: 4px solid #ffc107;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.tips-list li {
  border-left-color: #17a2b8;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin: 20px 0;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #667eea;
}

.stat-label {
  color: #6c757d;
  margin-top: 5px;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #dc3545;
  margin: 10px 0;
}

.success {
  background: #d1ecf1;
  color: #0c5460;
  padding: 15px;
  border-radius: 10px;
  border-left: 4px solid #17a2b8;
  margin: 10px 0;
}

.exercise-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  margin: 15px 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-left: 4px solid #28a745;
}

.exercise-title {
  font-weight: 600;
  color: #495057;
  margin-bottom: 10px;
}

.select-group {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.vocab-suggestion {
  background: white;
  border-radius: 10px;
  padding: 20px;
  margin: 15px 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  border-left: 4px solid #6f42c1;
}

.vocab-alternatives {
  margin-top: 8px;
}

.vocab-alt {
  background: #e3f2fd;
  padding: 4px 8px;
  margin: 2px;
  border-radius: 15px;
  display: inline-block;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  .tabs {
    flex-wrap: wrap;
  }
  
  .tab {
    flex: 1 1 50%;
    min-width: 120px;
  }
  
  .tab-content {
    padding: 20px;
  }
  
  .select-group {
    grid-template-columns: 1fr;
  }
  
  .header h1 {
    font-size: 2rem;
  }

  .stats {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
}
</style>
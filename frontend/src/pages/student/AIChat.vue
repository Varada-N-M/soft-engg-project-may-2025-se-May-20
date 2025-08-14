<template>
  <div class="ai-chat-container">
    <div class="container">
      <div class="header">
        <h1>✨ Communication Helper</h1>
        <p>Improve your writing skills with AI-powered suggestions</p>
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

            <div v-if="sentenceResults.encouragement" class="success">
              ✨ {{ sentenceResults.encouragement }}
            </div>

            <div v-if="sentenceResults.fun_fact" class="result-section">
              <h3>🧠 Fun Fact</h3>
              <div class="improved-text">{{ sentenceResults.fun_fact }}</div>
            </div>
          </div>
        </div>

        <!-- Writing Analyzer Tab -->
        <div v-show="activeTab === 'writing'" class="tab-content">
          <div class="form-group">
            <label for="writing-type">Writing Type:</label>
            <select id="writing-type" v-model="writingType" class="form-control">
              <option value="story">Story</option>
              <option value="essay">Essay</option>
              <option value="general">General</option>
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
            <div class="result-section">
              <h3>🤖 AI Feedback</h3>
              <div class="improved-text" v-html="formatAIResponse(writingResults.ai_feedback)"></div>
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
            <div v-if="grammarResults.is_perfect" class="success">
              ✅ {{ grammarResults.overall_feedback }}
            </div>
            
            <!-- Show grammar score -->
            <!-- <div v-if="grammarResults.grammar_score" class="result-section">
              <h3>📊 Grammar Score</h3>
              <div class="grammar-score">
                <div class="score-number">{{ grammarResults.grammar_score }}/100</div>
                <div class="score-feedback">{{ grammarResults.overall_feedback }}</div>
              </div>
            </div> -->

            <!-- Show AI feedback -->
            <div v-if="grammarResults.ai_feedback" class="result-section">
              <h3>🤖 AI Grammar Helper</h3>
              <div class="improved-text" v-html="formatAIResponse(grammarResults.ai_feedback)"></div>
            </div>

            <!-- Show fun grammar tips -->
            <div v-if="grammarResults.fun_grammar_tips && grammarResults.fun_grammar_tips.length > 0" class="result-section">
              <h3>💡 Fun Grammar Tips</h3>
              <ul class="tips-list">
                <li v-for="tip in grammarResults.fun_grammar_tips.slice(0, 3)" :key="tip">{{ tip }}</li>
              </ul>
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

            <!-- Vocabulary Results -->
            <div v-if="grammarResults && grammarResults.vocabulary_suggestions && grammarResults.vocabulary_suggestions.length > 0" class="result-section">
              <h3>📚 Vocabulary Enhancements</h3>
              <div v-for="suggestion in grammarResults.vocabulary_suggestions" :key="suggestion.original" class="vocab-suggestion">
                <strong>"{{ suggestion.original }}"</strong> could be replaced with:
                <div class="vocab-alternatives">
                  <span v-for="(alt, index) in suggestion.alternatives" :key="alt" class="vocab-alt">
                    {{ alt }}<span v-if="index < suggestion.alternatives.length - 1">, </span>
                  </span>

                </div>
              </div>
              <div class="success" v-if="grammarResults.vocab_tip">
                💡 {{ grammarResults.vocab_tip }}
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
      writingType: 'story',
      writingResults: null,
      
      // Grammar Check
      grammarInput: '',
      grammarResults: null
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
    
    async getVocabSuggestions() {
      if (!this.grammarInput.trim()) return
      
      this.loading = true
      this.error = null
      
      try {
        const response = await api.post('/api/child/vocabulary-suggestions', {
          text: this.grammarInput
        })
        
        // Merge vocabulary data into existing grammarResults
        if (this.grammarResults) {
          this.grammarResults = {
            ...this.grammarResults,
            vocabulary_suggestions: response.data.vocabulary_suggestions,
            vocab_tip: response.data.tip,
            vocab_encouragement: response.data.encouragement,
            vocab_fun_fact: response.data.fun_fact
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

.grammar-score {
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.score-number {
  font-size: 3rem;
  font-weight: bold;
  color: #667eea;
  margin-bottom: 10px;
}

.score-feedback {
  color: #6c757d;
  font-size: 1.1rem;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 15px 0;
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
  
  .header h1 {
    font-size: 2rem;
  }
}
</style>
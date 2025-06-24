<template>
  <div class="todo-container">
    <!-- Fun Header with Rainbow Background -->
    <div class="header">
      <div class="header-content">
        <h1 class="main-title">🌟 My Super Cool Tasks! 🌟</h1>
        <div class="stats-display" v-if="stats">
          <div class="stat-badge">📊 Total: {{ stats.total }}</div>
          <div class="stat-badge">✅ Done: {{ stats.completed }}</div>
          <div class="stat-badge">⏳ Pending: {{ stats.pending }}</div>
          <div class="stat-badge">🔄 Daily: {{ stats.daily_tasks }}</div>
        </div>
      </div>
    </div>

    <!-- Super Fun Todo Creation Form -->
    <div class="todo-form-card">
      <h2 class="form-title">✨ Create a New Adventure Task! ✨</h2>
      <form @submit.prevent="createTodo" class="todo-form">
        <div class="form-group">
          <label for="todoTitle" class="fun-label">🎯 What's your mission?</label>
          <input
            id="todoTitle"
            v-model="newTodo.to_do"
            type="text"
            class="form-input fun-input"
            placeholder="Enter your awesome task here! 🚀"
            required
          />
        </div>

        <div class="form-group">
          <label for="todoDescription" class="fun-label">📝 Tell me more about it!</label>
          <textarea
            id="todoDescription"
            v-model="newTodo.description"
            class="form-textarea fun-input"
            placeholder="Describe your super cool task... 🌈"
            rows="3"
            required
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="dueDate" class="fun-label">⏰ When should this be done?</label>
            <input
              id="dueDate"
              v-model="newTodo.due_date"
              type="datetime-local"
              class="form-input fun-input"
            />
          </div>
        </div>

        <div class="form-options">
          <label class="checkbox-label fun-checkbox">
            <input
              v-model="newTodo.is_daily"
              type="checkbox"
              class="form-checkbox"
            />
            <span class="checkmark rainbow-check"></span>
            <span class="checkbox-text">🔄 Daily Super Task!</span>
          </label>
        </div>

        <button
          type="submit"
          class="btn btn-rainbow btn-full btn-big"
          :disabled="isCreating || !newTodo.to_do.trim() || !newTodo.description.trim()"
        >
          {{ isCreating ? '🎨 Creating Magic...' : '🎉 Create My Task!' }}
        </button>
      </form>
    </div>

    <!-- Colorful Filters -->
    <div class="filters">
      <div class="filter-group">
        <label class="filter-label">🎭 Show me:</label>
        <select v-model="filters.is_done" @change="fetchTodos" class="filter-select fun-select">
          <option value="">🌈 All Tasks</option>
          <option value="false">⏳ To Do</option>
          <option value="true">✅ Completed</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label">🔄 Task Type:</label>
        <select v-model="filters.is_daily" @change="fetchTodos" class="filter-select fun-select">
          <option value="">🎪 All Types</option>
          <option value="true">🔄 Daily Tasks</option>
          <option value="false">⭐ Special Tasks</option>
        </select>
      </div>

      <div class="filter-group">
        <label class="filter-label">📅 Pick a Date:</label>
        <div class="date-filter-group">
          <input
            v-model="filters.date"
            @change="fetchTodos"
            type="date"
            class="filter-input fun-input"
          />
          <button @click="clearDateFilter" class="btn btn-sm btn-purple">🗑️ Clear</button>
        </div>
      </div>
    </div>

    <!-- Fun Bulk Actions -->
    <div class="bulk-actions" v-if="selectedTodos.length > 0">
      <div class="bulk-info">
        <span class="selected-count">🎯 {{ selectedTodos.length }} tasks selected!</span>
      </div>
      <div class="bulk-buttons">
        <button @click="bulkComplete" class="btn btn-sm btn-green">✅ Mark Complete</button>
        <button @click="bulkDelete" class="btn btn-sm btn-red">🗑️ Delete</button>
        <button @click="clearSelection" class="btn btn-sm btn-gray">❌ Clear Selection</button>
      </div>
    </div>

    <!-- Loading with Fun Animation -->
    <div v-if="loading" class="loading">
      <div class="loading-spinner">🌟</div>
      <p class="loading-text">Loading your awesome tasks...</p>
    </div>

    <!-- Colorful Messages -->
    <div v-if="error" class="error-message">
      <span>😱 Oops! {{ error }}</span>
      <button @click="error = ''" class="close-btn">❌</button>
    </div>

    <div v-if="successMessage" class="success-message">
      <span>🎉 Yay! {{ successMessage }}</span>
      <button @click="successMessage = ''" class="close-btn">✅</button>
    </div>

    <!-- Super Cool Todo List -->
    <div class="todo-list">
      <div v-if="todos.length === 0 && !loading" class="empty-state">
        <div class="empty-icon">🌱</div>
        <h3 class="empty-title">No tasks yet!</h3>
        <p class="empty-text">Create your first awesome task above! 🚀</p>
      </div>

      <div
        v-for="todo in todos"
        :key="todo.list_id"
        class="todo-item"
        :class="{ 
          'completed': todo.is_done, 
          'daily-task': todo.is_daily,
          'todo-pink': todo.list_id % 4 === 0,
          'todo-blue': todo.list_id % 4 === 1,
          'todo-green': todo.list_id % 4 === 2,
          'todo-purple': todo.list_id % 4 === 3
        }"
      >
        <div class="todo-content">
          <label class="checkbox-label fun-checkbox">
            <input
              v-model="selectedTodos"
              :value="todo.list_id"
              type="checkbox"
              class="form-checkbox"
            />
            <span class="checkmark rainbow-check"></span>
          </label>

          <div class="todo-details">
            <h3 class="todo-title">
              <span class="todo-emoji">{{ todo.is_daily ? '🔄' : '⭐' }}</span>
              {{ todo.to_do }}
            </h3>
            <p class="todo-description">{{ todo.description }}</p>
            <div class="todo-meta">
              <span class="todo-date">📅 Created: {{ formatDate(todo.created_at) }}</span>
              <span v-if="todo.completion_date" class="completion-date">
                ✅ Completed: {{ formatDate(todo.completion_date) }}
              </span>
              <span v-if="todo.is_daily" class="daily-badge">🔄 Daily</span>
            </div>
          </div>
        </div>

        <div class="todo-actions">
          <button
            @click="toggleComplete(todo)"
            class="btn btn-sm action-btn"
            :class="todo.is_done ? 'btn-orange' : 'btn-green'"
          >
            {{ todo.is_done ? '↩️ Undo' : '✅ Done!' }}
          </button>
          <button @click="editTodo(todo)" class="btn btn-sm btn-blue action-btn">✏️ Edit</button>
          <button @click="deleteTodo(todo.list_id)" class="btn btn-sm btn-red action-btn">🗑️ Delete</button>
        </div>
      </div>
    </div>

    <!-- Fun Edit Modal -->
    <div v-if="editingTodo" class="modal-overlay" @click="cancelEdit">
      <div class="modal-content fun-modal" @click.stop>
        <h3 class="modal-title">✏️ Edit Your Awesome Task! ✏️</h3>
        <form @submit.prevent="updateTodo" class="edit-form">
          <div class="form-group">
            <label class="fun-label">🎯 Task Title</label>
            <input
              v-model="editForm.to_do"
              type="text"
              class="form-input fun-input"
              required
            />
          </div>

          <div class="form-group">
            <label class="fun-label">📝 Description</label>
            <textarea
              v-model="editForm.description"
              class="form-textarea fun-input"
              rows="3"
              required
            ></textarea>
          </div>

          <div class="form-options">
            <label class="checkbox-label fun-checkbox">
              <input
                v-model="editForm.is_daily"
                type="checkbox"
                class="form-checkbox"
              />
              <span class="checkmark rainbow-check"></span>
              <span class="checkbox-text">🔄 Daily Task</span>
            </label>

            <label class="checkbox-label fun-checkbox">
              <input
                v-model="editForm.is_done"
                type="checkbox"
                class="form-checkbox"
              />
              <span class="checkmark rainbow-check"></span>
              <span class="checkbox-text">✅ Completed</span>
            </label>
          </div>

          <div class="modal-actions">
            <button type="submit" class="btn btn-rainbow" :disabled="isUpdating">
              {{ isUpdating ? '🎨 Updating...' : '💾 Save Changes!' }}
            </button>
            <button type="button" @click="cancelEdit" class="btn btn-gray">❌ Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, reactive, ref } from 'vue'

export default {
  name: 'TodoList',
  setup() {
    // Reactive state
    const todos = ref([])
    const stats = ref(null)
    const loading = ref(false)
    const error = ref('')
    const successMessage = ref('')
    const isCreating = ref(false)
    const isUpdating = ref(false)
    const selectedTodos = ref([])
    const editingTodo = ref(null)

    // Forms
    const newTodo = reactive({
      to_do: '',
      description: '',
      is_daily: false,
      due_date: ''
    })

    const editForm = reactive({
      list_id: null,
      to_do: '',
      description: '',
      is_daily: false,
      is_done: false
    })

    const filters = reactive({
      is_done: '',
      is_daily: '',
      date: ''
    })

    // API configuration
    const API_BASE = '/api'
    const getAuthHeaders = () => ({
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
      'Content-Type': 'application/json'
    })

    // Utility functions
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleString()
    }

    const showError = (message) => {
      error.value = message
      setTimeout(() => error.value = '', 5000)
    }

    const showSuccess = (message) => {
      successMessage.value = message
      setTimeout(() => successMessage.value = '', 3000)
    }

    const formatDateForAPI = (date) => {
      if (!date) return ''
      const d = new Date(date)
      return d.getFullYear() + '-' + 
             String(d.getMonth() + 1).padStart(2, '0') + '-' + 
             String(d.getDate()).padStart(2, '0')
    }

    // API calls
    const fetchStats = async () => {
      try {
        const response = await fetch(`${API_BASE}/todos/stats`, {
          headers: getAuthHeaders()
        })
        
        if (response.ok) {
          stats.value = await response.json()
        }
      } catch (err) {
        console.error('Failed to fetch stats:', err)
      }
    }

    const fetchTodos = async () => {
      loading.value = true
      try {
        const params = new URLSearchParams()
        if (filters.is_done !== '') params.append('is_done', filters.is_done)
        if (filters.is_daily !== '') params.append('is_daily', filters.is_daily)
        if (filters.date) params.append('date', formatDateForAPI(filters.date))

        const response = await fetch(`${API_BASE}/todos?${params}`, {
          headers: getAuthHeaders()
        })

        if (response.ok) {
          const data = await response.json()
          todos.value = data.todos || data
          // Fetch stats after getting todos
          await fetchStats()
        } else {
          const errorData = await response.json()
          showError(errorData.error || 'Failed to fetch todos')
        }
      } catch (err) {
        showError('Network error while fetching todos')
      } finally {
        loading.value = false
      }
    }

    const createTodo = async () => {
      if (!newTodo.to_do.trim() || !newTodo.description.trim()) {
        showError('Title and description are required')
        return
      }

      isCreating.value = true
      try {
        const todoData = { ...newTodo }
        if (todoData.due_date) {
          todoData.due_date = new Date(todoData.due_date).toISOString()
        }

        const response = await fetch(`${API_BASE}/todos`, {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify(todoData)
        })

        if (response.ok) {
          const data = await response.json()
          showSuccess(data.message || 'Todo created successfully!')

          // Reset form
          Object.assign(newTodo, {
            to_do: '',
            description: '',
            is_daily: false,
            due_date: ''
          })

          // Refresh todos
          await fetchTodos()
        } else {
          const errorData = await response.json()
          showError(errorData.error || 'Failed to create todo')
        }
      } catch (err) {
        showError('Network error while creating todo')
      } finally {
        isCreating.value = false
      }
    }

    const updateTodo = async () => {
      isUpdating.value = true
      try {
        const response = await fetch(`${API_BASE}/todos`, {
          method: 'PUT',
          headers: getAuthHeaders(),
          body: JSON.stringify(editForm)
        })

        if (response.ok) {
          const data = await response.json()
          showSuccess(data.message || 'Todo updated successfully!')
          editingTodo.value = null
          await fetchTodos()
        } else {
          const errorData = await response.json()
          showError(errorData.error || 'Failed to update todo')
        }
      } catch (err) {
        showError('Network error while updating todo')
      } finally {
        isUpdating.value = false
      }
    }

    const deleteTodo = async (listId) => {
      if (!confirm('Are you sure you want to delete this task? 🤔')) return

      try {
        const response = await fetch(`${API_BASE}/todos?list_id=${listId}`, {
          method: 'DELETE',
          headers: getAuthHeaders()
        })

        if (response.ok) {
          showSuccess('Task deleted successfully! 🗑️')
          await fetchTodos()
        } else {
          const errorData = await response.json()
          showError(errorData.error || 'Failed to delete todo')
        }
      } catch (err) {
        showError('Network error while deleting todo')
      }
    }

    const toggleComplete = async (todo) => {
      try {
        const response = await fetch(`${API_BASE}/todos`, {
          method: 'PUT',
          headers: getAuthHeaders(),
          body: JSON.stringify({
            list_id: todo.list_id,
            is_done: !todo.is_done
          })
        })

        if (response.ok) {
          await fetchTodos()
        } else {
          const errorData = await response.json()
          showError(errorData.error || 'Failed to update todo')
        }
      } catch (err) {
        showError('Network error while updating todo')
      }
    }

    const bulkComplete = async () => {
      if (selectedTodos.value.length === 0) return

      try {
        const response = await fetch(`${API_BASE}/todos/bulk`, {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify({
            list_ids: selectedTodos.value,
            action: 'complete'
          })
        })

        if (response.ok) {
          const data = await response.json()
          showSuccess(data.message || 'Todos completed successfully!')
          selectedTodos.value = []
          await fetchTodos()
        } else {
          const errorData = await response.json()
          showError(errorData.error || 'Failed to complete todos')
        }
      } catch (err) {
        showError('Network error while completing todos')
      }
    }

    const bulkDelete = async () => {
      if (selectedTodos.value.length === 0) return
      if (!confirm(`Are you sure you want to delete ${selectedTodos.value.length} tasks? 🤔`)) return

      try {
        const response = await fetch(`${API_BASE}/todos/bulk`, {
          method: 'POST',
          headers: getAuthHeaders(),
          body: JSON.stringify({
            list_ids: selectedTodos.value,
            action: 'delete'
          })
        })

        if (response.ok) {
          const data = await response.json()
          showSuccess(data.message || 'Todos deleted successfully!')
          selectedTodos.value = []
          await fetchTodos()
        } else {
          const errorData = await response.json()
          showError(errorData.error || 'Failed to delete todos')
        }
      } catch (err) {
        showError('Network error while deleting todos')
      }
    }

    const editTodo = (todo) => {
      editingTodo.value = todo
      Object.assign(editForm, {
        list_id: todo.list_id,
        to_do: todo.to_do,
        description: todo.description,
        is_daily: todo.is_daily,
        is_done: todo.is_done
      })
    }

    const cancelEdit = () => {
      editingTodo.value = null
    }

    const clearSelection = () => {
      selectedTodos.value = []
    }

    const clearDateFilter = () => {
      filters.date = ''
      fetchTodos()
    }

    // Lifecycle
    onMounted(async () => {
      await fetchTodos()
    })

    return {
      // State
      todos,
      stats,
      loading,
      error,
      successMessage,
      isCreating,
      isUpdating,
      selectedTodos,
      editingTodo,
      newTodo,
      editForm,
      filters,

      // Methods
      formatDate,
      fetchTodos,
      createTodo,
      updateTodo,
      deleteTodo,
      toggleComplete,
      bulkComplete,
      bulkDelete,
      editTodo,
      cancelEdit,
      clearSelection,
      clearDateFilter
    }
  }
}
</script>

<style scoped>
/* Base Container */
.todo-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

/* Fun Header */
.header {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 300% 300%;
  animation: rainbow 3s ease infinite;
  border-radius: 25px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

@keyframes rainbow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
}

.main-title {
  color: white;
  margin: 0;
  font-size: 2.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  font-weight: bold;
}

.stats-display {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.stat-badge {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 10px 15px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
}

/* Fun Form Card */
.todo-form-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 25px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  border: 4px solid #fff;
}

.form-title {
  margin-top: 0;
  margin-bottom: 25px;
  color: white;
  font-size: 1.8rem;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.form-group {
  margin-bottom: 25px;
}

.fun-label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: white;
  font-size: 1.1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.fun-input {
  width: 100%;
  padding: 15px 20px;
  border: 3px solid #fff;
  border-radius: 20px;
  font-size: 16px;
  font-family: inherit;
  background: rgba(255, 255, 255, 0.95);
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.fun-input:focus {
  outline: none;
  border-color: #feca57;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.form-options {
  display: flex;
  gap: 25px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.fun-checkbox {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 16px;
  color: white;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.checkbox-text {
  margin-left: 10px;
}

.rainbow-check {
  width: 25px;
  height: 25px;
  border: 3px solid #fff;
  border-radius: 8px;
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  position: relative;
  margin-right: 5px;
}

.form-checkbox {
  display: none;
}

.form-checkbox:checked + .rainbow-check::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-weight: bold;
  font-size: 16px;
}

/* Fun Buttons */
.btn {
  padding: 12px 25px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  font-family: inherit;
  transition: all 0.3s ease;
  text-align: center;
  display: inline-block;
  text-decoration: none;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-rainbow {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
  background-size: 300% 300%;
  animation: rainbow 3s ease infinite;
  color: white;
}

.btn-green {
  background: linear-gradient(45deg, #4CAF50, #8BC34A);
  color: white;
}

.btn-blue {
  background: linear-gradient(45deg, #2196F3, #03DAC6);
  color: white;
}

.btn-red {
  background: linear-gradient(45deg, #f44336, #ff9800);
  color: white;
}

.btn-orange {
  background: linear-gradient(45deg, #ff9800, #ffc107);
  color: white;
}

.btn-purple {
  background: linear-gradient(45deg, #9c27b0, #673ab7);
  color: white;
}

.btn-gray {
  background: linear-gradient(45deg, #607d8b, #9e9e9e);
  color: white;
}

.btn-sm {
  padding: 8px 16px;
  font-size: 14px;
}

.btn-full {
  width: 100%;
}

.btn-big {
  padding: 18px 35px;
  font-size: 18px;
}

/* Colorful Filters */
.filters {
  display: flex;
  gap: 25px;
  margin-bottom: 25px;
  padding: 25px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  align-items: end;
  flex-wrap: wrap;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 3px solid #fff;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #333;
  font-weight: bold;
}

.fun-select, .filter-input {
  padding: 10px 15px;
  border: 2px solid #ddd;
  border-radius: 15px;
  font-size: 14px;
  font-family: inherit;
  background: white;
  transition: all 0.3s ease;
}

.fun-select:focus, .filter-input:focus {
  outline: none;
  border-color: #4ecdc4;
  box-shadow: 0 0 10px rgba(78, 205, 196, 0.3);
}

.date-filter-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* Fun Bulk Actions */
.bulk-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 25px;
  padding: 20px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border-radius: 20px;
  color: white;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  flex-wrap: wrap;
}

.bulk-info {
  font-weight: bold;
  font-size: 16px;
}

.bulk-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* Loading Animation */
.loading {
  text-align: center;
  padding: 50px;
  color: white;
}

.loading-spinner {
  font-size: 3rem;
  animation: spin 2s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1.2rem;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* Colorful Messages */
.error-message, .success-message {
  padding: 20px 25px;
  border-radius: 20px;
  margin-bottom: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.error-message {
  background: linear-gradient(45deg, #f44336, #ff9800);
  color: white;
}

.success-message {
  background: linear-gradient(45deg, #4CAF50, #8BC34A);
  color: white;
}

.close-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 5px;
  color: inherit;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: white;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.empty-text {
  font-size: 1.1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* Colorful Todo List */
.todo-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.todo-item {
  border-radius: 20px;
  padding: 25px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.todo-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
}

.todo-pink {
  background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
}

.todo-blue {
  background: linear-gradient(135deg, #4ecdc4, #44a08d);
}

.todo-green {
  background: linear-gradient(135deg, #96ceb4, #8bc34a);
}

.todo-purple {
  background: linear-gradient(135deg, #667eea, #764ba2);
}

.todo-item.completed {
  opacity: 0.7;
  transform: scale(0.98);
}

.todo-item.daily-task {
  border-left: 8px solid #feca57;
}

.todo-content {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  flex: 1;
}

.todo-details {
  flex: 1;
}

.todo-title {
  margin: 0 0 10px 0;
  font-size: 1.3rem;
  font-weight: bold;
  color: white;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  gap: 10px;
}

.todo-emoji {
  font-size: 1.5rem;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
}

.todo-description {
  margin: 0 0 15px 0;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.6;
  font-size: 1rem;
}

.todo-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  flex-wrap: wrap;
}

.daily-badge {
  background: linear-gradient(45deg, #feca57, #ff9ff3);
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 11px;
  font-weight: bold;
}

.todo-actions {
  display: flex;
  gap: 10px;
  flex-shrink: 0;
  flex-wrap: wrap;
}

.action-btn {
  min-width: 80px;
}

/* Fun Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.fun-modal {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 25px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  border: 4px solid #fff;
}

.modal-title {
  margin-top: 0;
  margin-bottom: 25px;
  color: white;
  text-align: center;
  font-size: 1.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-top: 25px;
  flex-wrap: wrap;
}

/* Responsive Design */
@media (max-width: 768px) {
  .todo-container {
    padding: 15px;
  }
  
  .main-title {
    font-size: 2rem;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .filters {
    flex-direction: column;
    gap: 20px;
  }
  
  .bulk-actions {
    flex-direction: column;
    text-align: center;
  }
  
  .todo-item {
    flex-direction: column;
    gap: 20px;
  }
  
  .todo-content {
    width: 100%;
  }
  
  .todo-actions {
    justify-content: center;
  }
  
  .form-options {
    flex-direction: column;
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 1.5rem;
  }
  
  .todo-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>

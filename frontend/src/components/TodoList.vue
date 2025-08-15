<template>
  <div class="todo-container">
    <!-- Fun Header with Rainbow Background -->
    <div class="header">
      <div class="header-content">
        <h1 class="main-title font-fancy">🌟 My Super Cool Tasks! 🌟</h1>
        <div class="stats-display" v-if="stats">
          <div class="stat-badge stat-total">📊 Total: {{ stats.total }}</div>
          <div class="stat-badge stat-done">✅ Done: {{ stats.completed }}</div>
          <div class="stat-badge stat-pending">⏳ Pending: {{ stats.pending }}</div>
          <div class="stat-badge stat-daily">🔄 Daily: {{ stats.daily_tasks }}</div>
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
        <button @click="bulkDelete" class="btn btn-sm btn-teal">🗑️ Delete</button>
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
          'todo-pink': todo.list_id % 6 === 0,
          'todo-purple': todo.list_id % 6 === 1,
          'todo-green': todo.list_id % 6 === 2,
          'todo-violet': todo.list_id % 6 === 3,
          'todo-orange': todo.list_id % 6 === 4,
          'todo-teal': todo.list_id % 6 === 5
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
          <button @click="editTodo(todo)" class="btn btn-sm btn-purple action-btn">✏️ Edit</button>
          <button @click="deleteTodo(todo.list_id)" class="btn btn-sm btn-teal action-btn">🗑️ Delete</button>
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
/* Base Container - Matching CoolKids gradient */
.todo-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: linear-gradient(135deg, #00d4aa 0%, #00b4d8 25%, #0077b6 50%, #7209b7 75%, #a663cc 100%);
  min-height: 100vh;
  position: relative;
}

.todo-container::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 212, 170, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(114, 9, 183, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(0, 180, 216, 0.3) 0%, transparent 50%);
  pointer-events: none;
  z-index: -1;
}

/* Fun Header - CoolKids colors */
.header {
  background: linear-gradient(45deg, #00d4aa, #00b4d8, #0077b6, #7209b7, #a663cc, #feca57);
  background-size: 400% 400%;
  animation: rainbow 4s ease infinite;
  border-radius: 30px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2), 0 0 0 3px rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.header::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  animation: shimmer 3s infinite;
}

@keyframes rainbow {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@keyframes shimmer {
  0% { transform: translateX(-100%) translateY(-100%) rotate(30deg); }
  100% { transform: translateX(100%) translateY(100%) rotate(30deg); }
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  position: relative;
  z-index: 1;
}

.main-title {
  color: white;
  margin: 0;
  font-size: 2.8rem;
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.4);
  font-weight: bold;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.stats-display {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.stat-badge {
  color: white;
  padding: 12px 18px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  transition: transform 0.3s ease;
}

.stat-badge:hover {
  transform: translateY(-3px);
}

.stat-total { background: linear-gradient(135deg, #7209b7 0%, #a663cc 100%); }
.stat-done { background: linear-gradient(135deg, #00d4aa 0%, #00b4d8 100%); }
.stat-pending { background: linear-gradient(135deg, #0077b6 0%, #7209b7 100%); }
.stat-daily { background: linear-gradient(135deg, #00b4d8 0%, #a663cc 100%); }

/* Fun Form Card - CoolKids purple gradient */
.todo-form-card {
  background: linear-gradient(135deg, #7209b7 0%, #a663cc 100%);
  border-radius: 30px;
  padding: 35px;
  margin-bottom: 30px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25), 0 0 0 4px rgba(255, 255, 255, 0.1);
  border: 3px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.todo-form-card::before {
  content: '✨';
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 2rem;
  animation: twinkle 2s infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

.form-title {
  margin-top: 0;
  margin-bottom: 25px;
  color: white;
  font-size: 2rem;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.form-group {
  margin-bottom: 25px;
}

.fun-label {
  display: block;
  margin-bottom: 10px;
  font-weight: bold;
  color: white;
  font-size: 1.2rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.fun-input {
  width: 100%;
  padding: 18px 25px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  font-size: 16px;
  font-family: inherit;
  background: rgba(255, 255, 255, 0.95);
  transition: all 0.3s ease;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.fun-input:focus {
  outline: none;
  border-color: #00d4aa;
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
  background: white;
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
  font-size: 18px;
  color: white;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
  transition: transform 0.2s ease;
}

.fun-checkbox:hover {
  transform: scale(1.05);
}

.checkbox-text {
  margin-left: 12px;
}

.rainbow-check {
  width: 28px;
  height: 28px;
  border: 3px solid #fff;
  border-radius: 10px;
  background: linear-gradient(45deg, #00d4aa, #00b4d8, #7209b7);
  position: relative;
  margin-right: 5px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
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
  font-size: 18px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

/* Enhanced Buttons - CoolKids colors */
.btn {
  padding: 15px 30px;
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
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn:hover:not(:disabled)::before {
  left: 100%;
}

.btn:hover:not(:disabled) {
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-rainbow {
  background: linear-gradient(45deg, #00d4aa, #00b4d8, #0077b6, #7209b7, #a663cc, #feca57);
  background-size: 400% 400%;
  animation: rainbow 3s ease infinite;
  color: white;
}

.btn-green {
  background: linear-gradient(45deg, #00d4aa, #38ef7d);
  color: white;
}

.btn-purple {
  background: linear-gradient(45deg, #7209b7, #a663cc);
  color: white;
}

.btn-teal {
  background: linear-gradient(45deg, #00d4aa, #00b4d8);
  color: white;
}

.btn-orange {
  background: linear-gradient(45deg, #ff9a56, #ffad56);
  color: white;
}

.btn-gray {
  background: linear-gradient(45deg, #bdc3c7, #2c3e50);
  color: white;
}

.btn-sm {
  padding: 10px 20px;
  font-size: 14px;
}

.btn-full {
  width: 100%;
}

.btn-big {
  padding: 20px 40px;
  font-size: 20px;
}

/* Enhanced Filters - CoolKids teal gradient */
.filters {
  display: flex;
  gap: 25px;
  margin-bottom: 25px;
  padding: 30px;
  background: linear-gradient(135deg, #00d4aa 0%, #00b4d8 100%);
  border-radius: 25px;
  align-items: end;
  flex-wrap: wrap;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-label {
  font-size: 16px;
  color: white;
  font-weight: bold;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.fun-select, .filter-input {
  padding: 12px 18px;
  border: 2px solid rgba(255, 255, 255, 0.5);
  border-radius: 20px;
  font-size: 14px;
  font-family: inherit;
  background: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.fun-select:focus, .filter-input:focus {
  outline: none;
  border-color: #7209b7;
  box-shadow: 0 0 15px rgba(114, 9, 183, 0.4);
  background: white;
}

.date-filter-group {
  display: flex;
  gap: 10px;
  align-items: center;
}

/* Enhanced Bulk Actions - CoolKids gradient */
.bulk-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-bottom: 25px;
  padding: 25px;
  background: linear-gradient(135deg, #0077b6 0%, #7209b7 100%);
  border-radius: 25px;
  color: white;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  flex-wrap: wrap;
  border: 3px solid rgba(255, 255, 255, 0.2);
}

.bulk-info {
  font-weight: bold;
  font-size: 18px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.bulk-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* Enhanced Loading */
.loading {
  text-align: center;
  padding: 60px;
  color: white;
}

.loading-spinner {
  font-size: 4rem;
  animation: spin 2s linear infinite, pulse 1.5s ease-in-out infinite alternate;
  margin-bottom: 25px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  from { transform: scale(1); }
  to { transform: scale(1.2); }
}

.loading-text {
  font-size: 1.4rem;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

/* Enhanced Messages - CoolKids colors */
.error-message, .success-message {
  padding: 25px 30px;
  border-radius: 25px;
  margin-bottom: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 18px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.error-message {
  background: linear-gradient(45deg, #00d4aa, #0077b6);
  color: white;
}

.success-message {
  background: linear-gradient(45deg, #00d4aa, #38ef7d);
  color: white;
}

.close-btn {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
  color: inherit;
  border-radius: 50%;
  width: 35px;
  height: 35px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.1);
}

/* Enhanced Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: white;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border-radius: 25px;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 25px;
  animation: bounce 2s infinite;
}

.empty-title {
  font-size: 2.2rem;
  margin-bottom: 15px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.empty-text {
  font-size: 1.3rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

/* Enhanced Todo List - CoolKids colors */
.todo-list {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.todo-item {
  border-radius: 25px;
  padding: 30px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  transition: all 0.3s ease;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  border: 3px solid rgba(255, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.todo-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #00d4aa, #00b4d8, #0077b6, #7209b7, #a663cc);
}

.todo-item:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
}

.todo-pink {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
}

.todo-purple {
  background: linear-gradient(135deg, #7209b7 0%, #a663cc 100%);
}

.todo-green {
  background: linear-gradient(135deg, #00d4aa 0%, #38ef7d 100%);
}

.todo-violet {
  background: linear-gradient(135deg, #a663cc 0%, #764ba2 100%);
}

.todo-orange {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.todo-teal {
  background: linear-gradient(135deg, #00d4aa 0%, #00b4d8 100%);
}

.todo-item.completed {
  opacity: 0.8;
  transform: scale(0.98);
}

.todo-item.daily-task {
  border-left: 8px solid #feca57;
  box-shadow: 0 15px 40px rgba(254, 202, 87, 0.3);
}

.todo-content {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  flex: 1;
}

.todo-details {
  flex: 1;
}

.todo-title {
  margin: 0 0 15px 0;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  gap: 12px;
}

.todo-emoji {
  font-size: 1.8rem;
  animation: bounce 2s infinite;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  opacity: 0.7;
}

.todo-description {
  margin: 0 0 20px 0;
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.7;
  font-size: 1.1rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.todo-meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.8);
  flex-wrap: wrap;
}

.daily-badge {
  background: linear-gradient(135deg, #feca57, #ff9ff3);
  color: white;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.todo-actions {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
  flex-wrap: wrap;
}

.action-btn {
  min-width: 90px;
}

/* Enhanced Modal - CoolKids purple */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(8px);
}

.fun-modal {
  background: linear-gradient(135deg, #7209b7 0%, #a663cc 100%);
  border-radius: 30px;
  padding: 40px;
  width: 90%;
  max-width: 550px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 80px rgba(0, 0, 0, 0.4);
  border: 4px solid rgba(255, 255, 255, 0.2);
  position: relative;
}

.modal-title {
  margin-top: 0;
  margin-bottom: 30px;
  color: white;
  text-align: center;
  font-size: 1.8rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.modal-actions {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 30px;
  flex-wrap: wrap;
}

/* Responsive Design */
@media (max-width: 768px) {
  .todo-container {
    padding: 15px;
  }
  
  .main-title {
    font-size: 2.2rem;
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
    gap: 25px;
  }
  
  .todo-content {
    width: 100%;
  }
  
  .todo-actions {
    justify-content: center;
  }
  
  .form-options {
    flex-direction: column;
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .main-title {
    font-size: 1.8rem;
  }
  
  .todo-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
  
  .stats-display {
    justify-content: center;
  }
}
</style>
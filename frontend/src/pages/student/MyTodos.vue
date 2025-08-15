<template>
  <div class="min-h-screen flex">
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
        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2">My To-Do List ✅</h1>
              <p class="text-lg text-gray-600 font-medium">
                You have <span class="text-blue-500 font-bold">{{ todos.length }}</span> tasks on your list.
              </p>
            </div>

            <!-- Buttons (Right Side - Horizontal Row) -->
            <div class="flex space-x-4 min-w-fit font-playfair">
              <router-link to="/student/profile"
                class="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors duration-200 font-medium">
                Profile
              </router-link>

              <button @click="logout"
                class="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-red-100 text-red-700 hover:bg-red-200 transition-colors duration-200 font-medium">
                Logout
              </button>
            </div>
          </div>
        </div>

        <div class="flex justify-center mb-8">
          <button @click="openCreateModal"
            class="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-3 rounded-2xl font-medium shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center">
            <span class="text-xl mr-2">➕</span>
            Add New Task
          </button>
        </div>

        <div v-if="isLoading" class="text-center py-20">
          <p class="text-lg text-gray-600">Loading tasks...</p>
        </div>

        <div v-else-if="error" class="text-center py-20">
          <p class="text-lg text-red-500 font-medium">{{ error }}</p>
        </div>

        <div v-else-if="todos.length > 0" class="space-y-4">
          <div v-for="todo in todos" :key="todo.id" @click="openEditModal(todo)"
            class="bg-white rounded-3xl p-6 shadow-lg border-2 transition-transform hover:scale-105 cursor-pointer flex items-center justify-between"
            :class="{ 'border-green-400 bg-green-50': todo.is_completed, 'border-gray-200': !todo.is_completed }">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="font-bold text-gray-800 text-lg"
                  :class="{ 'line-through text-gray-500': todo.is_completed }">
                  {{ todo.task_name }}
                </h3>
                <span v-if="todo.is_daily" class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">🔁 Daily</span>
              </div>
              <p class="text-sm text-gray-600 mb-1">{{ todo.description }}</p>
              <p v-if="todo.completion_date" class="text-xs text-gray-500">
                Due: {{ formatDate(todo.completion_date) }}
              </p>
              <p class="text-xs text-gray-400 mt-1">Created: {{ formatDate(todo.created_at) }}</p>
            </div>

            <div class="flex-shrink-0 ml-4">
              <div v-if="todo.is_completed" class="text-2xl text-green-600 font-bold">✅</div>
              <div v-else class="text-2xl text-yellow-500 font-bold">⏳</div>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-20">
          <div class="text-6xl mb-4">✨</div>
          <h2 class="text-2xl font-bold text-gray-800 mb-2">No Tasks Yet!</h2>
          <p class="text-gray-600">Click the button above to add your first task.</p>
        </div>
      </div>
    </main>

    <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-3xl p-6 w-full max-w-md shadow-2xl max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-gray-800">
            {{ editingTodo ? 'Edit Task' : 'Add New Task' }}
          </h3>
          <button @click="closeModal" class="p-2 rounded-full hover:bg-gray-100 transition-colors">
            <svg class="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveTodo" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Task Name</label>
            <input v-model="todoForm.task_name" type="text"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="e.g., Finish science project" required>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea v-model="todoForm.description"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Add details about the task..." rows="3" required></textarea>
          </div>

          <div class="flex items-center">
            <input id="is-daily" type="checkbox" v-model="todoForm.is_daily"
              class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
            <label for="is-daily" class="ml-2 block text-sm text-gray-900">
              Recurring daily task
            </label>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Due Date (Optional)</label>
            <input v-model="todoForm.completion_date" type="date"
              class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
          </div>

          <div v-if="editingTodo" class="flex items-center">
            <input id="completed-checkbox" type="checkbox" v-model="todoForm.is_completed"
              class="h-4 w-4 text-green-600 border-gray-300 rounded focus:ring-green-500">
            <label for="completed-checkbox" class="ml-2 block text-sm text-gray-900">
              Mark as Completed
            </label>
          </div>

          <div class="flex space-x-3 pt-4">
            <button v-if="editingTodo" type="button" @click="deleteTodo"
              class="flex-1 py-3 px-4 rounded-xl border border-red-300 text-red-600 font-medium hover:bg-red-50 transition-colors">
              Delete
            </button>
            <button type="button" @click="closeModal"
              class="flex-1 py-3 px-4 rounded-xl border border-gray-300 text-gray-700 font-medium hover:bg-gray-50 transition-colors">
              Cancel
            </button>
            <button type="submit"
              class="flex-1 py-3 px-4 rounded-xl bg-gradient-to-r from-blue-500 to-purple-500 text-white font-medium shadow-lg hover:shadow-xl transition-all duration-200">
              {{ editingTodo ? 'Update Task' : 'Add Task' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/plugins/axios';
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { clearAuthData } from '@/utils/auth';

const router = useRouter();

// --- Reactive Data ---
const showModal = ref(false);
const editingTodo = ref(null);
const todos = ref([]);
const isLoading = ref(true);
const error = ref(null);

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

const logout = () => {
  clearAuthData();
  router.push('/');
};

const todoForm = ref({
  id: null,
  task_name: '',
  description: '',
  is_daily: false,
  is_completed: false,
  completion_date: null,
});

// --- Fetch To-Dos ---
const fetchTodos = async () => {
  isLoading.value = true;
  error.value = null;
  const token = localStorage.getItem('access_token');

  if (!token) {
    error.value = 'Authentication required.';
    isLoading.value = false;
    return;
  }

  try {
    const response = await api.get('/api/todos', {
      headers: { Authorization: `Bearer ${token}` }
    });

    todos.value = (response.data.todos || []).map(todo => ({
      id: todo.list_id,
      task_name: todo.to_do,
      description: todo.description,
      is_daily: todo.is_daily,
      is_completed: todo.is_done,
      created_at: todo.created_at,
      completion_date: todo.completion_date
    }));
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to load tasks.';
    console.error('Fetch Error:', err);
  } finally {
    isLoading.value = false;
  }
};

// --- Create New To-Do ---
const createTodo = async () => {
  const token = localStorage.getItem('access_token');
  if (!token) {
    error.value = 'Session expired.';
    return;
  }

  try {
    const response = await api.post('/api/todos', {
      to_do: todoForm.value.task_name.trim(),
      description: todoForm.value.description.trim(),
      is_daily: todoForm.value.is_daily || false,
      is_done: todoForm.value.is_completed || false,
      completion_date: todoForm.value.completion_date
        ? new Date(todoForm.value.completion_date).toISOString()
        : null
    }, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    // Add new task to list
    const newTodo = {
      id: response.data.list_id,
      task_name: response.data.to_do,
      description: response.data.description,
      is_daily: response.data.is_daily,
      is_completed: response.data.is_done,
      created_at: response.data.created_at,
      completion_date: response.data.completion_date
    };
    todos.value.unshift(newTodo);
    closeModal();
  } catch (err) {
    const errorMsg = err.response?.data?.error || 'Failed to create task.';
    error.value = errorMsg;
    alert(`Error: ${errorMsg}`);
    console.error('Create Error:', err);
  }
};

// --- Update To-Do ---
const updateTodo = async () => {
  const token = localStorage.getItem('access_token');
  if (!token || !editingTodo.value?.id) return;

  try {
    await api.put(`/api/todos/${editingTodo.value.id}`, {
      to_do: todoForm.value.task_name.trim(),
      description: todoForm.value.description.trim(),
      is_daily: todoForm.value.is_daily || false,
      is_done: todoForm.value.is_completed || false,
      // Only set completion date if it was just marked done
      completion_date: todoForm.value.is_completed && !editingTodo.value.is_completed
        ? new Date().toISOString()
        : todoForm.value.completion_date
          ? new Date(todoForm.value.completion_date).toISOString()
          : null
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Update local list
    const index = todos.value.findIndex(t => t.id === editingTodo.value.id);
    if (index !== -1) {
      todos.value[index] = { ...todos.value[index], ...todoForm.value };
    }
    closeModal();
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to update task.';
    console.error('Update Error:', err);
  }
};

// --- Delete To-Do ---
const deleteTodo = async () => {
  const confirmed = confirm(`Are you sure you want to delete "${editingTodo.value.task_name}"?`);
  if (!confirmed || !editingTodo.value?.id) return;

  const token = localStorage.getItem('access_token');
  try {
    await api.delete(`/api/todos/${editingTodo.value.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    todos.value = todos.value.filter(t => t.id !== editingTodo.value.id);
    closeModal();
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to delete task.';
    console.error('Delete Error:', err);
  }
};

// --- Save Handler ---
const saveTodo = () => {
  if (!todoForm.value.task_name.trim() || !todoForm.value.description.trim()) {
    alert('Task name and description are required.');
    return;
  }
  if (editingTodo.value) {
    updateTodo();
  } else {
    createTodo();
  }
};

// --- Modal Logic ---
const openCreateModal = () => {
  editingTodo.value = null;
  resetForm();
  showModal.value = true;
};

const openEditModal = (todo) => {
  editingTodo.value = todo;
  todoForm.value = { ...todo };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingTodo.value = null;
  resetForm();
};

const resetForm = () => {
  todoForm.value = {
    id: null,
    task_name: '',
    description: '',
    is_daily: false,
    is_completed: false,
    completion_date: null,
  };
};

// --- Format Date ---
const formatDate = (dateString) => {
  if (!dateString) return 'No date';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

// --- Lifecycle Hook ---
onMounted(() => {
  fetchTodos();
});
</script>

<style scoped>
.line-through {
  text-decoration: line-through;
}
</style>

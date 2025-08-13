<template>
  <div class="reset-password">
    <h1>Reset Password</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="email">Email:</label>
        <input 
          type="email" 
          id="email" 
          v-model="email" 
          :disabled="loading"
          required 
        />
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="success" class="success-message">
        Password reset email sent! Check your inbox.
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Sending...' : 'Send Reset Email' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const email = ref('');
    const loading = ref(false);
    const error = ref('');
    const success = ref(false);

    const submitForm = async () => {
      loading.value = true;
      error.value = '';
      success.value = false;

      try {
        await axios.post('http://127.0.0.1:5000/api/auth/forgot-password', {
          email: email.value
        });
        success.value = true;
        email.value = '';
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to send reset email';
      } finally {
        loading.value = false;
      }
    };

    return {
      email,
      loading,
      error,
      success,
      submitForm
    };
  }
};
</script>

<style scoped>
.reset-password {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #f8d7da;
  border-radius: 4px;
}

.success-message {
  color: #155724;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #d4edda;
  border-radius: 4px;
}
</style>
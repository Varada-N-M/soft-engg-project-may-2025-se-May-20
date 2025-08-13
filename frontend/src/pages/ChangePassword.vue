<template>
  <div class="change-password">
    <h1>Change Password</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="newPassword">New Password:</label>
        <input 
          type="password" 
          id="newPassword" 
          v-model="newPassword" 
          :disabled="loading"
          required 
        />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input 
          type="password" 
          id="confirmPassword" 
          v-model="confirmPassword" 
          :disabled="loading"
          required 
        />
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <div v-if="success" class="success-message">
        Password changed successfully! You can now log in with your new password.
      </div>
      <button type="submit" :disabled="loading">
        {{ loading ? 'Changing...' : 'Change Password' }}
      </button>
    </form>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  setup() {
    const newPassword = ref('');
    const confirmPassword = ref('');
    const loading = ref(false);
    const error = ref('');
    const success = ref(false);
    const token = ref('');

    onMounted(() => {
      // Get token from URL parameters
      const urlParams = new URLSearchParams(window.location.search);
      token.value = urlParams.get('token') || '';
      
      if (!token.value) {
        error.value = 'Invalid or missing reset token';
      }
    });

    const submitForm = async () => {
      if (newPassword.value !== confirmPassword.value) {
        error.value = 'Passwords do not match';
        return;
      }

      if (newPassword.value.length < 8) {
        error.value = 'Password must be at least 8 characters long';
        return;
      }

      loading.value = true;
      error.value = '';
      success.value = false;

      try {
        await axios.post(`http://127.0.0.1:5000/api/auth/reset-password?token=${token.value}`, {
          new_password: newPassword.value
        });
        success.value = true;
        newPassword.value = '';
        confirmPassword.value = '';
      } catch (err) {
        error.value = err.response?.data?.message || 'Failed to change password';
      } finally {
        loading.value = false;
      }
    };

    return {
      newPassword,
      confirmPassword,
      loading,
      error,
      success,
      submitForm
    };
  }
};
</script>

<style scoped>
.change-password {
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
<template>
  <div>
    <GuestNavbar />
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Card class="w-full max-w-md">
        <CardHeader class="space-y-1 text-center">
          <Logo class="text-3xl mb-2" />
          <CardTitle class="text-2xl font-bold">Change Password</CardTitle>
          <CardDescription>
            Enter your new password to secure your account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="submitForm" class="space-y-4">
            <div class="space-y-2">
              <Label for="newPassword">New Password</Label>
              <Input
                id="newPassword"
                type="password"
                v-model="newPassword"
                :disabled="loading"
                placeholder="Enter new password"
                required
              />
            </div>
            <div class="space-y-2">
              <Label for="confirmPassword">Confirm Password</Label>
              <Input
                id="confirmPassword"
                type="password"
                v-model="confirmPassword"
                :disabled="loading"
                placeholder="Confirm new password"
                required
              />
            </div>
            <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              {{ error }}
            </div>
            <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-md">
              Password changed successfully! You can now log in with your new password.
            </div>
            <Button type="submit" :disabled="loading" class="w-full">
              {{ loading ? 'Changing...' : 'Change Password' }}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import GuestNavbar from '@/components/app/GuestNavbar.vue'
import Logo from '@/components/partials/Logo.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

// Reactive state

// Variables are already reactive due to script setup
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)
const token = ref('')

onMounted(() => {
  // Get token from URL parameters
  const urlParams = new URLSearchParams(window.location.search)
  token.value = urlParams.get('token') || ''
  
  if (!token.value) {
    error.value = 'Invalid or missing reset token'
  }
})

const submitForm = async () => {
  if (newPassword.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  if (newPassword.value.length < 8) {
    error.value = 'Password must be at least 8 characters long'
    return
  }

  loading.value = true
  error.value = ''
  success.value = false

  try {
    await axios.post(`http://127.0.0.1:5000/api/auth/reset-password?token=${token.value}`, {
      new_password: newPassword.value
    })
    success.value = true
    newPassword.value = ''
    confirmPassword.value = ''
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to change password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Custom styles if needed */
</style>
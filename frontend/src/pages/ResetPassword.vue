<template>
  <div>
    <GuestNavbar />
    <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Card class="w-full max-w-md">
        <CardHeader class="space-y-1 text-center">
          <Logo class="text-3xl mb-2" />
          <CardTitle class="text-2xl font-bold">Reset Password</CardTitle>
          <CardDescription>
            Enter your email address and we'll send you a link to reset your password
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form @submit.prevent="submitForm" class="space-y-4">
            <div class="space-y-2">
              <Label for="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                v-model="email"
                :disabled="loading"
                placeholder="Enter your email address"
                required
              />
            </div>
            <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
              {{ error }}
            </div>
            <div v-if="success" class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-md">
              Password reset email sent! Check your inbox.
            </div>
            <Button type="submit" :disabled="loading" class="w-full">
              {{ loading ? 'Sending...' : 'Send Reset Email' }}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import GuestNavbar from '@/components/app/GuestNavbar.vue'
import Logo from '@/components/partials/Logo.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

// Reactive state
const email = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)

const submitForm = async () => {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    await axios.post('http://127.0.0.1:5000/api/auth/forgot-password', {
      email: email.value
    })
    success.value = true
    email.value = ''
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to send reset email'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Custom styles if needed */
</style>
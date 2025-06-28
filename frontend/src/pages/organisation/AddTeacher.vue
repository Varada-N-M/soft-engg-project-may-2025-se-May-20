<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <OrgDashboardLayout>
      <template v-slot:breadcrumb>
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem class="hidden md:block">
              <BreadcrumbLink href="#">
                Organisation
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator class="hidden md:block"/>
            <BreadcrumbItem>
              <BreadcrumbPage>Dashboard</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </template>
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center py-4">
          <div class="flex items-center space-x-4">
            <Button
                variant="ghost"
                @click="$router.push('/org/teachers')"
                class="p-2"
            >
              <ArrowLeft class="w-5 h-5" />
            </Button>
            <div class="flex items-center space-x-4">
              <div class="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
                <UserPlus class="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 class="text-2xl font-bold text-gray-900">Add Main Teacher</h1>
                <p class="text-sm text-gray-600">Register a new main teacher for school assignment</p>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <Button variant="outline" @click="resetForm">
              <RotateCcw class="w-4 h-4 mr-2" />
              Reset Form
            </Button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <form @submit.prevent="submitForm" class="space-y-8">
        <!-- Personal Information Section -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center">
              <User class="w-5 h-5 mr-2" />
              Personal Information
            </CardTitle>
            <CardDescription>
              Basic personal details of the teacher
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label for="firstName">First Name *</Label>
                <Input
                    id="firstName"
                    v-model="form.firstName"
                    placeholder="Enter first name"
                    required
                    :class="{ 'border-red-500': errors.firstName }"
                />
                <p v-if="errors.firstName" class="text-sm text-red-600">{{ errors.firstName }}</p>
              </div>

              <div class="space-y-2">
                <Label for="lastName">Last Name *</Label>
                <Input
                    id="lastName"
                    v-model="form.lastName"
                    placeholder="Enter last name"
                    required
                    :class="{ 'border-red-500': errors.lastName }"
                />
                <p v-if="errors.lastName" class="text-sm text-red-600">{{ errors.lastName }}</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label for="email">Email Address *</Label>
                <Input
                    id="email"
                    v-model="form.email"
                    type="email"
                    placeholder="teacher@school.edu"
                    required
                    :class="{ 'border-red-500': errors.email }"
                />
                <p v-if="errors.email" class="text-sm text-red-600">{{ errors.email }}</p>
              </div>

              <div class="space-y-2">
                <Label for="phone">Phone Number *</Label>
                <Input
                    id="phone"
                    v-model="form.phone"
                    type="tel"
                    placeholder="+1 (555) 123-4567"
                    required
                    :class="{ 'border-red-500': errors.phone }"
                />
                <p v-if="errors.phone" class="text-sm text-red-600">{{ errors.phone }}</p>
              </div>
            </div>

            <div class="space-y-2">
              <Label for="dateOfBirth">Date of Birth</Label>
              <Input
                  id="dateOfBirth"
                  v-model="form.dateOfBirth"
                  type="date"
                  :max="maxBirthDate"
              />
            </div>
          </CardContent>
        </Card>

        <!-- School Assignment Section -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center">
              <School class="w-5 h-5 mr-2" />
              School Assignment
            </CardTitle>
            <CardDescription>
              School and teaching assignment details
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label for="schoolName">School Name *</Label>
                <Select v-model="form.schoolId" required>
                  <SelectTrigger :class="{ 'border-red-500': errors.schoolId }">
                    <SelectValue placeholder="Select a school" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem v-for="school in schools" :key="school.id" :value="school.id">
                      {{ school.name }}
                    </SelectItem>
                  </SelectContent>
                </Select>
                <p v-if="errors.schoolId" class="text-sm text-red-600">{{ errors.schoolId }}</p>
              </div>

              <div class="space-y-2">
                <Label for="employeeId">Employee ID *</Label>
                <Input
                    id="employeeId"
                    v-model="form.employeeId"
                    placeholder="EMP-2024-001"
                    required
                    :class="{ 'border-red-500': errors.employeeId }"
                />
                <p v-if="errors.employeeId" class="text-sm text-red-600">{{ errors.employeeId }}</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label for="primarySubject">Primary Subject *</Label>
                <Select v-model="form.primarySubject" required>
                  <SelectTrigger :class="{ 'border-red-500': errors.primarySubject }">
                    <SelectValue placeholder="Select primary subject" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem v-for="subject in subjects" :key="subject" :value="subject">
                      {{ subject }}
                    </SelectItem>
                  </SelectContent>
                </Select>
                <p v-if="errors.primarySubject" class="text-sm text-red-600">{{ errors.primarySubject }}</p>
              </div>

              <div class="space-y-2">
                <Label for="gradeLevel">Grade Level *</Label>
                <Select v-model="form.gradeLevel" required>
                  <SelectTrigger :class="{ 'border-red-500': errors.gradeLevel }">
                    <SelectValue placeholder="Select grade level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem v-for="grade in gradeLevels" :key="grade" :value="grade">
                      {{ grade }}
                    </SelectItem>
                  </SelectContent>
                </Select>
                <p v-if="errors.gradeLevel" class="text-sm text-red-600">{{ errors.gradeLevel }}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Employment Details Section -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center">
              <Briefcase class="w-5 h-5 mr-2" />
              Employment Details
            </CardTitle>
            <CardDescription>
              Employment and qualification information
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label for="startDate">Start Date *</Label>
                <Input
                    id="startDate"
                    v-model="form.startDate"
                    type="date"
                    required
                    :class="{ 'border-red-500': errors.startDate }"
                />
                <p v-if="errors.startDate" class="text-sm text-red-600">{{ errors.startDate }}</p>
              </div>

              <div class="space-y-2">
                <Label for="employmentType">Employment Type *</Label>
                <Select v-model="form.employmentType" required>
                  <SelectTrigger :class="{ 'border-red-500': errors.employmentType }">
                    <SelectValue placeholder="Select employment type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="full-time">Full-time</SelectItem>
                    <SelectItem value="part-time">Part-time</SelectItem>
                    <SelectItem value="contract">Contract</SelectItem>
                    <SelectItem value="substitute">Substitute</SelectItem>
                  </SelectContent>
                </Select>
                <p v-if="errors.employmentType" class="text-sm text-red-600">{{ errors.employmentType }}</p>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label for="qualification">Highest Qualification *</Label>
                <Select v-model="form.qualification" required>
                  <SelectTrigger :class="{ 'border-red-500': errors.qualification }">
                    <SelectValue placeholder="Select qualification" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="bachelor">Bachelor's Degree</SelectItem>
                    <SelectItem value="master">Master's Degree</SelectItem>
                    <SelectItem value="doctorate">Doctorate</SelectItem>
                    <SelectItem value="diploma">Teaching Diploma</SelectItem>
                    <SelectItem value="certificate">Teaching Certificate</SelectItem>
                  </SelectContent>
                </Select>
                <p v-if="errors.qualification" class="text-sm text-red-600">{{ errors.qualification }}</p>
              </div>

              <div class="space-y-2">
                <Label for="experience">Years of Experience</Label>
                <Input
                    id="experience"
                    v-model.number="form.experience"
                    type="number"
                    min="0"
                    max="50"
                    placeholder="0"
                />
              </div>
            </div>

            <div class="space-y-2">
              <Label for="specializations">Additional Specializations</Label>
              <Textarea
                  id="specializations"
                  v-model="form.specializations"
                  placeholder="List any additional specializations, certifications, or areas of expertise..."
                  rows="3"
              />
            </div>
          </CardContent>
        </Card>

        <!-- Emergency Contact Section -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center">
              <Phone class="w-5 h-5 mr-2" />
              Emergency Contact
            </CardTitle>
            <CardDescription>
              Emergency contact information
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2">
                <Label for="emergencyName">Contact Name</Label>
                <Input
                    id="emergencyName"
                    v-model="form.emergencyContact.name"
                    placeholder="Emergency contact name"
                />
              </div>

              <div class="space-y-2">
                <Label for="emergencyPhone">Contact Phone</Label>
                <Input
                    id="emergencyPhone"
                    v-model="form.emergencyContact.phone"
                    type="tel"
                    placeholder="+1 (555) 123-4567"
                />
              </div>
            </div>

            <div class="space-y-2">
              <Label for="emergencyRelation">Relationship</Label>
              <Input
                  id="emergencyRelation"
                  v-model="form.emergencyContact.relationship"
                  placeholder="e.g., Spouse, Parent, Sibling"
              />
            </div>
          </CardContent>
        </Card>

        <!-- Form Actions -->
        <div class="flex justify-end space-x-4 pt-6">
          <Button
              type="button"
              variant="outline"
              @click="$router.push('/')"
              :disabled="isSubmitting"
          >
            Cancel
          </Button>
          <Button
              type="submit"
              :disabled="isSubmitting"
              class="bg-green-600 hover:bg-green-700"
          >
            <Loader2 v-if="isSubmitting" class="w-4 h-4 mr-2 animate-spin" />
            <UserPlus v-else class="w-4 h-4 mr-2" />
            {{ isSubmitting ? 'Adding Teacher...' : 'Add Teacher' }}
          </Button>
        </div>
      </form>
    </main>

    <!-- Success Modal -->
    <div v-if="showSuccessModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <Card class="w-full max-w-md mx-4">
        <CardContent class="p-6 text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <CheckCircle class="w-8 h-8 text-green-600" />
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Teacher Added Successfully!</h3>
          <p class="text-gray-600 mb-6">
            {{ form.firstName }} {{ form.lastName }} has been registered as a main teacher.
          </p>
          <div class="flex space-x-3">
            <Button variant="outline" @click="addAnother" class="flex-1">
              Add Another
            </Button>
            <Button @click="goToDashboard" class="flex-1 bg-green-600 hover:bg-green-700">
              Go to Dashboard
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
    </OrgDashboardLayout>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import {
  ArrowLeft, UserPlus, User, School, Briefcase, Phone,
  RotateCcw, Loader2, CheckCircle
} from 'lucide-vue-next'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList, BreadcrumbPage,
  BreadcrumbSeparator
} from "@/components/ui/breadcrumb";
import OrgDashboardLayout from "@/components/partials/OrgDashboardLayout.vue";

const router = useRouter()

// Form data
const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  dateOfBirth: '',
  schoolId: '',
  employeeId: '',
  primarySubject: '',
  gradeLevel: '',
  startDate: '',
  employmentType: '',
  qualification: '',
  experience: 0,
  specializations: '',
  emergencyContact: {
    name: '',
    phone: '',
    relationship: ''
  }
})

// Form validation errors
const errors = ref({})
const isSubmitting = ref(false)
const showSuccessModal = ref(false)

// Static data
const schools = ref([
  { id: 'school-001', name: 'Lincoln Elementary School' },
  { id: 'school-002', name: 'Washington Middle School' },
  { id: 'school-003', name: 'Roosevelt High School' },
  { id: 'school-004', name: 'Jefferson Academy' },
  { id: 'school-005', name: 'Madison Charter School' }
])

const subjects = ref([
  'Mathematics', 'English Language Arts', 'Science', 'Social Studies',
  'Physical Education', 'Art', 'Music', 'Computer Science',
  'Foreign Language', 'Special Education', 'Library Science'
])

const gradeLevels = ref([
  'Pre-K', 'Kindergarten', '1st Grade', '2nd Grade', '3rd Grade',
  '4th Grade', '5th Grade', '6th Grade', '7th Grade', '8th Grade',
  '9th Grade', '10th Grade', '11th Grade', '12th Grade', 'Mixed Grades'
])

// Computed properties
const maxBirthDate = computed(() => {
  const date = new Date()
  date.setFullYear(date.getFullYear() - 18) // Minimum age 18
  return date.toISOString().split('T')[0]
})

// Form validation
const validateForm = () => {
  const newErrors = {}

  if (!form.value.firstName.trim()) {
    newErrors.firstName = 'First name is required'
  }

  if (!form.value.lastName.trim()) {
    newErrors.lastName = 'Last name is required'
  }

  if (!form.value.email.trim()) {
    newErrors.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    newErrors.email = 'Please enter a valid email address'
  }

  if (!form.value.phone.trim()) {
    newErrors.phone = 'Phone number is required'
  }

  if (!form.value.schoolId) {
    newErrors.schoolId = 'School selection is required'
  }

  if (!form.value.employeeId.trim()) {
    newErrors.employeeId = 'Employee ID is required'
  }

  if (!form.value.primarySubject) {
    newErrors.primarySubject = 'Primary subject is required'
  }

  if (!form.value.gradeLevel) {
    newErrors.gradeLevel = 'Grade level is required'
  }

  if (!form.value.startDate) {
    newErrors.startDate = 'Start date is required'
  }

  if (!form.value.employmentType) {
    newErrors.employmentType = 'Employment type is required'
  }

  if (!form.value.qualification) {
    newErrors.qualification = 'Qualification is required'
  }

  errors.value = newErrors
  return Object.keys(newErrors).length === 0
}

// Form submission
const submitForm = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))

    console.log('Teacher data submitted:', form.value)
    showSuccessModal.value = true
  } catch (error) {
    console.error('Error submitting form:', error)
    // Handle error (show toast, etc.)
  } finally {
    isSubmitting.value = false
  }
}

// Form actions
const resetForm = () => {
  form.value = {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    dateOfBirth: '',
    schoolId: '',
    employeeId: '',
    primarySubject: '',
    gradeLevel: '',
    startDate: '',
    employmentType: '',
    qualification: '',
    experience: 0,
    specializations: '',
    emergencyContact: {
      name: '',
      phone: '',
      relationship: ''
    }
  }
  errors.value = {}
}

const addAnother = () => {
  showSuccessModal.value = false
  resetForm()
}

const goToDashboard = () => {
  router.push('/')
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">

    <OrgDashboardLayout>
      <template v-slot:breadcrumb>
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem class="hidden md:block">
              <BreadcrumbLink href="#">
                Home
              </BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator class="hidden md:block"/>
            <BreadcrumbItem>
              <BreadcrumbPage>Teachers</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </template>
      <!-- Header -->
      <header class="bg-white shadow-sm border-b">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center py-4">
            <div class="flex items-center space-x-4">
              <Button
                  variant="ghost"
                  @click="$router.push('/org/home')"
                  class="p-2"
              >
                <ArrowLeft class="w-5 h-5"/>
              </Button>
              <div class="flex items-center space-x-4">
                <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                  <Users class="w-6 h-6 text-white"/>
                </div>
                <div>
                  <h1 class="text-2xl font-bold text-gray-900">Teachers Management</h1>
                  <p class="text-sm text-gray-600">View and manage all registered teachers</p>
                </div>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <Button variant="outline" @click="exportTeachers">
                <Download class="w-4 h-4 mr-2"/>
                Export
              </Button>
              <Button @click="$router.push('/org/add-teacher')" class="bg-green-600 hover:bg-green-700">
                <UserPlus class="w-4 h-4 mr-2"/>
                Add Teacher
              </Button>
            </div>
          </div>
        </div>
      </header>

      <!-- Main Content -->
      <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        <!-- Filters and Search -->
        <Card class="mb-8">
          <CardContent class="p-6">
            <div
                class="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0 lg:space-x-4">
              <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 flex-1">
                <div class="relative flex-1 max-w-md">
                  <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4"/>
                  <Input
                      v-model="searchQuery"
                      placeholder="Search teachers by name, email, or employee ID..."
                      class="pl-10"
                  />
                </div>

                <Select v-model="selectedSchool">
                  <SelectTrigger class="w-48">
                    <SelectValue placeholder="All Schools"/>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Schools</SelectItem>
                    <SelectItem v-for="school in schools" :key="school.id" :value="school.id">
                      {{ school.name }}
                    </SelectItem>
                  </SelectContent>
                </Select>

                <Select v-model="selectedSubject">
                  <SelectTrigger class="w-48">
                    <SelectValue placeholder="All Subjects"/>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Subjects</SelectItem>
                    <SelectItem v-for="subject in subjects" :key="subject" :value="subject">
                      {{ subject }}
                    </SelectItem>
                  </SelectContent>
                </Select>

                <Select v-model="selectedStatus">
                  <SelectTrigger class="w-32">
                    <SelectValue placeholder="All Status"/>
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="inactive">Inactive</SelectItem>
                    <SelectItem value="pending">Pending</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div class="flex items-center space-x-2">
                <Button variant="outline" @click="clearFilters">
                  <X class="w-4 h-4 mr-2"/>
                  Clear Filters
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Teachers Table -->
        <Card>
          <CardHeader>
            <div class="flex items-center justify-between">
              <div>
                <CardTitle class="flex items-center">
                  <Users class="w-5 h-5 mr-2"/>
                  Teachers List
                </CardTitle>
                <CardDescription>
                  {{ filteredTeachers.length }} of {{ teachers.length }} teachers
                </CardDescription>
              </div>
              <div class="flex items-center space-x-2">
                <Button variant="outline" size="sm" @click="toggleView">
                  <Grid class="w-4 h-4 mr-2"/>
                  {{ viewMode === 'table' ? 'Card View' : 'Table View' }}
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <!-- Table View -->
            <div v-if="viewMode === 'table'" class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                      @click="sortBy('name')">
                    <div class="flex items-center">
                      Teacher
                      <ArrowUpDown class="w-4 h-4 ml-1"/>
                    </div>
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                      @click="sortBy('school')">
                    <div class="flex items-center">
                      School
                      <ArrowUpDown class="w-4 h-4 ml-1"/>
                    </div>
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Subject & Grade
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Employment
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                      @click="sortBy('startDate')">
                    <div class="flex items-center">
                      Start Date
                      <ArrowUpDown class="w-4 h-4 ml-1"/>
                    </div>
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="teacher in paginatedTeachers" :key="teacher.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <span class="text-sm font-medium text-blue-600">
                          {{ teacher.firstName[0] }}{{ teacher.lastName[0] }}
                        </span>
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-gray-900">
                          {{ teacher.firstName }} {{ teacher.lastName }}
                        </div>
                        <div class="text-sm text-gray-500">{{ teacher.email }}</div>
                        <div class="text-xs text-gray-400">ID: {{ teacher.employeeId }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ teacher.schoolName }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ teacher.primarySubject }}</div>
                    <div class="text-sm text-gray-500">{{ teacher.gradeLevel }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900 capitalize">{{ teacher.employmentType }}</div>
                    <div class="text-sm text-gray-500">{{ teacher.experience }} years exp.</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatDate(teacher.startDate) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                        class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                        :class="getStatusClass(teacher.status)"
                    >
                      {{ teacher.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex items-center space-x-2">
                      <Button variant="ghost" size="sm" @click="viewTeacher(teacher)">
                        <Eye class="w-4 h-4"/>
                      </Button>
                      <Button variant="ghost" size="sm" @click="editTeacher(teacher)">
                        <Edit class="w-4 h-4"/>
                      </Button>
                      <Button variant="ghost" size="sm" @click="deleteTeacher(teacher)"
                              class="text-red-600 hover:text-red-800">
                        <Trash2 class="w-4 h-4"/>
                      </Button>
                    </div>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>

            <!-- Card View -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <Card v-for="teacher in paginatedTeachers" :key="teacher.id" class="hover:shadow-md transition-shadow">
                <CardContent class="p-6">
                  <div class="flex items-start justify-between mb-4">
                    <div class="flex items-center space-x-3">
                      <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                      <span class="text-lg font-medium text-blue-600">
                        {{ teacher.firstName[0] }}{{ teacher.lastName[0] }}
                      </span>
                      </div>
                      <div>
                        <h3 class="text-lg font-semibold text-gray-900">
                          {{ teacher.firstName }} {{ teacher.lastName }}
                        </h3>
                        <p class="text-sm text-gray-500">{{ teacher.employeeId }}</p>
                      </div>
                    </div>
                    <span
                        class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                        :class="getStatusClass(teacher.status)"
                    >
                    {{ teacher.status }}
                  </span>
                  </div>

                  <div class="space-y-2 mb-4">
                    <div class="flex items-center text-sm text-gray-600">
                      <School class="w-4 h-4 mr-2"/>
                      {{ teacher.schoolName }}
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <BookOpen class="w-4 h-4 mr-2"/>
                      {{ teacher.primarySubject }} - {{ teacher.gradeLevel }}
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <Mail class="w-4 h-4 mr-2"/>
                      {{ teacher.email }}
                    </div>
                    <div class="flex items-center text-sm text-gray-600">
                      <Calendar class="w-4 h-4 mr-2"/>
                      Started {{ formatDate(teacher.startDate) }}
                    </div>
                  </div>

                  <div class="flex items-center justify-between pt-4 border-t">
                    <span class="text-sm text-gray-500 capitalize">{{ teacher.employmentType }}</span>
                    <div class="flex items-center space-x-1">
                      <Button variant="ghost" size="sm" @click="viewTeacher(teacher)">
                        <Eye class="w-4 h-4"/>
                      </Button>
                      <Button variant="ghost" size="sm" @click="editTeacher(teacher)">
                        <Edit class="w-4 h-4"/>
                      </Button>
                      <Button variant="ghost" size="sm" @click="deleteTeacher(teacher)"
                              class="text-red-600 hover:text-red-800">
                        <Trash2 class="w-4 h-4"/>
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <!-- Pagination -->
            <div class="flex items-center justify-between mt-6 pt-6 border-t">
              <div class="text-sm text-gray-700">
                Showing {{ ((currentPage - 1) * itemsPerPage) + 1 }} to
                {{ Math.min(currentPage * itemsPerPage, filteredTeachers.length) }} of {{ filteredTeachers.length }}
                results
              </div>
              <div class="flex items-center space-x-2">
                <Button
                    variant="outline"
                    size="sm"
                    @click="currentPage--"
                    :disabled="currentPage === 1"
                >
                  <ChevronLeft class="w-4 h-4"/>
                  Previous
                </Button>

                <div class="flex items-center space-x-1">
                  <Button
                      v-for="page in visiblePages"
                      :key="page"
                      :variant="page === currentPage ? 'default' : 'outline'"
                      size="sm"
                      @click="currentPage = page"
                      class="w-8 h-8 p-0"
                  >
                    {{ page }}
                  </Button>
                </div>

                <Button
                    variant="outline"
                    size="sm"
                    @click="currentPage++"
                    :disabled="currentPage === totalPages"
                >
                  Next
                  <ChevronRight class="w-4 h-4"/>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </main>

      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <Card class="w-full max-w-md mx-4">
          <CardContent class="p-6">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mr-4">
                <AlertTriangle class="w-6 h-6 text-red-600"/>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">Delete Teacher</h3>
                <p class="text-sm text-gray-600">This action cannot be undone</p>
              </div>
            </div>
            <p class="text-gray-700 mb-6">
              Are you sure you want to delete <strong>{{ teacherToDelete?.firstName }} {{
                teacherToDelete?.lastName
              }}</strong>?
              This will permanently remove their record from the system.
            </p>
            <div class="flex space-x-3">
              <Button variant="outline" @click="showDeleteModal = false" class="flex-1">
                Cancel
              </Button>
              <Button @click="confirmDelete" class="flex-1 bg-red-600 hover:bg-red-700">
                Delete Teacher
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </OrgDashboardLayout>
  </div>
</template>

<script setup lang="ts">
import {ref, computed, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from '@/components/ui/card'
import {Button} from '@/components/ui/button'
import {Input} from '@/components/ui/input'
import {Select, SelectContent, SelectItem, SelectTrigger, SelectValue} from '@/components/ui/select'
import {
  ArrowLeft, Users, UserPlus, Download, Search, X, Grid, Eye, Edit, Trash2,
  ArrowUpDown, ChevronLeft, ChevronRight, UserCheck, School, TrendingUp,
  BookOpen, Mail, Calendar, AlertTriangle
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

// State
const searchQuery = ref('')
const selectedSchool = ref('all')
const selectedSubject = ref('all')
const selectedStatus = ref('all')
const viewMode = ref('table')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const sortField = ref('name')
const sortDirection = ref('asc')
const showDeleteModal = ref(false)
const teacherToDelete = ref(null)

// Stats
const stats = ref({
  total: 24,
  active: 22,
  schools: 5,
  newThisMonth: 3
})

// Mock data
const schools = ref([
  {id: 'school-001', name: 'Lincoln Elementary School'},
  {id: 'school-002', name: 'Washington Middle School'},
  {id: 'school-003', name: 'Roosevelt High School'},
  {id: 'school-004', name: 'Jefferson Academy'},
  {id: 'school-005', name: 'Madison Charter School'}
])

const subjects = ref([
  'Mathematics', 'English Language Arts', 'Science', 'Social Studies',
  'Physical Education', 'Art', 'Music', 'Computer Science'
])

const teachers = ref([
  {
    id: 'T001',
    firstName: 'Sarah',
    lastName: 'Johnson',
    email: 'sarah.johnson@lincoln.edu',
    phone: '+1 (555) 123-4567',
    employeeId: 'EMP-2024-001',
    schoolId: 'school-001',
    schoolName: 'Lincoln Elementary School',
    primarySubject: 'Mathematics',
    gradeLevel: '3rd Grade',
    employmentType: 'full-time',
    qualification: 'master',
    experience: 8,
    startDate: '2024-01-15',
    status: 'active'
  },
  {
    id: 'T002',
    firstName: 'Michael',
    lastName: 'Chen',
    email: 'michael.chen@washington.edu',
    phone: '+1 (555) 234-5678',
    employeeId: 'EMP-2024-002',
    schoolId: 'school-002',
    schoolName: 'Washington Middle School',
    primarySubject: 'Science',
    gradeLevel: '7th Grade',
    employmentType: 'full-time',
    qualification: 'bachelor',
    experience: 5,
    startDate: '2024-02-01',
    status: 'active'
  },
  {
    id: 'T003',
    firstName: 'Emily',
    lastName: 'Rodriguez',
    email: 'emily.rodriguez@roosevelt.edu',
    phone: '+1 (555) 345-6789',
    employeeId: 'EMP-2024-003',
    schoolId: 'school-003',
    schoolName: 'Roosevelt High School',
    primarySubject: 'English Language Arts',
    gradeLevel: '10th Grade',
    employmentType: 'full-time',
    qualification: 'master',
    experience: 12,
    startDate: '2023-08-20',
    status: 'active'
  },
  {
    id: 'T004',
    firstName: 'David',
    lastName: 'Wilson',
    email: 'david.wilson@jefferson.edu',
    phone: '+1 (555) 456-7890',
    employeeId: 'EMP-2024-004',
    schoolId: 'school-004',
    schoolName: 'Jefferson Academy',
    primarySubject: 'Social Studies',
    gradeLevel: '8th Grade',
    employmentType: 'part-time',
    qualification: 'bachelor',
    experience: 3,
    startDate: '2024-03-10',
    status: 'pending'
  },
  {
    id: 'T005',
    firstName: 'Lisa',
    lastName: 'Anderson',
    email: 'lisa.anderson@madison.edu',
    phone: '+1 (555) 567-8901',
    employeeId: 'EMP-2024-005',
    schoolId: 'school-005',
    schoolName: 'Madison Charter School',
    primarySubject: 'Art',
    gradeLevel: 'Mixed Grades',
    employmentType: 'contract',
    qualification: 'diploma',
    experience: 15,
    startDate: '2023-09-05',
    status: 'active'
  }
])

// Computed properties
const filteredTeachers = computed(() => {
  let filtered = teachers.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(teacher =>
        teacher.firstName.toLowerCase().includes(query) ||
        teacher.lastName.toLowerCase().includes(query) ||
        teacher.email.toLowerCase().includes(query) ||
        teacher.employeeId.toLowerCase().includes(query)
    )
  }

  // School filter
  if (selectedSchool.value !== 'all') {
    filtered = filtered.filter(teacher => teacher.schoolId === selectedSchool.value)
  }

  // Subject filter
  if (selectedSubject.value !== 'all') {
    filtered = filtered.filter(teacher => teacher.primarySubject === selectedSubject.value)
  }

  // Status filter
  if (selectedStatus.value !== 'all') {
    filtered = filtered.filter(teacher => teacher.status === selectedStatus.value)
  }

  // Sort
  filtered.sort((a, b) => {
    let aValue, bValue

    switch (sortField.value) {
      case 'name':
        aValue = `${a.firstName} ${a.lastName}`
        bValue = `${b.firstName} ${b.lastName}`
        break
      case 'school':
        aValue = a.schoolName
        bValue = b.schoolName
        break
      case 'startDate':
        aValue = new Date(a.startDate)
        bValue = new Date(b.startDate)
        break
      default:
        aValue = a[sortField.value]
        bValue = b[sortField.value]
    }

    if (sortDirection.value === 'asc') {
      return aValue < bValue ? -1 : aValue > bValue ? 1 : 0
    } else {
      return aValue > bValue ? -1 : aValue < bValue ? 1 : 0
    }
  })

  return filtered
})

const totalPages = computed(() => Math.ceil(filteredTeachers.value.length / itemsPerPage.value))

const paginatedTeachers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredTeachers.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const total = totalPages.value
  const current = currentPage.value

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    } else if (current >= total - 3) {
      pages.push(1, '...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1, '...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...', total)
    }
  }

  return pages.filter(page => page !== '...' || pages.indexOf(page) === pages.lastIndexOf(page))
})

// Methods
const sortBy = (field: string) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortDirection.value = 'asc'
  }
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedSchool.value = 'all'
  selectedSubject.value = 'all'
  selectedStatus.value = 'all'
  currentPage.value = 1
}

const toggleView = () => {
  viewMode.value = viewMode.value === 'table' ? 'card' : 'table'
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'active':
      return 'bg-green-100 text-green-800'
    case 'inactive':
      return 'bg-gray-100 text-gray-800'
    case 'pending':
      return 'bg-yellow-100 text-yellow-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const viewTeacher = (teacher: any) => {
  console.log('View teacher:', teacher)
  // Implement view teacher functionality
}

const editTeacher = (teacher: any) => {
  console.log('Edit teacher:', teacher)
  // Implement edit teacher functionality
}

const deleteTeacher = (teacher: any) => {
  teacherToDelete.value = teacher
  showDeleteModal.value = true
}

const confirmDelete = () => {
  if (teacherToDelete.value) {
    const index = teachers.value.findIndex(t => t.id === teacherToDelete.value.id)
    if (index > -1) {
      teachers.value.splice(index, 1)
      stats.value.total--
      if (teacherToDelete.value.status === 'active') {
        stats.value.active--
      }
    }
  }
  showDeleteModal.value = false
  teacherToDelete.value = null
}

const exportTeachers = () => {
  console.log('Export teachers')
  // Implement export functionality
}

onMounted(() => {
  console.log('Teachers list mounted')
})
</script>

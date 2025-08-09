<template>
  <div class="min-h-screen bg-gray-100 flex page-font">
    <!-- Parent Navbar -->
    <ParentNavbar :page-title="getPageTitle()" />

    <!-- Main Content -->
    <div class="flex-1 lg:ml-64">
      <!-- Mobile Header Spacing -->
      <div class="h-16 lg:h-0"></div>

      <!-- Page Content -->
      <div class="p-6">
        <!-- Dashboard Page -->
        <div v-if="currentPage === 'dashboard'">
          <!-- Header -->
          <div class="bg-white rounded-[20px] p-6 mb-6 shadow">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">Alex's Weekly Progress Report</h1>
            <p class="text-gray-600">Week of Dec 18 - Dec 24 • 4h 32m of learning</p>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-blue-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">+3 this week</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">12</h3>
              <p class="text-gray-600 text-sm">Lessons Completed</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-yellow-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">+380 pts</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">2450</h3>
              <p class="text-gray-600 text-sm">Total XP Points</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-purple-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">+2 new</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">15</h3>
              <p class="text-gray-600 text-sm">Badges Earned</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center justify-between mb-3">
                <div class="bg-orange-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 18.657A8 8 0 016.343 7.343S7 9 9 10c0-2 .5-5 2.986-7C14 5 16.09 5.777 17.656 7.343A7.975 7.975 0 0120 13a7.975 7.975 0 01-2.343 5.657z"></path>
                  </svg>
                </div>
                <span class="text-sm font-medium text-blue-600 bg-blue-100 px-2 py-1 rounded-full">Active</span>
              </div>
              <h3 class="text-2xl font-bold text-gray-800">7</h3>
              <p class="text-gray-600 text-sm">Day Streak</p>
            </div>
          </div>

          <!-- Topics Learned -->
          <div class="bg-white rounded-[20px] p-6 shadow mb-6">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Topics Learned This Week</h2>
            <div class="space-y-3">
              <div v-for="topic in topics" :key="topic.id" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div class="flex items-center gap-3">
                  <div class="bg-blue-100 p-2 rounded-lg">
                    <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <h4 class="font-medium text-gray-800">{{ topic.name }}</h4>
                    <p class="text-sm text-gray-600">{{ topic.subject }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-sm font-medium text-gray-800">{{ topic.progress }}% complete</div>
                  <div class="text-xs text-gray-500">{{ topic.timeSpent }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              @click="congratulateChild"
              class="bg-green-500 hover:bg-green-600 text-white font-medium py-3 px-8 rounded-[20px] shadow-lg transition-colors flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
              </svg>
              Congratulate Alex
            </button>
            <button 
              @click="encourageMoreLearning"
              class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-8 rounded-[20px] shadow-lg transition-colors flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
              </svg>
              Encourage More Learning
            </button>
          </div>
        </div>

        <!-- Lessons Page -->
        <div v-else-if="currentPage === 'lessons'">
          <!-- Header -->
          <div class="bg-white rounded-[20px] p-6 mb-6 shadow">
            <div class="flex items-center justify-between">
              <div>
                <h1 class="text-3xl font-bold text-gray-800 mb-2">Weekly Lessons Overview</h1>
                <p class="text-gray-600">All lessons taught from Monday to Friday • Week of Dec 18 - Dec 22</p>
              </div>
              <div class="bg-blue-100 p-3 rounded-[20px]">
                <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
              </div>
            </div>
          </div>

          <!-- Weekly Summary Stats -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center gap-3 mb-3">
                <div class="bg-green-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"></path>
                  </svg>
                </div>
                <h3 class="font-semibold text-gray-800">Total Lessons</h3>
              </div>
              <p class="text-3xl font-bold text-gray-800">{{ getTotalLessons() }}</p>
              <p class="text-sm text-gray-600">Across all subjects</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center gap-3 mb-3">
                <div class="bg-purple-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                  </svg>
                </div>
                <h3 class="font-semibold text-gray-800">Subjects Covered</h3>
              </div>
              <p class="text-3xl font-bold text-gray-800">{{ getUniqueSubjects() }}</p>
              <p class="text-sm text-gray-600">Different subjects</p>
            </div>

            <div class="bg-white rounded-[20px] p-6 shadow">
              <div class="flex items-center gap-3 mb-3">
                <div class="bg-orange-100 p-2 rounded-lg">
                  <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <h3 class="font-semibold text-gray-800">Total Time</h3>
              </div>
              <p class="text-3xl font-bold text-gray-800">{{ getTotalTime() }}</p>
              <p class="text-sm text-gray-600">Learning time</p>
            </div>
          </div>

          <!-- Daily Lessons Grid -->
          <div class="space-y-6">
            <div v-for="day in weeklyLessons" :key="day.day" class="bg-white rounded-[20px] shadow">
              <!-- Day Header -->
              <div class="bg-gradient-to-r from-blue-500 to-indigo-600 text-white p-4 rounded-[20px]">
                <div class="flex items-center justify-between">
                  <div>
                    <h2 class="text-xl font-bold">{{ day.day }}</h2>
                    <p class="text-blue-100">{{ day.date }} • {{ day.lessons.length }} lessons</p>
                  </div>
                  <div class="">
                    <span class="text-sm font-medium">{{ getDayTotalTime(day.lessons) }}</span>
                  </div>
                </div>
              </div>

              <!-- Lessons List -->
              <div class="p-6">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  <div v-for="lesson in day.lessons" :key="lesson.id" class="border border-gray-200 rounded-[20px] p-4 hover:shadow-md transition-shadow">
                    <div class="flex items-start justify-between mb-3">
                      <div class="flex items-center gap-3">
                        <div :class="getSubjectColor(lesson.subject)" class="p-2 rounded-lg">
                          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getSubjectIcon(lesson.subject)"></path>
                          </svg>
                        </div>
                        <div>
                          <h3 class="font-semibold text-gray-800">{{ lesson.title }}</h3>
                          <p class="text-sm text-gray-600">{{ lesson.subject }}</p>
                        </div>
                      </div>
                      <div class="text-right">
                        <div :class="getStatusColor(lesson.status)" class="px-2 py-1 rounded-full text-xs font-medium mb-1">
                          {{ lesson.status }}
                        </div>
                        <p class="text-xs text-gray-500">{{ lesson.duration }}</p>
                      </div>
                    </div>

                    <div class="mb-3">
                      <p class="text-sm text-gray-700 mb-2">{{ lesson.description }}</p>
                      <div class="flex items-center gap-4 text-xs text-gray-500">
                        <span>⏰ {{ lesson.time }}</span>
                        <span>📊 {{ lesson.difficulty }}</span>
                        <span>🎯 {{ lesson.score }}%</span>
                      </div>
                    </div>

                    <!-- Progress Bar -->
                    <div class="mb-3">
                      <div class="flex items-center justify-between mb-1">
                        <span class="text-xs text-gray-600">Progress</span>
                        <span class="text-xs text-gray-600">{{ lesson.progress }}%</span>
                      </div>
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          :class="getProgressColor(lesson.progress)"
                          class="h-2 rounded-full transition-all duration-300"
                          :style="{ width: `${lesson.progress}%` }"
                        ></div>
                      </div>
                    </div>

                    <!-- Skills Learned -->
                    <div v-if="lesson.skills && lesson.skills.length > 0">
                      <p class="text-xs text-gray-600 mb-2">Skills Learned:</p>
                      <div class="flex flex-wrap gap-1">
                        <span 
                          v-for="skill in lesson.skills" 
                          :key="skill"
                          class="bg-blue-50 text-blue-700 px-2 py-1 rounded text-xs"
                        >
                          {{ skill }}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- No lessons message -->
                <div v-if="day.lessons.length === 0" class="text-center py-8 text-gray-500">
                  <svg class="w-12 h-12 mx-auto mb-3 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                  </svg>
                  <p>No lessons scheduled for this day</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Lesson Updates Page -->
        <div v-else-if="currentPage === 'lesson-updates'" class="bg-white rounded-[20px] p-6 shadow">
          <div class="text-center py-12">
            <div class="bg-blue-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM4 1h11l5 5v4.5"></path>
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-800 mb-2">Lesson Updates</h2>
            <p class="text-gray-600 mb-4">Stay updated with Alex's latest learning progress and lesson completions.</p>
            <p class="text-gray-500">This page is coming soon...</p>
          </div>
        </div>

        <!-- SafeSteps Page -->
        <div v-else-if="currentPage === 'safesteps'" class="bg-white rounded-[20px] p-6 shadow">
          <div class="text-center py-12">
            <!-- <div class="bg-green-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5-6a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div> -->
            <h2 class="text-2xl font-bold text-gray-800 mb-2">SafeSteps</h2>
            <p class="text-gray-600 mb-4">Monitor Alex's online safety and digital wellness while learning.</p>
            <p class="text-gray-500">coming soon...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modals
    <div v-if="showCongratulationsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="showCongratulationsModal = false">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl" @click.stop>
        <div class="text-center">
          <div class="bg-yellow-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"></path>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Congratulations Sent!</h3>
          <p class="text-gray-600 mb-4">Your encouraging message has been sent to Alex. Keep supporting their learning journey!</p>
          <button 
            @click="showCongratulationsModal = false"
            class="bg-green-500 text-white font-medium py-2 px-6 rounded-lg hover:bg-green-600 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <div v-if="showEncouragementModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="showEncouragementModal = false">
      <div class="bg-white rounded-2xl p-6 max-w-md w-full shadow-2xl" @click.stop>
        <div class="text-center">
          <div class="bg-blue-500 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">Encouragement Sent!</h3>
          <p class="text-gray-600 mb-4">Alex will receive a motivational message to continue their amazing learning progress!</p>
          <button 
            @click="showEncouragementModal = false"
            class="bg-blue-500 text-white font-medium py-2 px-6 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ParentNavbar from "@/components/partials/ParentNavbar.vue"

// Reactive data
const showCongratulationsModal = ref(false)
const showEncouragementModal = ref(false)
const currentPage = ref('dashboard')

// Router
const route = useRoute()
const router = useRouter()

// Methods
const getPageTitle = () => {
  switch (currentPage.value) {
    case 'dashboard':
      return 'Dashboard'
    case 'lessons':
      return 'Lessons'
    case 'lesson-updates':
      return 'Lesson Updates'
    case 'safesteps':
      return 'SafeSteps'
    default:
      return 'Parent Portal'
  }
}

const congratulateChild = () => {
  showCongratulationsModal.value = true
}

const encourageMoreLearning = () => {
  showEncouragementModal.value = true
}

// Lesson helper methods
const getTotalLessons = () => {
  return weeklyLessons.reduce((total, day) => total + day.lessons.length, 0)
}

const getUniqueSubjects = () => {
  const subjects = new Set()
  weeklyLessons.forEach(day => {
    day.lessons.forEach(lesson => subjects.add(lesson.subject))
  })
  return subjects.size
}

const getTotalTime = () => {
  let totalMinutes = 0
  weeklyLessons.forEach(day => {
    day.lessons.forEach(lesson => {
      const minutes = parseInt(lesson.duration.replace('min', ''))
      totalMinutes += minutes
    })
  })
  const hours = Math.floor(totalMinutes / 60)
  const minutes = totalMinutes % 60
  return `${hours}h ${minutes}m`
}

const getDayTotalTime = (lessons) => {
  let totalMinutes = 0
  lessons.forEach(lesson => {
    const minutes = parseInt(lesson.duration.replace('min', ''))
    totalMinutes += minutes
  })
  const hours = Math.floor(totalMinutes / 60)
  const minutes = totalMinutes % 60
  return hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`
}

const getSubjectColor = (subject) => {
  const colors = {
    'Mathematics': 'bg-blue-500',
    'Science': 'bg-green-500',
    'Reading': 'bg-purple-500',
    'Language Arts': 'bg-pink-500',
    'History': 'bg-orange-500',
    'Art': 'bg-red-500'
  }
  return colors[subject] || 'bg-gray-500'
}

const getSubjectIcon = (subject) => {
  const icons = {
    'Mathematics': 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z',
    'Science': 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547A8.014 8.014 0 004 21h16a8.014 8.014 0 00-.244-5.572zM8 3a5 5 0 015 5v5H8V8a5 5 0 015-5z',
    'Reading': 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253',
    'Language Arts': 'M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z',
    'History': 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
    'Art': 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zM7 3H5a2 2 0 00-2 2v12a4 4 0 004 4h2a2 2 0 002-2V5a2 2 0 00-2-2z'
  }
  return icons[subject] || 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'
}

const getStatusColor = (status) => {
  const colors = {
    'Completed': 'bg-green-100 text-green-800',
    'In Progress': 'bg-yellow-100 text-yellow-800',
    'Not Started': 'bg-gray-100 text-gray-800'
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}

const getProgressColor = (progress) => {
  if (progress >= 80) return 'bg-green-500'
  if (progress >= 60) return 'bg-yellow-500'
  if (progress >= 40) return 'bg-orange-500'
  return 'bg-red-500'
}

// Sample data
const topics = [
  {
    id: 1,
    name: 'Multiplication Tables',
    subject: 'Mathematics',
    progress: 85,
    timeSpent: '45m'
  },
  {
    id: 2,
    name: 'Solar System',
    subject: 'Science',
    progress: 92,
    timeSpent: '38m'
  },
  {
    id: 3,
    name: 'Story Comprehension',
    subject: 'Reading',
    progress: 78,
    timeSpent: '52m'
  },
  {
    id: 4,
    name: 'Basic Chemistry',
    subject: 'Science',
    progress: 65,
    timeSpent: '29m'
  }
]

// Weekly lessons data
const weeklyLessons = [
  {
    day: 'Monday',
    date: 'Dec 18, 2023',
    lessons: [
      {
        id: 1,
        title: 'Multiplication Tables (6-8)',
        subject: 'Mathematics',
        description: 'Learning multiplication tables for numbers 6, 7, and 8 with interactive exercises.',
        time: '9:00 AM',
        duration: '45min',
        difficulty: 'Medium',
        status: 'Completed',
        progress: 95,
        score: 88,
        skills: ['Multiplication', 'Mental Math', 'Pattern Recognition']
      },
      {
        id: 2,
        title: 'Plant Life Cycles',
        subject: 'Science',
        description: 'Understanding how plants grow from seeds to mature plants.',
        time: '10:30 AM',
        duration: '35min',
        difficulty: 'Easy',
        status: 'Completed',
        progress: 100,
        score: 92,
        skills: ['Biology', 'Life Cycles', 'Observation']
      },
      {
        id: 3,
        title: 'Reading Comprehension - Adventure Stories',
        subject: 'Reading',
        description: 'Reading and analyzing short adventure stories for main ideas.',
        time: '2:00 PM',
        duration: '40min',
        difficulty: 'Medium',
        status: 'Completed',
        progress: 85,
        score: 90,
        skills: ['Reading', 'Comprehension', 'Analysis']
      }
    ]
  },
  {
    day: 'Tuesday',
    date: 'Dec 19, 2023',
    lessons: [
      {
        id: 4,
        title: 'Fractions Introduction',
        subject: 'Mathematics',
        description: 'Basic understanding of fractions, halves, quarters, and thirds.',
        time: '9:00 AM',
        duration: '50min',
        difficulty: 'Medium',
        status: 'Completed',
        progress: 78,
        score: 85,
        skills: ['Fractions', 'Visual Math', 'Problem Solving']
      },
      {
        id: 5,
        title: 'Weather Patterns',
        subject: 'Science',
        description: 'Learning about different types of weather and how they form.',
        time: '10:45 AM',
        duration: '30min',
        difficulty: 'Easy',
        status: 'Completed',
        progress: 90,
        score: 94,
        skills: ['Meteorology', 'Observation', 'Data Analysis']
      },
      {
        id: 6,
        title: 'Creative Writing - My Pet',
        subject: 'Language Arts',
        description: 'Writing a descriptive paragraph about a favorite pet.',
        time: '1:30 PM',
        duration: '35min',
        difficulty: 'Medium',
        status: 'In Progress',
        progress: 60,
        score: 0,
        skills: ['Writing', 'Creativity', 'Grammar']
      },
      {
        id: 7,
        title: 'Ancient Egypt Overview',
        subject: 'History',
        description: 'Introduction to ancient Egyptian civilization and pyramids.',
        time: '3:00 PM',
        duration: '25min',
        difficulty: 'Easy',
        status: 'Completed',
        progress: 100,
        score: 96,
        skills: ['History', 'Culture', 'Geography']
      }
    ]
  },
  {
    day: 'Wednesday',
    date: 'Dec 20, 2023',
    lessons: [
      {
        id: 8,
        title: 'Division Basics',
        subject: 'Mathematics',
        description: 'Introduction to division as the opposite of multiplication.',
        time: '9:15 AM',
        duration: '45min',
        difficulty: 'Medium',
        status: 'Completed',
        progress: 82,
        score: 87,
        skills: ['Division', 'Inverse Operations', 'Problem Solving']
      },
      {
        id: 9,
        title: 'Animal Habitats',
        subject: 'Science',
        description: 'Exploring different animal habitats and adaptations.',
        time: '11:00 AM',
        duration: '40min',
        difficulty: 'Easy',
        status: 'Completed',
        progress: 95,
        score: 91,
        skills: ['Biology', 'Ecosystems', 'Animal Behavior']
      },
      {
        id: 10,
        title: 'Poetry Reading - Nature Poems',
        subject: 'Reading',
        description: 'Reading and understanding nature-themed poetry.',
        time: '2:15 PM',
        duration: '30min',
        difficulty: 'Medium',
        status: 'Completed',
        progress: 88,
        score: 89,
        skills: ['Poetry', 'Literary Analysis', 'Vocabulary']
      }
    ]
  },
  {
    day: 'Thursday',
    date: 'Dec 21, 2023',
    lessons: [
      {
        id: 11,
        title: 'Geometry Shapes',
        subject: 'Mathematics',
        description: 'Identifying and properties of 2D shapes like triangles, squares, circles.',
        time: '9:00 AM',
        duration: '40min',
        difficulty: 'Easy',
        status: 'Completed',
        progress: 92,
        score: 93,
        skills: ['Geometry', 'Shape Recognition', 'Properties']
      },
      {
        id: 12,
        title: 'Simple Machines',
        subject: 'Science',
        description: 'Understanding levers, pulleys, and inclined planes.',
        time: '10:30 AM',
        duration: '35min',
        difficulty: 'Medium',
        status: 'In Progress',
        progress: 45,
        score: 0,
        skills: ['Physics', 'Engineering', 'Problem Solving']
      },
      {
        id: 13,
        title: 'Spelling Practice - Long Vowels',
        subject: 'Language Arts',
        description: 'Practicing spelling words with long vowel sounds.',
        time: '1:45 PM',
        duration: '25min',
        difficulty: 'Easy',
        status: 'Completed',
        progress: 100,
        score: 95,
        skills: ['Spelling', 'Phonics', 'Vocabulary']
      },
      {
        id: 14,
        title: 'Watercolor Techniques',
        subject: 'Art',
        description: 'Learning basic watercolor painting techniques and color mixing.',
        time: '3:15 PM',
        duration: '45min',
        difficulty: 'Medium',
        status: 'Completed',
        progress: 75,
        score: 88,
        skills: ['Art', 'Color Theory', 'Creativity']
      }
    ]
  },
  {
    day: 'Friday',
    date: 'Dec 22, 2023',
    lessons: [
      {
        id: 15,
        title: 'Word Problems Practice',
        subject: 'Mathematics',
        description: 'Solving real-world math problems using addition and subtraction.',
        time: '9:30 AM',
        duration: '50min',
        difficulty: 'Medium',
        status: 'Not Started',
        progress: 0,
        score: 0,
        skills: ['Problem Solving', 'Critical Thinking', 'Application']
      },
      {
        id: 16,
        title: 'Solar System Review',
        subject: 'Science',
        description: 'Review of planets, their order, and characteristics.',
        time: '11:15 AM',
        duration: '30min',
        difficulty: 'Easy',
        status: 'Not Started',
        progress: 0,
        score: 0,
        skills: ['Astronomy', 'Memory', 'Facts']
      },
      {
        id: 17,
        title: 'Book Report Presentation',
        subject: 'Reading',
        description: 'Presenting a book report on a chosen adventure book.',
        time: '2:00 PM',
        duration: '35min',
        difficulty: 'Hard',
        status: 'Not Started',
        progress: 0,
        score: 0,
        skills: ['Presentation', 'Public Speaking', 'Analysis']
      }
    ]
  }
]
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

.page-font {
  font-family: 'Montserrat', sans-serif;
}
</style>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-4">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="bg-white rounded-3xl shadow-xl p-6 mb-8 border-l-8 border-blue-500">
        <div class="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 class="font-fancy text-4xl font-bold text-gray-800 mb-2">
              CoolKids Survey Report
            </h1>
            <p class="text-lg text-gray-600">
              📊 Class Survey Results & Analytics Dashboard
            </p>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-center">
              <div class="text-3xl font-bold text-blue-600">{{ totalResponses }}</div>
              <div class="text-sm text-gray-500">Total Responses</div>
            </div>
            <button
              @click="exportData"
              class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium transition-all hover:scale-105 shadow-lg"
            >
              📥 Export Data
            </button>
          </div>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-gradient-to-r from-purple-500 to-purple-600 rounded-2xl p-6 text-white shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-purple-100 text-sm">Average Age</p>
              <p class="text-3xl font-bold">{{ averageAge }} years</p>
            </div>
            <div class="text-4xl">🎂</div>
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-green-500 to-green-600 rounded-2xl p-6 text-white shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-green-100 text-sm">Most Popular Subject</p>
              <p class="text-xl font-bold">{{ mostPopularSubject }}</p>
            </div>
            <div class="text-4xl">📚</div>
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-orange-500 to-orange-600 rounded-2xl p-6 text-white shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-orange-100 text-sm">Most Common Hobby</p>
              <p class="text-xl font-bold">{{ mostCommonHobby }}</p>
            </div>
            <div class="text-4xl">🎨</div>
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-pink-500 to-pink-600 rounded-2xl p-6 text-white shadow-xl">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-pink-100 text-sm">Favorite Color</p>
              <p class="text-xl font-bold">{{ mostPopularColor }}</p>
            </div>
            <div class="text-4xl">🌈</div>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Age Distribution -->
        <div class="bg-white rounded-3xl shadow-xl p-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-3">📊</span> Age Distribution
          </h3>
          <div class="space-y-3">
            <div v-for="(count, age) in ageDistribution" :key="age" class="flex items-center">
              <span class="w-16 text-sm font-medium text-gray-600">{{ age }} yrs</span>
              <div class="flex-1 mx-4">
                <div class="bg-gray-200 rounded-full h-6 relative overflow-hidden">
                  <div 
                    class="bg-gradient-to-r from-blue-400 to-blue-600 h-full rounded-full transition-all duration-1000 flex items-center justify-end pr-2"
                    :style="{ width: `${(count / totalResponses) * 100}%` }"
                  >
                    <span class="text-white text-xs font-bold" v-if="count > 0">{{ count }}</span>
                  </div>
                </div>
              </div>
              <span class="text-sm text-gray-500 w-12">{{ Math.round((count / totalResponses) * 100) }}%</span>
            </div>
          </div>
        </div>

        <!-- Favorite Subjects -->
        <div class="bg-white rounded-3xl shadow-xl p-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-3">📚</span> Favorite Subjects
          </h3>
          <div class="space-y-3">
            <div v-for="(data, subject) in subjectData" :key="subject" class="flex items-center">
              <span class="text-2xl mr-3">{{ data.emoji }}</span>
              <span class="w-20 text-sm font-medium text-gray-600 capitalize">{{ subject }}</span>
              <div class="flex-1 mx-4">
                <div class="bg-gray-200 rounded-full h-6 relative overflow-hidden">
                  <div 
                    class="h-full rounded-full transition-all duration-1000 flex items-center justify-end pr-2"
                    :class="data.color"
                    :style="{ width: `${(data.count / totalResponses) * 100}%` }"
                  >
                    <span class="text-white text-xs font-bold" v-if="data.count > 0">{{ data.count }}</span>
                  </div>
                </div>
              </div>
              <span class="text-sm text-gray-500 w-12">{{ Math.round((data.count / totalResponses) * 100) }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Learning Styles & Colors -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Learning Styles -->
        <div class="bg-white rounded-3xl shadow-xl p-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-3">🧠</span> Learning Styles
          </h3>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="(data, style) in learningStyleData" :key="style" 
                 class="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-2xl p-4 text-center border-2 border-indigo-200">
              <div class="text-3xl mb-2">{{ data.emoji }}</div>
              <div class="text-lg font-bold text-indigo-800">{{ data.count }}</div>
              <div class="text-sm text-indigo-600 capitalize">{{ style.replace('-', ' ') }}</div>
            </div>
          </div>
        </div>

        <!-- Favorite Colors -->
        <div class="bg-white rounded-3xl shadow-xl p-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-3">🎨</span> Favorite Colors
          </h3>
          <div class="grid grid-cols-4 gap-3">
            <div v-for="(data, color) in colorData" :key="color" 
                 class="text-center p-3 rounded-2xl bg-gray-50 border-2 border-gray-200">
              <div class="w-12 h-12 rounded-full mx-auto mb-2 border-4 border-white shadow-lg" 
                   :class="data.class"></div>
              <div class="text-lg font-bold text-gray-800">{{ data.count }}</div>
              <div class="text-xs text-gray-600 capitalize">{{ color }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Dream Jobs & Animals -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <!-- Popular Dream Jobs -->
        <div class="bg-white rounded-3xl shadow-xl p-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-3">🚀</span> Dream Jobs
          </h3>
          <div class="space-y-3">
            <div v-for="job in topDreamJobs" :key="job.name" 
                 class="flex items-center justify-between p-3 bg-gradient-to-r from-emerald-50 to-emerald-100 rounded-xl border border-emerald-200">
              <span class="font-medium text-emerald-800">{{ job.name }}</span>
              <span class="bg-emerald-500 text-white px-3 py-1 rounded-full text-sm font-bold">{{ job.count }}</span>
            </div>
          </div>
        </div>

        <!-- Favorite Animals -->
        <div class="bg-white rounded-3xl shadow-xl p-6">
          <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
            <span class="mr-3">🐾</span> Favorite Animals
          </h3>
          <div class="grid grid-cols-4 gap-3">
            <div v-for="(data, animal) in animalData" :key="animal" 
                 class="text-center p-3 rounded-2xl bg-gradient-to-br from-yellow-50 to-yellow-100 border-2 border-yellow-200">
              <div class="text-3xl mb-1">{{ data.emoji }}</div>
              <div class="text-lg font-bold text-yellow-800">{{ data.count }}</div>
              <div class="text-xs text-yellow-700 capitalize">{{ animal }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Superpowers -->
      <div class="bg-white rounded-3xl shadow-xl p-6 mb-8">
        <h3 class="text-2xl font-bold text-gray-800 mb-4 flex items-center">
          <span class="mr-3">⚡</span> Desired Superpowers
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="(data, power) in superpowerData" :key="power" 
               class="flex items-center p-4 bg-gradient-to-r from-red-50 to-red-100 rounded-2xl border-2 border-red-200">
            <span class="text-3xl mr-4">{{ data.emoji }}</span>
            <div class="flex-1">
              <div class="font-bold text-red-800 capitalize">{{ power.replace('-', ' ') }}</div>
              <div class="text-sm text-red-600">{{ data.count }} students</div>
            </div>
            <div class="text-2xl font-bold text-red-700">{{ data.count }}</div>
          </div>
        </div>
      </div>

      <!-- Individual Responses -->
      <div class="bg-white rounded-3xl shadow-xl p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-2xl font-bold text-gray-800 flex items-center">
            <span class="mr-3">👥</span> Individual Responses
          </h3>
          <div class="flex items-center gap-4">
            <select v-model="sortBy" class="px-4 py-2 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500">
              <option value="name">Sort by Name</option>
              <option value="age">Sort by Age</option>
              <option value="subject">Sort by Subject</option>
            </select>
            <button
              @click="showAllResponses = !showAllResponses"
              class="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-xl transition-all"
            >
              {{ showAllResponses ? 'Show Less' : 'Show All' }}
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="(response, index) in displayedResponses" :key="index" 
               class="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-5 border-2 border-gray-200 hover:border-blue-300 transition-all hover:shadow-lg">
            <div class="flex items-center justify-between mb-4">
              <h4 class="text-xl font-bold text-gray-800">{{ response.name }}</h4>
              <span class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                {{ response.age }} years
              </span>
            </div>
            
            <div class="space-y-3 text-sm">
              <div class="flex items-center">
                <span class="font-medium text-gray-600 w-20">Subject:</span>
                <span class="text-gray-800 capitalize">{{ response.favoriteSubject }}</span>
              </div>
              
              <div class="flex items-center">
                <span class="font-medium text-gray-600 w-20">Color:</span>
                <div class="flex items-center">
                  <div class="w-4 h-4 rounded-full mr-2" :class="getColorClass(response.favoriteColor)"></div>
                  <span class="text-gray-800 capitalize">{{ response.favoriteColor }}</span>
                </div>
              </div>
              
              <div class="flex items-center">
                <span class="font-medium text-gray-600 w-20">Animal:</span>
                <span class="text-gray-800 capitalize">{{ response.favoriteAnimal }}</span>
              </div>
              
              <div>
                <span class="font-medium text-gray-600">Dream Job:</span>
                <p class="text-gray-800 mt-1">{{ response.dreamJob }}</p>
              </div>
              
              <div>
                <span class="font-medium text-gray-600">Happiness:</span>
                <p class="text-gray-800 mt-1 text-xs leading-relaxed">{{ response.happiness.substring(0, 100) }}{{ response.happiness.length > 100 ? '...' : '' }}</p>
              </div>
            </div>
          </div>
        </div>

        <div v-if="!showAllResponses && surveyResponses.length > 6" class="text-center mt-6">
          <button
            @click="showAllResponses = true"
            class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl font-medium transition-all hover:scale-105"
          >
            View All {{ surveyResponses.length }} Responses
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'

const showAllResponses = ref(false)
const sortBy = ref('name')

// Mock survey data - in real app, this would come from an API
const surveyResponses = reactive([
  {
    name: 'Emma Johnson',
    age: 9,
    favoriteSubject: 'art',
    hobbies: ['drawing', 'reading', 'music'],
    learningStyle: 'visual',
    favoriteColor: 'purple',
    dreamJob: 'Artist',
    favoriteAnimal: 'cat',
    superpower: 'flying',
    happiness: 'Playing with my friends and drawing beautiful pictures makes me super happy!'
  },
  {
    name: 'Liam Smith',
    age: 10,
    favoriteSubject: 'science',
    hobbies: ['sports', 'building', 'games'],
    learningStyle: 'kinesthetic',
    favoriteColor: 'blue',
    dreamJob: 'Scientist',
    favoriteAnimal: 'dog',
    superpower: 'super-strength',
    happiness: 'I love doing experiments and playing soccer with my team!'
  },
  {
    name: 'Sophia Davis',
    age: 8,
    favoriteSubject: 'music',
    hobbies: ['music', 'dancing', 'reading'],
    learningStyle: 'auditory',
    favoriteColor: 'pink',
    dreamJob: 'Singer',
    favoriteAnimal: 'dolphin',
    superpower: 'telepathy',
    happiness: 'Singing songs and dancing makes my heart feel so joyful!'
  },
  {
    name: 'Noah Wilson',
    age: 11,
    favoriteSubject: 'math',
    hobbies: ['games', 'building', 'sports'],
    learningStyle: 'visual',
    favoriteColor: 'green',
    dreamJob: 'Video Game Designer',
    favoriteAnimal: 'tiger',
    superpower: 'time-travel',
    happiness: 'Creating cool things and solving puzzles is the best!'
  },
  {
    name: 'Ava Brown',
    age: 9,
    favoriteSubject: 'english',
    hobbies: ['reading', 'drawing', 'cooking'],
    learningStyle: 'reading',
    favoriteColor: 'yellow',
    dreamJob: 'Writer',
    favoriteAnimal: 'panda',
    superpower: 'invisible',
    happiness: 'Reading amazing stories and writing my own adventures!'
  },
  {
    name: 'Oliver Garcia',
    age: 10,
    favoriteSubject: 'pe',
    hobbies: ['sports', 'dancing', 'games'],
    learningStyle: 'kinesthetic',
    favoriteColor: 'red',
    dreamJob: 'Professional Soccer Player',
    favoriteAnimal: 'lion',
    superpower: 'super-strength',
    happiness: 'Running fast and scoring goals makes me feel amazing!'
  },
  {
    name: 'Isabella Martinez',
    age: 8,
    favoriteSubject: 'art',
    hobbies: ['drawing', 'music', 'cooking'],
    learningStyle: 'visual',
    favoriteColor: 'orange',
    dreamJob: 'Chef',
    favoriteAnimal: 'elephant',
    superpower: 'shape-shift',
    happiness: 'Making delicious food for my family and friends!'
  },
  {
    name: 'Ethan Anderson',
    age: 11,
    favoriteSubject: 'science',
    hobbies: ['building', 'reading', 'games'],
    learningStyle: 'kinesthetic',
    favoriteColor: 'teal',
    dreamJob: 'Engineer',
    favoriteAnimal: 'penguin',
    superpower: 'flying',
    happiness: 'Building robots and learning how things work!'
  }
])

const totalResponses = computed(() => surveyResponses.length)

const averageAge = computed(() => {
  const sum = surveyResponses.reduce((acc, response) => acc + response.age, 0)
  return Math.round(sum / totalResponses.value * 10) / 10
})

const ageDistribution = computed(() => {
  const distribution: Record<number, number> = {}
  surveyResponses.forEach(response => {
    distribution[response.age] = (distribution[response.age] || 0) + 1
  })
  return distribution
})

const subjectData = computed(() => {
  const subjects = {
    math: { count: 0, emoji: '🔢', color: 'bg-gradient-to-r from-blue-400 to-blue-600' },
    science: { count: 0, emoji: '🔬', color: 'bg-gradient-to-r from-green-400 to-green-600' },
    english: { count: 0, emoji: '📖', color: 'bg-gradient-to-r from-purple-400 to-purple-600' },
    art: { count: 0, emoji: '🎨', color: 'bg-gradient-to-r from-pink-400 to-pink-600' },
    music: { count: 0, emoji: '🎵', color: 'bg-gradient-to-r from-yellow-400 to-yellow-600' },
    pe: { count: 0, emoji: '⚽', color: 'bg-gradient-to-r from-orange-400 to-orange-600' }
  }
  
  surveyResponses.forEach(response => {
    if (subjects[response.favoriteSubject as keyof typeof subjects]) {
      subjects[response.favoriteSubject as keyof typeof subjects].count++
    }
  })
  
  return subjects
})

const mostPopularSubject = computed(() => {
  const subjects = subjectData.value
  let maxCount = 0
  let popular = ''
  
  Object.entries(subjects).forEach(([subject, data]) => {
    if (data.count > maxCount) {
      maxCount = data.count
      popular = subject
    }
  })
  
  return popular.charAt(0).toUpperCase() + popular.slice(1)
})

const mostCommonHobby = computed(() => {
  const hobbyCounts: Record<string, number> = {}
  
  surveyResponses.forEach(response => {
    response.hobbies.forEach(hobby => {
      hobbyCounts[hobby] = (hobbyCounts[hobby] || 0) + 1
    })
  })
  
  let maxCount = 0
  let commonHobby = ''
  
  Object.entries(hobbyCounts).forEach(([hobby, count]) => {
    if (count > maxCount) {
      maxCount = count
      commonHobby = hobby
    }
  })
  
  return commonHobby.charAt(0).toUpperCase() + commonHobby.slice(1)
})

const colorData = computed(() => {
  const colors = {
    red: { count: 0, class: 'bg-red-500' },
    blue: { count: 0, class: 'bg-blue-500' },
    green: { count: 0, class: 'bg-green-500' },
    yellow: { count: 0, class: 'bg-yellow-500' },
    purple: { count: 0, class: 'bg-purple-500' },
    pink: { count: 0, class: 'bg-pink-500' },
    orange: { count: 0, class: 'bg-orange-500' },
    teal: { count: 0, class: 'bg-teal-500' }
  }
  
  surveyResponses.forEach(response => {
    if (colors[response.favoriteColor as keyof typeof colors]) {
      colors[response.favoriteColor as keyof typeof colors].count++
    }
  })
  
  return colors
})

const mostPopularColor = computed(() => {
  const colors = colorData.value
  let maxCount = 0
  let popular = ''
  
  Object.entries(colors).forEach(([color, data]) => {
    if (data.count > maxCount) {
      maxCount = data.count
      popular = color
    }
  })
  
  return popular.charAt(0).toUpperCase() + popular.slice(1)
})

const learningStyleData = computed(() => {
  const styles = {
    visual: { count: 0, emoji: '👀' },
    auditory: { count: 0, emoji: '👂' },
    kinesthetic: { count: 0, emoji: '✋' },
    reading: { count: 0, emoji: '📖' }
  }
  
  surveyResponses.forEach(response => {
    if (styles[response.learningStyle as keyof typeof styles]) {
      styles[response.learningStyle as keyof typeof styles].count++
    }
  })
  
  return styles
})

const animalData = computed(() => {
  const animals = {
    dog: { count: 0, emoji: '🐕' },
    cat: { count: 0, emoji: '🐱' },
    elephant: { count: 0, emoji: '🐘' },
    lion: { count: 0, emoji: '🦁' },
    dolphin: { count: 0, emoji: '🐬' },
    panda: { count: 0, emoji: '🐼' },
    tiger: { count: 0, emoji: '🐅' },
    penguin: { count: 0, emoji: '🐧' }
  }
  
  surveyResponses.forEach(response => {
    if (animals[response.favoriteAnimal as keyof typeof animals]) {
      animals[response.favoriteAnimal as keyof typeof animals].count++
    }
  })
  
  return animals
})

const superpowerData = computed(() => {
  const powers = {
    flying: { count: 0, emoji: '🦅' },
    invisible: { count: 0, emoji: '👻' },
    'super-strength': { count: 0, emoji: '💪' },
    telepathy: { count: 0, emoji: '🧠' },
    'time-travel': { count: 0, emoji: '⏰' },
    'shape-shift': { count: 0, emoji: '🦋' }
  }
  
  surveyResponses.forEach(response => {
    if (powers[response.superpower as keyof typeof powers]) {
      powers[response.superpower as keyof typeof powers].count++
    }
  })
  
  return powers
})

const topDreamJobs = computed(() => {
  const jobCounts: Record<string, number> = {}
  
  surveyResponses.forEach(response => {
    const job = response.dreamJob.toLowerCase()
    jobCounts[job] = (jobCounts[job] || 0) + 1
  })
  
  return Object.entries(jobCounts)
    .map(([name, count]) => ({ name: name.charAt(0).toUpperCase() + name.slice(1), count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5)
})

const displayedResponses = computed(() => {
  let sorted = [...surveyResponses]
  
  if (sortBy.value === 'name') {
    sorted.sort((a, b) => a.name.localeCompare(b.name))
  } else if (sortBy.value === 'age') {
    sorted.sort((a, b) => a.age - b.age)
  } else if (sortBy.value === 'subject') {
    sorted.sort((a, b) => a.favoriteSubject.localeCompare(b.favoriteSubject))
  }
  
  return showAllResponses.value ? sorted : sorted.slice(0, 6)
})

const getColorClass = (color: string) => {
  const colorMap: Record<string, string> = {
    red: 'bg-red-500',
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    purple: 'bg-purple-500',
    pink: 'bg-pink-500',
    orange: 'bg-orange-500',
    teal: 'bg-teal-500'
  }
  return colorMap[color] || 'bg-gray-500'
}

const exportData = () => {
  const dataStr = JSON.stringify(surveyResponses, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'coolkids-survey-results.json'
  link.click()
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
/* Custom animations for charts */
@keyframes slideIn {
  from {
    width: 0%;
  }
  to {
    width: var(--target-width);
  }
}

/* Smooth transitions */
* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Enhanced hover effects */
.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
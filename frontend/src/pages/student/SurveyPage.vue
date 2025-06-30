<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500 p-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="font-fancy text-6xl font-bold text-white mb-2 drop-shadow-lg">
          CoolKids
        </h1>
        <div class="bg-white/90 backdrop-blur-sm rounded-3xl p-6 shadow-2xl">
          <h2 class="text-3xl font-bold text-gray-800 mb-2">🌟 Fun Survey Time! 🌟</h2>
          <p class="text-lg text-gray-600">Tell us about yourself - we'd love to know more about you!</p>
        </div>
      </div>

      <!-- Survey Form -->
      <form @submit.prevent="submitSurvey" class="space-y-6">
        <!-- Question 1: Name -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-yellow-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            🎯 What's your awesome name?
          </label>
          <input
            v-model="answers.name"
            type="text"
            class="w-full p-4 text-lg border-3 border-yellow-400 rounded-2xl focus:border-orange-400 focus:ring-4 focus:ring-orange-200 transition-all"
            placeholder="Type your name here..."
            required
          />
        </div>

        <!-- Question 2: Age -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-green-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            🎂 How old are you?
          </label>
          <select
            v-model="answers.age"
            class="w-full p-4 text-lg border-3 border-green-400 rounded-2xl focus:border-blue-400 focus:ring-4 focus:ring-blue-200 transition-all"
            required
          >
            <option value="">Choose your age</option>
            <option v-for="age in [6, 7, 8, 9, 10, 11, 12, 13, 14, 15]" :key="age" :value="age">
              {{ age }} years old
            </option>
          </select>
        </div>

        <!-- Question 3: Favorite Subject -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-purple-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            📚 What's your favorite school subject?
          </label>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <label v-for="subject in subjects" :key="subject.value" 
                   class="flex items-center p-3 bg-purple-100 rounded-2xl border-2 border-purple-200 hover:border-purple-400 cursor-pointer transition-all">
              <input
                v-model="answers.favoriteSubject"
                type="radio"
                :value="subject.value"
                class="mr-3 w-5 h-5 text-purple-600"
                required
              />
              <span class="text-lg">{{ subject.emoji }} {{ subject.label }}</span>
            </label>
          </div>
        </div>

        <!-- Question 4: Hobbies -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-pink-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            🎨 What do you love doing in your free time? (Pick all that you like!)
          </label>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <label v-for="hobby in hobbies" :key="hobby.value"
                   class="flex items-center p-3 bg-pink-100 rounded-2xl border-2 border-pink-200 hover:border-pink-400 cursor-pointer transition-all">
              <input
                v-model="answers.hobbies"
                type="checkbox"
                :value="hobby.value"
                class="mr-3 w-5 h-5 text-pink-600"
              />
              <span class="text-lg">{{ hobby.emoji }} {{ hobby.label }}</span>
            </label>
          </div>
        </div>

        <!-- Question 5: Learning Style -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-orange-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            🧠 How do you learn best?
          </label>
          <div class="space-y-3">
            <label v-for="style in learningStyles" :key="style.value"
                   class="flex items-center p-4 bg-orange-100 rounded-2xl border-2 border-orange-200 hover:border-orange-400 cursor-pointer transition-all">
              <input
                v-model="answers.learningStyle"
                type="radio"
                :value="style.value"
                class="mr-4 w-5 h-5 text-orange-600"
                required
              />
              <span class="text-lg">{{ style.emoji }} {{ style.label }}</span>
            </label>
          </div>
        </div>

        <!-- Question 6: Favorite Color -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-indigo-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            🌈 What's your favorite color?
          </label>
          <div class="grid grid-cols-4 md:grid-cols-6 gap-3">
            <label v-for="color in colors" :key="color.value"
                   class="flex flex-col items-center p-3 bg-white rounded-2xl border-3 hover:scale-105 cursor-pointer transition-all"
                   :class="answers.favoriteColor === color.value ? 'border-gray-800 shadow-lg' : 'border-gray-200'">
              <input
                v-model="answers.favoriteColor"
                type="radio"
                :value="color.value"
                class="sr-only"
                required
              />
              <div class="w-8 h-8 rounded-full mb-2" :class="color.class"></div>
              <span class="text-sm font-medium">{{ color.label }}</span>
            </label>
          </div>
        </div>

        <!-- Question 7: Dream Job -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-teal-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            🚀 What do you want to be when you grow up?
          </label>
          <input
            v-model="answers.dreamJob"
            type="text"
            class="w-full p-4 text-lg border-3 border-teal-400 rounded-2xl focus:border-cyan-400 focus:ring-4 focus:ring-cyan-200 transition-all"
            placeholder="Tell us your dream job..."
            required
          />
        </div>

        <!-- Question 8: Favorite Animal -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-emerald-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            🐾 What's your favorite animal?
          </label>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <label v-for="animal in animals" :key="animal.value"
                   class="flex flex-col items-center p-4 bg-emerald-100 rounded-2xl border-2 border-emerald-200 hover:border-emerald-400 cursor-pointer transition-all">
              <input
                v-model="answers.favoriteAnimal"
                type="radio"
                :value="animal.value"
                class="sr-only"
                required
              />
              <span class="text-3xl mb-2">{{ animal.emoji }}</span>
              <span class="text-lg font-medium">{{ animal.label }}</span>
            </label>
          </div>
        </div>

        <!-- Question 9: Superpower -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-red-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            ⚡ If you could have any superpower, what would it be?
          </label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <label v-for="power in superpowers" :key="power.value"
                   class="flex items-center p-4 bg-red-100 rounded-2xl border-2 border-red-200 hover:border-red-400 cursor-pointer transition-all">
              <input
                v-model="answers.superpower"
                type="radio"
                :value="power.value"
                class="mr-4 w-5 h-5 text-red-600"
                required
              />
              <span class="text-lg">{{ power.emoji }} {{ power.label }}</span>
            </label>
          </div>
        </div>

        <!-- Question 10: Happiness -->
        <div class="bg-white/95 backdrop-blur-sm rounded-3xl p-6 shadow-xl border-4 border-yellow-300">
          <label class="block text-xl font-bold text-gray-800 mb-3">
            😊 What makes you happiest?
          </label>
          <textarea
            v-model="answers.happiness"
            class="w-full p-4 text-lg border-3 border-yellow-400 rounded-2xl focus:border-orange-400 focus:ring-4 focus:ring-orange-200 transition-all resize-none"
            rows="4"
            placeholder="Tell us what makes you smile the biggest smile..."
            required
          ></textarea>
        </div>

        <!-- Submit Button -->
        <div class="text-center pt-6">
          <button
            type="submit"
            :disabled="isSubmitting"
            class="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-bold text-2xl px-12 py-4 rounded-full shadow-2xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!isSubmitting">🎉 Submit My Awesome Survey! 🎉</span>
            <span v-else>📤 Sending...</span>
          </button>
        </div>
      </form>

      <!-- Success Message -->
      <div v-if="showSuccess" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div class="bg-white rounded-3xl p-8 shadow-2xl text-center max-w-md mx-4">
          <div class="text-6xl mb-4">🎊</div>
          <h3 class="text-2xl font-bold text-gray-800 mb-2">Awesome Job!</h3>
          <p class="text-lg text-gray-600 mb-4">Thank you for completing the survey!</p>
          <button
            @click="showSuccess = false"
            class="bg-gradient-to-r from-green-400 to-blue-500 text-white font-bold px-6 py-3 rounded-full hover:scale-105 transition-all"
          >
            Cool! 😎
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const isSubmitting = ref(false)
const showSuccess = ref(false)

const answers = reactive({
  name: '',
  age: '',
  favoriteSubject: '',
  hobbies: [] as string[],
  learningStyle: '',
  favoriteColor: '',
  dreamJob: '',
  favoriteAnimal: '',
  superpower: '',
  happiness: ''
})

const subjects = [
  { value: 'math', label: 'Math', emoji: '🔢' },
  { value: 'science', label: 'Science', emoji: '🔬' },
  { value: 'english', label: 'English', emoji: '📖' },
  { value: 'art', label: 'Art', emoji: '🎨' },
  { value: 'music', label: 'Music', emoji: '🎵' },
  { value: 'pe', label: 'PE/Sports', emoji: '⚽' }
]

const hobbies = [
  { value: 'reading', label: 'Reading', emoji: '📚' },
  { value: 'drawing', label: 'Drawing', emoji: '✏️' },
  { value: 'sports', label: 'Sports', emoji: '🏃' },
  { value: 'music', label: 'Music', emoji: '🎼' },
  { value: 'games', label: 'Video Games', emoji: '🎮' },
  { value: 'cooking', label: 'Cooking', emoji: '👨‍🍳' },
  { value: 'dancing', label: 'Dancing', emoji: '💃' },
  { value: 'building', label: 'Building/Lego', emoji: '🧱' }
]

const learningStyles = [
  { value: 'visual', label: 'Looking at pictures and videos', emoji: '👀' },
  { value: 'auditory', label: 'Listening to explanations', emoji: '👂' },
  { value: 'kinesthetic', label: 'Doing hands-on activities', emoji: '✋' },
  { value: 'reading', label: 'Reading books and texts', emoji: '📖' }
]

const colors = [
  { value: 'red', label: 'Red', class: 'bg-red-500' },
  { value: 'blue', label: 'Blue', class: 'bg-blue-500' },
  { value: 'green', label: 'Green', class: 'bg-green-500' },
  { value: 'yellow', label: 'Yellow', class: 'bg-yellow-500' },
  { value: 'purple', label: 'Purple', class: 'bg-purple-500' },
  { value: 'pink', label: 'Pink', class: 'bg-pink-500' },
  { value: 'orange', label: 'Orange', class: 'bg-orange-500' },
  { value: 'teal', label: 'Teal', class: 'bg-teal-500' }
]

const animals = [
  { value: 'dog', label: 'Dog', emoji: '🐕' },
  { value: 'cat', label: 'Cat', emoji: '🐱' },
  { value: 'elephant', label: 'Elephant', emoji: '🐘' },
  { value: 'lion', label: 'Lion', emoji: '🦁' },
  { value: 'dolphin', label: 'Dolphin', emoji: '🐬' },
  { value: 'panda', label: 'Panda', emoji: '🐼' },
  { value: 'tiger', label: 'Tiger', emoji: '🐅' },
  { value: 'penguin', label: 'Penguin', emoji: '🐧' }
]

const superpowers = [
  { value: 'flying', label: 'Flying through the sky', emoji: '🦅' },
  { value: 'invisible', label: 'Becoming invisible', emoji: '👻' },
  { value: 'super-strength', label: 'Super strength', emoji: '💪' },
  { value: 'telepathy', label: 'Reading minds', emoji: '🧠' },
  { value: 'time-travel', label: 'Time travel', emoji: '⏰' },
  { value: 'shape-shift', label: 'Shape shifting', emoji: '🦋' }
]

const submitSurvey = async () => {
  isSubmitting.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    console.log('Survey submitted:', answers)
    showSuccess.value = true
    
    // Reset form after successful submission
    Object.keys(answers).forEach(key => {
      if (Array.isArray(answers[key as keyof typeof answers])) {
        (answers[key as keyof typeof answers] as string[]).length = 0
      } else {
        (answers as any)[key] = ''
      }
    })
  } catch (error) {
    console.error('Error submitting survey:', error)
    alert('Oops! Something went wrong. Please try again!')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
/* Custom animations for enhanced interactivity */
.hover\:scale-105:hover {
  transform: scale(1.05);
}

/* Ensure smooth transitions */
* {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Custom focus styles for better accessibility */
input:focus,
select:focus,
textarea:focus {
  outline: none;
}

/* Enhanced border styles */
.border-3 {
  border-width: 3px;
}

.border-4 {
  border-width: 4px;
}
</style>
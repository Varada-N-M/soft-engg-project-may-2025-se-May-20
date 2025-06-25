<template>
  <div class="min-h-screen bg-gradient-to-br from-green-200 to-cyan-200 p-6">
    <!-- Header -->
    <h1 class="text-4xl font-bold text-center text-gray-800 font-fancy mb-4">📚 Lesson Updates</h1>

    <!-- Lesson Table -->
    <div class="overflow-x-auto rounded-xl shadow-md bg-white">
      <table class="min-w-full text-sm text-gray-700 text-left">
        <thead class="bg-cyan-400 text-white text-md">
          <tr>
            <th scope="col" class="px-6 py-4">Day</th>
            <th scope="col" class="px-6 py-4">Subject</th>
            <th scope="col" class="px-6 py-4">Lesson Taught</th>
            <th scope="col" class="px-6 py-4">Class Activity Summary</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(lesson, index) in lessons" :key="index" class="odd:bg-green-100 even:bg-green-50">
            <td class="px-6 py-4 font-semibold">{{ lesson.day }}</td>
            <td class="px-6 py-4">{{ lesson.subject }}</td>
            <td class="px-6 py-4">{{ lesson.lesson }}</td>
            <td class="px-6 py-4">{{ lesson.activity }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const lessons = [
  { day: 'Monday', subject: 'Math', lesson: 'Introduction to Fractions', activity: 'Used paper cut-outs to compare 1/2, 1/4, 3/4' },
  { day: 'Monday', subject: 'English', lesson: 'Types of Nouns (Common & Proper)', activity: 'Worksheet activity and group examples' },
  { day: 'Tuesday', subject: 'Science', lesson: 'States of Matter: Solid, Liquid, Gas', activity: 'Melting ice and steam experiment demonstration' },
  { day: 'Wednesday', subject: 'Social Studies', lesson: 'Community Helpers', activity: 'Class discussion and drawing different helpers' },
  { day: 'Thursday', subject: 'Computers', lesson: 'Parts of a Computer', activity: 'Hands-on identification of hardware components' },
  { day: 'Friday', subject: 'Math', lesson: 'Paragraph Writing: Fractions on Number Line', activity: 'Wrote a short paragraph on "My Favourite Game"' },
]
</script>

<style scoped>
/* Optional: Override scrollbar for fun theme */
::-webkit-scrollbar {
  height: 8px;
}
::-webkit-scrollbar-thumb {
  background: #38bdf8;
  border-radius: 10px;
}
</style>

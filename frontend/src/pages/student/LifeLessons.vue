<!-- LifeLessonsPage.vue -->
<template>
  <div class="min-h-screen bg-gray-50 p-8 font-inter">
    <header class="max-w-4xl mx-auto mb-8 text-center">
      <router-link to="/student/home" class="inline-flex items-center text-gray-500 hover:text-gray-700 transition-colors mb-4 rounded-lg px-3 py-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Dashboard
      </router-link>
      <h1 class="text-4xl font-extrabold text-gray-900 mb-2">Life Lessons 💡</h1>
      <p class="text-lg text-gray-600 font-medium">
        Explore valuable lessons to help you grow. You've completed <span class="text-green-500 font-bold">{{ completedLessons.length }}</span> out of <span class="text-blue-500 font-bold">{{ lifeLessons.length }}</span> lessons!
      </p>
    </header>

    <main class="max-w-6xl mx-auto">
      <div v-if="lifeLessons.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <LifeLessonCard
          v-for="lesson in lifeLessons"
          :key="lesson.id"
          :lesson="lesson"
          @lesson-completed="markLessonAsComplete"
        />
      </div>
      <div v-else class="text-center py-20">
        <div class="text-6xl mb-4">📚</div>
        <h2 class="text-2xl font-bold text-gray-800 mb-2">No Life Lessons Available Yet</h2>
        <p class="text-gray-600">Check back soon for more inspiring content!</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import LifeLessonCard from './LifeLessonCard.vue'; // Make sure this path is correct

// Reactive data for life lessons
// In a real application, you'd fetch this data from an API (e.g., Firestore).
const lifeLessons = ref([
  {
    id: 1,
    title: 'Manage & Save Money',
    description: 'Learn how to manage & save money',
    youtubeLink: 'https://youtu.be/hYbRu_MXI80?feature=shared',
    completed: false,
    completionDate: null,
  },
  {
    id: 2,
    title: 'Manage stress & emotions',
    description: 'Learn how to manage stress & emotions',
    youtubeLink: 'https://youtu.be/Vs-MyQgfH3A?feature=shared', 
    completed: false,
    completionDate: null,
  },
  {
    id: 3,
    title: 'Effective Communication Skills',
    description: 'Improve your ability to express yourself clearly and listen actively.',
    youtubeLink: 'https://youtu.be/BW82k7lwI_U?feature=shared', // Example link
    completed: false,
    completionDate: null,
  },
  {
    id: 4,
    title: 'Understanding Emotional Intelligence',
    description: 'Develop awareness of your own and others\' emotions.',
    youtubeLink: 'https://youtu.be/jfbnKI9Zjb0?feature=shared', // Example link
    completed: false,
    completionDate: null,
  },
  {
    id: 5,
    title: 'The Art of Problem Solving',
    description: 'Strategies for breaking down complex problems and finding solutions.',
    youtubeLink: 'https://youtu.be/6_LX9mo0Thw?feature=shared', // Example link
    completed: false,
    completionDate: null,
  },
]);

// Computed property to get only completed lessons
const completedLessons = computed(() => lifeLessons.value.filter(lesson => lesson.completed));

// Function to mark a lesson as complete
const markLessonAsComplete = (lessonId) => {
  const lesson = lifeLessons.value.find(l => l.id === lessonId);
  if (lesson && !lesson.completed) {
    lesson.completed = true;
    lesson.completionDate = new Date().toISOString().split('T')[0]; // Store date in YYYY-MM-DD format
    console.log(`Lesson ${lesson.title} marked as complete.`);
    // In a real app, you would also update this in your backend (e.g., Firestore)
  }
};
</script>

<style scoped>
/* No specific styles needed here as Tailwind is mostly used, but you can add custom ones if required. */
.font-inter {
  font-family: 'Inter', sans-serif;
}
</style>


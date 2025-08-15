<template>
  <div class="min-h-screen flex">
    <aside
      class="w-64  bg-opacity-90 backdrop-blur-sm p-6 fixed left-5 top-3 bottom-3 rounded-[20px] overflow-y-auto z-50 shadow-[0_0_10px_rgba(0,0,0,0.14)] flex flex-col">
      <div class="mb-8">
        <h2 class="text-3xl font-extrabold text-gray-900 font-playfair">My Dashboard</h2>
      </div>
      <nav class="space-y-3">
        <router-link v-for="link in navLinks" :key="link.name" :to="link.path"
          class="flex items-center gap-4 py-2 px-2 rounded-xl text-gray-700 hover:text-yellow-600 transition-colors duration-200 font-medium font-playfair">
          <span class="text-xl">{{ link.icon }}</span> {{ link.name }}
        </router-link>
      </nav>
    </aside>

    <main class="flex-1 ml-64 p-8 overflow-y-auto bg-gray-50">
      <div class="max-w-7xl ml-3">
        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md">
          <div class="flex flex-wrap items-center justify-between gap-6">
            <!-- Greeting Text (Left Side) -->
            <div class="flex-1 min-w-max font-playfair">
              <h1 class="text-4xl font-bold text-gray-900 mb-2" v-if="studentProfile">
                Welcome back, {{ studentProfile.first_name }}!
              </h1>
              <h1 class="text-4xl font-bold text-gray-900 mb-2 font-playfair" v-else>
                Welcome Back.
              </h1>
              <p class="text-gray-600 text-lg">
                Your adventure awaits. Let's make today a great day!
              </p>
            </div>

            <!-- Buttons (Right Side - Horizontal Row) -->
            <div class="flex space-x-4 min-w-fit font-playfair">
              <router-link to="/student/profile"
                class="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-blue-100 text-blue-700 hover:bg-blue-200 transition-colors duration-200 font-medium">
                Profile
              </router-link>

              <button @click="logout"
                class="flex items-center justify-center gap-2 py-3 px-6 rounded-xl bg-red-100 text-red-700 hover:bg-red-200 transition-colors duration-200 font-medium">
                Logout
              </button>
            </div>
          </div>
        </div>
        
        <!-- NEW Stats Section -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard icon="✨" label="Total XP" :value="studentProfile.xp_points" />
          <StatCard icon="🏅" label="Badges Earned" :value="studentProfile.badge_count" :loading="isBadgeCountLoading" />
          <StatCard icon="🎯" label="Total Habits" :value="studentProfile.habit_count" />
          <StatCard icon="✅" label="Activities Completed" :value="studentProfile.activity_points" :loading="isCompletedSkillsLoading" unit="this week" />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div class="bg-white rounded-3xl p-8 shadow-md">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3 mb-6 font-playfair">
              Daily Gratitude
            </h2>
            <div v-if="todaysGratitude" class="bg-pink-50 p-6 rounded-2xl">
              <p class="text-gray-800 italic text-lg leading-relaxed">
                "{{ todaysGratitude }}"
              </p>
              <div class="flex items-center gap-2 mt-4">
                <span class="text-green-500">✅</span>
                <span class="text-sm text-gray-600 font-medium font-playfair">You completed this today!</span>
              </div>
            </div>
            <div v-else class="text-center py-6">
              <div class="text-5xl mb-4">💭</div>
              <p class="text-gray-700 text-lg mb-4 font-playfair">
                What's one thing you're thankful for today?
              </p>
              <router-link to="/student/journal"
                class="bg-pink-500 text-white font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-pink-600 transition-colors inline-block text-center font-playfair">
                Write Gratitude
              </router-link>
            </div>
          </div>

          <div class="bg-white rounded-3xl p-8 shadow-md font-playfair">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3 mb-6">
              Learn with AI
            </h2>
            <div class="p-6 rounded-2xl">
              <div class="flex items-center gap-3 mb-4">
                <div class="text-lg text-gray-700 font-medium">Meet Rohit!</div>
              </div>
              <p class="text-gray-800 mb-4 leading-relaxed">
                "Hi! I'm here to talk, teach and help you improve your Communication Skills!"
              </p>
              <router-link to="/student/ai-companion"
                class="bg-blue-500 text-white font-semibold px-6 py-3 rounded-xl shadow-lg hover:bg-blue-600 transition-colors inline-block text-center">
                Chat Now
              </router-link>
            </div>
          </div>
        </div>

        <!-- Weekly Skills Section -->
        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md font-playfair">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3 mb-6">
            Weekly Skills Challenge
          </h2>

          <div v-if="weeklySkill">
            <div class="flex flex-col lg:flex-row gap-6">
              <!-- Video -->
              <div class="w-full lg:w-2/3">
                <div class="relative w-full overflow-hidden pb-[56.25%] rounded-xl shadow-lg">
                  <iframe :src="`https://www.youtube.com/embed/${getYouTubeVideoId(weeklySkill.video_url)}`"
                    class="absolute inset-0 w-full h-full rounded-xl" frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen title="YouTube Lesson Video">
                  </iframe>
                </div>
              </div>

              <!-- Info -->
              <div class="flex-1 flex flex-col">
                <h5 class="font-bold text-gray-900 text-lg mb-4">
                  Your This Week's Challenge: {{ weeklySkill.skill_name }}
                </h5>
                <button @click="markWeeklySkillAsLearned(weeklySkill)" :class="{
                  'bg-green-600 hover:bg-green-700': !weeklySkillCompletionState.isComplete,
                  'bg-green-500 cursor-default': weeklySkillCompletionState.isComplete,
                  'opacity-70': weeklySkillCompletionState.isLoading
                }" class="self-start mt-auto px-4 py-2 text-white rounded-xl shadow transition-colors duration-200 text-sm font-medium flex items-center gap-2"
                  :disabled="weeklySkillCompletionState.isComplete || weeklySkillCompletionState.isLoading">
                  <span v-if="!weeklySkillCompletionState.isComplete && !weeklySkillCompletionState.isLoading">
                    Mark as Complete
                  </span>
                  <span v-if="weeklySkillCompletionState.isLoading">Completing...</span>
                  <span v-if="weeklySkillCompletionState.isComplete">Lesson Completed!</span>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="text-center">
            <h3 class="text-xl font-semibold text-gray-900 mb-4">
              All Weekly Skills Completed 🎉
            </h3>
            <p class="text-gray-700 mb-4">
              You’ve completed all the weekly skill challenges. Great job!
            </p>
            <ul class="list-disc list-inside text-gray-700 inline-block text-left">
              <li v-for="skill in completedWeeklySkills" :key="skill.id">
                {{ skill.skill_name }}
              </li>
            </ul>
          </div>
        </div>

        <!-- Life Lessons Section -->
        <div class="bg-white rounded-3xl p-8 mb-8 shadow-md font-playfair">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-3">
              Life Lessons
            </h2>
            <router-link to="/student/life-lessons" class="text-blue-600 hover:text-blue-800 font-semibold">
              View All
            </router-link>
          </div>

          <div v-if="lifelessons.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="lesson in lifelessons.slice(0, 2)" :key="lesson.id"
              class="bg-gray-100 rounded-[20px] p-6 transition-transform hover:scale-101 cursor-pointer">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">
                {{ lesson.skill_name }}
              </h3>
              <div class="flex gap-3">
                <button @click="watchLesson(lesson.video_url)"
                  class="bg-blue-600 text-white px-4 py-2 rounded-[15px] hover:bg-blue-700 transition-colors cursor-pointer">
                  Watch Lesson
                </button>
                <button @click="markLifeLessonAsLearned(lesson.id)" :class="{
                  'bg-green-600 hover:bg-green-700': !lessonCompletionState[lesson.id]?.isComplete,
                  'bg-green-500 cursor-default': lessonCompletionState[lesson.id]?.isComplete,
                  'opacity-70': lessonCompletionState[lesson.id]?.isLoading
                }" class="px-4 py-2 text-white rounded-xl shadow transition-colors duration-200 text-sm font-medium flex items-center gap-2"
                  :disabled="lessonCompletionState[lesson.id]?.isComplete || lessonCompletionState[lesson.id]?.isLoading">
                  <span
                    v-if="!lessonCompletionState[lesson.id]?.isComplete && !lessonCompletionState[lesson.id]?.isLoading">
                    Mark as Complete
                  </span>
                  <span v-if="lessonCompletionState[lesson.id]?.isLoading">Completing...</span>
                  <span v-if="lessonCompletionState[lesson.id]?.isComplete">Lesson Completed!</span>
                </button>
              </div>
            </div>
          </div>

          <div v-else class="text-center">
            <h3 class="text-xl font-semibold text-gray-900 mb-4">
              All Life Lessons Completed! 🎉
            </h3>
            <p class="text-gray-700">You’ve finished all available lessons. Great work!</p>
          </div>
        </div>


      </div>
    </main>
  </div>
</template>

<script setup>
import { clearAuthData } from '@/utils/auth';
import { computed, onMounted, ref } from 'vue';
import StatCard from './StatCard.vue';
import { useRouter } from 'vue-router';

// Import smaller, reusable components (assuming they are created)
import api from '@/plugins/axios.ts';

// Router instance
const router = useRouter();

const habits = ref([])
const studentProfile = ref({});
const isLoading = ref(true);
const xpPoints = ref();
const error = ref(null);

const isComplete = ref(false);

// Logout function
const logout = () => {
  clearAuthData();
  router.push('/');
};

const navLinks = ref([
  { name: 'Home', path: '/student/home', icon: '🏠' },
  { name: 'Lesson Updates', path: '/student/lesson-updates', icon: '📚' },
  { name: 'To-do List', path: '/student/todolist', icon: '✔️' },
  { name: 'Habits', path: '/student/habit', icon: '🎯' },
  { name: 'Life Lessons', path: '/student/life-lessons', icon: '📖' },
  { name: 'Journal', path: '/student/journal', icon: '✍️' },
  { name: 'AI Companion', path: '/student/ai-companion', icon: '🤖' },
  { name: 'Badges', path: '/student/badges', icon: '🏅' },
]);

const categoryToEmojiMap = {
  reading: '📚',
  health: '💧',
  chores: '🧹',
  sports: '🏃',
  creative: '🎨',
  other: '🎯',
};

const markAsComplete = () => {
  isComplete.value = true;
};

const getEmojiForCategory = (category) => {
  return categoryToEmojiMap[category] || '🎯';
};

const fetchHabits = async () => {
  const token = localStorage.getItem('access_token');
  try {
    const response = await api.get('/api/child/habits', {
      headers: { Authorization: `Bearer ${token}` },
    });

    habits.value = response.data.habits_created || [];

    const today = new Date().toISOString().split('T')[0];
    habits.value = response.data.habits_created.map(habit => {
      const isCompletedToday = response.data.completed_habits.some(
        c => c.habit_id === habit.habit_id && c.completion_date && c.completion_date.startsWith(today)
      );

      return {
        id: habit.habit_id,
        emoji: getEmojiForCategory(habit.category),
        title: habit.name,
        description: habit.description,
        category: habit.category,
        xp: habit.habit_xp,
        completed: isCompletedToday,
      };
    });
  } catch (err) {
    console.error('Failed to fetch habits:', err);
    // You could show an error message to the user here
  } finally {
    isLoading.value = false;
  }
};

const toggleHabit = async (habitId) => {
  const token = localStorage.getItem('access_token');
  const habitToToggle = habits.value.find(h => h.id === habitId);

  // Prevent multiple clicks and mark as done
  if (habitToToggle && !habitToToggle.completed) {
    try {
      // The backend POST endpoint marks it as complete
      await api.post(`/api/child/habit/${habitId}/complete`, null, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Update the UI after successful API call
      habitToToggle.completed = true;
      alert(`🎉 You earned +${habitToToggle.xp} XP!`);

    } catch (err) {
      console.error('Failed to complete habit:', err);
      if (err.response && err.response.status === 400) {
        alert('This habit is already completed for today!');
      } else {
        alert('An error occurred. Please try again.');
      }
    }
  }
};

const fetchUserProfile = async () => {
  const token = localStorage.getItem('access_token');
  try {
    // Assuming you have an endpoint like '/api/child/profile'
    const response = await api.get('/api/child/profile', {
      headers: { Authorization: `Bearer ${token}` },
    });

    xpPoints.value = response.data.xp_points;
  } catch (err) {
    error.value = 'Failed to fetch user profile data.';
    console.error('Failed to fetch user profile:', err);
  }
};

const markSkillAsComplete = async (skillId) => { // Removed ': number' from here
  try {
    await api.post(`/api/child/skills/${skillId}/complete`);
    isComplete.value = true
    console.log(`Weekly skill with ID ${skillId} marked as complete`)
  } catch (err) {
    console.error('Error marking skill as complete:', err)
  }
}

const todaysGratitude = ref('');

const currentLifeSkill = ref({
  id: 1,
  title: 'Making a Simple Sandwich',
  description: 'Learn to prepare your own healthy lunch! This week we\'ll practice making sandwich safely.',
  emoji: '🥪'
});


const learningStories = ref([])
const loading = ref(false)
const story_error = ref(null)

// Fetch skills from backend
const fetchSkills = async () => {
  try {
    loading.value = true
    story_error.value = null

    // Get token from localStorage
    const token = localStorage.getItem('token')

    if (!token) {
      throw new Error('No authentication token found')
    }

    // Make API call to get skills
    const response = await api.get('/api/child/skills', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    // Extract skills from response and take only first 2
    const skills = response.data.skills || []
    learningStories.value = skills.slice(0, 2)

    console.log('Skills fetched:', learningStories.value)

  } catch (err) {
    console.error('Error fetching skills:', err)
    story_error.value = err.response?.data?.error || err.message || 'Failed to fetch skills'
    learningStories.value = []
  } finally {
    loading.value = false
  }
}

// Dynamic data fetched from API
const lessonUpdates = ref([]);
const badgeCount = ref(0);
const isBadgeCountLoading = ref();
const completedSkillsCount = ref(0);
const isCompletedSkillsLoading = ref();

const toggleActivity = (activityId) => {
  const activity = todaysActivities.value.find((a) => a.id === activityId);
  if (activity && !activity.completed) {
    activity.completed = true;
  }
};

const fetchData = async (url, loadingRef, dataRef, transform = (d) => d, key = '') => {
  const token = localStorage.getItem('access_token');
  if (!token) return;

  loadingRef.value = true;
  try {
    const response = await api.get(url, { headers: { Authorization: `Bearer ${token}` } });
    dataRef.value = transform(response.data[key] || response.data) || [];
  } catch (err) {
    console.error(`Error fetching data from ${url}:`, err);
  } finally {
    loadingRef.value = false;
  }
};


const lessons = ref([])
const errorMessage = ref('')

const getDayFromDate = (dateString) => {
  try {
    const date = new Date(dateString)
    const options = { weekday: 'long' }
    return date.toLocaleDateString('en-US', options)
  } catch (error) {
    return 'Unknown'
  }
}

const fetchLessonUpdates = async () => {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await api.get('/api/child/lesson-updates')

    if (response.data.lesson_updates) {
      // Transform backend data to match frontend structure
      lessons.value = response.data.lesson_updates.map(update => ({
        lesson_id: update.lesson_id,
        lesson: update.lesson,
        summary: update.summary,
        created_at: update.created_at,
        teacher_name: update.teacher_name,
        // Extract day from created_at date
        day: getDayFromDate(update.created_at),
        // Extract subject from lesson name (simple heuristic)
        subject: getSubjectFromLesson(update.lesson)
      }))
    } else {
      lessons.value = []
    }
  } catch (error) {
    console.error('Error fetching lesson updates:', error)
    if (error.response && error.response.data && error.response.data.message) {
      // Handle case where no teachers are linked to child
      errorMessage.value = error.response.data.message
    } else {
      errorMessage.value = 'Failed to load lesson updates. Please try again.'
    }
    lessons.value = []
  } finally {
    isLoading.value = false
  }
}

const getSubjectFromLesson = (lessonName) => {
  const lesson = lessonName.toLowerCase()
  if (lesson.includes('math') || lesson.includes('fraction') || lesson.includes('number') || lesson.includes('arithmetic')) {
    return 'Math'
  } else if (lesson.includes('english') || lesson.includes('grammar') || lesson.includes('writing') || lesson.includes('reading')) {
    return 'English'
  } else if (lesson.includes('science') || lesson.includes('experiment') || lesson.includes('biology') || lesson.includes('chemistry') || lesson.includes('physics')) {
    return 'Science'
  } else if (lesson.includes('social') || lesson.includes('history') || lesson.includes('geography') || lesson.includes('community')) {
    return 'Social Studies'
  } else if (lesson.includes('computer') || lesson.includes('technology') || lesson.includes('coding')) {
    return 'Technology'
  } else {
    return 'General'
  }
}

// Helper function to format date
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(today.getDate() - 1)

    if (date.toDateString() === today.toDateString()) {
      return 'Today'
    } else if (date.toDateString() === yesterday.toDateString()) {
      return 'Yesterday'
    } else {
      return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }
  } catch (error) {
    return 'Unknown'
  }
}

// Computed properties
const uniqueSubjects = computed(() => {
  const set = new Set(lessons.value.map(l => l.subject))
  return Array.from(set)
})

const uniqueTeachers = computed(() => {
  const set = new Set(lessons.value.filter(l => l.teacher_name).map(l => l.teacher_name))
  return Array.from(set)
})

const weeklySkill = ref({})

const fetchweeklySkill = async () => {
  try {
    const response = await api.get('/api/child/skills')

    console.log('Weekly skill fetched:', response.data)
    const weeklySkills = response.data.skills.filter(skill => skill.skill_type === 'weekly' && skill.is_learned === false)
    // get one random element from the array
    weeklySkill.value = weeklySkills[Math.floor(Math.random() * weeklySkills.length)]
  } catch (error) {
    console.error('Error fetching weekly skill:', error)
  }
}

const lifelessons = ref([]) // Change to array since you're filtering multiple items

const fetchLifelessons = async () => {
  try {
    const response = await api.get('/api/child/skills')
    console.log('Life lessons fetched:', response.data)

    const filteredSkills = response.data.skills.filter(skill => skill.skill_type === 'regular' && skill.is_learned === false)
    console.log('Life lessons filtered:', filteredSkills)

    lifelessons.value = filteredSkills

    // Initialize completion states for each lesson
    filteredSkills.forEach(lesson => {
      if (!lessonCompletionState.value[lesson.id]) {
        lessonCompletionState.value[lesson.id] = {
          isComplete: false, // You might want to check if it's already completed from the API
          isLoading: false
        };
      }
    });

  } catch (error) {
    console.error('Error fetching lifelessons:', error)
    lifelessons.value = []
  }
}

// Function to handle watching lesson
const watchLesson = (videoUrl) => {
  if (videoUrl) {
    // Open video in new tab
    window.open(videoUrl, '_blank')
  } else {
    console.error('No video URL available')
    // Optional: Show a toast/alert to user
    alert('Video not available')
  }
}


const fetchStudentProfile = async () => {
  try {
    const response = await api.get('/api/child/profile')
    studentProfile.value = response.data.profile
  } catch (error) {
    console.error('Error fetching student profile:', error)
  }
}


const getYouTubeVideoId = (url) => {
  if (!url) return null
  try {
    const urlObj = new URL(url)
    if (urlObj.hostname === 'youtu.be') {
      return urlObj.pathname.substring(1) // e.g., /DWvJk9bNDWo → DWvJk9bNDWo
    } else if (urlObj.hostname.includes('youtube.com')) {
      return urlObj.searchParams.get('v')
    }
  } catch (e) {
    console.error('Invalid URL:', url)
  }
  return null
}

const message = ref('');

// Weekly skill completion state
const weeklySkillCompletionState = ref({
  isComplete: false,
  isLoading: false
});

// Life lessons completion state - object to track each lesson individually
const lessonCompletionState = ref({});

const markWeeklySkillAsLearned = async (skill) => {
  weeklySkillCompletionState.value.isLoading = true;

  try {
    const response = await api.post(`/api/child/skills/${weeklySkill.value.id}/complete`);
    console.log('Weekly skill completed:', response.data);

    // Update UI
    message.value = 'Weekly skill completed!';
    weeklySkillCompletionState.value.isComplete = true;

    // Optional: Show success message
    alert('🎉 Weekly skill completed! You earned XP!');

  } catch (error) {
    console.error('Error completing weekly skill:', error);

    // Handle error (show message to user)
    if (error.response?.status === 400) {
      alert('This skill is already completed!');
      weeklySkillCompletionState.value.isComplete = true;
    } else {
      alert('An error occurred. Please try again.');
    }
  } finally {
    weeklySkillCompletionState.value.isLoading = false;
  }
};

// New function specifically for life lessons
const markLifeLessonAsLearned = async (lessonId) => {
  // Initialize state for this lesson if it doesn't exist
  if (!lessonCompletionState.value[lessonId]) {
    lessonCompletionState.value[lessonId] = {
      isComplete: false,
      isLoading: false
    };
  }

  // Set loading state for this specific lesson
  lessonCompletionState.value[lessonId].isLoading = true;

  try {
    const response = await api.post(`/api/child/skills/${lessonId}/complete`);
    console.log('Life lesson completed:', response.data);

    // Update completion state for this specific lesson
    lessonCompletionState.value[lessonId].isComplete = true;

    // Optional: Show success message
    alert('🎉 Life lesson completed! You earned XP!');

  } catch (error) {
    console.error('Error completing life lesson:', error);

    // Handle error (show message to user)
    if (error.response?.status === 400) {
      alert('This lesson is already completed!');
      lessonCompletionState.value[lessonId].isComplete = true;
    } else {
      alert('An error occurred. Please try again.');
    }
  } finally {
    lessonCompletionState.value[lessonId].isLoading = false;
  }
};

const markSkillAsLearned = async (id) => {
  message.value = '';
  isLoading.value = true;

  try {
    const response = await api.post(`/api/child/skills/${weeklySkill.value.id}/complete`);
    console.log('Skill completed:', response.data);

    // Update UI
    message.value = 'Mark as completed!';
    isComplete.value = true;
  } catch (error) {
    console.error('Error updating skill completed:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  await fetchLessonUpdates()
  await fetchweeklySkill()
  await fetchLifelessons()
  await fetchStudentProfile()
})

</script>
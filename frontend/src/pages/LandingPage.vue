<template>
  <div class="min-h-screen bg-white flex flex-col">
    <WarpBackground :beam-delay-min="1" grid-color="rgba(228, 228, 228, 0.53)">
      <!-- Hero Section -->
      <div class="min-h-screen  ">
        <!-- Navbar -->
        <div class="flex justify-between items-center text-4xl mb-5 font-fancy p-6 md:p-10">
          <div class="text-4xl font-semibold">
            <logo/>
          </div>
        </div>

        <!-- Content -->
        <div
            class="flex-1 backdrop-blur-xl py-14 shadow rounded-2xl  items-center gap-8 px-5 mx-4 md:mx-40 text-center">
          <div
              class="absolute top-10 right-10 pt-2 w-32 h-32 rounded-full outline-double outline-4  outline-blue-500 outline-offset-2 bg-[url('../assets/child-photo2.jpg')] bg-cover bg-no-repeat">
          </div>
          <div
              class="absolute bottom-10 left-10 pt-2 w-32 h-32 rounded-full outline-double outline-4  outline-yellow-500 outline-offset-2 bg-[url('../assets/child-photo.jpg')] bg-cover bg-no-repeat">
          </div>
          <div class="relative w-full">
            <h1 class=" text-3xl md:text-2xl text-slate-800">
              Welcome to
              <logo/>
            </h1>
            <h2 class="text-4xl md:text-6xl leading-20 font-medium">
              The best place to <span class="italic text-yellow-500  tilt-left-2 creative-underline">learn</span> & <br>
              <span class="italic text-blue-600 creative-underline tilt-right-1">play</span>
              for your Kids
            </h2>

            <p class="text-xl mx-auto text-center md:text-base max-w-[800px] text-slate-600 mb-8 my-10 leading-relaxed">
              The ultimate platform designed for every member of the educational community.
              Discover features tailored specifically for students, teachers, parents, and administrators.
            </p>

            <div class="text-center">
              <router-link to="/student/login">
                <Button class="bg-blue-500 cursor-pointer hover:bg-blue-600" size="lg">
                  Get Started
                </Button>
              </router-link>
            </div>
          </div>
        </div>

      </div>
    </WarpBackground>

    <!-- Features Section -->
    <div class="w-full max-w-7xl mx-auto flex flex-col gap-6 p-5 md:p-10">
      <h2 class="text-3xl md:text-4xl text-center mb-16 md:mb-25 text-slate-700 drop-shadow-sm">Features</h2>

      <!-- Students Card -->
      <div
          class="bg-white/95 rounded-3xl md:rounded-[45px] backdrop-blur-sm border border-white/30 transition-all duration-300 flex flex-col md:flex-row gap-0 items-stretch overflow-hidden min-h-[300px] mb-16 md:mb-25 shadow-lg">
        <div
            class="w-full md:w-[650px] h-52 md:h-auto rounded-3xl md:rounded-[45px] bg-gradient-to-br from-sky-400 to-cyan-400 flex items-center justify-center text-white text-lg font-bold text-center flex-shrink-0">
          <img src="../assets/child.svg" alt="Children SVG" width="600" class="max-w-full max-h-full"/>
        </div>
        <div class="flex-1 p-6 md:p-10 flex flex-col justify-center">
          <h3 class="font-fancy text-3xl md:text-6xl text-slate-700 mb-4">For Students</h3>
          <p class="text-base text-gray-500 mb-5 leading-relaxed">
            Empower your learning journey with tools designed to help you succeed academically and personally.
          </p>
          <ul class="list-none p-0 space-y-2">
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Interactive homework tracker and assignment calendar
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Grade monitoring with real-time updates and progress analytics
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Collaborative study groups and peer-to-peer learning spaces
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Digital portfolio to showcase projects and achievements
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Personalized learning paths based on individual strengths
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Communication tools to connect with teachers and classmates
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Achievement badges and gamified learning experiences
            </li>
          </ul>
        </div>
      </div>

      <!-- Teachers Card -->
      <div
          class="bg-white/95 rounded-3xl md:rounded-[45px] backdrop-blur-sm border border-white/30 transition-all duration-300 flex flex-col md:flex-row-reverse gap-0 items-stretch overflow-hidden min-h-[300px] mb-16 md:mb-25 shadow-lg">
        <div
            class="w-full md:w-[650px] h-52 md:h-auto rounded-3xl md:rounded-[45px] bg-gradient-to-br from-emerald-400 to-teal-300 flex items-center justify-center text-white text-lg font-bold text-center flex-shrink-0">
          <img src="../assets/teacher.svg" alt="Teacher SVG" width="400" class="max-w-full max-h-full"/>
        </div>
        <div class="flex-1 p-6 md:p-10 flex flex-col justify-center">
          <h3 class="font-fancy text-3xl md:text-6xl text-slate-700 mb-4">For Teachers</h3>
          <p class="text-base text-gray-500 mb-5 leading-relaxed">
            Streamline your teaching process with comprehensive classroom management and educational tools.
          </p>
          <ul class="list-none p-0 space-y-2">
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Intuitive gradebook with automated calculation and reporting
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Lesson planning templates and curriculum alignment tools
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Student progress tracking with detailed analytics dashboard
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Digital classroom management and attendance tracking
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Parent communication portal with instant messaging
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Assignment creation with multimedia support and rubrics
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Professional development resources and teaching communities
            </li>
          </ul>
        </div>
      </div>

      <!-- Parents Card -->
      <div
          class="bg-white/95 rounded-3xl md:rounded-[45px] backdrop-blur-sm border border-white/30 transition-all duration-300 flex flex-col md:flex-row gap-0 items-stretch overflow-hidden min-h-[300px] mb-16 md:mb-25 shadow-lg">
        <div
            class="w-full md:w-[650px] h-52 md:h-auto rounded-3xl md:rounded-[45px] bg-gradient-to-br from-pink-400 to-yellow-300 flex items-center justify-center text-white text-lg font-bold text-center flex-shrink-0">
          <img src="../assets/parent.svg" alt="Parent SVG" width="600" class="max-w-full max-h-full"/>
        </div>
        <div class="flex-1 p-6 md:p-10 flex flex-col justify-center">
          <h3 class="font-fancy text-3xl md:text-6xl text-slate-700 mb-4">For Parents</h3>
          <p class="text-base text-gray-500 mb-5 leading-relaxed">
            Stay connected with your child's educational journey and support their growth every step of the way.
          </p>
          <ul class="list-none p-0 space-y-2">
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Real-time access to grades, assignments, and school announcements
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Direct messaging with teachers and school administrators
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Attendance monitoring with instant notifications
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Parent-teacher conference scheduling and virtual meetings
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Homework help resources and educational activity suggestions
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              School event calendar with RSVP functionality
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Child's academic progress reports and milestone tracking
            </li>
          </ul>
        </div>
      </div>

      <!-- Administrators Card -->
      <div
          class="bg-white/95 rounded-3xl md:rounded-[45px] backdrop-blur-sm border border-white/30 transition-all duration-300 flex flex-col md:flex-row-reverse gap-0 items-stretch overflow-hidden min-h-[300px] mb-16 md:mb-25 shadow-lg">
        <div
            class="w-full md:w-[650px] h-52 md:h-auto rounded-3xl md:rounded-[45px] bg-gradient-to-br from-teal-200 to-pink-200 flex items-center justify-center text-white text-lg font-bold text-center flex-shrink-0">
          <img src="../assets/org.svg" alt="Organization SVG" width="600" class="max-w-full max-h-full"/>
        </div>
        <div class="flex-1 p-6 md:p-10 flex flex-col justify-center">
          <h3 class="font-fancy text-3xl md:text-6xl text-slate-700 mb-4">For Administrators</h3>
          <p class="text-base text-gray-500 mb-5 leading-relaxed">
            Manage your educational institution efficiently with powerful administrative tools and insights.
          </p>
          <ul class="list-none p-0 space-y-2">
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Comprehensive school-wide analytics and performance dashboards
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Staff management system with role-based permissions
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Student enrollment and records management platform
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Budget tracking and resource allocation tools
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Communication broadcast system for school-wide announcements
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Compliance reporting and documentation management
            </li>
            <li class="pl-6 relative text-base text-slate-600 leading-relaxed before:content-['✨'] before:absolute before:left-0 before:top-0">
              Integration with existing school systems and third-party tools
            </li>
          </ul>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="text-center mt-12 p-6 md:p-10 bg-white/80 rounded-xl backdrop-blur-sm">
        <h2 class="font-fancy text-3xl md:text-4xl text-slate-700 mb-5">Ready to Transform Education?</h2>
        <p class="text-lg text-gray-500 mb-8 max-w-4xl mx-auto">
          Join thousands of schools, teachers, students, and parents who trust CoolKids for their educational needs.
        </p>
        <button
            class="bg-gradient-to-br from-indigo-500 to-purple-600 text-white border-none px-8 md:px-10 py-3 md:py-4 rounded-full text-lg font-bold cursor-pointer transition-all duration-300 shadow-lg hover:-translate-y-1 hover:shadow-xl"
            @click="handleGetStarted">
          Get Started Today
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>

import Logo from "@/components/partials/Logo.vue";
import {WarpBackground} from "@/components/ui/warp-background/index.js";
import {Button} from "@/components/ui/button/index.js";

const handleGetStarted = () => {
  alert('Welcome to CoolKids! Sign up to get started.');
};
</script>

<style scoped>
@reference '@/css/index.css';

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.tilt-left-1 {
  transform: rotate(-1deg);
}

.tilt-left-2 {
  transform: rotate(-2deg);
}

.tilt-left-3 {
  transform: rotate(-3deg);
}

.tilt-right-1 {
  transform: rotate(1deg);
}

.creative-underline {
  position: relative;
  display: inline-block;
  padding: 2px 4px;
}

.creative-underline::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: currentColor;
  opacity: 0.8;
}

.students .card-image {
  background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
}

.teachers .card-image {
  background: linear-gradient(45deg, #43e97b 0%, #38f9d7 100%);
}

.parents .card-image {
  background: linear-gradient(45deg, #fa709a 0%, #fee140 100%);
}

.administrators .card-image {
  background: linear-gradient(45deg, #a8edea 0%, #fed6e3 100%);
}

.features-list li {
  padding: 8px 0;
  padding-left: 25px;
  position: relative;
  font-size: 16px;
  color: #34495e;
  line-height: 1.5;
}

.features-list li:before {
  content: "✨";
  position: absolute;
  left: 0;
  top: 8px;
}

</style>
<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-400 via-purple-400 to-pink-300 flex items-center justify-center p-4 page-font">
    <!-- Floating decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-20 left-10 w-16 h-16 bg-yellow-300 rounded-full opacity-60 animate-bounce"></div>
      <div class="absolute top-40 right-20 w-12 h-12 bg-green-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 0.5s"></div>
      <div class="absolute bottom-32 left-20 w-20 h-20 bg-blue-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 1s"></div>
      <div class="absolute bottom-20 right-10 w-14 h-14 bg-red-300 rounded-full opacity-60 animate-bounce" style="animation-delay: 1.5s"></div>
      <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-24 h-24 bg-orange-300 rounded-full opacity-40 animate-pulse" style="animation-delay: 2s"></div>
    </div>

    <div class="w-full max-w-2xl text-center relative z-10">
      <!-- 404 Card -->
      <div class="bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl border border-white/20 p-8 mb-8">
        <!-- Large 404 Text -->
        <div class="mb-8">
          <h1 class="text-9xl font-bold text-transparent bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text mb-4">
            404
          </h1>
          <h2 class="text-3xl font-bold text-gray-800 mb-2">Oops! Page Not Found</h2>
          <p class="text-gray-600 text-lg">
            Looks like you've wandered off the learning path! 🧭
          </p>
          <p class="text-gray-500 mt-2">
            The page you're looking for doesn't exist, but don't worry - we'll help you get back on track!
          </p>
        </div>

        <!-- Animated Character -->
        <div class="mb-8">
          <div class="text-8xl animate-bounce">🤔</div>
        </div>

        <!-- Login Options -->
        <div class="space-y-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-4">Choose Your Learning Journey:</h3>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Student Login -->
            <router-link 
              to="/student/login" 
              class="group bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              <div class="flex flex-col items-center space-y-3">
                <div class="bg-white/20 p-3 rounded-full group-hover:bg-white/30 transition-colors">
                  <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h4 class="text-lg font-bold">Student</h4>
                  <p class="text-sm opacity-90">Start Learning!</p>
                </div>
                <div class="text-2xl">🎓</div>
              </div>
            </router-link>

            <!-- Teacher Login -->
            <router-link 
              to="/teacher/login" 
              class="group bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              <div class="flex flex-col items-center space-y-3">
                <div class="bg-white/20 p-3 rounded-full group-hover:bg-white/30 transition-colors">
                  <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.973 5.973 0 004 15v3H1v-3a3 3 0 013.75-2.906z"/>
                  </svg>
                </div>
                <div>
                  <h4 class="text-lg font-bold">Teacher</h4>
                  <p class="text-sm opacity-90">Educate & Inspire</p>
                </div>
                <div class="text-2xl">🍎</div>
              </div>
            </router-link>

            <!-- Parent Login -->
            <router-link 
              to="/parent/login" 
              class="group bg-gradient-to-r from-purple-500 to-purple-600 hover:from-purple-600 hover:to-purple-700 text-white p-6 rounded-2xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
            >
              <div class="flex flex-col items-center space-y-3">
                <div class="bg-white/20 p-3 rounded-full group-hover:bg-white/30 transition-colors">
                  <svg class="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                </div>
                <div>
                  <h4 class="text-lg font-bold">Parent</h4>
                  <p class="text-sm opacity-90">Support & Monitor</p>
                </div>
                <div class="text-2xl">👨‍👩‍👧‍👦</div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Back to Home -->
        <div class="mt-8 pt-6 border-t border-gray-200">
          <router-link 
            to="/" 
            class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-800 font-medium transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
            </svg>
            Back to Home
          </router-link>
        </div>
      </div>

      <!-- Fun Footer -->
      <div class="text-center text-white/80">
        <p class="text-lg font-medium">
          "Every mistake is a learning opportunity!" ✨
        </p>
        <p class="text-sm mt-2 opacity-75">
          - CoolKids Learning Platform
        </p>
      </div>
    </div>
  </div>
</template>

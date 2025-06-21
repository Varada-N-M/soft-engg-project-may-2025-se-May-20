<template>
  <div id="app">
    <div class="wrapper">
      <div class="full-page-div">
        <div class="navbar">
          <div class="logo font-semibold"><logo/></div>
        </div>
        <div class="content">
          <div class="hero-section">
            <h1 class="hero-title">Welcome to <logo/></h1>
            <p class="hero-subtitle">
              The ultimate platform designed for every member of the educational community.
              Discover features tailored specifically for students, teachers, parents, and administrators.
            </p>
            <div class="center-wrapper">
              <router-link to="/student/login" class="start-btn">Get Started</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="features-container">
      <h2 class="section-title">Features</h2>

      <div class="user-card students">
        <div class="card-image">
          <img src="../assets/child.svg" alt="Children SVG" width="600" />
        </div>
        <div class="card-content">
          <h3 class="user-type-title">For Students</h3>
          <p class="user-description">
            Empower your learning journey with tools designed to help you succeed academically and personally.
          </p>
          <ul class="features-list">
            <li>Interactive homework tracker and assignment calendar</li>
            <li>Grade monitoring with real-time updates and progress analytics</li>
            <li>Collaborative study groups and peer-to-peer learning spaces</li>
            <li>Digital portfolio to showcase projects and achievements</li>
            <li>Personalized learning paths based on individual strengths</li>
            <li>Communication tools to connect with teachers and classmates</li>
            <li>Achievement badges and gamified learning experiences</li>
          </ul>
        </div>
      </div>

      <div class="user-card teachers reverse">
        <div class="card-image">
          <img src="../assets/teacher.svg" alt="Parent SVG" width="400" />
        </div>
        <div class="card-content">
          <h3 class="user-type-title">For Teachers</h3>
          <p class="user-description">
            Streamline your teaching process with comprehensive classroom management and educational tools.
          </p>
          <ul class="features-list">
            <li>Intuitive gradebook with automated calculation and reporting</li>
            <li>Lesson planning templates and curriculum alignment tools</li>
            <li>Student progress tracking with detailed analytics dashboard</li>
            <li>Digital classroom management and attendance tracking</li>
            <li>Parent communication portal with instant messaging</li>
            <li>Assignment creation with multimedia support and rubrics</li>
            <li>Professional development resources and teaching communities</li>
          </ul>
        </div>
      </div>

      <div class="user-card parents">
        <div class="card-image">
          <img src="../assets/parent.svg" alt="Parent SVG" width="600" />
        </div>
        <div class="card-content">
          <h3 class="user-type-title">For Parents</h3>
          <p class="user-description">
            Stay connected with your child's educational journey and support their growth every step of the way.
          </p>
          <ul class="features-list">
            <li>Real-time access to grades, assignments, and school announcements</li>
            <li>Direct messaging with teachers and school administrators</li>
            <li>Attendance monitoring with instant notifications</li>
            <li>Parent-teacher conference scheduling and virtual meetings</li>
            <li>Homework help resources and educational activity suggestions</li>
            <li>School event calendar with RSVP functionality</li>
            <li>Child's academic progress reports and milestone tracking</li>
          </ul>
        </div>
      </div>

      <div class="user-card administrators reverse">
        <div class="card-image">
          <img src="../assets/org.svg" alt="Organization SVG" width="600" />
        </div>
        <div class="card-content">
          <h3 class="user-type-title">For Administrators</h3>
          <p class="user-description">
            Manage your educational institution efficiently with powerful administrative tools and insights.
          </p>
          <ul class="features-list">
            <li>Comprehensive school-wide analytics and performance dashboards</li>
            <li>Staff management system with role-based permissions</li>
            <li>Student enrollment and records management platform</li>
            <li>Budget tracking and resource allocation tools</li>
            <li>Communication broadcast system for school-wide announcements</li>
            <li>Compliance reporting and documentation management</li>
            <li>Integration with existing school systems and third-party tools</li>
          </ul>
        </div>
      </div>

      <div class="cta-section">
        <h2 class="cta-title">Ready to Transform Education?</h2>
        <p style="font-size: 18px; color: #7f8c8d; margin-bottom: 30px;">
          Join thousands of schools, teachers, students, and parents who trust CoolKids for their educational needs.
        </p>
        <button class="cta-button" @click="handleGetStarted">
          Get Started Today
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>

import Logo from "@/components/partials/Logo.vue";

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

#app, .wrapper {
  min-height: 99.5vh;
  background: white;
  display: flex;
  flex-direction: column;
}

.full-page-div {
  background:  linear-gradient(
      135deg,
      rgba(139, 255, 168, 0.75) 20%, /* 50% opacity green */
      rgba(60, 200, 218, 0.75) 100%  /* 50% opacity blue */
  ),
  url("/src/assets/bg-landing-page.png") center/cover no-repeat;
  border-radius: 12px;
  color: black;
  margin: 10px;
  padding: 20px;
  flex: 1;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  @apply font-fancy;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 35px;
  margin-bottom: 20px;
  @apply font-fancy;
}

.logo {
  font-size: 35px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.login-btn {
  color: rgb(33, 31, 31);
  border: 1px solid rgba(0, 0, 0, 0.2);
  padding: 10px 20px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  backdrop-filter: blur(6px);
  transition: all 0.3s ease;
}

.login-btn:hover {
  box-shadow: 0 3px 3px rgba(0, 0, 0, 0.15);
}

.center-wrapper {
  text-align: center;
}

.start-btn{
  color: rgb(33, 31, 31);
  border: 1px solid rgba(0, 0, 0, 0.2);
  background: white;
  padding: 10px 20px;
  border-radius: 25px;
  width: 200px;
  text-align: center;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  backdrop-filter: blur(6px);
  transition: all 0.3s ease;
}

.content {
  font-size: 20px;
  font-family: "Manrope", sans-serif;
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  padding: 20px 0;
  margin: 160px;
}

.hero-section {
  text-align: center;
  margin-bottom: 40px;
}

.hero-title {
  @apply font-fancy;
  font-size: 48px;
  color: #2c3e50;
  margin-bottom: 15px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.hero-subtitle {
  font-size: 22px;
  color: #34495e;
  margin-bottom: 30px;
  max-width: 600px;
  line-height: 1.6;
}

.features-container {
  width: 100%;
  max-width: 1370px;
  display: flex;
  flex-direction: column;
  gap: 25px;
  padding: 40px 20px;
}

.section-title {
  font-size: 40px;
  text-align: center;
  margin-bottom: 100px;
  color: #2c3e50;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.user-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 45px;
  padding: 0;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
  display: flex;
  gap: 0;
  align-items: stretch;
  overflow: hidden;
  min-height: 300px;
  margin-bottom: 100px;
}

.user-card.reverse {
  flex-direction: row-reverse;
}

.card-image {
  width: 650px;
  height: auto;
  border-radius: 45px;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  box-shadow: none;
  flex-shrink: 0;
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

.card-content {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.user-type-title {
  @apply font-fancy;
  font-size: 60px;
  color: #2c3e50;
  margin-bottom: 15px;
}

.user-description {
  font-size: 16px;
  color: #7f8c8d;
  margin-bottom: 20px;
  line-height: 1.6;
}

.features-list {
  list-style: none;
  padding: 0;
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

.cta-section {
  text-align: center;
  margin-top: 50px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.cta-title {
  @apply font-fancy;
  font-size: 36px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.cta-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 30px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .auth-buttons {
    align-self: flex-end;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .user-card {
    flex-direction: column !important;
    text-align: center;
    gap: 0;
    min-height: auto;
  }

  .card-image {
    width: 100%;
    height: 200px;
  }

  .card-content {
    padding: 30px 20px;
  }

  .features-container {
    padding: 0 10px;
  }
}

@media (max-width: 600px) {
  .full-page-div {
    margin: 5px;
    padding: 15px;
  }

  .user-card {
    padding: 0;
  }

  .card-content {
    padding: 25px 15px;
  }

  .user-type-title {
    font-size: 24px;
  }

  .section-title {
    font-size: 28px;
  }
}
</style>
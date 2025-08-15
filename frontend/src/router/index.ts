import {createWebHistory, createRouter} from 'vue-router'
import { isAuthenticated, getUserType, getHomeRoute, isPublicRoute, isAuthorizedRoute, clearAuthData } from '../utils/auth'

import LandingPage from '../pages/LandingPage.vue'
import LoginStudent from '../pages/student/LoginStudent.vue';
import RegisterStudent from '../pages/student/RegisterStudent.vue';
import RegisterOrganisation from '../pages/organisation/RegisterOrganisation.vue';
import RegisterParent from '../pages/parent/RegisterParent.vue';
import LoginParent from "../pages/parent/LoginParent.vue";
import ParentHome from "../pages/parent/ParentHome.vue";
import ParentLessonUpdates from "../pages/parent/ParentLessonUpdates.vue";
import LoginOrganisation from "../pages/organisation/LoginOrganisation.vue";
import HomeOrganisation from "../pages/organisation/HomeOrganisation.vue";
import HomeStudent from "../pages/student/HomeStudent.vue";
import Badges from "../pages/student/Badges.vue";
import Habit from '../pages/student/Habit.vue';
import LessonUpdates from "../pages/student/LessonUpdates.vue";
import SurveyPage from "../pages/student/SurveyPage.vue";
import WeeklyReport from "../pages/student/WeeklyReport.vue";
import AIChat from "../pages/student/AIChat.vue";
import TodoList from "../pages/student/MyTodos.vue";
import LifeLessons from "../pages/student/LifeLessons.vue";
import StudentProfile from "../pages/student/StudentProfile.vue";
import LoginTeacher from '../pages/teacher/LoginTeacher.vue';
import RegisterTeacher from '../pages/teacher/RegisterTeacher.vue';
import SurveyReport from "../pages/teacher/SurveyReport.vue";
import TeacherLessonUpdates from "../pages/teacher/LessonUpdates.vue";
import AddStudent from "../pages/teacher/AddStudent.vue";
import StudentJournal from "../pages/student/StudentJournal.vue";
import LinkChild from '../pages/parent/LinkChild.vue';
import LinkedChildren from '../pages/parent/LinkedChildren.vue';
import AddTeacher from "../pages/organisation/AddTeacher.vue";
import TeachersList from "../pages/organisation/TeachersList.vue";
import TeacherDashboard from "../pages/teacher/Dashboard.vue";
import TeacherProfile from "../pages/teacher/TeacherProfile.vue";
import TeacherStudents from "../pages/teacher/TeacherStudents.vue";
import StudentProgress from "../pages/teacher/StudentProgress.vue";
import ClassAnalytics from "../pages/teacher/ClassAnalytics.vue";
import ChildProgress from "../pages/parent/ChildProgress.vue";
import Achievements from "../pages/parent/Achievements.vue";
import NotFound from "../pages/NotFound.vue";
import ChangePassword from '../pages/ChangePassword.vue';
import ResetPassword from '../pages/ResetPassword.vue';

const routes = [
    {path: '/', component: LandingPage},

    // BEGIN PASSWORD RECOVERY
    {path: '/user/password/change', component: ChangePassword},
    {path: '/user/password/reset', component: ResetPassword},
    // END PASSWORD RECOVERY

    // BEGIN STUDENT SECTION
    {path: '/student/login', component: LoginStudent},
    {path: '/student/register', component: RegisterStudent},
    {path: '/student/home', component: HomeStudent},
    {path: '/student/badges', component: Badges},
    {path: '/student/habit', component: Habit},
    {path: '/student/lesson-updates', component: LessonUpdates},
    {path: '/student/survey', component: SurveyPage},
    {path: '/student/journal', component: StudentJournal},
    {path: '/student/weekly-report', component: WeeklyReport},
    {path: '/student/ai-companion', component: AIChat},
    {path: '/student/todolist', component: TodoList},
    {path: '/student/life-lessons', component: LifeLessons},
    {path: '/student/profile', component: StudentProfile},
    // END STUDENT SECTION


    // BEGIN ORG SECTION
    {path: '/org/register', component: RegisterOrganisation},
    {path: '/org/login', component: LoginOrganisation},
    {path: '/org/home', component: HomeOrganisation},
    {path: '/org/survey-report', component: SurveyReport},
    {path: '/org/add-teacher', component: AddTeacher},
    {path: '/org/teachers', component: TeachersList},
    // END ORG SECTION


    // BEGIN PARENT SECTION
    {path: '/parent/register', component: RegisterParent},
    {path: '/parent/login', component: LoginParent},
    {path: '/parent/home', component: ParentHome},
    {path: '/parent/lesson-updates', component: ParentLessonUpdates},
    {path: '/parent/link-child', component: LinkChild},
    {path: '/parent/children', component: LinkedChildren},
    {path: '/parent/child-progress/:childId', component: ChildProgress},
    {path: '/parent/achievements/:childId', component: Achievements},
    // END PARENT SECTION


    // BEGIN TEACHER SECTION
    {path: '/teacher/login', component: LoginTeacher},
    {path: '/teacher/register', component: RegisterTeacher},
    {path: '/teacher/dashboard', component: TeacherDashboard},
    {path: '/teacher/home', component: TeacherDashboard},
    {path: '/teacher/profile', component: TeacherProfile},
    {path: '/teacher/students', component: TeacherStudents},
    {path: '/teacher/survey-report', component: SurveyReport},
    {path: '/teacher/lesson-updates', component: TeacherLessonUpdates},
    {path: '/teacher/add-student', component: AddStudent},
    {path: '/teacher/student-progress/:studentId', component: StudentProgress},
    {path: '/teacher/class-analytics', component: ClassAnalytics},
    // END TEACHER SECTION

    // 404 Catch-all route - must be last
    {path: '/:pathMatch(.*)*', component: NotFound},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

// Navigation Guards
router.beforeEach((to, _from, next) => {
    const authenticated = isAuthenticated()
    const userType = getUserType()
    const toPath = to.path

    // If user is not authenticated
    if (!authenticated) {
        // Allow access to public routes (login, register, landing)
        if (isPublicRoute(toPath)) {
            next()
        } else {
            // Redirect to landing page for protected routes
            next('/')
        }
        return
    }

    // If user is authenticated
    if (authenticated && userType) {
        // If trying to access login/register pages, redirect to user's home
        if (toPath.includes('/login') || toPath.includes('/register')) {
            const homeRoute = getHomeRoute(userType)
            next(homeRoute)
            return
        }

        // Check if user is authorized for the route
        if (isAuthorizedRoute(toPath, userType)) {
            next()
        } else {
            // Redirect to user's appropriate home page
            const homeRoute = getHomeRoute(userType)
            next(homeRoute)
        }
        return
    }

    // Fallback - clear invalid auth data and redirect to landing
    clearAuthData()
    next('/')
})

export default router;

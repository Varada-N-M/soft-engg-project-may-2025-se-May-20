import {createWebHistory, createRouter} from 'vue-router'

import LandingPage from '../pages/LandingPage.vue'
import LoginStudent from '../pages/student/LoginStudent.vue';
import RegisterStudent from '../pages/student/RegisterStudent.vue';
import RegisterOrganisation from '../pages/organisation/RegisterOrganisation.vue';
import RegisterParent from '../pages/parent/RegisterParent.vue';
import LoginParent from "../pages/parent/LoginParent.vue";
import LoginOrganisation from "../pages/organisation/LoginOrganisation.vue";
import HomeOrganisation from "../pages/organisation/HomeOrganisation.vue";
import HomeStudent from "../pages/student/HomeStudent.vue";
import Badges from "../pages/student/Badges.vue";
import Habit from '../pages/student/Habit.vue';
import LessonUpdates from "../pages/student/LessonUpdates.vue";
import ChildReport from '../pages/parent/ChildReport.vue';

const routes = [
    {path: '/', component: LandingPage},

    // BEGIN STUDENT SECTION
    {path: '/student/login', component: LoginStudent},
    {path: '/student/register', component: RegisterStudent},
    {path: '/student/home', component: HomeStudent},
    {path: '/student/badges', component: Badges},
    {path: '/student/habit', component: Habit},
    {path: '/student/lesson-updates', component: LessonUpdates},
    // END STUDENT SECTION


    // BEGIN ORG SECTION
    {path: '/org/register', component: RegisterOrganisation},
    {path: '/org/login', component: LoginOrganisation},
    {path: '/org/home', component: HomeOrganisation},
    // END ORG SECTION


    // BEGIN PARENT SECTION
    {path: '/parent/register', component: RegisterParent},
    {path: '/parent/login', component: LoginParent},
    {path: '/parent/child-report', component: ChildReport},
    // END PARENT SECTION

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;
import {createWebHistory, createRouter} from 'vue-router'

import LandingPage from '../pages/landing-page.vue'
import LoginStudent from '../pages/student/login-student.vue';
import RegisterStudent from '../pages/student/register-student.vue';
import RegisterOrganisation from '../pages/organisation/register-organisation.vue';
import RegisterParent from '../pages/parent/register-parent.vue';
import LoginParent from "../pages/parent/login-parent.vue";
import LoginOrganisation from "../pages/organisation/login-organisation.vue";
import HomeOrganisation from "../pages/organisation/home-organisation.vue";

const routes = [
    {path: '/', component: LandingPage},

    // BEGIN STUDENT SECTION
    {path: '/student/login', component: LoginStudent},
    {path: '/student/register', component: RegisterStudent},
    // END STUDENT SECTION


    // BEGIN ORG SECTION
    {path: '/org/register', component: RegisterOrganisation},
    {path: '/org/login', component: LoginOrganisation},
    {path: '/org/home', component: HomeOrganisation},
    // END ORG SECTION


    // BEGIN PARENT SECTION
    {path: '/parent/register', component: RegisterParent},
    {path: '/parent/login', component: LoginParent},
    // END PARENT SECTION

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;
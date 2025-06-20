import { createWebHistory, createRouter } from 'vue-router'

import LandingPage from '../pages/LandingPage.vue'
import Login from '../pages/auth/Login.vue';
import Register from '../pages/auth/Register.vue';
import { default as OrgRegister } from '../pages/organisation/Register.vue';

const routes = [
  { path: '/', component: LandingPage },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/org/register', component: OrgRegister },

]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router;
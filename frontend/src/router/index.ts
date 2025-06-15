import { createMemoryHistory, createRouter } from 'vue-router'

import LandingPage from '../pages/LandingPage.vue'

const routes = [
  { path: '/', component: LandingPage },

]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router;
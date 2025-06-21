import { createApp } from 'vue'
import './css/index.css'
import './css/custom.css'
import App from './App.vue'
import router from './router'

createApp(App)
    .use(router)
    .mount('#app')

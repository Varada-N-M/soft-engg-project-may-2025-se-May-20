// src/plugins/axios.js
import axios from 'axios'
import {BACKEND_BASE_URL} from '../constants'

// Axios instance
const api = axios.create({
    baseURL: BACKEND_BASE_URL,
    timeout: 10000,
    withCredentials: true,
})

/**
 * Get token from localStorage (or Vuex/Pinia)
 */
function getAccessToken() {
    return localStorage.getItem('access_token')
}

function getRefreshToken() {
    return localStorage.getItem('refresh_token')
}

/**
 * Save new tokens
 */
function saveTokens({accessToken, refreshToken}) {
    if (accessToken) localStorage.setItem('access_token', accessToken)
    if (refreshToken) localStorage.setItem('refresh_token', refreshToken)
}

// 🟢 Request interceptor — attach access token
api.interceptors.request.use(
    config => {
        const token = getAccessToken()
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    error => Promise.reject(error)
)

// 🟠 Response interceptor — handle 401 and attempt refresh
let isRefreshing = false
let failedQueue = [] // queue failed requests during refresh

const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
        if (error) {
            prom.reject(error)
        } else {
            prom.resolve(token)
        }
    })
    failedQueue = []
}

api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config

        if (error.response?.status === 401 && !originalRequest._retry) {
            // Avoid multiple retries
            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({resolve, reject})
                })
                    .then(token => {
                        originalRequest.headers.Authorization = `Bearer ${token}`
                        return api(originalRequest)
                    })
                    .catch(err => Promise.reject(err))
            }

            isRefreshing = true
            originalRequest._retry = true

            try {
                // 💡 Call refresh endpoint with your refresh token
                const response = await axios.post(`${BACKEND_BASE_URL}/api/auth/refresh`, {}, {
                    headers: {
                        Authorization: `Bearer ${getRefreshToken()}`
                    },
                    withCredentials: true
                })

                const {access_token, refresh_token} = response.data
                saveTokens({accessToken: access_token, refreshToken: refresh_token})
                processQueue(null, access_token)

                // Set auth header and repeat the original request
                originalRequest.headers.Authorization = `Bearer ${access_token}`
                return api(originalRequest)
            } catch (refreshError) {
                processQueue(refreshError, null)
                // optionally, logout
                localStorage.removeItem('access_token')
                localStorage.removeItem('refresh_token')
                // window.location.href = '/login'
                return Promise.reject(refreshError)
            } finally {
                isRefreshing = false
            }
        }

        return Promise.reject(error)
    }
)

export default api

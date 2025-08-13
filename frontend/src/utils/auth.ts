// Authentication utility functions

/**
 * Check if user is authenticated
 */
export function isAuthenticated(): boolean {
  const token = localStorage.getItem('access_token')
  return !!token
}

/**
 * Get current user type from localStorage
 */
export function getUserType(): string | null {
  return localStorage.getItem('user_type')
}

/**
 * Get current user email from localStorage
 */
export function getUserEmail(): string | null {
  return localStorage.getItem('user_email')
}

/**
 * Clear all authentication data
 */
export function clearAuthData(): void {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_type')
}

/**
 * Get the home page route for each user type
 */
export function getHomeRoute(userType: string): string {
  switch (userType) {
    case 'student':
      return '/student/home'
    case 'teacher':
    case 'principal':
      return '/teacher/dashboard'
    case 'parent':
      return '/parent/home'
    case 'organization':
    case 'admin':
      return '/org/home'
    default:
      return '/'
  }
}

/**
 * Check if the current route is a public route (doesn't require authentication)
 */
export function isPublicRoute(routePath: string): boolean {
  const publicRoutes = [
    '/',
    '/student/login',
    '/student/register', 
    '/teacher/login',
    '/teacher/register',
    '/parent/login',
    '/parent/register',
    '/org/login',
    '/org/register',
    '/user/password/change',
    '/user/password/reset'
  ]
  
  return publicRoutes.includes(routePath)
}

/**
 * Check if the route belongs to the current user type
 */
export function isAuthorizedRoute(routePath: string, userType: string): boolean {
  if (isPublicRoute(routePath)) {
    return true
  }

  switch (userType) {
    case 'student':
      return routePath.startsWith('/student/')
    case 'teacher':
    case 'principal':
      return routePath.startsWith('/teacher/')
    case 'parent':
      return routePath.startsWith('/parent/')
    case 'organization':
    case 'admin':
      return routePath.startsWith('/org/')
    default:
      return false
  }
}

/**
 * Logout function that can be used across components
 * Returns a logout function that clears auth data and navigates to landing
 */
export function useLogout() {
  return () => {
    clearAuthData()
    // For direct navigation without router dependency
    if (typeof window !== 'undefined') {
      window.location.href = '/'
    }
  }
}
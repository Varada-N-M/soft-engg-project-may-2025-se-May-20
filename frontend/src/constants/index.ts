// Use local backend in development, production URL in production
export const BACKEND_BASE_URL = import.meta.env.MODE === 'production' 
  ? 'https://soft-engg-project-may-2025-se-may-20-10.onrender.com'
  : 'http://localhost:5001';
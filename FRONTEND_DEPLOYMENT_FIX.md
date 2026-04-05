# Frontend Deployment Fix - Render.com Static Site

## Problem
Frontend was deployed as static site but Vue Router wasn't handling client-side routing properly. The 404 error on `/student/register` happened because the static server didn't know to redirect to `index.html`.

## Solution

### Files Updated
1. ✅ `frontend/src/constants/index.ts` - Now uses environment variable for backend URL
2. ✅ `frontend/vite.config.ts` - Added proxy for local development
3. ✅ `frontend/.env.example` - Template for environment variables
4. ✅ `frontend/render.json` - Render configuration for SPA routing
5. ✅ `frontend/public/_redirects` - Redirect all routes to index.html

---

## Deployment Steps

### Step 1: Build Frontend with Backend URL

Before deploying, you have two options:

**Option A: Use Environment Variables (Recommended)**

1. Create `.env` file in `frontend/`:
```env
VITE_BACKEND_URL=https://your-backend-service.onrender.com
```

2. Build the frontend:
```bash
cd frontend
npm install
npm run build
```

**Option B: Hardcode Backend URL (Simple)**

Just update `frontend/src/constants/index.ts`:
```typescript
export const BACKEND_BASE_URL = 'https://your-backend-url.onrender.com';
```

---

### Step 2: Redeploy Frontend on Render.com

1. Go to Render Dashboard → Your Frontend Service
2. Click "Reconnect" or redeploy to trigger a new build
3. Render will automatically use the new `_redirects` file

---

### Step 3: Configure Backend URL

#### Option A: If you have a backend service on Render

Your backend should be at: `https://your-backend-service.onrender.com`

Update the environment variable before redeploying:

1. Update `frontend/src/constants/index.ts`:
```typescript
export const BACKEND_BASE_URL = 'https://your-backend-service.onrender.com';
```

2. Or set `VITE_BACKEND_URL` on Render:
   - Dashboard → Frontend Service → Environment
   - Add: `VITE_BACKEND_URL=https://your-backend-service.onrender.com`

#### Option B: If backend is on different platform

Update the URL to wherever your backend is deployed:
- Azure: `https://your-app.azurewebsites.net`
- Heroku: `https://your-app.herokuapp.com`
- AWS: Your AWS endpoint

---

## Verification

### Test Frontend Routes

1. **Homepage:** `https://growwise-o79a.onrender.com/` ✅ Should load
2. **Sign Up:** `https://growwise-o79a.onrender.com/student/signup` ✅ Should show signup form
3. **Login:** `https://growwise-o79a.onrender.com/login` ✅ Should show login form

### Test Backend Connection

In browser console, test API call:
```javascript
fetch('https://your-backend.onrender.com/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'test@test.com', password: 'test123' })
})
.then(r => r.json())
.then(d => console.log(d))
```

Should return API response (success or error), not 404.

---

## Configuration Checklist

- [ ] Backend URL is correctly set in `frontend/src/constants/index.ts`
- [ ] Frontend deployed on Render.com as static site
- [ ] `_redirects` file exists in `frontend/public/`
- [ ] Frontend build is up to date
- [ ] Backend is running and accessible
- [ ] CORS is configured correctly on backend

---

## Common Issues & Fixes

### Issue: Still getting 404 on `/student/register`
**Fix:** 
1. Clear browser cache (Ctrl+Shift+Del)
2. Hard refresh (Ctrl+F5)
3. Check Network tab in DevTools to see if API calls go to correct backend

### Issue: API calls returning 404
**Fix:**
1. Verify backend service is running on Render
2. Check backend URL is correct
3. Verify backend has `/api/` routes (not just `/`)
4. Check CORS settings on backend

### Issue: CORS errors
**Fix on backend** - Ensure `app.py` has CORS configured:
```python
CORS(app, 
     origins=['https://growwise-o79a.onrender.com'],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
```

---

## What Your Setup Should Look Like

```
Frontend (Static Site)
├─ Render.com: https://growwise-o79a.onrender.com
├─ Vue Router handles client-side routing
└─ API calls to backend at: https://your-backend.onrender.com

Backend (Python API)
├─ Render.com or other platform
├─ Flask running on :5000/4000
├─ PostgreSQL database connected
└─ API endpoints at: /api/*
```

---

## Local Development

For local development with both frontend and backend:

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
# Backend at http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend at http://localhost:5173
```

Frontend will automatically proxy API calls to `http://localhost:5000` (configured in `vite.config.ts`).

---

## Next Steps

1. **Identify your backend service name** on Render
2. **Get the backend URL:** `https://[service-name].onrender.com`
3. **Update frontend** with correct backend URL
4. **Redeploy frontend** on Render
5. **Test all flows** (signup, login, etc.)

---

**Need Help?**

Tell me:
1. What's your backend service name on Render?
2. What URL does your backend API use?
3. Are you still getting 404 errors?

Then I can help troubleshoot further!

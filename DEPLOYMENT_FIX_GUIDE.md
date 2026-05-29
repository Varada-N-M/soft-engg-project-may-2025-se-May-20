# Student Registration Deployment Fix Guide

## Current Status
- ❌ Backend at `https://soft-engg-project-may-2025-se-may-20-10.onrender.com` is **FAILING**
- ❌ Reason: PostgreSQL database connection error (`dpg-d793b3uuk2gs73e5o8h0-a`)
- ❌ Student registration doesn't work because backend is down

---

## Quick Diagnosis: Check Your Render Services

### Step 1: Go to Render Dashboard
- https://dashboard.render.com/

### Step 2: Find Your Backend Service
Look for a service related to GrowWise backend. Check:
- **Service Name** (e.g., "growwise-backend", "soft-engg-project-backend")
- **Status** (should be "Live", not "Failed")
- **URL** (should be visible on the service page)

### Step 3: Check Environment Variables
Click on the service → **Environment** → Look for:
- `DATABASE_URL` - Is it set?
- `FLASK_ENV` - Should be `production`
- `JWT_KEY` - Is it set?

### Step 4: Check Logs
Click on **Logs** → Look for error messages

---

## Solution Option A: Use SQLite (Quick Fix ⚡)

If you want to get it working **immediately**:

### On Render Dashboard:
1. Go to Backend Service → **Environment**
2. Find `DATABASE_URL` and **DELETE IT** (or leave it empty)
3. Click "Save Changes"
4. Click "Reconnect" or "Redeploy"
5. Wait for deployment to finish

**Result:** Backend will use SQLite automatically (fallback configured)

---

## Solution Option B: Fix PostgreSQL (Production Way 🚀)

If you want to keep PostgreSQL:

### Check Your Database Service:
1. Go to Render Dashboard
2. Find your PostgreSQL database service
3. Click on it → **Info** tab
4. Copy the **Internal Database URL** (not external)
5. It looks like: `postgresql://user:pass@hostname:5432/dbname`

### Update Backend Environment Variables:
1. Go to Backend Service → **Environment**
2. Set these variables:
   ```
   FLASK_ENV=production
   DATABASE_URL=<paste-the-internal-url-here>
   JWT_KEY=your-secret-key-here
   SECRET_KEY=your-secret-key-here
   ```
3. Click "Save Changes"
4. Click "Reconnect" or "Redeploy"

---

## What We've Already Fixed

✅ **run.py** - Updated to listen on `0.0.0.0` (required for Render)
✅ **config.py** - Added SQLite fallback + connection pool settings
✅ **Database fallback** - Will use SQLite if PostgreSQL fails

---

## Next Steps After Deployment

Once you redeploy:

1. **Test the backend health:**
   ```
   curl https://soft-engg-project-may-2025-se-may-20-10.onrender.com/
   ```
   Should return something (not error 502)

2. **Test student registration:**
   - Go to `https://growwise-o79a.onrender.com/student/register`
   - Fill the form
   - Submit

3. **Check logs if it fails:**
   - Render Dashboard → Backend Service → Logs

---

## Need Help?

Share with me:
1. Your backend service name from Render
2. What error you see in the logs
3. Whether you have a PostgreSQL database service on Render

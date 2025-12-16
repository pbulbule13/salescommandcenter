# Deploy Sales Command Center to Render - Step by Step

## Complete Deployment Guide (5 Minutes)

### Step 1: Sign Up / Sign In to Render (1 minute)

1. Open your browser and go to: **https://dashboard.render.com/register**
2. Choose one of these options:
   - Click **"Sign up with GitHub"** (RECOMMENDED - easiest)
   - Or sign up with email

3. If using GitHub:
   - Authorize Render to access your GitHub account
   - Grant access to the `salescommandcenter` repository

### Step 2: Create New Blueprint (30 seconds)

1. Once logged in to Render Dashboard:
   - Click the **"New +"** button (top right)
   - Select **"Blueprint"** from the dropdown

2. Connect Repository:
   - You'll see "Connect a repository"
   - Find and select: **`pbulbule13/salescommandcenter`**
   - Click **"Connect"**

### Step 3: Configure Blueprint (1 minute)

1. Render will automatically detect `render.yaml`
2. You'll see two services being created:
   - ✅ **sales-command-center-db** (PostgreSQL Database)
   - ✅ **sales-command-center** (Web Service)

3. Set Environment Variables (OPTIONAL):
   - If you want AI features, add:
     - **Key**: `OPENAI_API_KEY`
     - **Value**: `your-openai-api-key-here`
   - Otherwise, skip this (you can add later)

4. Click **"Apply"** button

### Step 4: Wait for Deployment (2-3 minutes)

Render will now:
1. ✅ Create PostgreSQL database
2. ✅ Clone your GitHub repository
3. ✅ Run `build.sh` (install dependencies)
4. ✅ Initialize database (schema + seed data)
5. ✅ Start the web service

You'll see progress logs like:
```
Cloning repository...
Installing dependencies...
Creating database schema...
Loading seed data...
Starting server...
Live at: https://sales-command-center-xxxx.onrender.com
```

### Step 5: Access Your Application

Once deployment completes:
1. You'll see: **"Live"** status (green)
2. Click on the service name: **sales-command-center**
3. You'll see your service URL: `https://sales-command-center-xxxx.onrender.com`
4. Click the URL or copy it to your browser

**Your Sales Command Center is now live!** 🎉

---

## Alternative: CLI Deployment

If you prefer command-line deployment:

### Install Render CLI

```bash
npm install -g render-cli
```

### Login to Render

```bash
render login
```

### Deploy

```bash
cd C:\Users\pbkap\Documents\euron\Projects\salescommandcenter
render blueprint deploy
```

---

## What You'll See After Deployment

### Your Live URL will show:
- ✅ Sales Dashboard with all 4 charts working
- ✅ Fixed height charts (no page extension)
- ✅ Database with 20+ records per table
- ✅ All API endpoints functional

### Test URLs (replace with your actual URL):
```
Dashboard: https://your-app.onrender.com/
Health Check: https://your-app.onrender.com/health
API Metrics: https://your-app.onrender.com/api/dashboard/metrics
Revenue Trend: https://your-app.onrender.com/api/dashboard/revenue-trend
Regional Data: https://your-app.onrender.com/api/dashboard/regional-performance
Pipeline: https://your-app.onrender.com/api/pipeline/funnel
Products: https://your-app.onrender.com/api/products/performance
```

---

## Troubleshooting

### If Build Fails:
1. Go to your service in Render Dashboard
2. Click "Logs" tab
3. Look for the error message
4. Common issues:
   - Missing dependencies → Already in requirements.txt ✅
   - Database connection → Check DATABASE_URL is set ✅
   - Permission on build.sh → Render handles this ✅

### If Database Doesn't Initialize:
1. Go to Render Dashboard → Your web service
2. Click "Shell" tab
3. Run:
   ```bash
   cd sales_command_center
   python init_db.py
   ```

### Free Tier Sleeping:
- Free tier apps sleep after 15 min of inactivity
- First request after sleep takes 30-60 seconds
- Keep-alive services or upgrade to paid tier ($7/mo) for always-on

---

## Cost Breakdown

### Free Tier (What you get):
- ✅ PostgreSQL: 1GB storage, 90 days
- ✅ Web Service: 750 hours/month
- ✅ Auto-sleep when inactive
- ✅ Perfect for development/demo

### Paid Tier (If you need more):
- 💰 PostgreSQL: $7/month (always on, no expiration)
- 💰 Web Service: $7/month (always on, no sleep)
- 💰 Total: ~$14/month for production-ready setup

---

## Next Steps After Deployment

1. ✅ Share your live URL
2. ✅ Test all dashboard features
3. ✅ Add custom domain (optional)
4. ✅ Set up monitoring alerts
5. ✅ Add OPENAI_API_KEY for AI features

---

## Quick Reference

| What | Where |
|------|-------|
| Render Dashboard | https://dashboard.render.com |
| Your Repository | https://github.com/pbulbule13/salescommandcenter |
| Deployment Config | render.yaml in repo root |
| Build Script | build.sh in repo root |
| App Server | sales_command_center/app.py |

---

## Need Help?

If you encounter any issues during deployment:
1. Check Render logs in Dashboard
2. Review DEPLOYMENT.md for detailed troubleshooting
3. Check build.sh script execution
4. Verify DATABASE_URL is automatically set by Render

**Deployment should take less than 5 minutes total!**

---

**Ready? Go to: https://dashboard.render.com and follow the steps above!**

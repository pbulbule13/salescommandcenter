# Sales Command Center - Render Deployment Guide

## Quick Deploy to Render

### Prerequisites
- GitHub account with the repository: https://github.com/pbulbule13/salescommandcenter
- Render account (free tier available): https://render.com

### Deployment Steps

#### Option 1: Using Render Blueprint (Recommended)

1. **Login to Render**
   - Go to https://render.com
   - Sign in with your GitHub account

2. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository: `pbulbule13/salescommandcenter`
   - Render will automatically detect the `render.yaml` file

3. **Configure Environment Variables**
   - Render will prompt you to set these required variables:
     - `OPENAI_API_KEY`: Your OpenAI API key (optional but recommended for AI features)
     - `ANTHROPIC_API_KEY`: Your Anthropic API key (optional alternative)

4. **Deploy**
   - Click "Apply"
   - Render will:
     - Create a PostgreSQL database (free tier)
     - Build and deploy the web service
     - Run database initialization automatically

5. **Access Your Application**
   - Once deployed, Render will provide a URL like:
     `https://sales-command-center.onrender.com`

#### Option 2: Manual Deployment

1. **Create PostgreSQL Database**
   - Go to Render Dashboard
   - Click "New +" → "PostgreSQL"
   - Name: `sales-command-center-db`
   - Region: Oregon (or closest to you)
   - Plan: Free
   - Click "Create Database"

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `sales-command-center`
     - **Region**: Oregon (same as database)
     - **Branch**: `master`
     - **Root Directory**: Leave empty
     - **Runtime**: Python 3
     - **Build Command**: `./build.sh`
     - **Start Command**: `cd sales_command_center && uvicorn app:app --host 0.0.0.0 --port $PORT`

3. **Add Environment Variables**
   In the web service settings, add:
   ```
   PORT=10000
   ENVIRONMENT=production
   DEBUG=False
   DATABASE_URL=[Copy from PostgreSQL database]
   OPENAI_API_KEY=[Your OpenAI key]
   CORS_ORIGINS=*
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically

### Post-Deployment

#### Verify Deployment

1. **Check Health Endpoint**
   ```bash
   curl https://your-app.onrender.com/health
   ```

   Should return:
   ```json
   {
     "status": "healthy",
     "service": "Sales Command Center",
     "version": "1.0.0"
   }
   ```

2. **Access Dashboard**
   - Open `https://your-app.onrender.com` in your browser
   - You should see the Sales Command Center dashboard

3. **Test API Endpoints**
   ```bash
   curl https://your-app.onrender.com/api/dashboard/metrics
   curl https://your-app.onrender.com/api/dashboard/revenue-trend
   ```

#### Database Verification

The database should be automatically initialized with:
- ✅ Schema created (all tables)
- ✅ Seed data loaded (20+ records per table)

To verify, check the Render logs:
```
Database initialization completed successfully!
```

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string (auto-set by Render) |
| `PORT` | Yes | 10000 | Port for the web service |
| `ENVIRONMENT` | No | development | Set to `production` for Render |
| `DEBUG` | No | False | Enable debug mode |
| `OPENAI_API_KEY` | No | - | OpenAI API key for AI features |
| `ANTHROPIC_API_KEY` | No | - | Anthropic API key (alternative to OpenAI) |
| `SECRET_KEY` | No | auto-generated | Secret key for sessions |
| `JWT_SECRET_KEY` | No | auto-generated | JWT signing key |
| `CORS_ORIGINS` | No | * | Allowed CORS origins |

### Troubleshooting

#### Build Fails

1. **Check build logs** in Render dashboard
2. Common issues:
   - Missing dependencies → Check `requirements.txt`
   - Permission error on `build.sh` → Render should handle this automatically
   - Database connection error → Verify `DATABASE_URL` is set

#### Database Not Initialized

1. Go to Render dashboard → Web Service → Shell
2. Run manually:
   ```bash
   cd sales_command_center
   python init_db.py
   ```

#### Application Won't Start

1. Check the logs in Render dashboard
2. Verify environment variables are set
3. Check that `PORT` is set to `$PORT` (Render provides this)

#### CORS Errors

1. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

### Updating the Application

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update application"
   git push origin master
   ```

2. Render will automatically:
   - Detect the push
   - Rebuild the application
   - Deploy the new version
   - Keep the database intact

### Cost

**Free Tier Limits:**
- PostgreSQL: 1GB storage, expires after 90 days
- Web Service: 750 hours/month, spins down after 15 min of inactivity
- Auto-sleeps when not in use (15-30 second cold start)

**Paid Plans:**
- PostgreSQL: Starting at $7/month (persistent, no auto-sleep)
- Web Service: Starting at $7/month (always on, faster)

### Custom Domain (Optional)

1. Go to your web service settings
2. Add custom domain
3. Update DNS records as instructed by Render

### Monitoring

Render provides:
- Real-time logs
- Metrics dashboard
- Automatic health checks
- Email alerts for failures

Access via: Dashboard → Your Service → Metrics/Logs

### Backup Database

```bash
# Download backup from Render dashboard
# Or use pg_dump via Shell:
pg_dump $DATABASE_URL > backup.sql
```

## Support

- Render Documentation: https://render.com/docs
- GitHub Issues: https://github.com/pbulbule13/salescommandcenter/issues

## Architecture

```
GitHub Repository
    ↓
Render Blueprint (render.yaml)
    ↓
[PostgreSQL Database] ← [FastAPI Web Service]
         ↓                        ↓
    Schema + Seed Data     Dashboard + API Endpoints
```

## Next Steps

After deployment:
1. ✅ Set up custom domain (optional)
2. ✅ Configure monitoring alerts
3. ✅ Add API keys for AI features
4. ✅ Integrate with Salesforce/Netsuite (optional)
5. ✅ Set up email notifications (optional)

---

**Deployed**: Ready to use at `https://your-app.onrender.com`

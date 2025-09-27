# Railway Deployment Guide

## 🚀 Quick Deploy to Railway

### Step 1: Connect GitHub Repository
1. Go to [Railway](https://railway.app)
2. Click "Deploy from GitHub repo"
3. Select your `jam-hot-project` repository
4. **Important**: Set the **Root Directory** to `deploy/`

### Step 2: Add PostgreSQL Database
1. In your Railway project dashboard
2. Click "New" → "Database" → "Add PostgreSQL"
3. Railway will automatically provide the `DATABASE_URL` environment variable

### Step 3: Configure Deployment
Railway will automatically:
- Detect Python application
- Install dependencies from `requirements.txt`
- Run database restoration script
- Start the API server

### Step 4: Verify Deployment
Once deployed, test these endpoints:
- `https://your-app.railway.app/` - API status
- `https://your-app.railway.app/health` - Health check
- `https://your-app.railway.app/recipes/titles` - Recipe titles (main test)
- `https://your-app.railway.app/recipes/count` - Database statistics

## 🔧 Important Railway Settings

### Root Directory Setting
**Critical**: Set the root directory to `deploy/` in Railway settings:
1. Go to your service settings
2. Find "Source" section
3. Set "Root Directory" to `deploy`

This ensures Railway only deploys the contents of the `deploy/` folder.

### Environment Variables
Railway automatically provides:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Application port (usually 8000)

No manual environment variable setup needed!

## 📊 Expected Results

After successful deployment:
- **116 recipes** loaded from database dump
- **29 fruit profiles** available
- **252 recipe-fruit relationships** for filtering
- All API endpoints responding correctly

## 🐛 Troubleshooting

### Database Connection Issues
- Check Railway PostgreSQL service is running
- Verify `DATABASE_URL` is automatically set
- Check logs for connection errors

### Build Issues
- Ensure `requirements.txt` is in deploy folder
- Check Python version compatibility (3.11)
- Review build logs in Railway dashboard

### Data Loading Issues
- Check if `database_dump.sql` is included in deployment
- Review `restore_database.py` logs
- Verify PostgreSQL client is available in Railway environment

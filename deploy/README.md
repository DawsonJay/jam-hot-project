# Jam Hot API - Railway Deployment

This directory contains the Railway deployment configuration for the Jam Hot API.

## 🚀 Deployment Structure

```
deploy/
├── main.py              # FastAPI application
├── restore_database.py  # Database restoration script
├── database_dump.sql    # PostgreSQL database dump
├── requirements.txt     # Python dependencies
├── Procfile            # Railway process configuration
├── railway.json        # Railway deployment config
├── runtime.txt         # Python version specification
└── README.md           # This file
```

## 📡 API Endpoints

- `GET /` - API status and endpoint list
- `GET /health` - Health check
- `GET /recipes/titles` - Get all recipe titles
- `GET /recipes` - Get all recipes with full data
- `GET /recipes/count` - Get recipe statistics
- `GET /fruits` - Get all fruit profiles

## 🗄️ Database Setup

The deployment includes:
1. **Database dump** (`database_dump.sql`) - Contains all recipe and fruit profile data
2. **Restoration script** (`restore_database.py`) - Automatically restores data on deployment

## ⚙️ Railway Configuration

### Environment Variables Required:
- `DATABASE_URL` - Automatically provided by Railway PostgreSQL service
- `PORT` - Automatically provided by Railway (defaults to 8000)

### Deployment Process:
1. Railway builds the application using Nixpacks
2. Installs dependencies from `requirements.txt`
3. Runs `restore_database.py` to populate the database
4. Starts the API server with `python main.py`

## 🔧 Local Testing

To test locally before deployment:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://user:pass@host:port/database"

# Run the application
python main.py
```

## 📊 Current Database Contents

- **116 recipes** from multiple sources (AllRecipes, Serious Eats, Food Network, BBC Good Food)
- **29 fruit profiles** with scientific data
- **252 recipe-fruit relationships** for advanced filtering
- All recipes validated for quality (ratings required, jam-specific content)

## 🎯 Portfolio Value

This deployment demonstrates:
- **Full-stack development** - Database + API + deployment
- **Data quality focus** - Validated, structured recipe data
- **Scalable architecture** - FastAPI with PostgreSQL
- **DevOps skills** - Railway deployment with proper configuration
- **API design** - RESTful endpoints with comprehensive data access

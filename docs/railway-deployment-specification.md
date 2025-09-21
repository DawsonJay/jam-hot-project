# Railway Deployment Specification - Jam Hot Project

## Overview
This specification covers the deployment of the Jam Hot backend API on Railway, including configuration, optimization, and scaling considerations for both free and paid tiers.

## Railway Plan Selection

### Free Tier Considerations
- **Memory limit**: 512MB RAM
- **Storage**: Limited persistent storage
- **CPU**: Shared resources
- **Bandwidth**: Limited monthly usage
- **Sleep mode**: App sleeps after inactivity

### Paid Tier Benefits (Lowest tier)
- **Memory limit**: 1GB RAM
- **Storage**: More persistent storage
- **CPU**: Better performance
- **Bandwidth**: Higher limits
- **Always on**: No sleep mode

## Railway Configuration

### railway.json
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/api/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Environment Variables
```bash
# Railway will set these automatically
PORT=8080
RAILWAY_ENVIRONMENT=production
RAILWAY_PUBLIC_DOMAIN=your-app.railway.app

# PostgreSQL connection (Railway will provide)
DATABASE_URL=postgresql://user:password@host:port/database

# Custom environment variables
MODEL_PATH=/app/data/trained_model
CONFIDENCE_THRESHOLD=0.7
MAX_IMAGE_SIZE=5242880  # 5MB
```

## Backend Optimizations for Railway

### Memory Management
```python
# config/railway_config.py
import os

class RailwayConfig:
    # Memory limits
    MAX_MEMORY_MB = 400  # Leave buffer for system
    MODEL_MEMORY_MB = 200  # Estimated model size
    DATABASE_MEMORY_MB = 50  # Database cache
    
    # Model optimization
    MODEL_QUANTIZATION = True  # Use quantized model
    BATCH_SIZE = 1  # Process one image at a time
    IMAGE_SIZE = (224, 224)  # Smaller input size
    
    # Database optimization
    CONNECTION_POOL_SIZE = 5
    QUERY_CACHE_SIZE = 100
```

### Model Optimization
```python
# models/railway_model.py
class RailwayOptimizedModel:
    def __init__(self):
        # Load quantized model for Railway
        self.model = self.load_quantized_model()
        self.confidence_threshold = 0.7
    
    def load_quantized_model(self):
        # Use TensorFlow Lite or quantized model
        # Smaller file size, less memory usage
        pass
    
    def predict_single(self, image):
        # Process one image at a time
        # Return only top prediction to save memory
        pass
```

### Database Optimization
```python
# database/railway_db.py
import psycopg2
from psycopg2 import pool

class RailwayDatabase:
    def __init__(self):
        # Use connection pooling for PostgreSQL
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 5,  # min and max connections
            os.getenv('DATABASE_URL')
        )
        
    def get_connection(self):
        return self.connection_pool.getconn()
    
    def return_connection(self, conn):
        self.connection_pool.putconn(conn)
```

## Scaling Considerations

### Data Growth Strategy
- **Database size**: Estimated 500KB-1MB (well within 1GB free tier)
- **Local development**: Create and populate database locally
- **Database dump**: Use `pg_dump` to create database snapshot
- **Deployment**: Restore dump to Railway PostgreSQL service
- **Updates**: Manual dump/restore for rare database changes

### Performance Monitoring
```python
# utils/railway_monitoring.py
import psutil
import logging

class RailwayMonitor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def check_memory_usage(self):
        memory_percent = psutil.virtual_memory().percent
        if memory_percent > 80:
            self.logger.warning(f"High memory usage: {memory_percent}%")
            return False
        return True
    
    def log_performance_metrics(self):
        # Log memory, CPU, response times
        pass
```

## Database Deployment Process

### 1. Local Database Setup
```bash
# Create local PostgreSQL database
createdb jam_hot_local

# Run scraper to populate database
python scraper.py

# Create database dump
pg_dump jam_hot_local > jam_hot_dump.sql
```

### 2. Railway Database Setup
```bash
# Add PostgreSQL service to Railway project
# Get DATABASE_URL from Railway dashboard

# Restore database to Railway
psql $DATABASE_URL < jam_hot_dump.sql
```

### 3. Database Size Estimation
- **Recipes (200+)**: ~330KB
- **Fruits + Profiles (50+)**: ~105KB  
- **Relationships**: ~8KB
- **PostgreSQL overhead**: ~50KB
- **Total estimated**: 500KB-1MB
- **Railway free tier**: 1GB ✅ **Plenty of room!**

## Deployment Process

### 1. Railway Setup
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Link to existing project
railway link
```

### 2. Environment Configuration
```bash
# Set environment variables
railway variables set MODEL_PATH=/app/data/trained_model
railway variables set CONFIDENCE_THRESHOLD=0.7
railway variables set MAX_IMAGE_SIZE=5242880
```

### 3. Database Setup
```bash
# Create PostgreSQL service on Railway
railway add postgresql

# Run database migrations
railway run python scripts/run_migrations.py

# Populate database with scraped data
railway run python scripts/populate_database.py

# Update fruit coverage status (check profiles table)
railway run python scripts/update_coverage.py
```

### 4. Model Deployment
```bash
# Upload trained model
railway run python scripts/upload_model.py

# Test model loading
railway run python scripts/test_model.py
```

## Monitoring and Maintenance

### Health Checks
```python
# api/health.py
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "memory_usage": psutil.virtual_memory().percent,
        "model_loaded": model_manager.is_loaded(),
        "databases_connected": db_manager.is_connected(),
        "timestamp": datetime.utcnow().isoformat()
    }
```

### Logging Configuration
```python
# config/logging.py
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
```

### Error Handling
```python
# utils/railway_errors.py
class RailwayError(Exception):
    pass

class MemoryLimitError(RailwayError):
    pass

class DatabaseConnectionError(RailwayError):
    pass

def handle_railway_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except MemoryError:
            raise MemoryLimitError("Memory limit exceeded")
        except psycopg2.Error as e:
            raise DatabaseConnectionError(f"Database error: {e}")
    return wrapper
```

## Cost Optimization

### Free Tier Strategies
- **Model size**: Use smallest effective model
- **Database size**: Keep databases under 100MB
- **Caching**: Implement aggressive caching
- **Sleep handling**: Graceful wake-up from sleep

### Paid Tier Benefits
- **Larger model**: Use more accurate model
- **More data**: Store more recipes and fruit info
- **Better performance**: Faster response times
- **Always on**: No cold start delays

## Success Criteria
- **Deployment success**: App runs on Railway without errors
- **Performance**: <5 second response times
- **Memory usage**: <80% of Railway limits
- **Uptime**: 99%+ availability
- **Scalability**: Can handle 100+ concurrent users
- **Independence**: Works perfectly without maintenance for a year+
- **Stability**: Never crashes or glitches
- **Database size**: Well within Railway PostgreSQL limits

## Troubleshooting

### Common Issues
1. **Memory limit exceeded**: Reduce model size, optimize database
2. **Cold start delays**: Implement model preloading
3. **Database connection errors**: Check connection pooling
4. **Model loading failures**: Verify model file paths

### Debug Commands
```bash
# Check Railway logs
railway logs

# Check app status
railway status

# Run diagnostics
railway run python scripts/diagnostics.py
```

## Portfolio Value
- **Cloud deployment**: Real-world deployment experience
- **Resource optimization**: Memory and performance optimization
- **Monitoring**: Production monitoring and logging
- **Scaling**: Understanding of platform limitations and solutions
- **DevOps**: Deployment automation and configuration management

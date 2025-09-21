# Backend Specification - Jam Hot Project

## Overview
The backend API serves as the central processing hub, handling AI model inference, database queries, and API endpoints. It connects the frontend with the AI model and databases, providing a clean separation of concerns.

## Architecture

### API Server (FastAPI)
- **RESTful API**: Clean endpoints for frontend communication
- **Request handling**: Photo upload, database queries, error management
- **Response formatting**: Structured JSON responses
- **CORS support**: Enable frontend communication

### AI Model Integration
- **Model loading**: Load trained fruit classification model
- **Image preprocessing**: Resize, normalize images for model
- **Inference**: Run fruit classification on uploaded photos
- **Post-processing**: Format results for API response

### Database Management
- **Single PostgreSQL Database**: All data in one database
- **Fruits Table**: All AI-recognizable fruits (basic info only)
- **Profiles Table**: Detailed fruit information (only for covered fruits)
- **Recipes Table**: Jam recipes with ingredients, instructions, ratings
- **Recipe-Fruits Junction**: Many-to-many with primary fruit tracking
- **Smart Coverage**: Covered = has entry in profiles table
- **Focused scope**: Fruits only (herbs, spices, other ingredients not profiled)
- **Query optimization**: Efficient PostgreSQL queries with indexes

## API Endpoints

### Core Endpoints

#### POST /api/classify
**Purpose**: Upload photos and get fruit identification + info
**Request**:
```json
{
  "images": ["base64_image1", "base64_image2"],
  "return_recipes": true,
  "return_flavor_info": true,
  "confidence_threshold": 0.7
}
```
**Response**:
```json
{
  "fruits": [
    {
      "name": "strawberry",
      "confidence": 0.95,
      "status": "recognized_with_data",
      "flavor_profile": {...},
      "description": "...",
      "recipes_available": true
    },
    {
      "name": "dragon_fruit",
      "confidence": 0.88,
      "status": "recognized_no_data",
      "message": "Fruit recognized but no jam recipes available yet"
    },
    {
      "name": "unknown",
      "confidence": 0.45,
      "status": "unrecognized",
      "message": "Unable to identify this fruit with sufficient confidence"
    }
  ],
  "recipes": [...],
  "processing_time": 2.3
}
```

#### GET /api/recipes
**Purpose**: Get recipes for specific fruits
**Parameters**: `fruits=strawberry,blueberry&limit=10&difficulty=intermediate`
**Response**:
```json
{
  "recipes": [...],
  "total_count": 25,
  "filters_applied": {...}
}
```

#### GET /api/fruit-info
**Purpose**: Get detailed fruit information
**Parameters**: `fruits=strawberry,blueberry`
**Response**:
```json
{
  "fruits": [
    {
      "name": "strawberry",
      "description": "...",
      "flavor_profile": {...},
      "jam_uses": [...]
    }
  ]
}
```

#### GET /api/health
**Purpose**: Health check endpoint
**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "databases_connected": true,
  "timestamp": "2025-09-21T19:16:00Z"
}
```

## Technical Implementation

### FastAPI Application Structure
```python
# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from models.fruit_classifier import FruitClassifier
from database.recipe_db import RecipeDatabase
from database.fruit_db import FruitDatabase

app = FastAPI(title="Jam Hot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
classifier = FruitClassifier()
recipe_db = RecipeDatabase()
fruit_db = FruitDatabase()
```

### AI Model Integration
```python
# models/fruit_classifier.py
class FruitClassifier:
    def __init__(self):
        self.model = self.load_model()
        self.confidence_threshold = 0.7
        self.available_fruits = self.load_available_fruits()
    
    def classify_fruits(self, images, confidence_threshold=0.7):
        results = []
        for image in images:
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # Run inference
            predictions = self.model.predict(processed_image)
            top_prediction = predictions[0]
            
            fruit_name = top_prediction['name']
            confidence = top_prediction['confidence']
            
            # Determine status based on confidence and data availability
            if confidence >= confidence_threshold:
                if fruit_name in self.available_fruits:
                    status = "recognized_with_data"
                else:
                    status = "recognized_no_data"
            else:
                status = "unrecognized"
                fruit_name = "unknown"
            
            results.append({
                "name": fruit_name,
                "confidence": confidence,
                "status": status
            })
        
        return results
    
    def get_fruit_info(self, fruit_results):
        # Query databases only for recognized fruits with data
        fruits_with_data = [f for f in fruit_results if f['status'] == 'recognized_with_data']
        return self.query_fruit_database(fruits_with_data)
```

### Database Integration
```python
# database/database_manager.py
class DatabaseManager:
    def __init__(self, connection_string):
        self.connection = psycopg2.connect(connection_string)
    
    def get_recipes_by_fruits(self, fruit_names, filters=None):
        # Query recipes using JOIN with recipe_fruits table
        # AI identifies "strawberry" → JOIN recipes with recipe_fruits
        # Apply filters (difficulty, rating, etc.)
        # Return top 3 recipes per fruit combination
        pass
    
    def get_fruit_info(self, fruit_names):
        # Query fruit information using ai_identifier
        # AI identifies "strawberry" → JOIN fruits with profiles table
        # Return descriptions and flavor profiles for covered fruits
        pass
    
    def get_coverage_status(self, fruit_names):
        # Check which fruits are covered (have entry in profiles table)
        # LEFT JOIN fruits with profiles to determine coverage
        # Return status: covered, not_covered, or unrecognized
        pass
    
    def add_fruit_if_needed(self, fruit_name, ai_identifier):
        # Check if fruit exists in fruits table
        # If not, create new fruit entry
        # Return fruit_id for recipe_fruits relationship
        pass
```

## Project Structure
```
deployable/backend/                 # Production deployment only
├── main.py
├── railway.json                    # Railway deployment config
├── requirements.txt                # Python dependencies
├── models/
│   ├── fruit_classifier.py
│   └── model_utils.py
├── database/
│   ├── recipe_db.py
│   ├── fruit_db.py
│   └── database_utils.py
├── api/
│   ├── endpoints/
│   │   ├── classify.py
│   │   ├── recipes.py
│   │   └── fruit_info.py
│   └── schemas/
│       ├── requests.py
│       └── responses.py
├── utils/
│   ├── image_processing.py
│   └── validation.py
└── data/
    ├── database_migrations/        # PostgreSQL schema migrations
    │   ├── 001_create_tables.sql
    │   └── 002_add_indexes.sql
    └── trained_model/
        ├── model.h5
        └── class_labels.json
```

## Data Flow

### Photo Classification Flow
```
1. Frontend uploads photos → POST /api/classify
2. Backend preprocesses images
3. AI model classifies fruits
4. Backend queries fruit info database
5. Backend queries recipe database (if requested)
6. Backend returns combined results
7. Frontend displays results
```

### Recipe Query Flow
```
1. Frontend requests recipes → GET /api/recipes
2. Backend parses fruit parameters
3. Backend queries recipe database
4. Backend applies filters and sorting
5. Backend returns formatted recipes
6. Frontend displays recipe cards
```

## Error Handling

### API Error Responses
```json
{
  "error": "INVALID_IMAGE",
  "message": "Image format not supported",
  "details": "Supported formats: JPEG, PNG, WebP"
}
```

### Common Error Types
- **INVALID_IMAGE**: Unsupported image format
- **MODEL_ERROR**: AI model processing failed
- **DATABASE_ERROR**: Database query failed
- **VALIDATION_ERROR**: Request validation failed
- **RATE_LIMIT**: Too many requests

## Performance Optimization

### Model Optimization
- **Model caching**: Keep model in memory
- **Batch processing**: Process multiple images together
- **Image resizing**: Optimize image size for model
- **Async processing**: Non-blocking API calls
- **Railway optimization**: Lightweight model for free tier

### Database Optimization
- **Connection pooling**: Reuse database connections
- **Query optimization**: Efficient SQL queries
- **Indexing**: Proper database indexes
- **Caching**: Cache frequent queries
- **Lazy loading**: Only load data for recognized fruits

### Railway-Specific Optimizations
- **Memory management**: Optimize for Railway's memory limits
- **Cold start**: Fast model loading on startup
- **Database size**: Keep databases under Railway limits
- **Environment variables**: Use Railway's config system

## Security Considerations

### Input Validation
- **Image validation**: Check file types and sizes
- **Parameter validation**: Validate all input parameters
- **SQL injection**: Use parameterized queries
- **File upload limits**: Restrict file sizes

### CORS Configuration
- **Production**: Restrict origins to frontend domain
- **Development**: Allow localhost for testing
- **Headers**: Configure appropriate headers

## Success Criteria
- **API response time**: <3 seconds for classification
- **Model accuracy**: 90%+ fruit identification
- **Database performance**: <500ms for recipe queries
- **Error handling**: Graceful error responses with user-friendly messages
- **Uptime**: 99%+ availability
- **Independence**: Works perfectly without maintenance for a year+
- **Stability**: Never crashes or glitches when users try to use it
- **Concurrent users**: Handle 100+ users (nice to have, not priority)

## Portfolio Value
- **API design**: RESTful API with proper endpoints
- **Database integration**: PostgreSQL with efficient queries
- **AI integration**: Model inference in production
- **Error handling**: Robust error management
- **Performance**: Optimized for real-world use

## Development Timeline
- **Week 3, Days 1-2**: Build FastAPI application and basic endpoints
- **Week 3, Days 3-4**: Integrate AI model and databases
- **Week 3, Day 5**: Testing, optimization, and deployment

## Technical Dependencies
- **Python packages**: fastapi, uvicorn, psycopg2, sqlalchemy, tensorflow, pillow
- **AI model**: Trained fruit classification model (deployed)
- **Database**: Railway PostgreSQL service
- **Deployment**: Railway (free or lowest tier paid plan)
- **Environment**: Railway-compatible deployment configuration
- **Data source**: Populated by local Selenium scraper (not deployed)

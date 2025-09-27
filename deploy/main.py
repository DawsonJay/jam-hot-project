#!/usr/bin/env python3
"""
Jam Hot API - Railway Deployment
Main FastAPI application for serving recipe data.
"""

import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from urllib.parse import urlparse
from typing import List, Dict, Any
import json

app = FastAPI(
    title="Jam Hot API",
    description="AI-Powered Jam Recipe Database API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_database_connection():
    """Get database connection using Railway environment variables."""
    database_url = os.getenv('DATABASE_URL')
    
    if database_url:
        # Parse Railway DATABASE_URL
        parsed = urlparse(database_url)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password
        )
    else:
        # Fallback to individual environment variables
        conn = psycopg2.connect(
            host=os.getenv('PGHOST', 'localhost'),
            port=int(os.getenv('PGPORT', '5432')),
            database=os.getenv('PGDATABASE', 'jam_hot'),
            user=os.getenv('PGUSER', 'postgres'),
            password=os.getenv('PGPASSWORD', '')
        )
    
    return conn

@app.get("/")
async def root():
    """Root endpoint - API status."""
    return {
        "message": "🍓 Welcome to Jam Hot API!",
        "description": "AI-Powered Jam Recipe Database",
        "version": "1.0.0",
        "endpoints": {
            "/recipes/titles": "Get all recipe titles",
            "/recipes": "Get all recipes with full data",
            "/recipes/count": "Get recipe count statistics",
            "/health": "Health check"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2025-09-27T10:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.get("/recipes/titles")
async def get_recipe_titles() -> List[str]:
    """Get all recipe titles."""
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT title FROM recipes ORDER BY title")
        titles = [row[0] for row in cur.fetchall()]
        
        cur.close()
        conn.close()
        
        return titles
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recipe titles: {str(e)}")

@app.get("/recipes/count")
async def get_recipe_count() -> Dict[str, Any]:
    """Get recipe count statistics."""
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        
        # Total recipes
        cur.execute("SELECT COUNT(*) FROM recipes")
        total_recipes = cur.fetchone()[0]
        
        # Total fruit profiles
        cur.execute("SELECT COUNT(*) FROM fruit_profiles")
        total_fruits = cur.fetchone()[0]
        
        # Recipe-fruit relationships
        cur.execute("SELECT COUNT(*) FROM recipe_fruits")
        total_relationships = cur.fetchone()[0]
        
        # Recipes by source
        cur.execute("SELECT source, COUNT(*) FROM recipes GROUP BY source ORDER BY COUNT(*) DESC")
        by_source = dict(cur.fetchall())
        
        # Top fruit combinations
        cur.execute("""
            SELECT 
                STRING_AGG(fp.fruit_name, ', ' ORDER BY fp.fruit_name) as fruit_combination,
                COUNT(*) as recipe_count
            FROM recipes r
            JOIN recipe_fruits rf ON r.id = rf.recipe_id
            JOIN fruit_profiles fp ON rf.fruit_id = fp.id
            WHERE rf.is_primary = true
            GROUP BY r.id
            HAVING COUNT(*) > 0
        """)
        combinations = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return {
            "total_recipes": total_recipes,
            "total_fruit_profiles": total_fruits,
            "total_relationships": total_relationships,
            "recipes_by_source": by_source,
            "sample_fruit_combinations": [combo[0] for combo in combinations[:10]]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recipe statistics: {str(e)}")

@app.get("/recipes")
async def get_all_recipes() -> List[Dict[str, Any]]:
    """Get all recipes with full data."""
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id, title, ingredients, instructions, rating, review_count,
                source, source_url, image_url, servings, created_date, scraped_date
            FROM recipes 
            ORDER BY rating DESC, review_count DESC
        """)
        
        recipes = []
        for row in cur.fetchall():
            recipe = {
                "id": row[0],
                "title": row[1],
                "ingredients": json.loads(row[2]) if row[2] else [],
                "instructions": json.loads(row[3]) if row[3] else [],
                "rating": float(row[4]) if row[4] else None,
                "review_count": row[5],
                "source": row[6],
                "source_url": row[7],
                "image_url": row[8],
                "servings": row[9],
                "created_date": row[10].isoformat() if row[10] else None,
                "scraped_date": row[11].isoformat() if row[11] else None
            }
            recipes.append(recipe)
        
        cur.close()
        conn.close()
        
        return recipes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch recipes: {str(e)}")

@app.get("/fruits")
async def get_fruit_profiles() -> List[Dict[str, Any]]:
    """Get all fruit profiles."""
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id, fruit_name, scientific_name, description, 
                season, nutritional_data, jam_making_properties,
                image_url, created_date
            FROM fruit_profiles 
            ORDER BY fruit_name
        """)
        
        fruits = []
        for row in cur.fetchall():
            fruit = {
                "id": row[0],
                "fruit_name": row[1],
                "scientific_name": row[2],
                "description": row[3],
                "season": row[4],
                "nutritional_data": json.loads(row[5]) if row[5] else {},
                "jam_making_properties": json.loads(row[6]) if row[6] else {},
                "image_url": row[7],
                "created_date": row[8].isoformat() if row[8] else None
            }
            fruits.append(fruit)
        
        cur.close()
        conn.close()
        
        return fruits
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch fruit profiles: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

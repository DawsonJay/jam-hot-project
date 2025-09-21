# Database Schema - Jam Hot Project

## Overview
PostgreSQL database design for the Jam Hot project, optimized for Railway deployment and focused on essential recipe data.

## Database Design Philosophy
- **Single database** - All data in one PostgreSQL instance
- **Essential data focus** - Only store what's required for functionality
- **Fruits-only scope** - AI recognition and profiling limited to fruits
- **Smart coverage tracking** - Know which fruits have detailed profiles
- **Recipe ranking** - Use ratings and review counts for popularity

## Core Tables

### 1. Fruits Table
**Purpose**: All AI-recognizable fruits (basic info only)
```sql
CREATE TABLE fruits (
    id SERIAL PRIMARY KEY,
    fruit_name VARCHAR(100) UNIQUE NOT NULL,
    ai_identifier VARCHAR(100) UNIQUE NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields**:
- `id` - Primary key
- `fruit_name` - Standardized fruit name (singular form)
- `ai_identifier` - Name used by AI model for recognition
- `created_date` - When fruit was first added

**Example Data**:
```sql
INSERT INTO fruits (fruit_name, ai_identifier) VALUES 
('strawberry', 'strawberry'),
('blueberry', 'blueberry'),
('apple', 'apple');
```

### 2. Profiles Table
**Purpose**: Detailed fruit information (only for covered fruits)
```sql
CREATE TABLE profiles (
    fruit_id INTEGER PRIMARY KEY REFERENCES fruits(id),
    scientific_name VARCHAR(100),
    description TEXT,
    flavor_profile JSONB,
    jam_uses JSONB,
    season VARCHAR(50),
    storage_tips TEXT,
    nutrition JSONB,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields**:
- `fruit_id` - Foreign key to fruits table
- `scientific_name` - Scientific name (e.g., "Fragaria × ananassa")
- `description` - Detailed fruit description
- `flavor_profile` - JSON: {"sweet": 8, "tart": 6, "acidic": 4}
- `jam_uses` - JSON: ["jam", "preserves", "compote"]
- `season` - Peak season (e.g., "Summer")
- `storage_tips` - Storage and handling advice
- `nutrition` - JSON: {"calories": 32, "vitamin_c": "58mg"}

**Coverage Logic**: If a fruit has an entry in profiles table, it's "covered"

### 3. Recipes Table
**Purpose**: Jam recipes with essential data
```sql
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    ingredients JSONB NOT NULL,
    instructions JSONB NOT NULL,
    rating DECIMAL(3,2) NOT NULL,
    review_count INTEGER NOT NULL,
    source VARCHAR(100) NOT NULL,
    source_url TEXT NOT NULL,
    image_url TEXT NOT NULL,
    servings VARCHAR(50),
    prep_time VARCHAR(50),
    cook_time VARCHAR(50),
    total_time VARCHAR(50),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Essential Fields** (Required):
- `title` - Recipe name
- `ingredients` - JSON: [{"quantity": "2 cups", "unit": "cups", "ingredient": "strawberries"}]
- `instructions` - JSON: ["Step 1: Wash and hull strawberries", "Step 2: Combine with sugar"]
- `rating` - User rating (0.0-5.0)
- `review_count` - Number of reviews
- `source` - Site name ("Allrecipes", "Ball Canning", "Food.com")
- `source_url` - Original recipe URL
- `image_url` - Primary recipe image URL

**Nice-to-Have Fields** (Optional):
- `servings` - Number of servings or jars
- `prep_time` - Preparation time
- `cook_time` - Cooking time
- `total_time` - Total time

### 4. Recipe_Fruits Junction Table
**Purpose**: Many-to-many relationship between recipes and fruits
```sql
CREATE TABLE recipe_fruits (
    recipe_id INTEGER REFERENCES recipes(id),
    fruit_id INTEGER REFERENCES fruits(id),
    is_primary BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (recipe_id, fruit_id)
);
```

**Fields**:
- `recipe_id` - Foreign key to recipes table
- `fruit_id` - Foreign key to fruits table
- `is_primary` - Is this the main fruit in the recipe?

**Example Data**:
```sql
-- Strawberry jam recipe
INSERT INTO recipe_fruits VALUES (1, 1, TRUE);  -- strawberry (primary)
INSERT INTO recipe_fruits VALUES (1, 4, FALSE); -- lemon (supporting)

-- Mixed berry jam recipe
INSERT INTO recipe_fruits VALUES (2, 1, TRUE);  -- strawberry (primary)
INSERT INTO recipe_fruits VALUES (2, 2, TRUE);  -- blueberry (primary)
```

## Indexes for Performance
```sql
-- Recipe ranking queries
CREATE INDEX idx_recipes_rating ON recipes(rating DESC);
CREATE INDEX idx_recipes_review_count ON recipes(review_count DESC);

-- Fruit lookups
CREATE INDEX idx_fruits_ai_identifier ON fruits(ai_identifier);
CREATE INDEX idx_fruits_name ON fruits(fruit_name);

-- Recipe-fruit relationships
CREATE INDEX idx_recipe_fruits_recipe_id ON recipe_fruits(recipe_id);
CREATE INDEX idx_recipe_fruits_fruit_id ON recipe_fruits(fruit_id);
CREATE INDEX idx_recipe_fruits_primary ON recipe_fruits(is_primary) WHERE is_primary = TRUE;
```

## Data Population Strategy

### 1. Fruit Population
- Only add fruits that appear in recipes
- Extract fruit names from recipe ingredients
- Normalize to singular form (strawberries → strawberry)
- Create basic fruit entry first, add profile later if needed

### 2. Recipe Population
- Scrape recipes from target sites
- Extract fruits from ingredients list
- Determine primary fruits (in title = primary)
- Create recipe-fruit relationships
- Only save recipes with all essential fields

### 3. Profile Population
- Add detailed profiles for covered fruits
- Focus on fruits that are primary ingredients
- Use profiles table to track coverage status

## Query Examples

### Get Recipes by Fruit
```sql
SELECT r.*, f.fruit_name, rf.is_primary
FROM recipes r
JOIN recipe_fruits rf ON r.id = rf.recipe_id
JOIN fruits f ON rf.fruit_id = f.id
WHERE f.ai_identifier = 'strawberry'
ORDER BY r.rating DESC, r.review_count DESC
LIMIT 3;
```

### Get Fruit Coverage Status
```sql
SELECT f.fruit_name, 
       CASE WHEN p.fruit_id IS NOT NULL THEN 'covered' ELSE 'not_covered' END as status
FROM fruits f
LEFT JOIN profiles p ON f.id = p.fruit_id
WHERE f.ai_identifier = 'strawberry';
```

### Get Top Recipes for Mixed Fruits
```sql
SELECT r.*, 
       STRING_AGG(f.fruit_name, ', ') as fruits,
       COUNT(rf.fruit_id) as fruit_count
FROM recipes r
JOIN recipe_fruits rf ON r.id = rf.recipe_id
JOIN fruits f ON rf.fruit_id = f.id
WHERE f.ai_identifier IN ('strawberry', 'blueberry')
GROUP BY r.id
HAVING COUNT(rf.fruit_id) = 2  -- Both fruits present
ORDER BY r.rating DESC, r.review_count DESC
LIMIT 3;
```

## Railway Optimization
- **Connection pooling** - Use psycopg2 with connection pooling
- **Query optimization** - Indexes on frequently queried fields
- **JSONB usage** - Efficient storage and querying of structured data
- **Minimal data** - Only store essential fields to reduce storage costs

---
*This schema was designed on 2025-09-21-2120 based on essential data analysis and project requirements.*

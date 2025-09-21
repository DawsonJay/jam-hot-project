-- Database Creation Script for Jam Hot Project
-- PostgreSQL database schema for Railway deployment
-- Created: 2025-09-21-2120

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Fruits Table
-- All AI-recognizable fruits (basic info only)
CREATE TABLE fruits (
    id SERIAL PRIMARY KEY,
    fruit_name VARCHAR(100) UNIQUE NOT NULL,
    ai_identifier VARCHAR(100) UNIQUE NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Profiles Table
-- Detailed fruit information (only for covered fruits)
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

-- 3. Recipes Table
-- Jam recipes with essential data
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

-- 4. Recipe_Fruits Junction Table
-- Many-to-many relationship between recipes and fruits
CREATE TABLE recipe_fruits (
    recipe_id INTEGER REFERENCES recipes(id),
    fruit_id INTEGER REFERENCES fruits(id),
    is_primary BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (recipe_id, fruit_id)
);

-- Performance Indexes
-- Recipe ranking queries
CREATE INDEX idx_recipes_rating ON recipes(rating DESC);
CREATE INDEX idx_recipes_review_count ON recipes(review_count DESC);
CREATE INDEX idx_recipes_source ON recipes(source);

-- Fruit lookups
CREATE INDEX idx_fruits_ai_identifier ON fruits(ai_identifier);
CREATE INDEX idx_fruits_name ON fruits(fruit_name);

-- Recipe-fruit relationships
CREATE INDEX idx_recipe_fruits_recipe_id ON recipe_fruits(recipe_id);
CREATE INDEX idx_recipe_fruits_fruit_id ON recipe_fruits(fruit_id);
CREATE INDEX idx_recipe_fruits_primary ON recipe_fruits(is_primary) WHERE is_primary = TRUE;

-- Composite indexes for common queries
CREATE INDEX idx_recipes_rating_reviews ON recipes(rating DESC, review_count DESC);
CREATE INDEX idx_recipe_fruits_fruit_primary ON recipe_fruits(fruit_id, is_primary);

-- Sample data for testing
-- Insert some basic fruits
INSERT INTO fruits (fruit_name, ai_identifier) VALUES 
('strawberry', 'strawberry'),
('blueberry', 'blueberry'),
('apple', 'apple'),
('lemon', 'lemon'),
('orange', 'orange'),
('peach', 'peach'),
('blackberry', 'blackberry'),
('raspberry', 'raspberry'),
('cherry', 'cherry'),
('grape', 'grape');

-- Insert sample profile for strawberry
INSERT INTO profiles (fruit_id, scientific_name, description, flavor_profile, jam_uses, season, storage_tips, nutrition) VALUES 
(1, 'Fragaria × ananassa', 'Sweet, juicy berries perfect for jams and preserves', 
 '{"sweet": 8, "tart": 6, "acidic": 4, "floral": 3}',
 '["jam", "preserves", "compote", "syrup"]',
 'Summer',
 'Store in refrigerator for up to 5 days. Freeze for longer storage.',
 '{"calories": 32, "vitamin_c": "58mg", "fiber": "2g", "sugar": "4.9g"}');

-- Insert sample recipe
INSERT INTO recipes (title, ingredients, instructions, rating, review_count, source, source_url, image_url, servings, prep_time, cook_time) VALUES 
('Classic Strawberry Jam',
 '[{"quantity": "4", "unit": "cups", "ingredient": "strawberries"}, {"quantity": "3", "unit": "cups", "ingredient": "sugar"}, {"quantity": "1", "unit": "tbsp", "ingredient": "lemon juice"}]',
 '["Wash and hull strawberries", "Combine strawberries and sugar in large pot", "Bring to boil, add lemon juice", "Cook until thickened", "Ladle into sterilized jars"]',
 4.5,
 127,
 'Allrecipes',
 'https://www.allrecipes.com/recipe/classic-strawberry-jam',
 'https://images.media-allrecipes.com/images/classic-strawberry-jam.jpg',
 'Makes 4 half-pint jars',
 '20 minutes',
 '15 minutes');

-- Link recipe to fruits
INSERT INTO recipe_fruits (recipe_id, fruit_id, is_primary) VALUES 
(1, 1, TRUE),  -- strawberry (primary)
(1, 4, FALSE); -- lemon (supporting)

-- Create views for common queries
CREATE VIEW recipe_summary AS
SELECT 
    r.id,
    r.title,
    r.rating,
    r.review_count,
    r.source,
    r.image_url,
    STRING_AGG(f.fruit_name, ', ' ORDER BY rf.is_primary DESC) as fruits,
    COUNT(rf.fruit_id) as fruit_count
FROM recipes r
JOIN recipe_fruits rf ON r.id = rf.recipe_id
JOIN fruits f ON rf.fruit_id = f.id
GROUP BY r.id, r.title, r.rating, r.review_count, r.source, r.image_url;

-- Create view for fruit coverage status
CREATE VIEW fruit_coverage AS
SELECT 
    f.id,
    f.fruit_name,
    f.ai_identifier,
    CASE WHEN p.fruit_id IS NOT NULL THEN 'covered' ELSE 'not_covered' END as coverage_status,
    p.description,
    p.flavor_profile
FROM fruits f
LEFT JOIN profiles p ON f.id = p.fruit_id;

-- Grant permissions (adjust as needed for Railway)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO jam_hot_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO jam_hot_user;

COMMIT;

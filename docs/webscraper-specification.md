# Web Scraper Specification - Jam Hot Project

## Overview
The web scraper component is responsible for building a comprehensive recipe database from multiple sources using a modular framework approach. This demonstrates advanced web scraping skills, object-oriented design, and data engineering capabilities.

## Architecture

### Core Framework Pattern
- **Base Scraper Class**: Handles common functionality (HTTP, errors, rate limiting, validation)
- **Site-Specific Adapters**: Handle site-specific HTML parsing and data extraction
- **Recipe Aggregator**: Orchestrates multiple scrapers and combines data
- **Data Validator**: Ensures recipe quality and completeness

### Design Pattern
Uses the **Adapter Pattern** - a core scraper framework with site-specific adapters that handle the unique characteristics of each recipe source.

## Target Recipe Sources

### Primary Sources
1. **AllRecipes.com** - Variety and creativity
2. **Ball Canning (ballmasonjars.com)** - Tested, reliable recipes
3. **Food.com** - Additional variety

### Secondary Sources
4. **National Center for Home Food Preservation** - Government recipes
5. **Specialized jam blogs** - Unique combinations
6. **Extension services** - University jam recipes

## Technical Implementation

### Core Scraper Framework
```python
# Base scraper responsibilities:
- Selenium WebDriver management
- Rate limiting (0.3 seconds between requests)
- Error handling and retry logic
- Data validation and quality control
- Database integration
- Logging and progress tracking
- Headless browser optimization
```

### Site-Specific Adapters
```python
# Each adapter handles:
- Search logic for finding recipes by fruit
- HTML parsing for site-specific structure
- Data mapping to standard recipe format
- Site-specific quirks and edge cases
- Fruit extraction from ingredients list
- Primary fruit detection (in title = primary)
```

### Data Quality Strategy
- **Multi-source redundancy**: If one site fails, others still work
- **Quality comparison**: Compare recipes across sources
- **Deduplication**: Remove duplicate recipes
- **Source tracking**: Know where each recipe came from
- **Rating filters**: Only high-rated recipes (flexible based on site data)
- **Completeness validation**: Title, ingredients, instructions required
- **Fruit-only focus**: Only tag and profile actual fruits, ignore herbs/spices
- **Fruit extraction**: From ingredients only, not recipe titles
- **Name standardization**: Normalize to singular form (strawberry, not strawberries)

## Project Structure
```
scraper/                        # Development tools (local only)
├── core/
│   ├── base_scraper.py
│   ├── selenium_scraper.py
│   ├── rate_limiter.py
│   └── data_validator.py
├── adapters/
│   ├── allrecipes_adapter.py
│   ├── ball_canning_adapter.py
│   ├── food_com_adapter.py
│   └── jam_blog_adapter.py
├── recipe_aggregator.py
├── database_setup.py
└── data/
    ├── database_migrations/    # PostgreSQL schema migrations
    │   ├── 001_create_tables.sql
    │   └── 002_add_indexes.sql
    └── scraped_data/           # Raw scraped data before processing
```

## Data Schema

### PostgreSQL Database Schema
```sql
-- Fruits table (all AI-recognizable fruits, basic info only)
CREATE TABLE fruits (
    id SERIAL PRIMARY KEY,
    fruit_name VARCHAR(100) UNIQUE NOT NULL,
    ai_identifier VARCHAR(100) UNIQUE NOT NULL,
    created_date TIMESTAMP
);

-- Profiles table (detailed information, only for covered fruits)
CREATE TABLE profiles (
    fruit_id INTEGER PRIMARY KEY REFERENCES fruits(id),
    scientific_name VARCHAR(100),
    description TEXT,
    flavor_profile JSONB,
    jam_uses JSONB,
    season VARCHAR(50),
    storage_tips TEXT,
    nutrition JSONB,
    created_date TIMESTAMP
);

-- Recipes table
CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    ingredients JSONB,
    instructions JSONB,
    prep_time VARCHAR(50),
    cook_time VARCHAR(50),
    total_time VARCHAR(50),
    servings INTEGER,
    rating DECIMAL(3,2),
    views INTEGER,
    source VARCHAR(100),
    source_url TEXT,
    recipe_type VARCHAR(50),
    difficulty VARCHAR(50),
    created_date TIMESTAMP,
    scraped_date TIMESTAMP
);

-- Many-to-many relationship (all fruits in recipe)
CREATE TABLE recipe_fruits (
    recipe_id INTEGER REFERENCES recipes(id),
    fruit_id INTEGER REFERENCES fruits(id),
    is_primary BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (recipe_id, fruit_id)
);
```

## Success Criteria
- **Recipe database**: 200+ jam recipes from multiple sources
- **Fruit coverage**: Detailed profiles for 50+ primary jam fruits
- **Scraper framework**: Working adapters for 3+ recipe sites
- **Data quality**: High-quality, validated recipes
- **Source diversity**: Recipes from multiple trusted sources
- **Smart tagging**: All fruits in recipes tagged (primary and secondary)
- **Coverage tracking**: Clear visibility of which fruits need profiles
- **Focused scope**: Fruits only (herbs, spices, and other ingredients not profiled)
- **Data reliability**: Regular, clean scraped data
- **Independence**: Populated database works without live scraping

## Portfolio Value
- **Framework design**: Object-oriented design with adapter pattern
- **Web scraping expertise**: Multiple sites, error handling, rate limiting
- **Data engineering**: Data processing, validation, aggregation
- **System architecture**: Separation of concerns, modularity, scalability
- **Industry patterns**: Real-world approach used by companies

## Development Timeline
- **Week 1, Days 1-2**: Analyze target sites and fine-tune database schema
- **Week 1, Day 3**: Create database and core scraper framework
- **Week 1, Days 4-5**: Perfect one site, then add others one by one

## Technical Dependencies
- **Python packages**: selenium, webdriver-manager, psycopg2, sqlalchemy, logging
- **Browser**: Chrome/Chromium (headless mode)
- **Database**: PostgreSQL for recipe storage
- **Rate limiting**: 0.3 seconds between requests
- **Error handling**: Fail completely if any site breaks
- **Deployment**: Local development only - not deployed
- **Development approach**: Core framework → one site perfect → scale to others

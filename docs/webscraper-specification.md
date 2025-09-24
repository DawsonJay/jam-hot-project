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

### Phase 1 Success (Immediate Goal)
- **Complete pipeline**: One strawberry jam recipe from AllRecipes to database
- **Data completeness**: All required fields (title, ingredients, instructions, rating, source URL)
- **Fruit extraction**: Correctly identified "strawberry" as primary fruit
- **Database integration**: Recipe stored in recipes table, fruit relationship in recipe_fruits table
- **Data quality**: Properly formatted, validated data
- **End-to-end validation**: From web scraping to database storage works

### Final Success Criteria (End Goal)
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

## Development Approach: Test-Driven, End-to-End

### Phase 1: Complete End-to-End for One Recipe (Priority)
**Goal**: Get ONE strawberry jam recipe from ONE site with complete processing

**Complete Pipeline**:
1. **Base adapter interface** - Define the framework
2. **AllRecipes adapter** - Site-specific logic for AllRecipes
3. **Core scraper** - Orchestrates the entire process
4. **Data processing pipeline** - Extract, validate, clean, standardize
5. **Fruit extraction** - Identify fruits in ingredients
6. **Database integration** - Store in proper format with relationships
7. **End-to-end test** - Verify complete pipeline works

**Validation Criteria**:
- Recipe data: Title, ingredients, instructions, rating, source URL
- Fruit extraction: Correctly identified "strawberry" as primary fruit
- Database storage: Recipe in recipes table, fruit relationship in recipe_fruits table
- Data quality: All required fields present, properly formatted
- Complete flow: From web scraping to database storage

### Phase 2: Expand Core Scraper Robustness
**Goal**: Make the core scraper production-ready

- Add error handling (site down, network issues)
- Add rate limiting (0.3 seconds between requests)
- Add data validation (complete recipe check)
- Add logging (progress tracking, error reporting)
- Add retry logic (temporary failures)

### Phase 3: Add More Sites
**Goal**: Get recipes from multiple sources

- Add Ball Canning adapter (same interface)
- Add Food.com adapter (same interface)
- Test multi-site scraping
- Validate different data formats

### Phase 4: Add More Fruits
**Goal**: Expand beyond strawberry

- Test with blueberry, apple, other fruits
- Validate fruit extraction works across different recipes
- Test multiple fruits per recipe

### Phase 5: Scale and Optimize
**Goal**: Production-ready scraper

- Add duplicate detection
- Add batch processing
- Add resume capability
- Add performance monitoring

## Development Timeline
- **Week 1, Days 1-2**: Complete end-to-end pipeline for one recipe (Phase 1)
- **Week 1, Day 3**: Expand core scraper robustness (Phase 2)
- **Week 1, Days 4-5**: Add more sites and fruits (Phases 3-4)

## Technical Dependencies
- **Python packages**: selenium, webdriver-manager, psycopg2, sqlalchemy, logging, beautifulsoup4, requests
- **Browser**: Chrome/Chromium (headless mode)
- **Database**: PostgreSQL for recipe storage (already set up)
- **Rate limiting**: 0.3 seconds between requests
- **Error handling**: Graceful degradation (one site fails, others continue)
- **Deployment**: Local development only - not deployed
- **Development approach**: Test-driven, end-to-end validation for one recipe first

## Key Design Principles
- **Start simple**: One recipe, one site, complete pipeline
- **Test-driven**: Validate each component works before adding complexity
- **End-to-end validation**: From web scraping to database storage
- **Incremental expansion**: Add sites and features only after core works
- **Real data**: Work with actual recipe data, not mock data
- **Complete processing**: Extract, validate, clean, standardize, store

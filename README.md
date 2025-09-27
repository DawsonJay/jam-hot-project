# Jam Hot - AI-Powered Fruit Classification for Jam Making

## Project Overview

**Jam Hot** is an AI-powered web application that identifies fruits from photos and provides jam-making recipes and flavor profiles. The project demonstrates transfer learning, web scraping, and full-stack development skills for portfolio purposes.

## Core Functionality

Upload a photo of fruit → Get fruit identification + jam recipes + flavor profiles

**Focus**: Fruits only (herbs, spices, and other ingredients are not identified or profiled)

## Current Status

### ✅ Completed Phases
- **Web Scraping Framework**: 4 site adapters (AllRecipes, Serious Eats, Food Network, BBC Good Food)
- **Database**: 116 jam recipes + 29 fruit profiles in PostgreSQL
- **API Backend**: FastAPI deployed on Railway with authentication
- **Security**: Environment variables, API key authentication

### 🔄 Current Phase: AI Model Development
- **Target**: Transfer learning for fruit classification
- **Dataset**: Fruit-360 (60,000+ images, 120+ fruit types)
- **Goal**: 90%+ accuracy, <2s inference, 50+ fruit types
- **Timeline**: 4-5 days estimated

## Deployment

**Live Application**: https://jam-hot-project-production.up.railway.app

**API Endpoints**:
- `GET /` - API status and available endpoints
- `GET /health` - Health check
- `GET /recipes/titles` - Get all recipe titles
- `GET /recipes` - Get all recipes with full data
- `GET /recipes/count` - Get recipe statistics
- `GET /fruits` - Get all fruit profiles
- `POST /admin/restore-database?api_key=<API_KEY>` - Manually restore database from dump (requires API key)

## Environment Variables

**For Railway Deployment:**
- `DATABASE_URL` - Automatically provided by Railway
- `ADMIN_API_KEY` - API key for admin endpoints (default: `jam-hot-admin-2025`)

**For Local Development:**
```bash
# Copy the example file and update with your values
cp .env.example .env
# Edit .env with your database credentials
```

## Quick Start

**2. Start the database:**
```bash
./scripts/database/start-db.sh
```

**3. Connect to database:**
```bash
psql -h localhost -p 5433 -U postgres -d jam_hot
```

**4. Stop the database:**
```bash
./scripts/database/stop-db.sh
```

## Project Documentation

**⚠️ IMPORTANT: The specifications in the `docs/` folder are the source of truth for this project's design and implementation.**

For detailed technical specifications, see the `docs/` folder:

- **[Project Definition](docs/project-definition.md)** - Master overview and project goals
- **[Backend Specification](docs/backend-specification.md)** - FastAPI + PostgreSQL + AI integration
- **[Web Scraper Specification](docs/webscraper-specification.md)** - Selenium framework with site adapters
- **[AI Model Specification](docs/ai-model-specification.md)** - Transfer learning with fruits-only focus
- **[Frontend Specification](docs/frontend-specification.md)** - React app with Material-UI
- **[Railway Deployment](docs/railway-deployment-specification.md)** - PostgreSQL deployment strategy
- **[Fruit Profile Creation](docs/fruit-profile-creation-specification.md)** - Framework for creating factual fruit profiles

**For AI Assistants**: See [AI-CONTEXT.md](AI-CONTEXT.md) for orientation instructions.

**For Database Setup**: See [scripts/database/README.md](scripts/database/README.md) for detailed database management instructions.

**Note**: This README provides a high-level overview. All technical details, design decisions, and implementation requirements are defined in the specification files above.

## Technical Architecture

### Component 1: Web Scraper Framework
- **Purpose**: Build recipe database from multiple sources using Selenium-based framework
- **Architecture**: Core scraper + site-specific adapters (Adapter Pattern)
- **Targets**: AllRecipes.com, Ball Canning, Food.com, specialized jam blogs
- **Technology**: Selenium for dynamic content handling
- **Output**: PostgreSQL database with structured recipes and fruit relationships
- **Skills**: Web scraping, framework design, data processing, database design

### Component 2: AI Fruit Classification
- **Purpose**: Identify fruits from photos using transfer learning
- **Approach**: Fine-tune pre-trained model (ResNet50/EfficientNet) on fruit data
- **Data**: Fruit-360 dataset (60,000+ images, 120+ fruit types) + custom fruit photos
- **Scope**: Fruits only (herbs, spices, other ingredients not identified)
- **Skills**: Transfer learning, computer vision, model training

### Component 3: Web Application
- **Purpose**: Connect AI classification with recipe database
- **Frontend**: React app with Material-UI and camera upload
- **Backend**: Python FastAPI with model inference
- **Database**: PostgreSQL with smart coverage tracking
- **Skills**: Full-stack development, API integration, user experience

## Project Goals

### Primary Goals
- **Portfolio project**: Demonstrate AI/ML and full-stack skills for Canadian immigration
- **Real AI skills**: Transfer learning, not just API calls
- **Complete solution**: End-to-end application
- **Fast development**: 2-3 weeks timeline
- **Independence**: Works perfectly without maintenance for a year+

### Technical Goals
- **Transfer learning**: Fine-tune pre-trained model on fruit data
- **Web scraping framework**: Modular Selenium scraper for multiple recipe sources
- **Data engineering**: Clean, structured PostgreSQL database from multiple sources
- **Production deployment**: Working web application on Railway
- **Reliability**: Stable, user-friendly, responsive design

## Data Sources

### Fruit Images
- **Fruit-360 dataset**: 60,000+ fruit images, 120+ fruit types
- **Custom photos**: Personal fruit photos for testing
- **Data augmentation**: Rotate, flip, adjust brightness
- **Scope**: Fruits only (herbs, spices, other ingredients not identified)

### Jam Recipes
- **Multiple sources**: AllRecipes.com, Ball Canning, Food.com, specialized jam blogs
- **Selenium framework**: Modular system with site-specific adapters
- **Recipe data**: Title, ingredients, instructions, ratings, prep time, source
- **Fruit extraction**: Extract fruits from ingredients, identify primary fruits
- **Quality control**: Filter by ratings, validate completeness, deduplicate across sources
- **Database**: PostgreSQL with smart coverage tracking

### Database Design
- **Fruits table**: All AI-recognizable fruits (basic info only)
- **Profiles table**: Detailed fruit information (only for covered fruits)
- **Recipes table**: Jam recipes with ingredients, instructions, ratings
- **Recipe-Fruits junction**: Many-to-many with primary fruit tracking
- **Size**: Estimated 500KB-1MB (well within Railway free tier)

## Development Timeline

### Week 1: Site Analysis + Database Setup + Core Scraper
- **Days 1-2**: Analyze target sites and fine-tune database schema
- **Day 3**: Set up PostgreSQL database and create tables
- **Days 4-5**: Build core Selenium scraper framework and first adapter
- **Parallel**: Collect and preprocess fruit image data

### Week 2: Scraper Scaling + AI Model Training
- **Days 1-2**: Scale scraper to multiple sites and populate database
- **Days 3-4**: Set up transfer learning pipeline and train model
- **Day 5**: Validate model performance and optimize

### Week 3: Backend + Frontend + Deployment
- **Days 1-2**: Build FastAPI backend with PostgreSQL integration
- **Days 3-4**: Build React frontend with Material-UI
- **Day 5**: Deploy to Railway and test end-to-end functionality

## Technical Stack

### Backend
- **Python**: FastAPI for API development
- **TensorFlow/PyTorch**: Model training and inference
- **PostgreSQL**: Recipe database storage
- **Selenium**: Web scraping for dynamic content
- **psycopg2**: PostgreSQL database adapter
- **Object-oriented design**: Core scraper + site adapters

### Frontend
- **React**: User interface
- **Material-UI**: UI component library
- **Camera API**: Photo capture functionality
- **Axios**: HTTP client for API communication

### Deployment
- **Railway**: Backend hosting with PostgreSQL service
- **Database strategy**: Local development → dump → restore
- **Model files**: Pre-trained models for inference
- **Database size**: 500KB-1MB (well within Railway free tier)

## Skills Demonstrated

### AI/ML Skills
- **Transfer learning**: Fine-tuning pre-trained models
- **Computer vision**: Image classification
- **Data engineering**: Collecting and processing datasets
- **Model optimization**: Making models production-ready

### Full-Stack Development
- **Backend API**: Python FastAPI with model inference
- **Frontend**: React with Material-UI and camera functionality
- **Database design**: PostgreSQL with smart coverage tracking
- **Web scraping framework**: Modular Selenium scraper for multiple sources
- **Object-oriented design**: Core scraper + site adapters pattern
- **Deployment**: Railway hosting with database management

### Problem-Solving
- **Real problem**: You actually want to make jam
- **End-to-end solution**: Complete application
- **User experience**: Making AI accessible and useful
- **Practical value**: Actually useful for jam making

## Project Structure

```
jam-hot/
├── README.md
├── AI-CONTEXT.md
├── docs/
│   ├── project-definition.md
│   ├── backend-specification.md
│   ├── webscraper-specification.md
│   ├── ai-model-specification.md
│   ├── frontend-specification.md
│   └── railway-deployment-specification.md
├── scraper/
│   ├── core/
│   │   ├── base_scraper.py
│   │   ├── rate_limiter.py
│   │   └── data_validator.py
│   ├── adapters/
│   │   ├── allrecipes_adapter.py
│   │   ├── ball_canning_adapter.py
│   │   ├── food_com_adapter.py
│   │   └── jam_blog_adapter.py
│   ├── recipe_aggregator.py
│   └── database_setup.py
├── ai_model/
│   ├── data_collection.py
│   ├── model_training.py
│   └── model_inference.py
├── web_app/
│   ├── backend/
│   │   ├── main.py
│   │   ├── database/
│   │   └── models/
│   └── frontend/
│       ├── src/
│       └── public/
└── data/
    ├── jam_hot_dump.sql
    ├── fruit_images/
    └── trained_model/
```

## Success Criteria

### Technical Success
- **Model accuracy**: 90%+ fruit identification accuracy
- **Recipe database**: 200+ jam recipes from multiple sources
- **Scraper framework**: Working adapters for 3+ recipe sites
- **Web app**: Functional photo upload and results display
- **Deployment**: Working production application on Railway

### Portfolio Success
- **Real AI skills**: Transfer learning, not just API calls
- **Complete solution**: End-to-end application
- **Practical value**: Actually useful for users
- **Technical depth**: Multiple skills demonstrated
- **Framework design**: Modular, scalable web scraping system
- **Industry patterns**: Object-oriented design, adapter pattern

### Reliability Success
- **Independence**: Works perfectly without maintenance for a year+
- **Stability**: Never crashes or glitches when users try to use it
- **User experience**: Fun, easy to use, responsive design
- **Data quality**: Regular, clean scraped data
- **Error handling**: Graceful degradation with user-friendly messages

## Future Enhancements

### Phase 2 (Future)
- **Multi-fruit detection**: Identify multiple fruits in one photo
- **Recipe recommendations**: Suggest recipes based on available fruits
- **User accounts**: Save favorite recipes and fruits
- **Mobile app**: Native mobile application

### Phase 3 (Future)
- **Community features**: User-submitted recipes and photos
- **Advanced AI**: Custom model training for specific regions
- **Integration**: Connect with grocery stores for fruit availability

## Key Design Decisions

- **Fruits-only focus**: Herbs, spices, and other ingredients not identified
- **PostgreSQL database**: Single database with smart coverage tracking
- **Selenium scraping**: Dynamic content handling for future-proofing
- **Local development**: Database created locally, deployed via dump/restore
- **Railway deployment**: Backend hosting with PostgreSQL service
- **Methodical approach**: Site analysis → database setup → core scraper → scaling

## Notes

- **Focus on core functionality**: Single fruit identification first
- **Quality over quantity**: Better to have fewer, high-quality recipes
- **Test thoroughly**: Verify model accuracy with real fruit photos
- **Keep it simple**: Don't overcomplicate the first version
- **Reliability first**: Clean, stable code that works independently

---

**Project Status**: Specifications Complete  
**Target Completion**: 2-3 weeks  
**Primary Goal**: Portfolio project demonstrating AI/ML and full-stack skills for Canadian immigration

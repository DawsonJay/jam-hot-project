# Project Definition - Jam Hot

## Project Overview

**Jam Hot** is an AI-powered web application that identifies fruits from photos and provides jam-making recipes and information. The project demonstrates transfer learning, web scraping, and full-stack development skills as part of a portfolio strategy for Canadian immigration.

## Core Value Proposition

**For Users**: Upload a photo of fruit → Get fruit identification + jam recipes + flavor profiles

**For Portfolio**: Demonstrates real AI/ML skills, full-stack development, and practical problem-solving

## Project Goals

### Primary Goals
- **Portfolio project**: Demonstrate AI/ML and full-stack skills for Canadian immigration
- **Real AI skills**: Transfer learning, not just API calls
- **Complete solution**: End-to-end application
- **Fast development**: 2-3 weeks timeline
- **Personal utility**: Actually useful for jam making

### Technical Goals
- **Transfer learning**: Fine-tune pre-trained model on fruit data
- **Web scraping framework**: Modular scraper for multiple recipe sources
- **Data engineering**: Clean, structured recipe database from multiple sources
- **Production deployment**: Working web application

## Project Architecture

### Three-Component System

#### Component 1: Web Scraper Framework
- **Purpose**: Build recipe database from multiple sources
- **Architecture**: Core scraper + site-specific adapters
- **Targets**: AllRecipes.com, Ball Canning, Food.com, specialized jam blogs
- **Output**: Unified, structured recipe database
- **Skills**: Web scraping, framework design, data processing, database design

#### Component 2: AI Fruit Classification
- **Purpose**: Identify fruits from photos using transfer learning
- **Approach**: Fine-tune pre-trained model (ResNet50/EfficientNet) on fruit data
- **Data**: Fruit-360 dataset + custom fruit photos
- **Skills**: Transfer learning, computer vision, model training

#### Component 3: Web Application
- **Purpose**: Connect AI classification with recipe database
- **Frontend**: React app with camera upload
- **Backend**: Python API with model inference
- **Database**: PostgreSQL with scraped recipes
- **Skills**: Full-stack development, API integration, user experience

## Data Flow

```
User uploads fruit photo(s)
    ↓
Frontend sends to Backend API
    ↓
Backend runs AI Model + queries databases
    ↓
Backend returns: Fruit ID + Recipes + Flavor info
    ↓
Frontend displays results to user
```

## Architecture

### Frontend (React)
- **Photo upload**: Single or multiple fruit photos
- **Results display**: Fruit identification, recipes, flavor profiles
- **User interface**: Clean, intuitive design

### Backend API (FastAPI)
- **AI Model**: Fruit classification and flavor analysis
- **Recipe Database**: Jam recipes with ingredients and instructions
- **Fruit Info Database**: Fruit descriptions and flavor profiles
- **API endpoints**: Handle photo upload and data queries

## Technical Stack

### Backend
- **Python**: FastAPI for API development
- **TensorFlow/PyTorch**: Model training and inference
- **PostgreSQL**: Relational database with proper schema
- **BeautifulSoup**: Web scraping
- **Requests**: HTTP client for scraping

### Frontend
- **React**: User interface
- **Material-UI**: UI components
- **Camera API**: Photo capture functionality

### Data Sources
- **Fruit Images**: Fruit-360 dataset (60,000+ images, 120+ fruit types)
- **Jam Recipes**: Selenium web scraping from multiple sources → PostgreSQL
- **Fruit Information**: Curated fruit descriptions and flavor profiles → PostgreSQL
- **Custom Data**: Personal fruit photos for testing
- **Database Design**: Single PostgreSQL database with smart coverage tracking
- **Scope**: Fruits only (no herbs, spices, or other ingredients)
- **Fruit Population**: Only from recipes (if not in recipe, we don't need it)
- **Name Standardization**: Normalize to singular form (strawberry)
- **Data Strategy**: Local development → Database dump → Railway restore
- **Database Size**: Estimated 500KB-1MB (well within Railway free tier)
- **Update Strategy**: Manual dump/restore for rare database changes

## Success Criteria

### Technical Success
- **Model accuracy**: 90%+ fruit identification accuracy
- **Recipe database**: 200+ jam recipes from multiple sources
- **Scraper framework**: Working adapters for 3+ recipe sites
- **Web app**: Functional photo upload and results display
- **Deployment**: Working production application

### Portfolio Success
- **Real AI skills**: Transfer learning, not just API calls
- **Complete solution**: End-to-end application
- **Practical value**: Actually useful for users
- **Technical depth**: Multiple skills demonstrated
- **Framework design**: Modular, scalable web scraping system

### Reliability Success
- **Independence**: Works perfectly without maintenance for a year+
- **Stability**: Never crashes or glitches when users try to use it
- **User experience**: Fun, easy to use, responsive design
- **Data quality**: Regular, clean scraped data
- **Error handling**: Graceful degradation with user-friendly messages

## Development Timeline

### Week 1: Core Scraper Framework + Data Collection
- **Days 1-2**: Analyze target sites and fine-tune database schema
- **Day 3**: Create database and core scraper framework
- **Days 4-5**: Perfect one site, then add others one by one
- **Parallel**: Collect and preprocess fruit image data

### Week 2: AI Model Training
- **Days 1-2**: Set up transfer learning pipeline
- **Days 3-4**: Train model on fruit data
- **Day 5**: Validate and optimize model performance

### Week 3: Web Application
- **Days 1-2**: Build backend API with model inference
- **Days 3-4**: Build React frontend with photo upload
- **Day 5**: Deploy populated databases and trained model to Railway

## Project Structure

```
jam-hot/
├── README.md
├── AI-CONTEXT.md
├── docs/
│   ├── project-definition.md
│   ├── webscraper-specification.md
│   ├── ai-model-specification.md
│   ├── frontend-specification.md
│   ├── backend-specification.md
│   └── railway-deployment-specification.md
├── scraper/                        # Development tools (local only)
│   ├── core/
│   │   ├── base_scraper.py
│   │   ├── selenium_scraper.py
│   │   ├── rate_limiter.py
│   │   └── data_validator.py
│   ├── adapters/
│   │   ├── allrecipes_adapter.py
│   │   ├── ball_canning_adapter.py
│   │   ├── food_com_adapter.py
│   │   └── jam_blog_adapter.py
│   ├── recipe_aggregator.py
│   └── database_setup.py
├── data_collection/                # Development tools (local only)
│   ├── fruit_data_downloader.py
│   └── model_training.py
├── deployable/                     # Production deployment
│   ├── backend/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── database/
│   │   └── api/
│   ├── frontend/
│   │   ├── src/
│   │   └── public/
│   └── data/
│       ├── database_migrations/    # PostgreSQL schema migrations
│       └── trained_model/
```

## Skills Demonstrated

### AI/ML Skills
- **Transfer learning**: Fine-tuning pre-trained models
- **Computer vision**: Image classification
- **Data engineering**: Collecting and processing datasets
- **Model optimization**: Making models production-ready

### Full-Stack Development
- **Backend API**: Python with model inference
- **Frontend**: React with camera functionality
- **Database design**: Structured data storage
- **Web scraping framework**: Modular scraper for multiple sources
- **Object-oriented design**: Core scraper + site adapters pattern

### Problem-Solving
- **Real problem**: You actually want to make jam
- **End-to-end solution**: Complete application
- **User experience**: Making AI accessible and useful
- **Practical value**: Actually useful for jam making

## Portfolio Context

### Immigration Goals
- **Target**: Canadian Express Entry by January 2026
- **Strategy**: Demonstrate AI/ML skills progression
- **Positioning**: "Self-Directed Achiever" building toward AI/robotics

### Growth Story
- **Current**: Web development skills
- **Demonstrating**: AI/ML capabilities
- **Future**: Robotics and advanced AI applications

### Employer Appeal
- **Technical depth**: Multiple AI and development skills
- **Complete solution**: End-to-end application
- **Real-world application**: Solves actual problems
- **Modern approach**: Transfer learning, web scraping, full-stack development

## Risk Mitigation

### Technical Risks
- **Data quality**: Multiple sources provide redundancy
- **Model accuracy**: Transfer learning proven approach
- **Development time**: Modular architecture enables parallel work
- **Deployment**: Lightweight hosting requirements

### Portfolio Risks
- **Scope creep**: Clear success criteria and timeline
- **Technical complexity**: Transfer learning vs custom training
- **Time management**: 2-3 week timeline with clear milestones

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

## Success Metrics

### Technical Metrics
- Model accuracy percentage
- Recipe database size
- Scraper success rate
- Web app performance
- Deployment success

### Portfolio Metrics
- Skills demonstrated
- Code quality and architecture
- Documentation completeness
- Real-world utility
- Employer appeal

---

**Project Status**: Planning Complete, Ready for Implementation  
**Target Completion**: 2-3 weeks  
**Primary Goal**: Portfolio project demonstrating AI/ML and full-stack skills

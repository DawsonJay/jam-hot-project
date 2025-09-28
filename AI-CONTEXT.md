# AI Context - Jam Hot Project

## For New AI Assistants

When you first start working on this project, please follow these steps in order:

### 1. Read This Project's README
- **File**: `README.md` (in this directory)
- **Purpose**: Understand the Jam Hot project overview, technical architecture, and goals
- **Key Points**: AI-powered fruit classification for jam making, 3 main components, 2-3 week timeline

### 2. Read and Apply Behaviors File
- **File**: `/home/james/Documents/portfolio-profile/behaviors.md`
- **Purpose**: Apply consistent behaviors and approaches throughout the session
- **Critical**: This file defines how to work with the portfolio-profile project system

### 3. Read Portfolio-Profile README
- **File**: `/home/james/Documents/portfolio-profile/README.md`
- **Purpose**: Understand the broader portfolio project context and structure
- **Key Points**: Canadian immigration goals, portfolio strategy, file organization

### 4. Read Chat Records for Context
- **Directory**: `/home/james/Documents/portfolio-profile/records/jam-hot/`
- **Purpose**: Understand previous work, decisions made, and current project state
- **Files to read** (in chronological order):
  - `chat-record-2025-09-21-1857.md`
  - `chat-record-2025-09-21-1904.md`
  - (any additional records created after this file)

### 5. Read Technical Specifications
- **Directory**: `docs/` (in this project)
- **Purpose**: Understand detailed technical implementation and design decisions
- **Files to read** (in order of importance):
  - `project-definition.md` - Master overview and project goals
  - `backend-specification.md` - FastAPI + PostgreSQL + AI integration
  - `webscraper-specification.md` - Selenium framework with site adapters
  - `ai-model-specification.md` - Transfer learning with fruits-only focus
  - `frontend-specification.md` - React app with Material-UI
  - `railway-deployment-specification.md` - PostgreSQL deployment strategy
  - `fruit-profile-creation-specification.md` - Framework for creating factual fruit profiles

### 6. Read Key Definitions (if needed)
- **Chat Context**: `/home/james/Documents/portfolio-profile/definitions/chat-context-definition.md`
- **Chat Records**: `/home/james/Documents/portfolio-profile/definitions/chat-record-definition.md`
- **Purpose**: Understand the capture system and documentation approach

## Project Status
- **Current Phase**: AI Model Development
- **Last Updated**: 2025-09-27-1640
- **Completed Phases**: 
  - ✅ Web Scraping Framework (4 site adapters, 116 recipes, 29 fruit profiles)
  - ✅ Database & API Deployment (PostgreSQL + FastAPI on Railway)
  - ✅ Security Implementation (Environment variables, API authentication)
- **Next Steps**: AI Model Development - Transfer learning for fruit classification

## Key Behaviors to Remember
- Always use GMT/UTC timezone for timestamps (format: YYYY-MM-DD-HHMM)
- Discussion before coding - achieve full understanding before implementing
- Portfolio focus - consider what would be good for the portfolio
- Follow portfolio-profile project structure when creating files
- Ask about capture system after important moments
- Always include chat context when creating records
- **CRITICAL: NEVER commit or push to git without explicit user permission**

## CRITICAL: Fruit Profile Creation Rules
**⚠️ MANDATORY: When creating or updating fruit profiles, you MUST follow the [Fruit Profile Creation Specification](docs/fruit-profile-creation-specification.md) exactly.**

### Strict Requirements:
1. **ALL nutritional data** must come from USDA FoodData Central
2. **ALL pectin and acidity data** must be from scientific literature
3. **ALL images** must be from Unsplash with proper licensing
4. **NO estimated or guessed values** - everything must be scientifically verified
5. **ALL descriptions** must be factual, not marketing copy
6. **ALL sources** must be documented and verifiable

### Quality Assurance:
- Cross-reference all data with multiple sources
- Verify scientific names with botanical databases
- Check image URLs are accessible
- Ensure all values are within reasonable ranges
- Complete the quality assurance checklist before finalizing

### Failure to follow these rules will result in inaccurate data and compromise the project's scientific integrity.

## Portfolio Context
This project is part of a larger portfolio strategy for Canadian immigration (Express Entry by Jan 2026). The Jam Hot project demonstrates AI/ML skills, full-stack development, and practical problem-solving - all valuable for the portfolio narrative.

## Current Development Plan
- **Phase**: AI Model Development (4-5 days estimated)
- **Hardware**: AMD Ryzen 5 7430U, 30GB RAM, CPU-based training
- **Target**: 90%+ fruit identification accuracy, <2s inference, 50+ fruit types
- **Approach**: Transfer learning with Fruit-360 dataset (60,000+ images)
- **Integration**: FastAPI backend with existing PostgreSQL database

---
*This file was created on 2025-09-21-1916 and last updated on 2025-09-27-1640 to help new AI assistants quickly understand the project context and get up to speed.*

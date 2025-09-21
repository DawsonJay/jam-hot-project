# Frontend Specification - Jam Hot Project

## Overview
The frontend is a React web application that connects the AI fruit classification with the recipe database. Users can upload fruit photos and receive identification results along with relevant jam recipes and flavor profiles. The app focuses on fruits only - herbs, spices, and other ingredients are not identified or profiled.

## Core Functionality
**User Flow**: Upload fruit photo → Get fruit identification + jam recipes + flavor profiles

## Technical Stack

### Frontend Framework
- **React**: Modern JavaScript framework
- **Material-UI**: UI component library for consistent design
- **Camera API**: Photo capture functionality
- **Axios**: HTTP client for API communication

### Backend Integration
- **Python FastAPI**: Backend API with model inference
- **PostgreSQL**: Recipe database storage
- **Model inference**: Real-time fruit classification

## User Interface Design

### Main Interface
- **Photo upload area**: Drag-and-drop or camera capture
- **Results display**: Fruit identification with confidence scores
- **Recipe cards**: Jam recipes with ratings and prep time
- **Flavor profile**: Visual representation of fruit characteristics

### Key Components
1. **PhotoUpload**: Camera capture and file upload
2. **FruitResults**: Identification results and confidence
3. **RecipeList**: Jam recipes with filtering and sorting
4. **FlavorProfile**: Visual flavor characteristics
5. **Navigation**: Simple, intuitive navigation

### Responsive Design
- **Mobile-first**: Optimized for mobile devices
- **Desktop**: Enhanced experience for larger screens
- **Touch-friendly**: Large buttons and touch targets
- **Fast loading**: Optimized images and lazy loading

## Technical Implementation

### Component Architecture
```javascript
// Main components:
- App.js (main application)
- PhotoUpload.js (camera/file upload)
- FruitResults.js (AI results display)
- RecipeList.js (recipe cards)
- FlavorProfile.js (flavor visualization)
- Navigation.js (site navigation)
```

### State Management
- **React Hooks**: useState, useEffect for local state
- **Context API**: Global state for user data
- **Local Storage**: Persist user preferences

### API Integration
```javascript
// Backend API endpoints:
- POST /api/classify (upload image(s), get fruit IDs + info)
- GET /api/recipes?fruits=strawberry,blueberry (get recipes for fruits)
- GET /api/fruit-info?fruits=strawberry,blueberry (get flavor profiles)
- GET /api/health (health check)
```

## User Experience

### Photo Upload Experience
- **Multiple options**: Camera capture, file upload, drag-and-drop
- **Image preview**: Show selected image before processing
- **Loading states**: Clear feedback during AI processing
- **Error handling**: Graceful error messages

### Results Display
- **Fruit identification**: Clear results with confidence scores
- **Status handling**: Different UI for recognized vs unrecognized fruits
- **Recipe recommendations**: Only show for fruits with available data
- **Flavor insights**: Educational information for recognized fruits
- **Graceful degradation**: Handle missing data elegantly
- **Scope clarity**: Clear messaging that only fruits are identified
- **Action buttons**: Save favorites, share results

### Performance Optimization
- **Image compression**: Reduce upload size
- **Lazy loading**: Load recipes as needed
- **No caching**: Process every image fresh for accuracy
- **Progressive loading**: Show results as available
- **Loading states**: Simple spinners for user feedback
- **Error boundaries**: Graceful error handling

## Project Structure
```
web_app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PhotoUpload.js
│   │   │   ├── FruitResults.js
│   │   │   ├── RecipeList.js
│   │   │   └── FlavorProfile.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   └── App.css
│   │   └── App.js
│   └── public/
│       ├── index.html
│       └── manifest.json
└── backend/
    ├── main.py
    └── models/
        └── fruit_classifier.py
```

## Integration Points

### AI Model Integration
- **Image preprocessing**: Resize, normalize for model
- **API communication**: Send image to backend
- **Result processing**: Handle classification results
- **Error handling**: Manage model failures gracefully

### Backend Integration
- **Photo upload**: Send multiple photos to backend API
- **Results processing**: Handle different fruit recognition statuses
- **Status handling**: 
  - Recognized with data: Show full results (has profile + has recipes)
  - Recognized no info: Show recognition with "no detailed profile" message
  - Recognized no recipes: Show fruit profile but "no jam recipes yet"
  - Unrecognized: Show "unable to identify" message
- **Error handling**: Manage API failures gracefully
- **Loading states**: Show progress during AI processing
- **Confidence display**: Show confidence scores for transparency

## Success Criteria
- **User experience**: Intuitive, fast, responsive, fun and easy to use
- **Photo upload**: Works on mobile and desktop
- **AI integration**: Reliable fruit identification
- **Recipe display**: Clear, useful recipe information
- **Performance**: Fast loading and smooth interactions
- **Mobile responsive**: Essential for portfolio showcase
- **Error handling**: User-friendly error messages
- **Independence**: Works perfectly without maintenance

## Portfolio Value
- **Full-stack development**: Frontend, backend, database integration
- **Modern React**: Hooks, context, modern patterns
- **API integration**: RESTful API design and consumption
- **User experience**: Mobile-first, responsive design
- **Real-world application**: Actually useful for users

## Development Timeline
- **Week 3, Days 1-2**: Build backend API with model inference
- **Week 3, Days 3-4**: Build React frontend with photo upload
- **Week 3, Day 5**: Integration, testing, and deployment

## Technical Dependencies
- **Frontend**: React, Material-UI, Axios
- **Backend**: FastAPI, TensorFlow, PostgreSQL
- **Deployment**: Vercel/Netlify for frontend, Railway for backend
- **Storage**: Model files and database on Railway
- **Environment**: Railway-compatible configuration

## Deployment Strategy
- **Frontend**: Static hosting (Vercel/Netlify)
- **Backend**: Lightweight hosting with model files
- **Database**: PostgreSQL with recipes
- **CDN**: Optimize image delivery
- **Monitoring**: Basic error tracking and analytics

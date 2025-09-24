# Frontend Specification - Jam Hot Project

## Overview
The frontend is a React web application that connects the AI fruit classification with the recipe database. Users can upload fruit photos one at a time and receive identification results along with relevant jam recipes. The app features three main screens: Main Upload, Jamdex (recipe browser), and Recipe Detail. The design is playful, colorful, and mobile-first with a fruit-themed aesthetic.

## Core Functionality
**User Flow**: Upload fruit photo → Get fruit identification + jam recipes → Browse recipes → View full recipe details

## Technical Stack

### Frontend Framework
- **React**: Modern JavaScript framework with hooks
- **Material-UI**: UI component library for consistent design
- **React Router**: Client-side routing between screens
- **Axios**: HTTP client for API communication

### Backend Integration
- **Python FastAPI**: Backend API with model inference
- **PostgreSQL**: Recipe database storage
- **Model inference**: Real-time fruit classification

## Five Main Screens

### 1. Main Upload Page (Home)
**Purpose**: Primary entry point for photo upload and fruit identification

**Features**:
- **Photo Upload Area**: Drag & drop zone with file upload option
- **Processing Feedback**: Clear accept/reject messages with reasons
- **Fruit List**: Horizontal scrollable row of identified fruits (max 3)
- **Manual Fruit Selection**: Plus button to add fruits without photos
- **Recipe Recommendations**: Smart-sorted recipes based on identified fruits
  - Perfect matches (uses all identified fruits)
  - Good matches (uses some identified fruits)
  - Partial matches (uses fewer fruits)

**User Experience**:
- Upload one photo → Processing → Fruit identified → Recipe recommendations appear
- Click plus button → Fruit selector popup → Select fruit → Recipe recommendations update
- Clear visual feedback for each step
- Progressive disclosure of recipe recommendations

### 2. Jamdex Page (Recipe Browser)
**Purpose**: Browse all available jam recipes

**Features**:
- **Recipe Grid**: Responsive grid of recipe preview cards
- **Recipe Cards**: Show title, rating, review count, and fruit indicators
- **No Search Bar**: Keep interface simple and focused

**User Experience**:
- Browse all recipes in a clean grid layout
- Click any recipe card to view full details
- Infinite scroll for loading more recipes

### 3. Recipe Detail Page
**Purpose**: View complete recipe with ingredients and instructions

**Features**:
- **Recipe Header**: Title, rating, review count, fruit indicators
- **Ingredients List**: Double-column layout when possible
- **Instructions**: Step-by-step cooking instructions
- **Print Button**: Generate print-friendly version
- **Navigation**: Back button to previous page

**User Experience**:
- Clean, readable layout optimized for cooking
- Print-friendly version for kitchen use
- Easy navigation back to previous page
- No related recipes or nutritional information

### 4. Fruitdex Page (Fruit Browser)
**Purpose**: Browse all available fruits

**Features**:
- **Fruit Grid**: Responsive grid of fruit preview cards
- **Fruit Cards**: Show fruit name, emoji/icon, and basic info
- **No Search Bar**: Keep interface simple and focused

**User Experience**:
- Browse all fruits in a clean grid layout
- Click any fruit card to view full profile
- Infinite scroll for loading more fruits

### 5. Fruit Profile Page
**Purpose**: View detailed information about a specific fruit

**Features**:
- **Fruit Header**: Name, emoji/icon, and basic info
- **Essential Information**: Description, flavor profile, season, storage tips, preparation
- **Jam Uses**: What types of jams the fruit is good for
- **Navigation**: Back button to previous page

**User Experience**:
- Minimal content that fits on mobile screen with image
- Focus on essential information only
- Easy navigation back to previous page

## Component Architecture

### Page Components
```
src/pages/
├── HomePage.jsx           # Main upload page
├── JamdexPage.jsx         # Recipe browser
├── RecipeDetailPage.jsx   # Full recipe view
├── FruitdexPage.jsx       # Fruit browser
└── FruitProfilePage.jsx   # Individual fruit info
```

### Feature Components
```
src/components/
├── PhotoUpload/
│   ├── PhotoUploadArea.jsx    # Drag & drop zone
│   ├── ProcessingStatus.jsx   # Loading/error states
│   └── FruitList.jsx          # Horizontal scrollable row
├── Recipe/
│   ├── RecipeCard.jsx         # Recipe preview card
│   ├── RecipeGrid.jsx         # Responsive recipe grid
│   ├── RecipeDetail.jsx       # Full recipe display
│   └── PrintView.jsx          # Print-optimized layout
├── Fruit/
│   ├── FruitCard.jsx          # Fruit preview card
│   ├── FruitGrid.jsx          # Responsive fruit grid
│   ├── FruitProfile.jsx       # Full fruit display
│   └── FruitSelector.jsx      # Manual fruit selection popup
├── Navigation/
│   ├── Sidebar.jsx            # Collapsible sidebar
│   └── Header.jsx             # App header with logo
└── Layout/
    ├── PageContainer.jsx      # Page wrapper
    └── ResponsiveGrid.jsx     # Responsive grid system
```

### Custom Hooks
```
src/hooks/
├── usePhotoUpload.js          # Photo upload logic
├── useFruitClassification.js  # AI classification
├── useRecipes.js              # Recipe data management
├── useFruits.js               # Fruit data management
└── useURLState.js             # URL-based state management
```

### Utilities
```
src/utils/
├── fruitEmojis.js             # Fruit emoji mapping
├── colorPalette.js            # Theme colors
├── responsive.js              # Responsive utilities
└── urlState.js                # URL parameter handling
```

## User Experience Flows

### Flow 1: Photo Upload → Recipe Discovery
```
Home Page → Upload Photo → Processing → Fruit List → Recipe Recommendations → Recipe Detail
```

### Flow 2: Manual Fruit Selection
```
Home Page → Click Plus → Fruit Selector Popup → Select Fruit → Recipe Recommendations
```

### Flow 3: Browse All Recipes
```
Home Page → Jamdex → Recipe Detail
```

### Flow 4: Browse All Fruits
```
Home Page → Fruitdex → Fruit Profile
```

### Flow 5: Navigation with State
```
Any Page → Navigate to Another Page → Return (fruits still selected)
```

### Flow 6: Recipe Management
```
Recipe Detail → Print Recipe → (Print Dialog)
```

## Responsive Design Strategy

### Mobile-First Approach (320px - 768px)
- **Single column layout**: Optimized for mobile screens
- **Large touch targets**: 44px minimum for buttons and links
- **Collapsible sidebar**: Mobile-friendly navigation with icons
- **Horizontal fruit scroll**: Scrollable row of identified fruits
- **Fruit emojis**: Visual identification and fun factor

### Tablet (768px - 1024px)
- **Two-column recipe grid**: Better use of screen space
- **Expanded sidebar**: More prominent navigation
- **Larger photo upload area**: More prominent upload interface

### Desktop (1024px+)
- **Three-column recipe grid**: Maximum recipe visibility
- **Persistent sidebar**: Always visible navigation
- **Hover effects**: Enhanced interactions and animations
- **Keyboard shortcuts**: Power user features

## Key Features

### Photo Upload Experience
- **Drag & drop zone**: Large, friendly upload area with file upload option
- **One at a time**: Simple, focused experience
- **Clear feedback**: "Great photo!" or "Try better lighting"
- **Fruit emojis**: Visual identification of recognized fruits
- **Progressive disclosure**: Show recipes as fruits are identified

### Fruit Management
- **Maximum 3 fruits**: Focused on practical jam making
- **Horizontal scroll**: Scrollable row of identified fruits
- **Manual selection**: Plus button with fruit selector popup
- **URL persistence**: State maintained across navigation

### Recipe Recommendations
- **Smart sorting**: Perfect matches first, then partial matches
- **Visual hierarchy**: Clear sections for different match levels
- **Quick preview**: Rating, review count, fruit indicators
- **No recipe images**: Focus on descriptive titles

### Jamdex Features
- **Grid layout**: Mobile-friendly card grid
- **Infinite scroll**: Load more recipes as needed
- **No search bar**: Keep interface simple and focused

### Recipe Detail
- **Double-column ingredients**: When possible on desktop
- **Clean layout**: Easy to read ingredients and instructions
- **Print optimization**: Separate print view with minimal styling
- **Navigation**: Easy back to previous page
- **No related recipes**: Keep it simple

### Fruit Profile
- **Minimal content**: Only essential information that fits on mobile
- **Essential info**: Description, flavor, season, storage, preparation, jam uses
- **Easy navigation**: Back button to previous page

## State Management

### URL-Based State
- **Selected fruits**: Stored in URL parameters (?fruits=strawberry,blueberry,lemon)
- **Persistent across pages**: State maintained when navigating
- **Simple implementation**: No complex state management needed
- **Shareable URLs**: Users can share URLs with selected fruits

### Local State (useState)
- Photo upload status and progress
- Current results and recommendations
- UI interactions (modals, popups, sidebar state)

### Context API
- User preferences and settings
- App-wide error handling
- Theme and styling preferences

### Server State
- Recipe data and search results
- Fruit information and classifications
- User upload history

## Performance Optimization

### Image Handling
- **Compression**: Reduce image size before upload
- **Lazy loading**: Load recipe images as needed
- **WebP support**: Modern image formats when available

### API Optimization
- **Batch requests**: Combine multiple API calls
- **Caching**: Cache fruit information and popular recipes
- **Progressive loading**: Show results as they become available

### Bundle Optimization
- **Code splitting**: Load components as needed
- **Tree shaking**: Remove unused Material-UI components
- **Lazy loading**: Defer non-critical components

## Accessibility Features

### Keyboard Navigation
- **Tab order**: Logical navigation through all interactive elements
- **Enter/Space**: Button activation
- **Arrow keys**: Recipe browsing and selection

### Screen Reader Support
- **Alt text**: Descriptive text for all images
- **ARIA labels**: Complex interactions and dynamic content
- **Semantic HTML**: Proper heading structure and landmarks

### Visual Accessibility
- **High contrast**: Support for high contrast mode
- **Scalable text**: Responsive typography
- **Color-blind friendly**: Palette designed for accessibility

## URL Structure

### Route Definitions
```
/                           # Home page
/jamdex                     # Recipe browser
/jamdex/recipe/123          # Recipe detail
/fruitdex                   # Fruit browser
/fruitdex/fruit/strawberry  # Fruit profile
/?fruits=strawberry,blueberry,lemon  # Home with selected fruits
```

### URL Parameters
- **fruits**: Comma-separated list of selected fruits
- **Example**: `/?fruits=strawberry,blueberry,lemon`
- **Persistence**: State maintained across all pages
- **Sharing**: URLs can be shared with selected fruits

## Navigation Structure

### Collapsible Sidebar
- **Mobile**: Collapsible sidebar with icons
- **Desktop**: Persistent sidebar with expanded labels
- **Icons**: Home, Jamdex, Fruitdex, Profile, Settings
- **No search bar**: Keep interface simple and focused

### Navigation Items
1. **Home** - Main upload page
2. **Jamdex** - Recipe browser
3. **Fruitdex** - Fruit browser
4. **Profile** - User preferences (future)
5. **Settings** - App settings (future)

## Success Criteria
- **User experience**: Intuitive, fast, responsive, fun and easy to use
- **Photo upload**: Works seamlessly on mobile and desktop
- **AI integration**: Reliable fruit identification with clear feedback
- **Recipe display**: Clear, useful recipe information
- **Performance**: Fast loading and smooth interactions
- **Mobile responsive**: Essential for portfolio showcase
- **Error handling**: User-friendly error messages
- **Independence**: Works perfectly without maintenance
- **Print functionality**: Clean, kitchen-friendly print layouts
- **State persistence**: Selected fruits maintained across navigation
- **Simple navigation**: Easy to understand and use

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

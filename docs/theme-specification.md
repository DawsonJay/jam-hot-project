# Theme Specification - Jam Hot Project

## Overview
This document defines the visual design system for the Jam Hot application. The theme is playful, colorful, and friendly, using fruit-inspired colors with light, neutral backgrounds. The design emphasizes mobile-first responsive layouts with a focus on accessibility and user experience.

## Design Philosophy
- **Playful & Friendly**: Fun, approachable design that makes jam making enjoyable
- **Fruit-Inspired**: Colors and elements that evoke fresh, natural fruits
- **Mobile-First**: Optimized for mobile devices with progressive enhancement
- **Accessible**: High contrast, readable typography, and inclusive design
- **Clean & Modern**: Simple layouts that don't overwhelm the content

## Color Palette

### Primary Colors (Fruit-Inspired)
```css
/* Strawberry Red - Primary action color */
--strawberry-red: #FF6B6B;
--strawberry-red-light: #FF8E8E;
--strawberry-red-dark: #E55A5A;

/* Blueberry Blue - Secondary actions */
--blueberry-blue: #4ECDC4;
--blueberry-blue-light: #6ED5CE;
--blueberry-blue-dark: #3BB5AD;

/* Lemon Yellow - Accent and highlights */
--lemon-yellow: #FFE66D;
--lemon-yellow-light: #FFEB85;
--lemon-yellow-dark: #E6CF5A;

/* Apple Green - Success states */
--apple-green: #95E1D3;
--apple-green-light: #A8E7DC;
--apple-green-dark: #7BCAB8;

/* Orange Orange - Warning and attention */
--orange-orange: #FF8A65;
--orange-orange-light: #FF9F7F;
--orange-orange-dark: #E67A4A;
```

### Neutral Colors
```css
/* Background Colors */
--cream-white: #FFF8F0;
--soft-gray: #F5F5F5;
--light-gray: #E8E8E8;
--medium-gray: #CCCCCC;

/* Text Colors */
--text-primary: #2C3E50;
--text-secondary: #5A6C7D;
--text-muted: #8A9BA8;
--text-inverse: #FFFFFF;

/* Border Colors */
--border-light: #E8E8E8;
--border-medium: #CCCCCC;
--border-dark: #999999;
```

### Accent Colors
```css
/* Additional Fruit Colors */
--peach: #FFB3BA;
--mint: #BAFFC9;
--lavender: #BAFFC9;
--grape: #C7CEEA;
--cherry: #FFB3BA;
```

### Status Colors
```css
/* Success */
--success: var(--apple-green);
--success-light: var(--apple-green-light);
--success-dark: var(--apple-green-dark);

/* Warning */
--warning: var(--orange-orange);
--warning-light: var(--orange-orange-light);
--warning-dark: var(--orange-orange-dark);

/* Error */
--error: var(--strawberry-red);
--error-light: var(--strawberry-red-light);
--error-dark: var(--strawberry-red-dark);

/* Info */
--info: var(--blueberry-blue);
--info-light: var(--blueberry-blue-light);
--info-dark: var(--blueberry-blue-dark);
```

## Typography

### Font Families
```css
/* Primary Font - Playful and friendly */
--font-primary: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Secondary Font - Clean and readable */
--font-secondary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Accent Font - Fun and approachable */
--font-accent: 'Quicksand', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Monospace Font - Code and data */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

### Font Weights
```css
--font-weight-light: 300;
--font-weight-regular: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Font Sizes (Mobile-First)
```css
/* Mobile Base Sizes */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */

/* Desktop Scaling */
@media (min-width: 768px) {
  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.25rem;    /* 20px */
  --text-2xl: 1.5rem;    /* 24px */
  --text-3xl: 2rem;      /* 32px */
  --text-4xl: 2.5rem;    /* 40px */
}
```

### Line Heights
```css
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;
```

## Spacing System

### Base Unit
- **Base unit**: 8px
- **All spacing**: Multiples of 8px for consistency

### Spacing Scale
```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.25rem;   /* 20px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-10: 2.5rem;   /* 40px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
--space-20: 5rem;     /* 80px */
--space-24: 6rem;     /* 96px */
```

### Layout Spacing
```css
/* Mobile */
--container-padding: var(--space-4);  /* 16px */
--section-spacing: var(--space-6);    /* 24px */
--component-spacing: var(--space-4);  /* 16px */

/* Tablet */
@media (min-width: 768px) {
  --container-padding: var(--space-6);  /* 24px */
  --section-spacing: var(--space-8);    /* 32px */
  --component-spacing: var(--space-5);  /* 20px */
}

/* Desktop */
@media (min-width: 1024px) {
  --container-padding: var(--space-8);  /* 32px */
  --section-spacing: var(--space-10);   /* 40px */
  --component-spacing: var(--space-6);  /* 24px */
}
```

## Border Radius

### Border Radius Scale
```css
--radius-none: 0;
--radius-sm: 0.125rem;   /* 2px */
--radius-base: 0.25rem;  /* 4px */
--radius-md: 0.375rem;   /* 6px */
--radius-lg: 0.5rem;     /* 8px */
--radius-xl: 0.75rem;    /* 12px */
--radius-2xl: 1rem;      /* 16px */
--radius-3xl: 1.5rem;    /* 24px */
--radius-full: 9999px;   /* Fully rounded */
```

### Component-Specific Radius
```css
--button-radius: var(--radius-lg);
--card-radius: var(--radius-xl);
--input-radius: var(--radius-md);
--modal-radius: var(--radius-2xl);
```

## Shadows

### Shadow Scale
```css
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
--shadow-base: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
--shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
--shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
--shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
```

### Component-Specific Shadows
```css
--card-shadow: var(--shadow-base);
--button-shadow: var(--shadow-sm);
--modal-shadow: var(--shadow-xl);
--dropdown-shadow: var(--shadow-lg);
```

## Component Styles

### Buttons
```css
/* Primary Button */
.btn-primary {
  background-color: var(--strawberry-red);
  color: var(--text-inverse);
  border-radius: var(--button-radius);
  padding: var(--space-3) var(--space-6);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--button-shadow);
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--strawberry-red-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* Secondary Button */
.btn-secondary {
  background-color: var(--blueberry-blue);
  color: var(--text-inverse);
  border-radius: var(--button-radius);
  padding: var(--space-3) var(--space-6);
  font-weight: var(--font-weight-medium);
  box-shadow: var(--button-shadow);
  transition: all 0.2s ease;
}

/* Outline Button */
.btn-outline {
  background-color: transparent;
  color: var(--strawberry-red);
  border: 2px solid var(--strawberry-red);
  border-radius: var(--button-radius);
  padding: var(--space-3) var(--space-6);
  font-weight: var(--font-weight-medium);
  transition: all 0.2s ease;
}
```

### Cards
```css
.recipe-card {
  background-color: var(--text-inverse);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: var(--space-4);
  transition: all 0.2s ease;
}

.recipe-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}
```

### Input Fields
```css
.input-field {
  background-color: var(--text-inverse);
  border: 2px solid var(--border-light);
  border-radius: var(--input-radius);
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
  transition: border-color 0.2s ease;
}

.input-field:focus {
  border-color: var(--strawberry-red);
  outline: none;
  box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.1);
}
```

## Responsive Breakpoints

### Breakpoint System
```css
/* Mobile First */
--breakpoint-sm: 640px;   /* Small tablets */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Laptops */
--breakpoint-xl: 1280px;  /* Desktops */
--breakpoint-2xl: 1536px; /* Large desktops */
```

### Media Query Mixins
```css
/* Mobile (default) */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

## Animation & Transitions

### Transition Timing
```css
--transition-fast: 0.15s ease;
--transition-base: 0.2s ease;
--transition-slow: 0.3s ease;
```

### Common Animations
```css
/* Fade In */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide Up */
@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

/* Bounce */
@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -8px, 0);
  }
  70% {
    transform: translate3d(0, -4px, 0);
  }
  90% {
    transform: translate3d(0, -2px, 0);
  }
}
```

## Accessibility Guidelines

### Color Contrast
- **Text on background**: Minimum 4.5:1 contrast ratio
- **Large text**: Minimum 3:1 contrast ratio
- **Interactive elements**: Minimum 3:1 contrast ratio

### Focus States
```css
.focus-visible {
  outline: 2px solid var(--strawberry-red);
  outline-offset: 2px;
}
```

### Touch Targets
- **Minimum size**: 44px × 44px
- **Recommended size**: 48px × 48px
- **Spacing**: Minimum 8px between touch targets

## Implementation Notes

### CSS Custom Properties
All theme values are defined as CSS custom properties for easy theming and dynamic updates.

### Material-UI Integration
The theme integrates with Material-UI's theming system:
```javascript
const theme = createTheme({
  palette: {
    primary: {
      main: '#FF6B6B', // strawberry-red
    },
    secondary: {
      main: '#4ECDC4', // blueberry-blue
    },
    // ... other palette colors
  },
  typography: {
    fontFamily: 'Poppins, Inter, sans-serif',
    // ... typography settings
  },
  // ... other theme settings
});
```

### Future Enhancements
- **Dark mode support**: Additional color palette for dark theme
- **Seasonal themes**: Special color schemes for different seasons
- **User customization**: Allow users to choose accent colors
- **Animation preferences**: Respect user's motion preferences

---

*This theme specification was created on 2025-09-24-0929 and will be updated as the design evolves.*

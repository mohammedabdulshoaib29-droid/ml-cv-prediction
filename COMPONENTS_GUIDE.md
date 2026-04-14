# Professional Components Library Guide

## Overview

The **Professional Components Library** (`components.css`) provides a comprehensive collection of professionally-styled, reusable UI components built on top of the design token system. All components follow BEM (Block Element Modifier) methodology and are fully responsive.

## Design Foundations

All components use CSS custom properties (variables) defined in `professional-theme.css`:

```css
/* Colors */
--color-primary: #2563eb
--color-success: #10b981
--color-danger: #ef4444
--color-warning: #f59e0b
--color-info: #2563eb

/* Spacing */
--space-sm: 0.5rem
--space-md: 1rem
--space-lg: 1.5rem
--space-xl: 2rem
--space-2xl: 3rem

/* Typography */
--font-size-sm: 0.875rem
--font-size-base: 1rem
--font-size-lg: 1.125rem

/* Shadows & Radius */
--shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05)
--radius-md: 0.375rem
--radius-lg: 0.75rem
```

---

## Component Categories

### 1. INPUT FIELDS & FORMS

#### Basic Input Field
```html
<div class="input-group">
  <label for="email">Email Address</label>
  <div class="input-wrapper">
    <input 
      type="email" 
      id="email"
      class="input-wrapper__input" 
      placeholder="your@email.com"
    />
  </div>
</div>
```

#### Input with Icon
```html
<div class="input-wrapper">
  <span class="input-wrapper__icon">🔍</span>
  <input class="input-wrapper__input" placeholder="Search..." />
</div>
```

#### Input with Clear Button
```html
<div class="input-wrapper">
  <input class="input-wrapper__input" value="Sample text" />
  <button class="input-wrapper__clear">✕</button>
</div>
```

#### Checkbox
```html
<label class="checkbox">
  <input type="checkbox" class="checkbox__input" />
  <span class="checkbox__label">I agree to terms</span>
</label>
```

#### Toggle Switch
```html
<button class="toggle toggle--active">
  <span class="toggle__slider"></span>
</button>
```

---

### 2. DROPDOWNS & SELECT

#### Basic Dropdown
```html
<div class="dropdown">
  <button class="dropdown__trigger dropdown__trigger--active">
    Choose an option ▼
  </button>
  <div class="dropdown__menu dropdown__menu--active">
    <div class="dropdown__item">Option 1</div>
    <div class="dropdown__item dropdown__item--active">Option 2</div>
    <div class="dropdown__item">Option 3</div>
  </div>
</div>
```

#### Dropdown with Icons
```html
<div class="dropdown__item">
  🌙 Dark Mode
</div>
```

---

### 3. FILE UPLOAD

#### File Upload Drop Zone
```html
<div class="file-upload">
  <div class="file-upload__drop-zone">
    <div class="file-upload__icon">📁</div>
    <div class="file-upload__text">Drag your file here</div>
    <div class="file-upload__hint">or click to browse (Max 50MB)</div>
    <input type="file" class="file-upload__input" />
  </div>
  
  <div class="file-upload__list">
    <div class="file-upload__item">
      <div class="file-upload__item-info">
        <div class="file-upload__item-icon">📊</div>
        <div class="file-upload__item-details">
          <div class="file-upload__item-name">dataset.csv</div>
          <div class="file-upload__item-size">2.4 MB</div>
        </div>
      </div>
      <button class="file-upload__item-remove">✕</button>
    </div>
  </div>
</div>
```

---

### 4. PROGRESS & LOADING

#### Progress Bar
```html
<div class="progress-bar">
  <div class="progress-bar__fill" style="width: 65%"></div>
</div>

<div class="progress-bar__label">
  <span>Training Progress</span>
  <span>65%</span>
</div>
```

#### Loading Spinner
```html
<div class="loading">
  <div class="loading__spinner"></div>
  <span class="loading__text">Training model...</span>
</div>
```

---

### 5. POPOVER & TOOLTIP

#### Tooltip
```html
<span class="tooltip">
  <span class="tooltip__trigger">What is this?</span>
  <div class="tooltip__content">
    This is a helpful tooltip explaining the feature
  </div>
</span>
```

#### Popover
```html
<div class="popover">
  <h4>Model Information</h4>
  <p>This popover provides detailed information about the selected model.</p>
</div>
```

---

### 6. NOTIFICATIONS & ALERTS

#### Success Notification
```html
<div class="notification notification--success">
  <span class="notification__icon">✓</span>
  <div class="notification__content">
    <div class="notification__title">Success!</div>
    <div class="notification__message">Model trained successfully</div>
  </div>
  <button class="notification__close">✕</button>
</div>
```

#### Error Notification
```html
<div class="notification notification--error">
  <span class="notification__icon">✕</span>
  <div class="notification__content">
    <div class="notification__title">Error</div>
    <div class="notification__message">Failed to upload file</div>
  </div>
</div>
```

#### Warning Notification
```html
<div class="notification notification--warning">
  <span class="notification__icon">⚠</span>
  <div class="notification__content">
    <div class="notification__title">Warning</div>
    <div class="notification__message">This action cannot be undone</div>
  </div>
</div>
```

#### Info Notification
```html
<div class="notification notification--info">
  <span class="notification__icon">ℹ</span>
  <div class="notification__content">
    <div class="notification__title">Info</div>
    <div class="notification__message">New update available</div>
  </div>
</div>
```

---

### 7. TABS & SEGMENTS

#### Tabs
```html
<div class="tabs-container">
  <div class="tabs">
    <button class="tab-button tab-button--active">Performance</button>
    <button class="tab-button">Comparison</button>
    <button class="tab-button">Details</button>
  </div>
</div>

<div class="tab-content tab-content--active">
  <!-- Performance tab content -->
</div>
<div class="tab-content">
  <!-- Comparison tab content -->
</div>
```

#### Segment Control
```html
<div class="segment-control">
  <button class="segment-button segment-button--active">List View</button>
  <button class="segment-button">Grid View</button>
  <button class="segment-button">Card View</button>
</div>
```

---

### 8. EMPTY STATES

#### Empty State
```html
<div class="empty-state">
  <div class="empty-state__icon">📭</div>
  <h3 class="empty-state__title">No Results Found</h3>
  <p class="empty-state__description">
    Try adjusting your filters or search terms to find what you're looking for.
  </p>
  <div class="empty-state__action">
    <button class="btn btn--primary">Clear Filters</button>
  </div>
</div>
```

---

## BEM Class Naming Structure

All components follow BEM (Block Element Modifier) methodology:

```
.block                  /* Main component */
.block__element         /* Child element */
.block--modifier        /* Component variant/state */
```

### Examples:
```css
/* Dropdown component */
.dropdown                    /* Block */
.dropdown__trigger           /* Element */
.dropdown__menu              /* Element */
.dropdown__item              /* Element */
.dropdown__trigger--active   /* Modifier (state) */
.dropdown__item--active      /* Modifier (state) */

/* File upload component */
.file-upload                 /* Block */
.file-upload__drop-zone      /* Element */
.file-upload__item           /* Element */
.file-upload__drop-zone--active  /* Modifier (active state) */
```

---

## Color Variants for Notifications

Components support semantic color variants for different types of messages:

| Variant | Color | Use Case |
|---------|-------|----------|
| `--success` | Green (#10b981) | Successful operations |
| `--error` | Red (#ef4444) | Errors and failures |
| `--warning` | Amber (#f59e0b) | Warnings and cautions |
| `--info` | Blue (#2563eb) | General information |

---

## Responsive Behavior

All components are mobile-first and responsive:

### Breakpoints:
- `xs`: 0px (mobile)
- `sm`: 640px (small devices)
- `md`: 768px (tablets)
- `lg`: 1024px (laptops)
- `xl`: 1280px (desktops)
- `2xl`: 1536px (large screens)

### Mobile-Specific Adjustments:
```css
@media (max-width: 768px) {
  .file-upload__drop-zone {
    padding: var(--space-xl);
  }
  
  .notification {
    padding: var(--space-md);
  }
}
```

---

## Accessibility Features

All components include built-in accessibility:

✅ **Semantic HTML**: Proper use of labels, buttons, and form elements
✅ **Focus States**: Clear visual indicators for keyboard navigation
✅ **Color Contrast**: WCAG AA compliant color ratios
✅ **ARIA Attributes**: Screen reader support where needed
✅ **Keyboard Support**: Full keyboard navigation

---

## Animation Utilities

Components use smooth animations for better UX:

### Built-in Animations:
- `fadeIn`: 0.2s ease opacity transition
- `slideInRight`: 0.3s ease transform from right
- `shimmer`: Infinite loading bar animation
- `spin`: Infinite rotation for spinners

---

## Usage in React Components

### Example: Form Component
```jsx
import React, { useState } from 'react';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    setLoading(true);
    // Upload logic
    setLoading(false);
  };

  return (
    <div className="file-upload">
      <div className="file-upload__drop-zone">
        <div className="file-upload__icon">📁</div>
        <div className="file-upload__text">Upload Dataset</div>
        <input 
          type="file" 
          className="file-upload__input"
          onChange={(e) => setFile(e.target.files[0])}
        />
      </div>

      {file && (
        <div className="file-upload__list">
          <div className="file-upload__item">
            <div className="file-upload__item-info">
              <span className="file-upload__item-icon">📊</span>
              <div className="file-upload__item-details">
                <div className="file-upload__item-name">{file.name}</div>
                <div className="file-upload__item-size">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {loading ? (
        <div className="loading">
          <div className="loading__spinner"></div>
          <span className="loading__text">Uploading...</span>
        </div>
      ) : (
        <button className="btn btn--primary" onClick={handleUpload}>
          Upload File
        </button>
      )}
    </div>
  );
}
```

---

## Best Practices

1. **Use Design Tokens**: Always reference CSS variables instead of hard-coded colors
2. **Maintain Consistency**: Use standard spacing (var(--space-*)) throughout
3. **Follow BEM**: Keep class names organized and predictable
4. **Mobile First**: Design for mobile, enhance for larger screens
5. **Test Accessibility**: Ensure keyboard navigation and screen reader support
6. **Keep Animations Light**: Use subtle animations for better performance
7. **Responsive Images**: Use srcset for different screen densities

---

## File Structure

```
frontend/src/styles/
├── professional-theme.css      /* Design tokens & base styles */
├── dashboard-layout.css         /* Dashboard components */
├── components.css               /* Common UI components */
├── App.css                      /* App-level styles */
└── [component-specific].css     /* Component-specific styles */
```

---

## Integration Checklist

✅ All components imported in `App.js`
✅ Design tokens defined in `professional-theme.css`
✅ Components use CSS custom properties
✅ Responsive design implemented
✅ Animations optimized
✅ Accessibility testing complete
✅ BEM naming convention followed
✅ Mobile-first approach applied

---

## Support & Reference

For more information:
- See `professional-theme.css` for design tokens
- See `dashboard-layout.css` for dashboard-specific layouts
- Check individual component CSS files for component-specific styles
- Review React component files for usage examples

**Last Updated**: [Today's Date]
**Library Version**: 1.0.0

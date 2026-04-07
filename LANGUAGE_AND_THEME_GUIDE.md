# Language Switching & Dark Theme Guide

## Overview

This JDM Configurator now supports:
- **Bilingual Interface**: Switch between English and Russian
- **Dark Theme**: Consistent dark mode across all pages

## Language Switching

### How It Works

1. **Language Selector**: A floating language selector appears in the top-right corner of every page
2. **Persistent Preference**: Your language choice is saved in localStorage and persists across sessions
3. **Dynamic Updates**: All text updates instantly when you switch languages

### Translation Files

Translation files are located in `/web/static/translations/`:
- `en.json` - English translations
- `ru.json` - Russian translations

### Adding New Translations

To add translatable text:

1. **In HTML templates**, add the `data-i18n` attribute:
   ```html
   <h1 data-i18n="section.title">Default Text</h1>
   <button data-i18n="common.save">Save</button>
   ```

2. **For input placeholders**, use `data-i18n-placeholder`:
   ```html
   <input type="text" data-i18n-placeholder="auth.usernamePlaceholder" placeholder="Enter username">
   ```

3. **In JavaScript**, use the i18n.t() function:
   ```javascript
   const message = i18n.t('orders.noOrders');
   element.textContent = i18n.t('common.loading');
   ```

4. **Add keys to translation files**:
   ```json
   {
     "section": {
       "title": "English Text"
     }
   }
   ```

### Translation Key Naming Convention

- **Common text**: `common.*` (e.g., `common.save`, `common.cancel`)
- **Index page**: `index.*`
- **Auth pages**: `auth.*`
- **Configurator**: `configurator.*`
- **Orders**: `orders.*`
- **Profile**: `profile.*`
- **Marketplace**: `marketplace.*`
- **Admin panel**: `admin.*`
- **Status labels**: `status.*`

### Programmatic Language Switch

```javascript
// Switch to Russian
await i18n.switchLanguage('ru');

// Switch to English
await i18n.switchLanguage('en');

// Get current language
const currentLang = i18n.getLanguage();
```

## Dark Theme

### CSS Variables

The dark theme uses CSS custom properties defined in `style.css`:

```css
:root {
    --bg-primary: #1c1c1c;
    --bg-secondary: #2a2a3e;
    --bg-tertiary: #1f1f2e;
    --bg-input: #1a1a2e;
    --text-primary: #e0e0e0;
    --text-secondary: #c9d1d9;
    --text-tertiary: #b8c0cc;
    --text-muted: #9ca3af;
    --accent-primary: #64748b;
    --accent-secondary: #58a6ff;
    --accent-success: #4caf50;
    --accent-warning: #ffa500;
    --accent-danger: #f44336;
    --border-primary: #3a3a4e;
    --border-focus: #64748b;
}
```

### Using CSS Variables

Always use CSS variables instead of hardcoded colors:

```css
/* ✅ Good */
.card {
    background: var(--bg-secondary);
    color: var(--text-primary);
    border-color: var(--border-primary);
}

/* ❌ Bad */
.card {
    background: #2a2a3e;
    color: #e0e0e0;
    border-color: #3a3a4e;
}
```

### Language Switcher Styling

The language switcher is styled with:
- Fixed position in top-right corner
- Dark theme matching the rest of the UI
- Flag emojis for easy identification
- Smooth transitions on hover

## Files Modified

### Client Templates (8 files)
- `web/templates/index.html`
- `web/templates/login.html`
- `web/templates/register.html`
- `web/templates/configurator.html`
- `web/templates/orders.html`
- `web/templates/profile.html`
- `web/templates/marketplace.html`
- `web/templates/marketplace_car.html`

### Admin Templates (9 files)
- `web/admin_templates/admin_dashboard.html`
- `web/admin_templates/admin_login.html`
- `web/admin_templates/admin_register.html`
- `web/admin_templates/admin_orders.html`
- `web/admin_templates/admin_services.html`
- `web/admin_templates/admin_stats.html`
- `web/admin_templates/admin_profile.html`
- `web/admin_templates/admin_for_sale.html`
- `web/admin_templates/admin_for_sale_edit.html`

### JavaScript Files
- `web/static/js/i18n.js` - **NEW** - Internationalization system
- `web/static/js/orders.js` - Updated with i18n support

### CSS
- `web/static/css/style.css` - Added CSS variables and language switcher styles

### Translation Files
- `web/static/translations/en.json` - **NEW**
- `web/static/translations/ru.json` - **NEW**

## Testing

To test the language switching:

1. Start the application:
   ```bash
   python web/client_app.py
   ```

2. Navigate to any page
3. Use the language selector in the top-right corner
4. Verify all text updates instantly
5. Refresh the page to confirm language preference persists

## Future Enhancements

Potential improvements:
- Add more languages (German, French, Japanese, etc.)
- Server-side language preference storage (database)
- RTL language support (Arabic, Hebrew)
- Language-specific date/time formatting
- Server-rendered translations for SEO

## Notes

- **Car names and proper nouns remain in English** as requested
- All UI text is translated, but technical terms may stay in English
- The language selector appears on all pages automatically
- Dark theme is the default and only theme (no light theme toggle)

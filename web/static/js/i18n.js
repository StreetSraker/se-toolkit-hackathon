// Internationalization (i18n) System
class I18n {
  constructor() {
    this.translations = {};
    this.currentLang = this.getStoredLanguage() || 'en';
    this.currentTheme = this.getStoredTheme() || 'dark';
    this.loaded = false;
  }

  // Get stored language from localStorage
  getStoredLanguage() {
    return localStorage.getItem('preferred_language');
  }

  // Store language preference
  storeLanguage(lang) {
    localStorage.setItem('preferred_language', lang);
  }

  // Get stored theme from localStorage
  getStoredTheme() {
    return localStorage.getItem('preferred_theme') || 'dark';
  }

  // Store theme preference
  storeTheme(theme) {
    localStorage.setItem('preferred_theme', theme);
  }

  // Load translations for a specific language
  async loadLanguage(lang) {
    if (this.translations[lang]) {
      this.currentLang = lang;
      this.storeLanguage(lang);
      return this.translations[lang];
    }

    try {
      const response = await fetch(`/static/translations/${lang}.json`);
      if (!response.ok) {
        throw new Error(`Failed to load translations for ${lang}`);
      }
      this.translations[lang] = await response.json();
      this.currentLang = lang;
      this.storeLanguage(lang);
      this.loaded = true;
      return this.translations[lang];
    } catch (error) {
      console.error('Error loading translations:', error);
      // Fallback to English
      if (lang !== 'en') {
        return this.loadLanguage('en');
      }
      return null;
    }
  }

  // Get translation by key (supports nested keys like "index.title")
  t(key) {
    const keys = key.split('.');
    let value = this.translations[this.currentLang];

    for (const k of keys) {
      if (value && typeof value === 'object' && k in value) {
        value = value[k];
      } else {
        console.warn(`Translation missing for key: ${key} in ${this.currentLang}`);
        return key;
      }
    }

    return value || key;
  }

  // Update all elements with data-i18n attribute
  updatePage() {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      const translation = this.t(key);
      
      // Only update if we got a valid translation (not the key itself)
      if (translation && translation !== key) {
        // Update text content for different element types
        if (el.tagName === 'INPUT' && el.type !== 'submit' && el.type !== 'button') {
          // For inputs, store original placeholder and update it
          if (!el.getAttribute('data-original-placeholder')) {
            el.setAttribute('data-original-placeholder', el.placeholder);
          }
          el.placeholder = translation;
        } else if (el.tagName === 'BUTTON' || el.tagName === 'A') {
          // Store original text as fallback
          if (!el.getAttribute('data-original-text')) {
            el.setAttribute('data-original-text', el.textContent);
          }
          el.textContent = translation;
        } else {
          // Store original text as fallback
          if (!el.getAttribute('data-original-text')) {
            el.setAttribute('data-original-text', el.textContent);
          }
          el.textContent = translation;
        }
      }
      // If translation failed, keep the original text/placeholder
    });

    // Update elements with data-i18n-placeholder attribute
    const placeholderElements = document.querySelectorAll('[data-i18n-placeholder]');
    placeholderElements.forEach(el => {
      const key = el.getAttribute('data-i18n-placeholder');
      const translation = this.t(key);
      
      // Only update if we got a valid translation
      if (translation && translation !== key) {
        el.placeholder = translation;
      }
      // Otherwise keep the original placeholder
    });

    // Update language selector if exists
    const langSelector = document.getElementById('languageSelect');
    if (langSelector) {
      langSelector.value = this.currentLang;
    }

    // Update HTML lang attribute
    document.documentElement.lang = this.currentLang;
  }

  // Switch language
  async switchLanguage(lang) {
    await this.loadLanguage(lang);
    this.updatePage();
    
    // Dispatch custom event for components that need to handle language changes
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
  }

  // Initialize i18n
  async init() {
    // Apply theme first
    this.applyTheme(this.currentTheme);
    
    // Load translations
    await this.loadLanguage(this.currentLang);
    
    // Create language selector first
    this.createLanguageSelector();
    
    // Then update the page (including selector value)
    this.updatePage();
  }

  // Create floating language selector
  createLanguageSelector() {
    if (document.getElementById('languageSelect')) return;

    const container = document.createElement('div');
    container.className = 'language-switcher';
    container.innerHTML = `
      <select id="languageSelect" onchange="i18n.switchLanguage(this.value)">
        <option value="en">GB English</option>
        <option value="ru">RU Русский</option>
      </select>
      <button id="themeToggle" class="theme-toggle" onclick="i18n.toggleTheme()" title="Toggle Theme">
        ${this.currentTheme === 'dark' ? '☀️' : '🌙'}
      </button>
    `;

    document.body.appendChild(container);
    
    // Set the selector value immediately after creation
    const selector = document.getElementById('languageSelect');
    if (selector) {
      selector.value = this.currentLang;
    }
  }

  // Get current language
  getLanguage() {
    return this.currentLang;
  }

  // Apply theme to the page
  applyTheme(theme) {
    this.currentTheme = theme;
    this.storeTheme(theme);
    
    if (theme === 'light') {
      document.documentElement.classList.add('light-theme');
    } else {
      document.documentElement.classList.remove('light-theme');
    }
    
    // Update theme toggle button if exists
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
      themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
      themeToggle.title = theme === 'dark' ? 'Switch to Light Theme' : 'Switch to Dark Theme';
    }
  }

  // Toggle between dark and light theme
  toggleTheme() {
    const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
    this.applyTheme(newTheme);
  }

  // Get current theme
  getTheme() {
    return this.currentTheme;
  }
}

// Create global i18n instance
const i18n = new I18n();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    i18n.init();
  });
} else {
  i18n.init();
}

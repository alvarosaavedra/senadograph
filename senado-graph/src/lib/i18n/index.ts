import { register, init, getLocaleFromNavigator } from 'svelte-i18n';
import { browser } from '$app/environment';

// Register locales
register('es', () => import('./es.json'));
register('en', () => import('./en.json'));

// Initialize i18n
export function setupI18n() {
  if (browser) {
    const savedLang = localStorage.getItem('language');
    const defaultLang = savedLang || 'es';
    
    init({
      fallbackLocale: 'es',
      initialLocale: defaultLang
    });
  }
}

// Set language
export function setLanguage(lang: 'es' | 'en') {
  if (browser) {
    localStorage.setItem('language', lang);
    window.location.reload();
  }
}

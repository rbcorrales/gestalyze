import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import { en } from './translations/en';
import { es } from './translations/es';

// Get browser language
const getBrowserLanguage = () => {
  const savedLanguage = localStorage.getItem('language');
  if (savedLanguage) return savedLanguage;

  const browserLang = navigator.language.split('-')[0];
  return ['en', 'es'].includes(browserLang) ? browserLang : 'en';
};

i18n.use(initReactI18next).init({
  resources: {
    en: { translation: en },
    es: { translation: es },
  },
  lng: getBrowserLanguage(),
  fallbackLng: 'en',
  interpolation: {
    escapeValue: false,
  },
});

export default i18n;

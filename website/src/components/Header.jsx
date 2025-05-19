import { useTranslation } from 'react-i18next';
import { GlobeAltIcon } from '@heroicons/react/24/outline';
import { useState, useEffect, useRef } from 'react';
import { siGithub } from 'simple-icons/icons';
import ThemeToggle from './ThemeToggle';

function Header() {
  const { t, i18n } = useTranslation();
  const [selectedLanguage, setSelectedLanguage] = useState(
    localStorage.getItem('language') || 'en'
  );
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);

  useEffect(() => {
    i18n.changeLanguage(selectedLanguage);
  }, [selectedLanguage, i18n]);

  useEffect(() => {
    function handleClickOutside(event) {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowMenu(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const changeLanguage = (lng) => {
    setSelectedLanguage(lng);
    localStorage.setItem('language', lng);
    setShowMenu(false);
  };

  const handleKeyDown = (event, action) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      action();
    } else if (event.key === 'Escape' && showMenu) {
      setShowMenu(false);
    }
  };

  return (
    <header
      className="fixed z-50 w-full border-b border-gray-200 bg-white/80 backdrop-blur-sm dark:border-gray-700 dark:bg-gray-900/80"
      role="banner"
    >
      <nav className="container mx-auto px-4 py-4" aria-label="Main navigation">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <a href="/" className="flex items-center space-x-2" aria-label={t('header.title')}>
              <img
                src="/gestalyze-logo.svg"
                alt=""
                className="h-8 w-8 text-primary"
                aria-hidden="true"
              />
              <span className="text-2xl font-normal tracking-[.2em] text-primary">
                {t('header.title')}
              </span>
            </a>
            <span
              className="flex hidden items-center text-sm text-gray-600 dark:text-gray-400 md:inline"
              aria-label={t('header.subtitle')}
            >
              {t('header.subtitle')}
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <div className="relative" ref={menuRef}>
              <button
                onClick={() => setShowMenu(!showMenu)}
                onKeyDown={(e) => handleKeyDown(e, () => setShowMenu(!showMenu))}
                className="flex items-center space-x-2 rounded-md p-1 text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:text-gray-400 dark:hover:text-gray-200"
                aria-expanded={showMenu}
                aria-haspopup="true"
                aria-label={t('header.languageMenu')}
              >
                <GlobeAltIcon className="h-5 w-5" aria-hidden="true" />
                <span className="hidden md:inline">{t('header.language')}</span>
              </button>
              {showMenu && (
                <div
                  className="absolute right-0 mt-2 w-48 rounded-lg border border-gray-200 bg-white py-2 shadow-lg dark:border-gray-700 dark:bg-gray-800"
                  role="menu"
                  aria-orientation="vertical"
                  aria-labelledby="language-menu"
                >
                  <button
                    onClick={() => changeLanguage('en')}
                    onKeyDown={(e) => handleKeyDown(e, () => changeLanguage('en'))}
                    className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none dark:text-gray-200 dark:hover:bg-gray-700 dark:focus:bg-gray-700"
                    role="menuitem"
                    aria-label={t('header.switchToEnglish')}
                  >
                    {t('header.en')}
                  </button>
                  <button
                    onClick={() => changeLanguage('es')}
                    onKeyDown={(e) => handleKeyDown(e, () => changeLanguage('es'))}
                    className="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none dark:text-gray-200 dark:hover:bg-gray-700 dark:focus:bg-gray-700"
                    role="menuitem"
                    aria-label={t('header.switchToSpanish')}
                  >
                    {t('header.es')}
                  </button>
                </div>
              )}
            </div>
            <a
              href="https://github.com/rbcorrales/gestalyze"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-md p-1 text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:text-gray-400 dark:hover:text-gray-200"
              aria-label={t('header.githubRepository')}
            >
              <svg
                className="h-6 w-6"
                viewBox="0 0 24 24"
                fill="currentColor"
                aria-hidden="true"
                focusable="false"
              >
                <path d={siGithub.path} />
              </svg>
            </a>
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Header;

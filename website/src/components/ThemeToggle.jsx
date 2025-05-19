import { useTheme } from '../context/ThemeContext';
import { useTranslation } from 'react-i18next';
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';

function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  const { t } = useTranslation();

  return (
    <button
      onClick={toggleTheme}
      className="flex items-center space-x-2 rounded-md p-1 text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:text-gray-400 dark:hover:text-gray-200"
      aria-label={theme === 'light' ? t('header.switchToDark') : t('header.switchToLight')}
    >
      {theme === 'light' ? (
        <MoonIcon className="h-5 w-5" aria-hidden="true" />
      ) : (
        <SunIcon className="h-5 w-5" aria-hidden="true" />
      )}
      <span className="hidden md:inline">
        {theme === 'light' ? t('header.darkMode') : t('header.lightMode')}
      </span>
    </button>
  );
}

export default ThemeToggle;

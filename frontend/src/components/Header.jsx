import { useTranslation } from 'react-i18next';
import { Bars3Icon, GlobeAltIcon } from '@heroicons/react/24/outline';
import { useState, useEffect } from 'react';
import logo from '../assets/gestalyze-logo.svg';

function Header({ onAboutClick }) {
  const { t, i18n } = useTranslation();
  const [selectedLanguage, setSelectedLanguage] = useState(localStorage.getItem('language') || 'en');
  const [showMenu, setShowMenu] = useState(false);

  useEffect(() => {
    i18n.changeLanguage(selectedLanguage);
  }, [selectedLanguage, i18n]);

  const changeLanguage = (lng) => {
    setSelectedLanguage(lng);
    localStorage.setItem('language', lng);
  };

  const toggleMenu = () => {
    setShowMenu(!showMenu);
  };

  return (
    <header className="w-full bg-[#1B263B] text-white p-4 border-b border-blue-800 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center">
          <img src={logo} alt={t('header.logoAlt')} className="h-8 w-auto mr-2 filter brightness-0 invert" />
          <h1 className="text-xl tracking-[.2em]">{t('header.title')}</h1>
        </div>
        <div className="flex items-center relative">
          <GlobeAltIcon className="h-6 w-6 text-white mr-2" title={t('header.languageSelector')} />
          <select value={selectedLanguage} onChange={(e) => changeLanguage(e.target.value)} className="bg-gray-800 text-white border border-gray-600 rounded p-1 mr-2">
            <option value="en">{t('header.en')}</option>
            <option value="es">{t('header.es')}</option>
          </select>
          <div className="relative">
            <Bars3Icon className="h-8 w-8 cursor-pointer" onClick={toggleMenu} title={t('header.menu')} />
            {showMenu && (
              <div className="absolute top-full right-0 bg-gray-700 text-white mt-2 rounded shadow-lg z-50 w-48">
                <button onClick={onAboutClick} className="block px-4 py-2 hover:bg-gray-600 w-full text-left">
                  {t('about.title')}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;

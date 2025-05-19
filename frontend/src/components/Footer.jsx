import { useTranslation } from 'react-i18next';
import { GithubIcon, ScaleIcon } from 'lucide-react';

function Footer({ onAboutClick, onPrivacyClick }) {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full bg-gray-800 text-white p-4 mt-auto">
      <div className="container mx-auto flex flex-col md:flex-row justify-between items-center">
        <div className="text-sm text-gray-400 mb-4 md:mb-0">
          © {currentYear} {t('footer.author')} - {t('footer.licensedUnder')}{' '}
          <a
            href="https://www.apache.org/licenses/LICENSE-2.0"
            target="_blank"
            rel="noopener noreferrer"
            className="text-gray-300 hover:text-white transition-colors underline"
          >
            {t('footer.apacheLicense')}
          </a>
          <ScaleIcon className="h-4 w-4 inline ml-1 text-gray-300" />
        </div>
        <div className="flex space-x-4 items-center">
          <a
            href="https://github.com/rbcorrales/gestalyze"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center text-gray-300 hover:text-white transition-colors underline"
          >
            <GithubIcon className="h-5 w-5 mr-1" />
            {t('footer.fork')}
          </a>
          <button 
            onClick={onAboutClick}
            className="text-gray-300 hover:text-white transition-colors underline"
          >
            {t('about.title')}
          </button>
          <button 
            onClick={onPrivacyClick}
            className="text-gray-300 hover:text-white transition-colors underline"
          >
            {t('footer.privacyPolicy')}
          </button>
        </div>
      </div>
    </footer>
  );
}

export default Footer; 
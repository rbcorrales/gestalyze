import { useTranslation } from 'react-i18next';
import { ScaleIcon } from 'lucide-react';
import { siGithub } from 'simple-icons/icons';
import { Link } from 'react-router-dom';

function Footer() {
  const { t } = useTranslation();
  const currentYear = new Date().getFullYear();
  return (
    <footer className="bg-gray-800 py-8 text-white" role="contentinfo">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center justify-between md:flex-row">
          <div className="mb-4 text-sm text-gray-400 md:mb-0">
            <span>{t('footer.copy', { year: currentYear })}</span>
            <span aria-hidden="true"> &mdash; </span>
            <span>{t('footer.builtWith')}</span>
            &nbsp;
            <a
              href="https://www.apache.org/licenses/LICENSE-2.0"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded text-gray-300 underline transition-colors hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
              aria-label={t('footer.apacheLicense')}
            >
              {t('footer.apacheLicense')}
            </a>
            <ScaleIcon className="ml-1 inline h-4 w-4 text-gray-300" aria-hidden="true" />
          </div>
          <div className="flex items-center space-x-4">
            <Link
              to="/privacy"
              className="rounded text-gray-300 underline transition-colors hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
              aria-label={t('footer.privacyPolicy')}
            >
              {t('footer.privacyPolicy')}
            </Link>
            <a
              href="https://github.com/rbcorrales/gestalyze"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center rounded text-gray-300 underline transition-colors hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
              aria-label={t('footer.fork')}
            >
              <svg
                className="mr-1 h-5 w-5"
                viewBox="0 0 24 24"
                fill="currentColor"
                aria-hidden="true"
                focusable="false"
              >
                <path d={siGithub.path} />
              </svg>
              {t('footer.fork')}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;

import { useTranslation } from 'react-i18next';
import { X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

function PrivacyPolicy() {
  const { t } = useTranslation();
  const navigate = useNavigate();

  const close = () => {
    navigate('/');
  };

  // Prevent overlay click from closing when clicking inside modal
  const stopPropagation = (e) => e.stopPropagation();

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
      onClick={close}
    >
      <div
        className="relative max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800"
        onClick={stopPropagation}
      >
        <button
          onClick={close}
          className="absolute right-4 top-4 rounded-full p-1 text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-700"
          aria-label={t('about.close')}
        >
          <X className="h-6 w-6" />
        </button>

        <h1 className="mb-6 text-2xl font-bold text-gray-900 dark:text-white">
          {t('privacy.title', 'Privacy Policy')}
        </h1>

        <div className="space-y-6 text-gray-600 dark:text-gray-300">
          <p>{t('privacy.introduction')}</p>

          <section>
            <h2 className="mb-2 text-xl font-semibold text-gray-900 dark:text-white">
              {t('privacy.dataCollection')}
            </h2>
            <p>{t('privacy.dataCollectionText')}</p>
          </section>

          <section>
            <h2 className="mb-2 text-xl font-semibold text-gray-900 dark:text-white">
              {t('privacy.dataUsage')}
            </h2>
            <p>{t('privacy.dataUsageText')}</p>
          </section>

          <section>
            <h2 className="mb-2 text-xl font-semibold text-gray-900 dark:text-white">
              {t('privacy.dataProtection')}
            </h2>
            <p>{t('privacy.dataProtectionText')}</p>
          </section>
        </div>
      </div>
    </div>
  );
}

export default PrivacyPolicy;

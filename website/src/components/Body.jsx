import { useTranslation } from 'react-i18next';

function Body() {
  const { t } = useTranslation();

  function Hero() {
    return (
      <section className="hero-gradient pb-16 pt-32" aria-labelledby="hero-title">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <h1
              id="hero-title"
              className="mb-6 text-4xl font-bold text-gray-900 text-primary dark:text-primary md:text-5xl"
            >
              {t('hero.title')}
            </h1>
            <p className="mb-8 text-xl text-gray-600 dark:text-gray-300">{t('hero.subtitle')}</p>
            <div className="flex flex-col justify-center gap-4 sm:flex-row">
              <a
                href="https://github.com/rbcorrales/gestalyze"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-primary focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                aria-label={t('hero.cta')}
              >
                {t('hero.cta')}
              </a>
              <a
                href="#features"
                className="btn-secondary focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                aria-label={t('hero.learnMore')}
              >
                {t('hero.learnMore')}
              </a>
            </div>
          </div>
        </div>
      </section>
    );
  }

  function Features() {
    const features = [
      { key: 'realTime', icon: '⚡' },
      { key: 'handCharacteristics', icon: '✋' },
      { key: 'signLanguage', icon: '👋' },
      { key: 'privacy', icon: '🔒' },
    ];
    return (
      <section id="features" className="section-bg py-16" aria-labelledby="features-title">
        <div className="container mx-auto px-4">
          <h2 id="features-title" className="section-title text-center">
            {t('features.title')}
          </h2>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4" role="list">
            {features.map((feature) => (
              <div key={feature.key} className="card text-center" role="listitem">
                <div className="mb-4 text-4xl" aria-hidden="true">
                  {feature.icon}
                </div>
                <h3 className="mb-2 text-xl font-semibold dark:text-white">
                  {t(`features.${feature.key}.title`)}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {t(`features.${feature.key}.description`)}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  function Integrations() {
    const integrations = [
      { key: 'homeAssistant', icon: '🏠' },
      { key: 'mqtt', icon: '🔌' },
      { key: 'development', icon: '⚙️' },
    ];
    return (
      <section className="section-bg-alt py-16" aria-labelledby="integrations-title">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 id="integrations-title" className="section-title">
              {t('integrations.title')}
            </h2>
            <p className="mx-auto max-w-3xl text-xl text-gray-600 dark:text-gray-300">
              {t('integrations.subtitle')}
            </p>
          </div>
          <div className="mx-auto grid max-w-6xl gap-8 md:grid-cols-2 lg:grid-cols-3" role="list">
            {integrations.map((integration) => (
              <div key={integration.key} className="card" role="listitem">
                <div className="mb-4 text-4xl" aria-hidden="true">
                  {integration.icon}
                </div>
                <h3 className="mb-4 text-xl font-semibold dark:text-white">
                  {t(`integrations.${integration.key}.title`)}
                </h3>
                <p className="mb-6 text-gray-600 dark:text-gray-300">
                  {t(`integrations.${integration.key}.description`)}
                </p>
                <ul className="space-y-2" role="list">
                  {t(`integrations.${integration.key}.features`, { returnObjects: true }).map(
                    (feature, index) => (
                      <li
                        key={index}
                        className="flex items-start text-gray-700 dark:text-gray-200"
                        role="listitem"
                      >
                        <svg
                          className="mr-2 mt-1 h-5 w-5 flex-shrink-0 text-blue-500"
                          style={{ minWidth: '20px', minHeight: '20px' }}
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          aria-hidden="true"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                        <span>{feature}</span>
                      </li>
                    )
                  )}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  function UseCases() {
    const useCases = [
      { key: 'accessibility', icon: '♿' },
      { key: 'smartHome', icon: '🏡' },
      { key: 'education', icon: '📚' },
      { key: 'gaming', icon: '🎮' },
    ];
    return (
      <section className="section-bg py-16" aria-labelledby="use-cases-title">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 id="use-cases-title" className="section-title">
              {t('useCases.title')}
            </h2>
            <p className="mx-auto max-w-3xl text-xl text-gray-600 dark:text-gray-300">
              {t('useCases.subtitle')}
            </p>
          </div>
          <div className="mx-auto grid max-w-6xl gap-8 md:grid-cols-2 lg:grid-cols-4" role="list">
            {useCases.map((useCase) => (
              <div key={useCase.key} className="card text-center" role="listitem">
                <div className="mb-4 text-4xl" aria-hidden="true">
                  {useCase.icon}
                </div>
                <h3 className="mb-3 text-xl font-semibold dark:text-white">
                  {t(`useCases.${useCase.key}.title`)}
                </h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {t(`useCases.${useCase.key}.description`)}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  function TechnicalDetails() {
    return (
      <section className="section-bg-alt py-16" aria-labelledby="technical-title">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 id="technical-title" className="section-title">
              {t('technical.title')}
            </h2>
            <p className="mx-auto max-w-3xl text-xl text-gray-600 dark:text-gray-300">
              {t('technical.subtitle')}
            </p>
          </div>
          <div className="mx-auto grid max-w-6xl gap-8 md:grid-cols-2 lg:grid-cols-4" role="list">
            {t('technical.details', { returnObjects: true }).map((detail, index) => (
              <div key={index} className="card" role="listitem">
                <h3 className="mb-3 text-xl font-semibold dark:text-white">{detail.title}</h3>
                <p className="text-gray-600 dark:text-gray-300">{detail.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    );
  }

  function ProjectStatus() {
    return (
      <section
        className="border-t border-yellow-200 bg-yellow-50 py-12 dark:border-yellow-900 dark:bg-yellow-950"
        aria-labelledby="project-status-title"
      >
        <div className="container mx-auto px-4 text-center">
          <h2
            id="project-status-title"
            className="mb-2 text-2xl font-semibold text-yellow-800 dark:text-yellow-200"
          >
            {t('projectStatus.title')}
          </h2>
          <p className="mx-auto mb-2 max-w-2xl text-lg text-yellow-700 dark:text-yellow-100">
            {t('projectStatus.description')}
          </p>
          <a
            href="https://github.com/rbcorrales/gestalyze-dev?tab=readme-ov-file#-roadmap--todo"
            target="_blank"
            rel="noopener noreferrer"
            className="primary-link text-base focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            aria-label={t('projectStatus.roadmap')}
          >
            {t('projectStatus.roadmap')}
          </a>
        </div>
      </section>
    );
  }

  return (
    <main id="main-content" className="flex-grow" role="main">
      <Hero />
      <Features />
      <Integrations />
      <UseCases />
      <TechnicalDetails />
      <ProjectStatus />
    </main>
  );
}

export default Body;

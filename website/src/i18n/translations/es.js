export const es = {
  header: {
    title: 'Gestalyze',
    subtitle: 'Análisis Inteligente de Gestos',
    language: 'Idioma',
    logoAlt: 'Logo de Gestalyze',
    en: 'English',
    es: 'Español',
    menu: 'Menú',
    darkMode: 'Modo Oscuro',
    lightMode: 'Modo Claro',
    switchToDark: 'Cambiar a modo oscuro',
    switchToLight: 'Cambiar a modo claro',
  },
  hero: {
    title: 'Análisis Inteligente de Gestos',
    subtitle: 'Reconocimiento y análisis de gestos en tiempo real usando visión por computadora',
    cta: 'Pruébalo Ahora',
    learnMore: 'Conoce Más',
  },
  features: {
    title: 'Características',
    realTime: {
      title: 'Análisis en Tiempo Real',
      description: 'Procesa gestos manuales en tiempo real usando la cámara de tus dispositivos',
    },
    handCharacteristics: {
      title: 'Características de la Mano',
      description:
        'Detecta dedos extendidos, la orientación de la mano y otras características para un análisis versátil de gestos.',
    },
    signLanguage: {
      title: 'Reconocimiento de Lenguaje de Señas',
      description: 'ASL actualmente soportado, extendible a otros lenguajes de señas.',
    },
    privacy: {
      title: 'Privacidad Primero',
      description:
        'Todo el procesamiento ocurre localmente en tus dispositivos. No se envían datos a servidores externos.',
    },
  },
  integrations: {
    title: 'Integraciones',
    subtitle: 'Conéctate con plataformas de hogar inteligente y crea integraciones personalizadas',
    homeAssistant: {
      title: 'Home Assistant',
      description:
        'Controla tus dispositivos de hogar inteligente usando gestos a través de nuestra integración oficial con Home Assistant. Crea automatizaciones personalizadas y controla toda tu casa con simples movimientos de mano.',
      features: [
        'Reconocimiento de gestos en tiempo real',
        'Creación de automatizaciones personalizadas',
        'Control de dispositivos mediante gestos',
        'Procesamiento seguro local',
      ],
    },
    mqtt: {
      title: 'Integración MQTT',
      description:
        'Integra Gestalyze con cualquier sistema compatible con MQTT. Nuestro middleware permite la transmisión de datos de gestos en tiempo real, facilitando la conexión con aplicaciones personalizadas, dispositivos IoT u otras plataformas de hogar inteligente.',
      features: [
        'Transmisión de datos de gestos en tiempo real',
        'Autenticación segura',
        'Suscripciones a temas personalizados',
        'Fácil integración con cualquier cliente MQTT',
      ],
    },
    development: {
      title: 'Características para Desarrolladores',
      description:
        'Gestalyze está construido pensando en la extensibilidad. La arquitectura modular permite a los desarrolladores crear integraciones personalizadas, entrenar nuevos modelos de gestos o extender las capacidades del sistema.',
      features: [
        'Código abierto bajo Licencia Apache 2.0',
        'Entrenamiento de modelos de gestos personalizados',
        'Arquitectura modular',
        'Documentación completa',
      ],
    },
  },
  useCases: {
    title: 'Casos de Uso',
    subtitle: 'Descubre cómo Gestalyze puede mejorar tu vida diaria',
    accessibility: {
      title: 'Accesibilidad',
      description:
        'Haz que la tecnología sea más accesible controlando dispositivos a través de gestos naturales. Perfecto para usuarios con desafíos de movilidad o aquellos que prefieren interacción sin contacto.',
    },
    smartHome: {
      title: 'Hogar Inteligente',
      description:
        'Controla tus dispositivos de hogar inteligente sin tocar ningún botón. Enciende/apaga luces, ajusta termostatos o activa escenas con simples movimientos de mano.',
    },
    education: {
      title: 'Educación',
      description:
        'Aprende lenguaje de señas con retroalimentación en tiempo real. Perfecto para estudiantes, profesores y cualquier persona interesada en aprender lenguaje de señas.',
    },
    gaming: {
      title: 'Gaming',
      description:
        'Mejora tu experiencia de juego con controles por gestos. Crea comandos de gestos personalizados para tus juegos favoritos y juega de una manera completamente nueva.',
    },
  },
  technical: {
    title: 'Detalles Técnicos',
    subtitle: 'Construido con tecnología moderna para un rendimiento óptimo',
    details: [
      {
        title: 'Procesamiento Local',
        description:
          'Todo el procesamiento ocurre en tu dispositivo, garantizando privacidad y reduciendo la latencia. No se envían datos a servidores externos.',
      },
      {
        title: 'Código Abierto',
        description:
          'Gestalyze es de código abierto y está disponible bajo la Licencia Apache 2.0. Contribuye al proyecto o personalízalo según tus necesidades.',
      },
      {
        title: 'Multiplataforma',
        description:
          'Funciona en Windows, macOS y Linux. Fácil de configurar y usar con dependencias mínimas.',
      },
      {
        title: 'Personalizable',
        description:
          'Entrena gestos personalizados o modifica los existentes para adaptarlos a tus necesidades específicas. La arquitectura modular facilita su extensión.',
      },
    ],
  },
  footer: {
    copy: '© {{year}} Gestalyze',
    fork: 'Fork en GitHub',
    apacheLicense: 'Licencia Apache 2.0',
    builtWith: 'Construido con ❤️ y licenciado bajo la',
    privacyPolicy: 'Política de Privacidad',
  },
  projectStatus: {
    title: 'Estado del Proyecto',
    description:
      'Gestalyze está en desarrollo activo. Algunas funciones pueden no funcionar como se espera todavía, pero estamos trabajando para mejorar la estabilidad y añadir nuevas capacidades. ¡Gracias por tu interés y apoyo!',
    roadmap: 'Consulta nuestra hoja de ruta para ver las próximas funciones y mejoras.',
  },
  privacy: {
    title: 'Política de Privacidad',
    introduction:
      'Esta Política de Privacidad describe cómo Gestalyze recopila, utiliza y protege su información personal.',
    dataCollection: 'Recopilación de Datos',
    dataCollectionText:
      'Gestalyze procesa datos de video de su cámara en tiempo real para detectar gestos manuales. No se almacenan ni transmiten datos a servidores externos.',
    dataUsage: 'Uso de Datos',
    dataUsageText:
      'Los datos de video se procesan localmente en su dispositivo para proporcionar funcionalidad de reconocimiento de gestos. Todo el procesamiento ocurre en tiempo real y no se guardan datos.',
    dataProtection: 'Protección de Datos',
    dataProtectionText:
      'Su privacidad es importante para nosotros. Gestalyze no almacena, comparte ni transmite ningún dato personal. Todo el procesamiento se realiza localmente en su dispositivo.',
  },
};

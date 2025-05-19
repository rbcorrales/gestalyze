const CONFIG = {
  WEBSOCKET_URL: process.env.NODE_ENV === 'production' 
    ? `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws`
    : 'ws://localhost:8000/ws', // Development URL

  DEFAULT_LANGUAGE: 'es', // Default language
  SUPPORTED_LANGUAGES: ['es', 'en'], // Extendable list of supported languages

  DEFAULT_CAMERA_UPDATE_INTERVAL: 300, // Default interval for sending camera frames in milliseconds
  MIN_CAMERA_UPDATE_INTERVAL: 50, // Minimum allowed value
  MAX_CAMERA_UPDATE_INTERVAL: 2000, // Maximum allowed value
  CAMERA_UPDATE_INTERVAL_STEP: 10, // Step for increasing/decreasing the interval

  ASL: {
    ENABLED: false, // Whether ASL recognition is enabled by default
    MODEL_TYPE: 'custom', // 'custom' or 'online'
    AVAILABLE_MODELS: [
      { id: 'custom', name: 'Custom Model' },
      { id: 'online', name: 'Online Model' }
    ]
  },

  // Add more configuration parameters as needed
};

export default CONFIG;

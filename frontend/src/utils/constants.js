export const WS_URL = import.meta.env.PROD 
  ? `ws://${window.location.host}/ws`
  : 'ws://localhost:8000/ws';

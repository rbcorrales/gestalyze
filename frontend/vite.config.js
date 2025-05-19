import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
      }
    },
    watch: {
      usePolling: true,
    },
  },
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  }
});

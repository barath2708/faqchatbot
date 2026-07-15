import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    allowedHosts: ['.app.github.dev'],
    proxy: {
      '/question': 'http://localhost:8000',
      '/admin': 'http://localhost:8000',
      '/sources': 'http://localhost:8000',
    },
  },
})
// vite.config.mts
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import { fileURLToPath } from 'url';
import { VitePWA } from 'vite-plugin-pwa';
import { visualizer } from 'rollup-plugin-visualizer';
import viteCompression from 'vite-plugin-compression';

// Converte import.meta.url em __dirname
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuração ESM completa
export default defineConfig(async () => {
  const glsl = (await import('vite-plugin-glsl')).default;

  return {
    plugins: [
      vue({
        template: {
          compilerOptions: {
            isCustomElement: (tag) => tag.includes('model-viewer'),
          },
        },
      }),
      VitePWA({
        registerType: 'autoUpdate',
        includeAssets: [
          '**/*.{glb,gltf,woff2,png,svg,ico}',
          'assets/models/**/*',
          'assets/shaders/**/*',
        ],
        manifest: {
          name: 'S.U.M - Sistema Unificado de Mapeamento',
          short_name: 'S.U.M',
          theme_color: '#6366f1',
          background_color: '#0f172a',
          display: 'standalone',
          description: 'Plataforma educacional para mapeamento inteligente de salas de aula',
          orientation: 'portrait',
          icons: [
            { src: '/pwa-192x192.png', sizes: '192x192', type: 'image/png', purpose: 'any maskable' },
            { src: '/pwa-512x512.png', sizes: '512x512', type: 'image/png', purpose: 'any maskable' },
            { src: '/pwa-maskable.png', sizes: '1024x1024', type: 'image/png', purpose: 'maskable' },
          ],
          screenshots: [
            { src: '/screenshots/dashboard-3d.png', sizes: '1280x720', type: 'image/png', label: 'Dashboard 3D Interativo' },
          ],
          categories: ['education', 'productivity'],
          shortcuts: [
            { name: 'Mapa da Sala', short_name: 'Mapa', description: 'Visualização 3D do mapeamento', url: '/classroom-map', icons: [{ src: '/icons/map-icon.png', sizes: '96x96' }] },
            { name: 'Dots - Perfil', short_name: 'Perfil', description: 'Seu perfil educacional completo', url: '/profile', icons: [{ src: '/icons/profile-icon.png', sizes: '96x96' }] },
          ],
        },
        workbox: {
          maximumFileSizeToCacheInBytes: 5000000,
          navigateFallback: '/index.html',
          navigateFallbackDenylist: [/^\/api\//, /^\/static\//],
          runtimeCaching: [
            {
              urlPattern: /\.(glb|gltf)$/,
              handler: 'CacheFirst',
              options: {
                cacheName: '3d-models-cache',
                expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 24 * 30 },
              },
            },
            {
              urlPattern: /\/api\/.*/,
              handler: 'NetworkFirst',
              options: {
                cacheName: 'api-cache',
                networkTimeoutSeconds: 10,
                expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 2 },
                backgroundSync: { name: 'api-queue', options: { maxRetentionTime: 60 * 60 } },
              },
            },
          ],
          skipWaiting: true,
          clientsClaim: true,
        },
        devOptions: { enabled: true, type: 'module', navigateFallback: 'index.html' },
      }),
      glsl(),
      visualizer({ open: false, filename: 'bundle-stats.html' }),
      viteCompression({ algorithm: 'brotliCompress', threshold: 10240, ext: '.br' }),
    ],
    resolve: {
      alias: {
        // Alias principal - cobre tudo em src/
        '@': path.resolve(__dirname, 'src'),
        
        // Aliases específicos para melhor organização
        '@components': path.resolve(__dirname, 'src/components'),
        '@views': path.resolve(__dirname, 'src/views'),
        '@store': path.resolve(__dirname, 'src/store'),
        '@services': path.resolve(__dirname, 'src/services'),
        '@composables': path.resolve(__dirname, 'src/composables'),
        '@types': path.resolve(__dirname, 'src/types'),
        '@assets': path.resolve(__dirname, 'src/assets'),
        '@models': path.resolve(__dirname, 'src/assets/models'),
        '@shaders': path.resolve(__dirname, 'src/shaders'),
  // Shared components live under src/shared (some files import as @shared or @/shared)
  '@shared': path.resolve(__dirname, 'src/shared'),
  // Support imports that use the @/shared/ prefix
  '@/shared': path.resolve(__dirname, 'src/shared'),
      },
    },
    build: {
      target: 'esnext',
      minify: 'terser',
      terserOptions: { 
        compress: { 
          drop_console: true, 
          drop_debugger: true 
        } 
      },
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes('node_modules')) {
              if (id.includes('three') || id.includes('gltf')) return 'three';
              if (id.includes('vue')) return 'vue';
              if (id.includes('chart')) return 'charts';
              return 'vendor';
            }
          },
        },
      },
      chunkSizeWarningLimit: 1000,
    },
    optimizeDeps: {
      include: [
        'three', 
        'troisjs', 
        '@google/model-viewer', 
        'chart.js',
        'vue',
        'vue-router',
        'pinia',
        'axios'
      ],
      // Removido o exclude que estava causando conflito
    },
    server: {
      port: 5173,
      host: '0.0.0.0',
      proxy: {
        '/api': { 
          target: 'http://backend:8000', 
          changeOrigin: true,
          secure: false
        },
        '/ws': { 
          target: 'ws://backend:8000', 
          ws: true 
        },
      },
    },
  };
});
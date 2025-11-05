// vite.config.mts
import { defineConfig } from "file:///app/node_modules/vite/dist/node/index.js";
import vue from "file:///app/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import path from "path";
import { fileURLToPath } from "url";
import { VitePWA } from "file:///app/node_modules/vite-plugin-pwa/dist/index.js";
import { visualizer } from "file:///app/node_modules/rollup-plugin-visualizer/dist/plugin/index.js";
import viteCompression from "file:///app/node_modules/vite-plugin-compression/dist/index.mjs";
var __vite_injected_original_import_meta_url = "file:///app/vite.config.mts";
var __filename = fileURLToPath(__vite_injected_original_import_meta_url);
var __dirname = path.dirname(__filename);
var vite_config_default = defineConfig(async () => {
  const glsl = (await import("file:///app/node_modules/vite-plugin-glsl/src/index.js")).default;
  return {
    plugins: [
      vue({
        template: {
          compilerOptions: {
            isCustomElement: (tag) => tag.includes("model-viewer")
          }
        }
      }),
      VitePWA({
        registerType: "autoUpdate",
        includeAssets: [
          "**/*.{glb,gltf,woff2,png,svg,ico}",
          "assets/models/**/*",
          "assets/shaders/**/*"
        ],
        manifest: {
          name: "S.U.M - Sistema Unificado de Mapeamento",
          short_name: "S.U.M",
          theme_color: "#6366f1",
          background_color: "#0f172a",
          display: "standalone",
          description: "Plataforma educacional para mapeamento inteligente de salas de aula",
          orientation: "portrait",
          icons: [
            { src: "/pwa-192x192.png", sizes: "192x192", type: "image/png", purpose: "any maskable" },
            { src: "/pwa-512x512.png", sizes: "512x512", type: "image/png", purpose: "any maskable" },
            { src: "/pwa-maskable.png", sizes: "1024x1024", type: "image/png", purpose: "maskable" }
          ],
          screenshots: [
            { src: "/screenshots/dashboard-3d.png", sizes: "1280x720", type: "image/png", label: "Dashboard 3D Interativo" }
          ],
          categories: ["education", "productivity"],
          shortcuts: [
            { name: "Mapa da Sala", short_name: "Mapa", description: "Visualiza\xE7\xE3o 3D do mapeamento", url: "/classroom-map", icons: [{ src: "/icons/map-icon.png", sizes: "96x96" }] },
            { name: "Dots - Perfil", short_name: "Perfil", description: "Seu perfil educacional completo", url: "/profile", icons: [{ src: "/icons/profile-icon.png", sizes: "96x96" }] }
          ]
        },
        workbox: {
          maximumFileSizeToCacheInBytes: 5e6,
          navigateFallback: "/index.html",
          navigateFallbackDenylist: [/^\/api\//, /^\/static\//],
          runtimeCaching: [
            {
              urlPattern: /\.(glb|gltf)$/,
              handler: "CacheFirst",
              options: {
                cacheName: "3d-models-cache",
                expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 24 * 30 }
              }
            },
            {
              urlPattern: /\/api\/.*/,
              handler: "NetworkFirst",
              options: {
                cacheName: "api-cache",
                networkTimeoutSeconds: 10,
                expiration: { maxEntries: 50, maxAgeSeconds: 60 * 60 * 2 },
                backgroundSync: { name: "api-queue", options: { maxRetentionTime: 60 * 60 } }
              }
            }
          ],
          skipWaiting: true,
          clientsClaim: true
        },
        devOptions: { enabled: true, type: "module", navigateFallback: "index.html" }
      }),
      glsl(),
      visualizer({ open: false, filename: "bundle-stats.html" }),
      viteCompression({ algorithm: "brotliCompress", threshold: 10240, ext: ".br" })
    ],
    resolve: {
      alias: {
        // Alias principal - cobre tudo em src/
        "@": path.resolve(__dirname, "src"),
        // Aliases específicos para melhor organização
        "@components": path.resolve(__dirname, "src/components"),
        "@views": path.resolve(__dirname, "src/views"),
        "@store": path.resolve(__dirname, "src/store"),
        "@services": path.resolve(__dirname, "src/services"),
        "@composables": path.resolve(__dirname, "src/composables"),
        "@types": path.resolve(__dirname, "src/types"),
        "@assets": path.resolve(__dirname, "src/assets"),
        "@models": path.resolve(__dirname, "src/assets/models"),
        "@shaders": path.resolve(__dirname, "src/shaders"),
        // Shared components live under src/shared (some files import as @shared or @/shared)
        "@shared": path.resolve(__dirname, "src/shared"),
        // Support imports that use the @/shared/ prefix
        "@/shared": path.resolve(__dirname, "src/shared")
      }
    },
    build: {
      target: "esnext",
      minify: "terser",
      terserOptions: {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      },
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (id.includes("node_modules")) {
              if (id.includes("three") || id.includes("gltf"))
                return "three";
              if (id.includes("vue"))
                return "vue";
              if (id.includes("chart"))
                return "charts";
              return "vendor";
            }
          }
        }
      },
      chunkSizeWarningLimit: 1e3
    },
    optimizeDeps: {
      include: [
        "three",
        "troisjs",
        "@google/model-viewer",
        "chart.js",
        "vue",
        "vue-router",
        "pinia",
        "axios"
      ]
      // Removido o exclude que estava causando conflito
    },
    server: {
      port: 5173,
      host: "0.0.0.0",
      proxy: {
        "/api": {
          target: "http://backend:8000",
          changeOrigin: true,
          secure: false
        },
        "/ws": {
          target: "ws://backend:8000",
          ws: true
        }
      }
    }
  };
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcubXRzIl0sCiAgInNvdXJjZXNDb250ZW50IjogWyJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiL2FwcFwiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiL2FwcC92aXRlLmNvbmZpZy5tdHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL2FwcC92aXRlLmNvbmZpZy5tdHNcIjsvLyB2aXRlLmNvbmZpZy5tdHNcbmltcG9ydCB7IGRlZmluZUNvbmZpZyB9IGZyb20gJ3ZpdGUnO1xuaW1wb3J0IHZ1ZSBmcm9tICdAdml0ZWpzL3BsdWdpbi12dWUnO1xuaW1wb3J0IHBhdGggZnJvbSAncGF0aCc7XG5pbXBvcnQgeyBmaWxlVVJMVG9QYXRoIH0gZnJvbSAndXJsJztcbmltcG9ydCB7IFZpdGVQV0EgfSBmcm9tICd2aXRlLXBsdWdpbi1wd2EnO1xuaW1wb3J0IHsgdmlzdWFsaXplciB9IGZyb20gJ3JvbGx1cC1wbHVnaW4tdmlzdWFsaXplcic7XG5pbXBvcnQgdml0ZUNvbXByZXNzaW9uIGZyb20gJ3ZpdGUtcGx1Z2luLWNvbXByZXNzaW9uJztcblxuLy8gQ29udmVydGUgaW1wb3J0Lm1ldGEudXJsIGVtIF9fZGlybmFtZVxuY29uc3QgX19maWxlbmFtZSA9IGZpbGVVUkxUb1BhdGgoaW1wb3J0Lm1ldGEudXJsKTtcbmNvbnN0IF9fZGlybmFtZSA9IHBhdGguZGlybmFtZShfX2ZpbGVuYW1lKTtcblxuLy8gQ29uZmlndXJhXHUwMEU3XHUwMEUzbyBFU00gY29tcGxldGFcbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyhhc3luYyAoKSA9PiB7XG4gIGNvbnN0IGdsc2wgPSAoYXdhaXQgaW1wb3J0KCd2aXRlLXBsdWdpbi1nbHNsJykpLmRlZmF1bHQ7XG5cbiAgcmV0dXJuIHtcbiAgICBwbHVnaW5zOiBbXG4gICAgICB2dWUoe1xuICAgICAgICB0ZW1wbGF0ZToge1xuICAgICAgICAgIGNvbXBpbGVyT3B0aW9uczoge1xuICAgICAgICAgICAgaXNDdXN0b21FbGVtZW50OiAodGFnKSA9PiB0YWcuaW5jbHVkZXMoJ21vZGVsLXZpZXdlcicpLFxuICAgICAgICAgIH0sXG4gICAgICAgIH0sXG4gICAgICB9KSxcbiAgICAgIFZpdGVQV0Eoe1xuICAgICAgICByZWdpc3RlclR5cGU6ICdhdXRvVXBkYXRlJyxcbiAgICAgICAgaW5jbHVkZUFzc2V0czogW1xuICAgICAgICAgICcqKi8qLntnbGIsZ2x0Zix3b2ZmMixwbmcsc3ZnLGljb30nLFxuICAgICAgICAgICdhc3NldHMvbW9kZWxzLyoqLyonLFxuICAgICAgICAgICdhc3NldHMvc2hhZGVycy8qKi8qJyxcbiAgICAgICAgXSxcbiAgICAgICAgbWFuaWZlc3Q6IHtcbiAgICAgICAgICBuYW1lOiAnUy5VLk0gLSBTaXN0ZW1hIFVuaWZpY2FkbyBkZSBNYXBlYW1lbnRvJyxcbiAgICAgICAgICBzaG9ydF9uYW1lOiAnUy5VLk0nLFxuICAgICAgICAgIHRoZW1lX2NvbG9yOiAnIzYzNjZmMScsXG4gICAgICAgICAgYmFja2dyb3VuZF9jb2xvcjogJyMwZjE3MmEnLFxuICAgICAgICAgIGRpc3BsYXk6ICdzdGFuZGFsb25lJyxcbiAgICAgICAgICBkZXNjcmlwdGlvbjogJ1BsYXRhZm9ybWEgZWR1Y2FjaW9uYWwgcGFyYSBtYXBlYW1lbnRvIGludGVsaWdlbnRlIGRlIHNhbGFzIGRlIGF1bGEnLFxuICAgICAgICAgIG9yaWVudGF0aW9uOiAncG9ydHJhaXQnLFxuICAgICAgICAgIGljb25zOiBbXG4gICAgICAgICAgICB7IHNyYzogJy9wd2EtMTkyeDE5Mi5wbmcnLCBzaXplczogJzE5MngxOTInLCB0eXBlOiAnaW1hZ2UvcG5nJywgcHVycG9zZTogJ2FueSBtYXNrYWJsZScgfSxcbiAgICAgICAgICAgIHsgc3JjOiAnL3B3YS01MTJ4NTEyLnBuZycsIHNpemVzOiAnNTEyeDUxMicsIHR5cGU6ICdpbWFnZS9wbmcnLCBwdXJwb3NlOiAnYW55IG1hc2thYmxlJyB9LFxuICAgICAgICAgICAgeyBzcmM6ICcvcHdhLW1hc2thYmxlLnBuZycsIHNpemVzOiAnMTAyNHgxMDI0JywgdHlwZTogJ2ltYWdlL3BuZycsIHB1cnBvc2U6ICdtYXNrYWJsZScgfSxcbiAgICAgICAgICBdLFxuICAgICAgICAgIHNjcmVlbnNob3RzOiBbXG4gICAgICAgICAgICB7IHNyYzogJy9zY3JlZW5zaG90cy9kYXNoYm9hcmQtM2QucG5nJywgc2l6ZXM6ICcxMjgweDcyMCcsIHR5cGU6ICdpbWFnZS9wbmcnLCBsYWJlbDogJ0Rhc2hib2FyZCAzRCBJbnRlcmF0aXZvJyB9LFxuICAgICAgICAgIF0sXG4gICAgICAgICAgY2F0ZWdvcmllczogWydlZHVjYXRpb24nLCAncHJvZHVjdGl2aXR5J10sXG4gICAgICAgICAgc2hvcnRjdXRzOiBbXG4gICAgICAgICAgICB7IG5hbWU6ICdNYXBhIGRhIFNhbGEnLCBzaG9ydF9uYW1lOiAnTWFwYScsIGRlc2NyaXB0aW9uOiAnVmlzdWFsaXphXHUwMEU3XHUwMEUzbyAzRCBkbyBtYXBlYW1lbnRvJywgdXJsOiAnL2NsYXNzcm9vbS1tYXAnLCBpY29uczogW3sgc3JjOiAnL2ljb25zL21hcC1pY29uLnBuZycsIHNpemVzOiAnOTZ4OTYnIH1dIH0sXG4gICAgICAgICAgICB7IG5hbWU6ICdEb3RzIC0gUGVyZmlsJywgc2hvcnRfbmFtZTogJ1BlcmZpbCcsIGRlc2NyaXB0aW9uOiAnU2V1IHBlcmZpbCBlZHVjYWNpb25hbCBjb21wbGV0bycsIHVybDogJy9wcm9maWxlJywgaWNvbnM6IFt7IHNyYzogJy9pY29ucy9wcm9maWxlLWljb24ucG5nJywgc2l6ZXM6ICc5Nng5NicgfV0gfSxcbiAgICAgICAgICBdLFxuICAgICAgICB9LFxuICAgICAgICB3b3JrYm94OiB7XG4gICAgICAgICAgbWF4aW11bUZpbGVTaXplVG9DYWNoZUluQnl0ZXM6IDUwMDAwMDAsXG4gICAgICAgICAgbmF2aWdhdGVGYWxsYmFjazogJy9pbmRleC5odG1sJyxcbiAgICAgICAgICBuYXZpZ2F0ZUZhbGxiYWNrRGVueWxpc3Q6IFsvXlxcL2FwaVxcLy8sIC9eXFwvc3RhdGljXFwvL10sXG4gICAgICAgICAgcnVudGltZUNhY2hpbmc6IFtcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgdXJsUGF0dGVybjogL1xcLihnbGJ8Z2x0ZikkLyxcbiAgICAgICAgICAgICAgaGFuZGxlcjogJ0NhY2hlRmlyc3QnLFxuICAgICAgICAgICAgICBvcHRpb25zOiB7XG4gICAgICAgICAgICAgICAgY2FjaGVOYW1lOiAnM2QtbW9kZWxzLWNhY2hlJyxcbiAgICAgICAgICAgICAgICBleHBpcmF0aW9uOiB7IG1heEVudHJpZXM6IDUwLCBtYXhBZ2VTZWNvbmRzOiA2MCAqIDYwICogMjQgKiAzMCB9LFxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgdXJsUGF0dGVybjogL1xcL2FwaVxcLy4qLyxcbiAgICAgICAgICAgICAgaGFuZGxlcjogJ05ldHdvcmtGaXJzdCcsXG4gICAgICAgICAgICAgIG9wdGlvbnM6IHtcbiAgICAgICAgICAgICAgICBjYWNoZU5hbWU6ICdhcGktY2FjaGUnLFxuICAgICAgICAgICAgICAgIG5ldHdvcmtUaW1lb3V0U2Vjb25kczogMTAsXG4gICAgICAgICAgICAgICAgZXhwaXJhdGlvbjogeyBtYXhFbnRyaWVzOiA1MCwgbWF4QWdlU2Vjb25kczogNjAgKiA2MCAqIDIgfSxcbiAgICAgICAgICAgICAgICBiYWNrZ3JvdW5kU3luYzogeyBuYW1lOiAnYXBpLXF1ZXVlJywgb3B0aW9uczogeyBtYXhSZXRlbnRpb25UaW1lOiA2MCAqIDYwIH0gfSxcbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgIH0sXG4gICAgICAgICAgXSxcbiAgICAgICAgICBza2lwV2FpdGluZzogdHJ1ZSxcbiAgICAgICAgICBjbGllbnRzQ2xhaW06IHRydWUsXG4gICAgICAgIH0sXG4gICAgICAgIGRldk9wdGlvbnM6IHsgZW5hYmxlZDogdHJ1ZSwgdHlwZTogJ21vZHVsZScsIG5hdmlnYXRlRmFsbGJhY2s6ICdpbmRleC5odG1sJyB9LFxuICAgICAgfSksXG4gICAgICBnbHNsKCksXG4gICAgICB2aXN1YWxpemVyKHsgb3BlbjogZmFsc2UsIGZpbGVuYW1lOiAnYnVuZGxlLXN0YXRzLmh0bWwnIH0pLFxuICAgICAgdml0ZUNvbXByZXNzaW9uKHsgYWxnb3JpdGhtOiAnYnJvdGxpQ29tcHJlc3MnLCB0aHJlc2hvbGQ6IDEwMjQwLCBleHQ6ICcuYnInIH0pLFxuICAgIF0sXG4gICAgcmVzb2x2ZToge1xuICAgICAgYWxpYXM6IHtcbiAgICAgICAgLy8gQWxpYXMgcHJpbmNpcGFsIC0gY29icmUgdHVkbyBlbSBzcmMvXG4gICAgICAgICdAJzogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgJ3NyYycpLFxuICAgICAgICBcbiAgICAgICAgLy8gQWxpYXNlcyBlc3BlY1x1MDBFRGZpY29zIHBhcmEgbWVsaG9yIG9yZ2FuaXphXHUwMEU3XHUwMEUzb1xuICAgICAgICAnQGNvbXBvbmVudHMnOiBwYXRoLnJlc29sdmUoX19kaXJuYW1lLCAnc3JjL2NvbXBvbmVudHMnKSxcbiAgICAgICAgJ0B2aWV3cyc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvdmlld3MnKSxcbiAgICAgICAgJ0BzdG9yZSc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvc3RvcmUnKSxcbiAgICAgICAgJ0BzZXJ2aWNlcyc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvc2VydmljZXMnKSxcbiAgICAgICAgJ0Bjb21wb3NhYmxlcyc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvY29tcG9zYWJsZXMnKSxcbiAgICAgICAgJ0B0eXBlcyc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvdHlwZXMnKSxcbiAgICAgICAgJ0Bhc3NldHMnOiBwYXRoLnJlc29sdmUoX19kaXJuYW1lLCAnc3JjL2Fzc2V0cycpLFxuICAgICAgICAnQG1vZGVscyc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvYXNzZXRzL21vZGVscycpLFxuICAgICAgICAnQHNoYWRlcnMnOiBwYXRoLnJlc29sdmUoX19kaXJuYW1lLCAnc3JjL3NoYWRlcnMnKSxcbiAgLy8gU2hhcmVkIGNvbXBvbmVudHMgbGl2ZSB1bmRlciBzcmMvc2hhcmVkIChzb21lIGZpbGVzIGltcG9ydCBhcyBAc2hhcmVkIG9yIEAvc2hhcmVkKVxuICAnQHNoYXJlZCc6IHBhdGgucmVzb2x2ZShfX2Rpcm5hbWUsICdzcmMvc2hhcmVkJyksXG4gIC8vIFN1cHBvcnQgaW1wb3J0cyB0aGF0IHVzZSB0aGUgQC9zaGFyZWQvIHByZWZpeFxuICAnQC9zaGFyZWQnOiBwYXRoLnJlc29sdmUoX19kaXJuYW1lLCAnc3JjL3NoYXJlZCcpLFxuICAgICAgfSxcbiAgICB9LFxuICAgIGJ1aWxkOiB7XG4gICAgICB0YXJnZXQ6ICdlc25leHQnLFxuICAgICAgbWluaWZ5OiAndGVyc2VyJyxcbiAgICAgIHRlcnNlck9wdGlvbnM6IHsgXG4gICAgICAgIGNvbXByZXNzOiB7IFxuICAgICAgICAgIGRyb3BfY29uc29sZTogdHJ1ZSwgXG4gICAgICAgICAgZHJvcF9kZWJ1Z2dlcjogdHJ1ZSBcbiAgICAgICAgfSBcbiAgICAgIH0sXG4gICAgICByb2xsdXBPcHRpb25zOiB7XG4gICAgICAgIG91dHB1dDoge1xuICAgICAgICAgIG1hbnVhbENodW5rcyhpZCkge1xuICAgICAgICAgICAgaWYgKGlkLmluY2x1ZGVzKCdub2RlX21vZHVsZXMnKSkge1xuICAgICAgICAgICAgICBpZiAoaWQuaW5jbHVkZXMoJ3RocmVlJykgfHwgaWQuaW5jbHVkZXMoJ2dsdGYnKSkgcmV0dXJuICd0aHJlZSc7XG4gICAgICAgICAgICAgIGlmIChpZC5pbmNsdWRlcygndnVlJykpIHJldHVybiAndnVlJztcbiAgICAgICAgICAgICAgaWYgKGlkLmluY2x1ZGVzKCdjaGFydCcpKSByZXR1cm4gJ2NoYXJ0cyc7XG4gICAgICAgICAgICAgIHJldHVybiAndmVuZG9yJztcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9LFxuICAgICAgICB9LFxuICAgICAgfSxcbiAgICAgIGNodW5rU2l6ZVdhcm5pbmdMaW1pdDogMTAwMCxcbiAgICB9LFxuICAgIG9wdGltaXplRGVwczoge1xuICAgICAgaW5jbHVkZTogW1xuICAgICAgICAndGhyZWUnLCBcbiAgICAgICAgJ3Ryb2lzanMnLCBcbiAgICAgICAgJ0Bnb29nbGUvbW9kZWwtdmlld2VyJywgXG4gICAgICAgICdjaGFydC5qcycsXG4gICAgICAgICd2dWUnLFxuICAgICAgICAndnVlLXJvdXRlcicsXG4gICAgICAgICdwaW5pYScsXG4gICAgICAgICdheGlvcydcbiAgICAgIF0sXG4gICAgICAvLyBSZW1vdmlkbyBvIGV4Y2x1ZGUgcXVlIGVzdGF2YSBjYXVzYW5kbyBjb25mbGl0b1xuICAgIH0sXG4gICAgc2VydmVyOiB7XG4gICAgICBwb3J0OiA1MTczLFxuICAgICAgaG9zdDogJzAuMC4wLjAnLFxuICAgICAgcHJveHk6IHtcbiAgICAgICAgJy9hcGknOiB7IFxuICAgICAgICAgIHRhcmdldDogJ2h0dHA6Ly9iYWNrZW5kOjgwMDAnLCBcbiAgICAgICAgICBjaGFuZ2VPcmlnaW46IHRydWUsXG4gICAgICAgICAgc2VjdXJlOiBmYWxzZVxuICAgICAgICB9LFxuICAgICAgICAnL3dzJzogeyBcbiAgICAgICAgICB0YXJnZXQ6ICd3czovL2JhY2tlbmQ6ODAwMCcsIFxuICAgICAgICAgIHdzOiB0cnVlIFxuICAgICAgICB9LFxuICAgICAgfSxcbiAgICB9LFxuICB9O1xufSk7Il0sCiAgIm1hcHBpbmdzIjogIjtBQUNBLFNBQVMsb0JBQW9CO0FBQzdCLE9BQU8sU0FBUztBQUNoQixPQUFPLFVBQVU7QUFDakIsU0FBUyxxQkFBcUI7QUFDOUIsU0FBUyxlQUFlO0FBQ3hCLFNB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

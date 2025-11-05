/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_APP_TITLE: string;
  readonly VITE_APP_VERSION: string;
  readonly VITE_APP_DESCRIPTION: string;
  readonly VITE_APP_AUTHOR: string;
  readonly VITE_APP_COPYRIGHT: string;
  readonly VITE_APP_THEME: string;
  readonly VITE_APP_LOGO: string;
  readonly VITE_APP_FAVICON: string;  
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
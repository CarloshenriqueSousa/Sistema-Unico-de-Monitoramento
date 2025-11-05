declare namespace JSX {
  interface IntrinsicElements {
    [elemName: string]: any;
    'model-viewer': any;
  }
}

declare module '*.glb' {
  const src: string;
  export default src;
}

declare module '*.gltf' {
  const src: string;
  export default src;
}

declare module '*.vs' {
  const src: string;
  export default src;
}

declare module '*.fs' {
  const src: string;
  export default src;
}
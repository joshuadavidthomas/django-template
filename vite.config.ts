import { defineConfig } from "vite";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/static/",
  build: {
    assetsDir: "",
    manifest: true,
    outDir: resolve(__dirname, "./static/dist"),
    rollupOptions: {
      input: [resolve(__dirname, "./static/src/main.ts")],
      output: {
        chunkFileNames: undefined,
      },
    },
  },
  plugins: [],
  publicDir: "",
  resolve: {
    extensions: [".js", ".json", ".ts"],
  },
  root: resolve(__dirname, "./static/src"),
  server: {
    host: "127.0.0.1",
    port: 5173,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
});

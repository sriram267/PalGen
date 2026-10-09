import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
  clearScreen: false,
  server: {
    port: 5173,
    host: true,
  },
  build: {
    target: "esnext",
    rollupOptions: {
      input: {
        island: resolve(__dirname, "index.html"),
        settings: resolve(__dirname, "settings.html"),
        mochi: resolve(__dirname, "mochi.html"),
      },
    },
  },
});

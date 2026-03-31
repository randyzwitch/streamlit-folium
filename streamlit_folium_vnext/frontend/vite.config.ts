import { defineConfig } from "vite"

export default defineConfig({
  base: "./",
  build: {
    outDir: "build",
    lib: {
      entry: "./src/index.ts",
      formats: ["es"],
      fileName: "index-[hash]",
    },
    rollupOptions: {
      output: {
        entryFileNames: "index-[hash].js",
      },
    },
  },
})

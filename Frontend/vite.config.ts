import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwind from "@tailwindcss/vite"; // Import the tailwind plugin

export default defineConfig({
  plugins: [react(), tailwind()], // Add tailwind() to the plugins array
});
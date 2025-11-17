/** @type {import('tailwindcss').Config} */
export default {
  content: ["./public/**/*.html"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#111827",
          accent: "#2563eb",
          muted: "#f8fafc"
        }
      }
    }
  },
  plugins: []
};

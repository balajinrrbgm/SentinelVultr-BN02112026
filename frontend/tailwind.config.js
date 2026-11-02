/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        vultr: {
          blue: "#007BFC",
          navy: "#021A3B",
          dark: "#0b1329",
          card: "#0f1c3f",
          border: "#1e293b",
          accent: "#00E5FF",
        },
      },
    },
  },
  plugins: [],
};


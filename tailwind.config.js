const defaultColors = require("tailwindcss/colors");

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./static/**/*.{js,ts,jsx,tsx}", "./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        primary: defaultColors.indigo,
        secondary: defaultColors.blue,
        tertiary: defaultColors.green,
        aspect: defaultColors.orange,
      },
    },
  },
  plugins: [],
};

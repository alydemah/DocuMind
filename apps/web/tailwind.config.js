const baseConfig = require("@documind/tailwind-config");

/** @type {import('tailwindcss').Config} */
module.exports = {
  ...baseConfig,
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
};

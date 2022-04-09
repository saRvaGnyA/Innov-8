const defaultTheme = require("tailwindcss/defaultTheme");
const colors = require("tailwindcss/colors");

module.exports = {
  content: ["*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["cairo", ...defaultTheme.fontFamily.sans],
      },
      
      colors: {
        light: "var(--light)",
        dark: "var(--dark)",
        darker: "var(--darker)",
        primary: {
          DEFAULT: "var(--color-primary)",
          50: "var(--color-primary-50)",
          100: "var(--color-primary-100)",
          light: "var(--color-primary-light)",
          lighter: "var(--color-primary-lighter)",
          dark: "var(--color-primary-dark)",
          darker: "var(--color-primary-darker)",
        },
        secondary: {
          DEFAULT: colors.fuchsia[600],
          50: colors.fuchsia[50],
          100: colors.fuchsia[100],
          light: colors.fuchsia[500],
          lighter: colors.fuchsia[400],
          dark: colors.fuchsia[700],
          darker: colors.fuchsia[800],
        },
        success: {
          DEFAULT: colors.green[600],
          50: colors.green[50],
          100: colors.green[100],
          light: colors.green[500],
          lighter: colors.green[400],
          dark: colors.green[700],
          darker: colors.green[800],
        },
        warning: {
          DEFAULT: colors.orange[600],
          50: colors.orange[50],
          100: colors.orange[100],
          light: colors.orange[500],
          lighter: colors.orange[400],
          dark: colors.orange[700],
          darker: colors.orange[800],
        },
        danger: {
          DEFAULT: colors.red[600],
          50: colors.red[50],
          100: colors.red[100],
          light: colors.red[500],
          lighter: colors.red[400],
          dark: colors.red[700],
          darker: colors.red[800],
        },
        info: {
          DEFAULT: colors.cyan[600],
          50: colors.cyan[50],
          100: colors.cyan[100],
          light: colors.cyan[500],
          lighter: colors.cyan[400],
          dark: colors.cyan[700],
          darker: colors.cyan[800],
        },
        "great-blue": {
          DEFAULT: "#2A669F",
          50: "#E4F7F8",
          100: "#CCEEF2",
          200: "#9CD7E5",
          300: "#6CB9D8",
          400: "#3B94CB",
          500: "#2A669F",
          600: "#234B83",
          700: "#1B3366",
          800: "#14204A",
          900: "#0C102E",
        },
        "chamki-green": {
          50: "#EBF2FA",
          100: "#DBE8F5",
          200: "#B2CFEB",
          300: "#8EB8E1",
          400: "#6AA1D7",
          500: "#4389CD",
          600: "#2E6EAD",
          700: "#225281",
          800: "#163655",
          900: "#0C1C2C",
        },
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
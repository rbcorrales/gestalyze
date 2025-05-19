import js from "@eslint/js";
import globals from "globals";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import a11yPlugin from "eslint-plugin-jsx-a11y";

export default [
  js.configs.recommended,
  // Global ignores
  {
    ignores: [
      // Dependencies
      "node_modules/**",

      // Build output
      "dist/**",

      // Config files
      "*.config.js",

      // Package files
      "package.json",
      "package-lock.json",

      // Public assets
      "public/**",
    ]
  },
  // React specific configuration
  {
    files: ["**/*.{js,jsx}"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.es2021,
        ...globals.node
      },
      parserOptions: {
        ecmaFeatures: {
          jsx: true
        }
      }
    },
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
      "jsx-a11y": a11yPlugin
    },
    rules: {
      // React specific rules
      "react/jsx-uses-react": "error",
      "react/jsx-uses-vars": "error",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",

      // Accessibility rules
      "jsx-a11y/alt-text": "error",
      "jsx-a11y/anchor-has-content": "error",
      "jsx-a11y/anchor-is-valid": "error",
      "jsx-a11y/aria-props": "error",
      "jsx-a11y/aria-role": "error",
      "jsx-a11y/aria-unsupported-elements": "error",
      "jsx-a11y/role-has-required-aria-props": "error",
      "jsx-a11y/role-supports-aria-props": "error",

      // General rules
      "no-unused-vars": "warn",
      "no-console": ["warn", { allow: ["warn", "error"] }]
    },
    settings: {
      react: {
        version: "detect"
      }
    }
  }
];

# Gestalyze Website ([gestalyze.com](https://gestalyze.com))

This is the official website for Gestalyze, a smart hand gesture analysis project. The website is built using React, Vite, and TailwindCSS.

## Features

- Responsive design
- Multi-language support (English and Spanish)
- Showcases project features and capabilities
- Accessibility-first approach

## Development

### Prerequisites

- Node.js (v18 or later)
- npm (v9 or later)

### Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:5173](http://localhost:5173) in your browser.

### Code Quality Tools

The project uses ESLint and Prettier to maintain code quality and consistent formatting.

#### Available Commands

- `npm run lint` - Check for code issues
- `npm run lint:fix` - Automatically fix linting issues
- `npm run format` - Format all files
- `npm run format:check` - Check if files are formatted correctly
- `npm run check` - Run both lint and format checks

#### Key Features

- **ESLint Configuration**:
  - React and React Hooks best practices
  - Accessibility (jsx-a11y) rules
  - Import ordering and organization
  - Integration with Prettier
  - Custom rules for better development experience

- **Prettier Configuration**:
  - Consistent code style
  - Tailwind CSS class sorting
  - 100 character line length
  - Single quotes
  - Semicolons required
  - Trailing commas in objects and arrays

### Building for Production

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

To preview the production build locally:

```bash
npm run preview
```

## Project Structure

```
website/
├── public/                # Static assets (logo, etc.)
├── src/
│   ├── components/        # React components
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   └── Body.jsx
│   ├── i18n/              # Internationalization
│   │   └── translations/
│   ├── App.jsx            # Main application component
│   ├── main.jsx           # Application entry point
│   └── index.css          # Global styles (TailwindCSS)
├── .eslintrc.json         # ESLint configuration
├── .prettierrc            # Prettier configuration
├── .gitignore             # Git ignore rules
├── index.html             # HTML template
├── package.json           # Project dependencies
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # TailwindCSS configuration
└── postcss.config.js      # PostCSS configuration
```

## Development Workflow

1. **Before Starting**:
   - Make sure all dependencies are installed (`npm install`)
   - Run `npm run check` to ensure code is clean

2. **During Development**:
   - Run `npm run dev` for development server
   - Use `npm run lint:fix` to automatically fix linting issues
   - Use `npm run format` to format your code

3. **Before Committing**:
   - Run `npm run check` to ensure code quality
   - Fix any linting or formatting issues
   - Ensure all tests pass (if applicable)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](../LICENSE) file for details.

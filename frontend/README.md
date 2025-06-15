# Vue.js Project Setup Guide

## Local Development Setup

### Prerequisites
- Node.js (v15 or higher)
- npm (Node Package Manager) or yarn

### Steps to Run Locally

1. **Make sure folder opened in terminal**

2. **Install Dependencies**
    ```bash
    npm install
    # or
    yarn install
    ```

3. **Run Development Server**
    ```bash
    npm run dev --port=5173
    # or
    yarn dev
    ```
    The application will be available at `http://localhost:5173` by default.

## Building for Production

1. **Create Production Build**
    ```bash
    npm run build
    # or
    yarn build
    ```
    This will generate a `dist` directory with production-ready files.

2. **Preview Production Build** (Optional)
    ```bash
    npm run preview
    # or
    yarn preview
    ```

## Additional Commands

- **Lint Code**
  ```bash
  npm run lint
  ```

- **Run Tests**
  ```bash
  npm run test
  ```

## Environment Variables
Create a `.env` file in the root directory and add necessary environment variables:
```
VITE_API_URL=your_api_url_here
```

## Note
Make sure to check `package.json` for all available scripts and project dependencies.






## Developer Notes :

1. Maintain all pages in src/pages and components in src/components

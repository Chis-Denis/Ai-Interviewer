# AI Interviewer - Frontend

Frontend application for the AI Interviewer built with Vue.js.

## Tech Stack

- **Framework**: Vue.js 3
- **Language**: TypeScript
- **Build Tool**: Vite
- **Package Manager**: npm or yarn

## Project Structure

```
frontend/
├── src/
│   ├── components/      # Vue components
│   ├── views/           # Page views
│   ├── router/          # Vue Router configuration
│   ├── stores/          # State management (Pinia)
│   ├── services/        # API services
│   ├── utils/           # Utility functions
│   ├── assets/          # Static assets
│   └── App.vue          # Root component
├── public/              # Public static files
├── package.json         # Dependencies
└── vite.config.ts       # Vite configuration
```

## Setup

### Prerequisites

- Node.js 16+ and npm/yarn
- Backend API running (see backend README)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
yarn install
```

3. Create a `.env` file in the frontend directory:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
```

## Running the Application

### Development Mode

```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:5173 (or the port shown in terminal).

### Production Build

```bash
npm run build
# or
yarn build
```

The built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
# or
yarn preview
```

## Configuration

### API Configuration

Update the API base URL in `.env` or `src/services/api.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

### Vite Configuration

Edit `vite.config.ts` to customize build settings, proxy configuration, etc.

## Project Structure Details

- **components/**: Reusable Vue components
- **views/**: Full page components (routes)
- **router/**: Vue Router setup and route definitions
- **stores/**: State management (Pinia recommended for Vue 3)
- **services/**: API service functions for backend communication
- **utils/**: Helper functions and utilities
- **assets/**: Images, styles, fonts, etc.

## Styling

You can use:
- **CSS/SCSS**: For component-scoped styles
- **Tailwind CSS**: Utility-first CSS framework
- **Vuetify/Material-UI**: Component libraries
- **Custom CSS**: In `src/assets/styles/`

## API Integration

API calls should be made through service files in `src/services/`. Example:

```typescript
// src/services/interviewService.ts
import api from './api'

export const getInterviews = () => api.get('/interviews')
export const createInterview = (data: any) => api.post('/interviews', data)
```

## Testing

Run tests:

```bash
npm run test:unit
# or
yarn test:unit
```

## Features

- Interview session management
- Real-time question display
- Response submission
- Results visualization
- Candidate management

## Deployment

### Build for Production

```bash
npm run build
```

Deploy the `dist/` folder to your hosting service (Vercel, Netlify, etc.).

### Environment Variables

Make sure to set production environment variables:
- `VITE_API_BASE_URL`: Your production API URL


# AI Interviewer

AI-powered interview system with automated question generation and interview analysis.

## Tech Stack

- **Backend**: FastAPI, SQLite, SQLAlchemy
- **Frontend**: Vue.js 3, TypeScript, Vite

## Project Structure

```
├── backend/     # FastAPI backend (Clean Architecture)
└── frontend/    # Vue.js frontend
```

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Architecture

The backend follows Clean Architecture principles with clear separation of concerns:
- **Domain**: Business entities and enums
- **Application**: Use cases, DTOs, repository interfaces
- **Infrastructure**: Database implementations, external services
- **Presentation**: API controllers, dependency injection

See `backend/ARCHITECTURE.md` for detailed architecture documentation.

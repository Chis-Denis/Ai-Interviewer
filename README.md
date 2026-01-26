# AI Interviewer

An intelligent interview system that conducts AI-powered interviews, generates contextual questions, and provides comprehensive analysis of candidate responses.

## What It Does

This system allows you to:
- **Start interviews** on any topic (e.g., "Python optimization", "System design", "Machine Learning")
- **Generate questions dynamically** - The AI creates 3-5 sequential questions that build on previous answers
- **Collect answers** interactively with order validation
- **Analyze responses** with sentiment analysis, key themes, strengths, weaknesses, and calculated metrics
- **Store everything** - Complete interview transcripts and summaries are persisted

## Quick Start

### Prerequisites
- Python 3.9+ (for backend)
- Node.js 18+ (for frontend)

### Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

# Create .env file
echo "LLM_API_KEY=your-api-key-here" > .env

# Run the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000` with interactive docs at `/docs`.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── backend/     # FastAPI backend (Clean Architecture)
└── frontend/    # Vue.js 3 frontend
```

## Tech Stack

- **Backend**: FastAPI, SQLite, SQLAlchemy, Pydantic
- **Frontend**: Vue.js 3, TypeScript, Vite
- **AI**: OpenAI API (configurable for other LLM providers)

## Documentation

- **Backend Details**: See `backend/README.md` for architecture, LLM interaction, and flow
- **API Documentation**: Available at `http://localhost:8000/docs` when running

## Features

- **Dynamic Question Generation** - Questions adapt based on previous answers
- **Comprehensive Analysis** - Sentiment, themes, strengths, weaknesses, and calculated metrics
- **Order Validation** - Ensures answers are submitted in sequence
- **Full Persistence** - All interviews and summaries are stored
- **Clean Architecture** - Well-structured, maintainable codebase

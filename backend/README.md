# AI Interviewer - Backend

Backend API for the AI Interviewer application built with FastAPI and SQLite.

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Python**: 3.9+

## Project Structure

```
backend/
├── Application/          # Application layer (Use Cases, DTOs, Repositories)
│   ├── dtos/            # Data Transfer Objects
│   ├── Exceptions/      # Custom exceptions
│   ├── Repositories/    # Repository interfaces
│   └── UseCases/        # Business logic use cases
├── Core/                # Core configuration
│   └── config.py        # Application configuration
├── Domain/              # Domain layer (Business entities)
│   ├── Entities/        # Domain entities
│   └── Enums/           # Domain enums
├── Infrastructure/      # Infrastructure layer
│   ├── Db/              # Database implementations
│   └── Llm/             # LLM service integrations
├── Presentation/        # Presentation layer (API)
│   ├── Controllers/     # API controllers/routes
│   ├── Helpers/         # Helper functions
│   ├── Mapping/         # DTO mapping
│   ├── Options/         # Configuration options
│   └── Validations/     # Input validations
├── tests/               # Test files
├── main.py              # FastAPI application entry point
└── requirements.txt     # Python dependencies
```

## Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository and navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the backend directory (optional):
```env
DATABASE_URL=sqlite:///./ai_interviewer.db
LLM_API_KEY=your-llm-api-key
ENVIRONMENT=development
```

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Database

The application uses SQLite by default. The database file will be created automatically at `./ai_interviewer.db` when you first run the application.

### Database Migrations

To manage database migrations, you can use Alembic:

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Testing

Run tests using pytest:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=. --cov-report=html
```

## Project Architecture

This project follows **Clean Architecture** principles:

- **Domain Layer**: Core business entities and enums (no dependencies)
- **Application Layer**: Use cases and business logic
- **Infrastructure Layer**: Database and external service implementations
- **Presentation Layer**: API controllers and request/response handling

## Configuration

Configuration is managed in `Core/config.py`. Environment variables can be set in a `.env` file.

## Dependencies

Key dependencies:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `sqlalchemy`: ORM
- `pydantic`: Data validation
- `python-dotenv`: Environment variable management

See `requirements.txt` for the complete list.
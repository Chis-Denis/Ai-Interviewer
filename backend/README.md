# AI Interviewer - Backend

FastAPI backend implementing an AI-powered interview system with Clean Architecture principles.

## Overview

This backend orchestrates the complete interview lifecycle: from creating interviews on a topic, generating contextual questions via LLM, collecting answers, to producing comprehensive summaries with analysis. The system is designed with maintainability, testability, and scalability in mind.

## Architecture

The project follows **Clean Architecture**, ensuring clear separation of concerns and dependency inversion:

```
┌─────────────────────────────────────┐
│     Presentation Layer (API)         │  ← FastAPI controllers, DTOs
├─────────────────────────────────────┤
│     Application Layer                │  ← Use cases, business logic
├─────────────────────────────────────┤
│     Domain Layer                     │  ← Entities, enums (no deps)
├─────────────────────────────────────┤
│     Infrastructure Layer             │  ← Database, LLM services
└─────────────────────────────────────┘
```

### Layer Responsibilities

- **Domain**: Pure business entities and enums. Zero external dependencies.
- **Application**: Use cases orchestrate business logic. Depends only on Domain.
- **Infrastructure**: Implements repository interfaces and external services. Depends on Application interfaces.
- **Presentation**: API endpoints, request/response handling. Depends on Application.

This structure ensures that business logic remains independent of frameworks and external services, making the codebase maintainable and testable.

## Interview Flow

The system follows a clear sequential flow:

1. **Create Interview** → User provides a topic (e.g., "Python optimization")
2. **Generate Questions** → LLM generates contextual questions (up to 5, sequential)
3. **Submit Answers** → User answers questions in order (validated)
4. **Generate Summary** → LLM analyzes all Q&A pairs and produces comprehensive summary

### Flow Details

**Question Generation**:
- Each question is generated dynamically based on the topic and previous Q&A pairs
- Questions build on previous answers to create a coherent conversation
- Order is enforced: questions must be answered sequentially
- Maximum of 5 questions per interview (configurable)

**Answer Submission**:
- Answers are validated to ensure proper order
- Interview status transitions automatically (NOT_STARTED → IN_PROGRESS)
- Duplicate answers for the same question are prevented

**Summary Generation**:
- Combines LLM analysis with calculated metrics
- Produces themes, key points, sentiment, strengths, weaknesses
- Calculates scores: clarity, confidence, consistency, overall usefulness

## LLM Interaction & Prompt Design

The system uses carefully crafted prompts to ensure high-quality, contextual interactions.

### Question Generation Prompts

**Context Building**: The system builds context from:
- Interview topic
- Previously asked questions
- Previous answers (if any)

**Prompt Strategy**:
- Focuses on practical, experience-based questions
- Avoids generic or theoretical questions
- Builds on previous answers to create depth
- Includes security measures to prevent prompt injection
- Enforces specific formatting (2 sentences, max 30 words)

**Key Features**:
- Context-aware: Questions adapt based on conversation history
- Progressive difficulty: Questions build complexity
- Security: Input integrity rules prevent manipulation attempts

### Summary Generation Prompts

**Analysis Approach**:
- Structured JSON output with strict schema validation
- Extracts exactly 3 themes and 5 key points
- Calculates sentiment (score + label)
- Identifies strengths, weaknesses, and missing information
- Generates professional summary text

**Validation**:
- Pydantic models ensure LLM responses match expected structure
- Field validators enforce data quality
- Error handling for malformed responses

### Retry Logic

The system includes retry logic with exponential backoff for:
- Network timeouts
- Rate limiting (429 errors)
- Server errors (500, 502, 503, 504)

This ensures resilience when dealing with external API calls.

## Code Quality

### Principles Applied

- **Single Responsibility**: Each class/function has one clear purpose
- **Dependency Inversion**: Depend on abstractions (interfaces), not concretions
- **Open/Closed**: Open for extension, closed for modification
- **Type Safety**: Comprehensive type hints throughout
- **Error Handling**: Custom exceptions with proper error propagation

### Code Organization

- **Use Cases**: Encapsulate business logic in clear, testable units
- **Repositories**: Abstract data access behind interfaces
- **DTOs**: Separate API contracts from domain models
- **Mappers**: Transform between layers cleanly

### Analysis & Scoring

The system includes sophisticated answer analysis:

**Calculated Metrics**:
- **Clarity Score**: Based on structure indicators, examples, metrics
- **Confidence Score**: Evaluates completeness and specificity
- **Consistency Score**: Measures answer length variance across interview
- **Overall Usefulness**: Average of clarity, confidence, and consistency

**Answer Evaluation**:
- Detects structure indicators (bullets, numbering, formatting)
- Identifies examples and concrete scenarios
- Finds metrics and quantifiable data
- Assesses completeness and depth

## Project Structure

```
backend/
├── Application/          # Business logic layer
│   ├── Analysis/        # Answer evaluation & scoring
│   ├── dtos/            # Data Transfer Objects
│   ├── Exceptions/      # Custom exceptions
│   ├── RepositoryInterfaces/  # Repository contracts
│   ├── Service/         # Service interfaces (LLM)
│   └── UseCases/        # Business use cases
├── Core/                # Configuration
├── Domain/              # Business entities & enums
├── Infrastructure/      # External implementations
│   ├── Db/             # Database (SQLAlchemy)
│   └── Llm/             # LLM service integration
├── Presentation/        # API layer
│   ├── Controllers/     # API endpoints
│   ├── Mapping/         # Entity ↔ DTO mapping
│   └── Validations/     # Error schemas
└── main.py             # Application entry point
```

## Setup & Configuration

### Environment Variables

Create a `.env` file:

```env
DATABASE_URL=sqlite:///./ai_interviewer.db
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
MAX_QUESTIONS_PER_INTERVIEW=5
```

### Running

```bash
# Development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

API documentation available at `/docs` (Swagger UI) and `/redoc`.

## Dependencies

Key libraries:
- `fastapi`: Modern web framework
- `sqlalchemy`: ORM for database operations
- `pydantic`: Data validation and settings
- `httpx`: Async HTTP client for LLM API
- `tenacity`: Retry logic for resilience

See `requirements.txt` for complete list.

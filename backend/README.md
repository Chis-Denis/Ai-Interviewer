# AI Interviewer — Backend

FastAPI backend for an AI-powered interview system, built with Clean Architecture.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Why Clean Architecture?](#why-clean-architecture)
3. [Why Anemic Domain Model?](#why-anemic-domain-model)
4. [Design Decisions](#design-decisions)
5. [Request Flow Example](#request-flow-example)
6. [Prompt Design & LLM Interaction](#prompt-design--llm-interaction)
7. [Error Handling Strategy](#error-handling-strategy)
8. [Project Structure](#project-structure)
9. [Setup](#setup)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   PRESENTATION                                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌────────────────┐  │
│  │   Interview     │  │    Question     │  │     Answer      │  │    Summary     │  │
│  │   Controller    │  │   Controller    │  │   Controller    │  │   Controller   │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  └───────┬────────┘  │
│           │                    │                    │                   │           │
│  ┌────────┴────────────────────┴────────────────────┴───────────────────┴────────┐  │
│  │                              Response DTOs / Mappers                          │  │
│  └───────────────────────────────────────┬──────────────────────────────────────┘  │
└──────────────────────────────────────────┼──────────────────────────────────────────┘
                                           │
                                           ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                   APPLICATION                                        │
│                                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │                               USE CASES                                       │   │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐             │   │
│  │  │   Create    │ │  Generate   │ │   Submit    │ │  Generate   │             │   │
│  │  │  Interview  │ │  Question   │ │   Answer    │ │   Summary   │             │   │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘             │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
│  ┌─────────────────────────────┐    ┌────────────────────────────────────────────┐  │
│  │    REPOSITORY INTERFACES    │    │                 SERVICES                    │  │
│  │  InterviewRepository        │    │  LLMOrchestrator, PromptBuilder            │  │
│  │  QuestionRepository         │    │  PromptLoader, ResponseParser              │  │
│  │  AnswerRepository           │    ├────────────────────────────────────────────┤  │
│  │  SummaryRepository          │    │  ANALYSIS: AnswerEvaluator, Scoring        │  │
│  └─────────────────────────────┘    └────────────────────────────────────────────┘  │
│                                                                                      │
│  ┌─────────────────────────────┐    ┌────────────────────────────────────────────┐  │
│  │      APPLICATION DTOs       │    │              EXCEPTIONS                    │  │
│  │  CreateInterviewDTO, etc.   │    │  InterviewNotFound, ValidationException    │  │
│  └─────────────────────────────┘    └────────────────────────────────────────────┘  │
└──────────────────────────────────────┬──────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                     DOMAIN                                           │
│                                                                                      │
│  ┌──────────────────────────────────┐    ┌───────────────────────────────────────┐  │
│  │            ENTITIES              │    │               ENUMS                    │  │
│  │  Interview, Question,            │    │  InterviewStatus (NOT_STARTED,        │  │
│  │  Answer, InterviewSummary        │    │    IN_PROGRESS, COMPLETED)            │  │
│  │                                  │    │  SentimentLabel (POSITIVE,            │  │
│  │                                  │    │    NEUTRAL, NEGATIVE)                 │  │
│  └──────────────────────────────────┘    └───────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                       ▲
                                       │ implements interfaces
┌──────────────────────────────────────┴──────────────────────────────────────────────┐
│                                 INFRASTRUCTURE                                       │
│                                                                                      │
│  ┌─────────────────────────────────────┐    ┌────────────────────────────────────┐  │
│  │            DATABASE                 │    │              LLM                    │  │
│  │  SQLAlchemy Models                  │    │  OpenAIClient                       │  │
│  │  SqlInterviewRepository             │    │  - Async HTTP calls                 │  │
│  │  SqlQuestionRepository              │    │  - Retry with exponential backoff   │  │
│  │  SqlAnswerRepository                │    │  - Rate limit handling              │  │
│  │  SqlSummaryRepository               │    └────────────────────────────────────┘  │
│  └─────────────────────────────────────┘                                            │
│                              ┌──────────────────┐                                    │
│                              │   SQLite DB      │                                    │
│                              └──────────────────┘                                    │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CONFIG (Cross-cutting)                                  │
│                         config.py + default.yaml + .env                              │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Why Clean Architecture?

### The Problem I Wanted to Avoid

In traditional layered apps, everything depends on everything. Controllers call services, services call the database directly, and if you want to swap SQLite for PostgreSQL — good luck, you're rewriting half the app. Same thing if OpenAI raises prices and you need to switch to Anthropic.

I didn't want that. I wanted to be able to change my mind about infrastructure without touching business logic.

### What Clean Architecture Gives Me

| Benefit | What it means in practice |
|---------|---------------------------|
| **Framework Independence** | FastAPI lives only in the presentation layer. If I ever need Flask, I swap one folder. |
| **Database Independence** | SQLite today, PostgreSQL tomorrow — I change one repository implementation and nothing else notices. |
| **LLM Provider Independence** | `OpenAIClient` implements an `LLMClient` interface. Swapping to Anthropic means writing one new class. |
| **Testability** | Use cases depend on interfaces. I can mock the database and LLM in tests without spinning up real services. |

### The Dependency Rule

This is the core idea: **dependencies always point inward**. Outer layers know about inner layers, never the reverse.

```
Infrastructure ──────┐
                     │
Presentation ────────┼──▶ Application ──▶ Domain
                     │
Config ──────────────┘
```

The Domain layer has zero dependencies — it's just plain Python classes. The Application layer defines interfaces that Infrastructure implements. This inversion is what makes everything swappable.

### "Isn't This Overkill for a Small Project?"

Honestly? A bit. For a quick prototype, a simple MVC structure would be fine. But I had a few reasons:

1. **LLM providers change constantly.** Prices shift, rate limits change, new models come out. Having an abstraction layer isn't paranoia — it's practical.
2. **It's a good demonstration.** This shows I understand how to structure code for maintainability, not just "make it work."
3. **It's actually not that much more code.** Once the structure is in place, adding new features is straightforward.

---

## Why Anemic Domain Model?

### What That Means

My entities — `Interview`, `Question`, `Answer` — are just data containers. They hold state but don't have behavior:

```python
class Interview:
    def __init__(self, id, topic, status, created_at, ...):
        self.id = id
        self.topic = topic
        self.status = status
        # No methods like interview.complete() or interview.add_question()
```

The alternative would be a "rich" domain model where entities have methods that encapsulate business logic:

```python
# Rich domain approach (not what I did)
class Interview:
    def generate_next_question(self, llm_service):
        # Logic lives inside the entity
        ...
```

### Why I Went Anemic

The rich domain model works great when you have complex business rules — think banking software where an `Account` needs to enforce overdraft limits, transaction histories, and interest calculations.

But my app is different:

| Factor | Rich Domain | Anemic + Use Cases |
|--------|-------------|-------------------|
| **Core logic** | Lives in entities | Lives in use cases |
| **LLM integration** | Awkward — entities calling async services? | Natural — use case orchestrates everything |
| **Testing** | Harder — need to mock inside entities | Easier — use cases are standalone |
| **Complexity** | Higher setup | Lower ceremony |

My app is mostly "call an external API, save the result, return it." The interesting logic is the LLM orchestration, not the entities themselves. Putting `generate_question()` inside an `Interview` entity would feel forced — it's not really "interview behavior," it's "application workflow."

---

## Design Decisions

Here's how I thought through some key choices, comparing what I did against simpler alternatives.

### Use Cases vs Fat Services

**What I did:** One class per action — `GenerateQuestionUseCase`, `SubmitAnswerUseCase`, etc.

**The alternative:** A single `InterviewService` class with methods for everything.

The problem with fat services is they grow. You start with 3 methods, then 8, then 15. Each method needs different dependencies. Testing becomes a nightmare because you're mocking 10 things to test one function.

With separate use cases, when something breaks, I open one file. When I test, I inject exactly what that use case needs. It's more files, but each one is dead simple.

### Separate DTOs per Layer

**What I did:** `CreateInterviewDTO` for input → `Interview` entity in the domain → `InterviewResponseDTO` for output.

**The alternative:** One `Interview` class everywhere.

This feels like overkill until something changes. Say I need to add a field to the API response but not to the database. Or I rename a column. With shared models, that change ripples everywhere. With separate DTOs, each layer controls its own shape.

The trade-off is more boilerplate. For 4 entities, it's borderline worth it. For a larger app, it's essential.

### Prompt Templates in Files

**What I did:** Prompts live in `prompts/question_prompt_v1.txt`, loaded at runtime.

**The alternative:** Inline strings in the code.

My prompts are 60+ lines each. Putting that inline would make the code unreadable. Plus, I can now:
- Edit prompts without touching Python
- Version them (`v1`, `v2`) for A/B testing or rollback
- Have non-developers review prompt changes

### Pydantic Validation for LLM Output

**What I did:** The LLM returns JSON, which I validate against a Pydantic model with strict field definitions.

**The alternative:** `json.loads(response)` and hope for the best.

LLMs hallucinate. They add fields you didn't ask for, omit required ones, return `"0.5"` as a string instead of a float. I've seen all of these.

Pydantic catches malformed responses immediately with clear errors. Without it, I'd get random `KeyError` exceptions somewhere downstream and have to trace back to figure out the LLM messed up.

### Custom Exception Hierarchy

**What I did:** Specific exceptions like `InterviewNotFoundException`, `MaxQuestionsReachedException`.

**The alternative:** Generic `raise Exception("Not found")` or `raise ValueError(...)`.

With custom exceptions, my error handler does this:

```python
if isinstance(exc, NotFoundException):
    return JSONResponse(status_code=404, ...)
if isinstance(exc, BusinessRuleException):
    return JSONResponse(status_code=400, ...)
```

No string matching. No if-else chains checking error messages. The exception type tells me exactly what happened and what HTTP status to return.

### Config in YAML + .env

**What I did:** Non-secret defaults in `default.yaml`, secrets in `.env`, both loaded by `config.py`.

**The alternative:** Hardcoded values in the code.

This keeps secrets out of git. It lets me have different configs for development vs production. And I can tweak things like `max_questions` or `temperature` without code changes.

---

## Request Flow Example

Here's what happens when someone clicks "Generate Question" — from the Vue frontend all the way to OpenAI and back.

```
┌──────────┐         ┌──────────────────────────────────────────────────────────────────┐
│          │         │                         BACKEND                                  │
│    UI    │         │                                                                  │
│  (Vue)   │         │  ┌─────────────────────────────────────────────────────────────┐│
│          │         │  │                    PRESENTATION                             ││
└────┬─────┘         │  │                                                             ││
     │               │  │   ┌─────────────────────────────────────────────────────┐   ││
     │ POST          │  │   │              QuestionController                     │   ││
     │ /interviews/  │  │   │                                                     │   ││
     │ {id}/questions│  │   │  1. Receive HTTP request                            │   ││
     │               │  │   │  2. Inject use case via FastAPI Depends             │   ││
     ▼               │  │   │  3. Call use_case.execute(dto)                      │   ││
┌─────────┐          │  │   │  4. Map Question entity → QuestionResponseDTO       │   ││
│ Request │─────────────────▶│  5. Return JSON                                    │   ││
└─────────┘          │  │   └──────────────────────┬──────────────────────────────┘   ││
                     │  └──────────────────────────┼──────────────────────────────────┘│
                     │                             │                                   │
                     │                             ▼                                   │
                     │  ┌─────────────────────────────────────────────────────────────┐│
                     │  │                    APPLICATION                              ││
                     │  │                                                             ││
                     │  │   ┌─────────────────────────────────────────────────────┐   ││
                     │  │   │           GenerateQuestionUseCase                   │   ││
                     │  │   │                                                     │   ││
                     │  │   │  1. interview_repo.get_by_id(interview_id)          │   ││
                     │  │   │  2. Validate: interview exists, not completed       │   ││
                     │  │   │  3. Check: question_count < MAX_QUESTIONS           │   ││
                     │  │   │  4. Fetch existing questions & answers for context  │   ││
                     │  │   │  5. llm_orchestrator.generate_question(context)     │   ││
                     │  │   │  6. Create Question entity                          │   ││
                     │  │   │  7. question_repo.create(question)                  │   ││
                     │  │   │  8. Return Question                                 │   ││
                     │  │   └───────────┬─────────────────────┬────────────────────┘   ││
                     │  │               │                     │                        ││
                     │  │               ▼                     ▼                        ││
                     │  │   ┌───────────────────┐  ┌──────────────────────────────┐   ││
                     │  │   │  LLMOrchestrator  │  │  Repository Interfaces       │   ││
                     │  │   │                   │  │  (injected implementations)  │   ││
                     │  │   │  1. Build context │  └──────────────────────────────┘   ││
                     │  │   │  2. Load prompt   │                                     ││
                     │  │   │  3. Render vars   │                                     ││
                     │  │   │  4. Call LLM      │                                     ││
                     │  │   │  5. Return text   │                                     ││
                     │  │   └─────────┬─────────┘                                     ││
                     │  └─────────────┼───────────────────────────────────────────────┘│
                     │                │                                                │
                     │                ▼                                                │
                     │  ┌─────────────────────────────────────────────────────────────┐│
                     │  │                   INFRASTRUCTURE                            ││
                     │  │                                                             ││
                     │  │   ┌───────────────────┐      ┌───────────────────────────┐  ││
                     │  │   │   OpenAIClient    │      │  SqlQuestionRepository    │  ││
                     │  │   │                   │      │                           │  ││
                     │  │   │  POST /v1/chat/   │      │  INSERT INTO questions    │  ││
                     │  │   │  completions      │      │  VALUES (...)             │  ││
                     │  │   └─────────┬─────────┘      └─────────────┬─────────────┘  ││
                     │  └─────────────┼──────────────────────────────┼────────────────┘│
                     └────────────────┼──────────────────────────────┼─────────────────┘
                                      │                              │
                                      ▼                              ▼
                              ┌───────────────┐              ┌───────────────┐
                              │   OpenAI API  │              │    SQLite     │
                              └───────────────┘              └───────────────┘
```

---

## Prompt Design & LLM Interaction

### The Challenge

Getting useful output from an LLM isn't just about asking nicely. The prompts need to be:
- **Reliable** — I need parseable, consistent output every time
- **Quality-focused** — Generic questions are useless; I need thoughtful follow-ups
- **Secure** — Users can type anything in the answer box, including "ignore previous instructions"
- **Fair** — The evaluation shouldn't reward flattery or penalize honest short answers unfairly

### Question Generation

The question prompt is built dynamically with context — the topic, previous questions asked, and previous answers given. This is what makes the questions feel like a real conversation rather than a random quiz.

Key constraints I enforce:
- **Focus on HOW/WHY**, not definitions. "What is polymorphism?" is useless. "Tell me about a time you used polymorphism to solve a problem" reveals actual understanding.
- **Build on previous answers.** If someone mentions they worked on a payment system, the next question should dig into that.
- **30 word limit.** Forces the LLM to be concise. No rambling preambles.
- **Security rules.** The prompt explicitly tells the LLM to treat user answers as data, not instructions. This mitigates prompt injection attempts.

### Summary Generation

For the summary, I need structured JSON output. Free-form text would be impossible to display consistently in the UI.

The prompt specifies the exact schema:
```json
{
  "themes": [3 strings],
  "key_points": [5 strings],
  "sentiment_score": 0.0-1.0,
  "sentiment_label": "positive"|"neutral"|"negative",
  "strengths": [...],
  "weaknesses": [...],
  "missing_information": [...],
  "full_summary_text": "2-3 sentences"
}
```

I also tell it how to handle edge cases: if someone types gibberish, use "Unclear Response" as a theme instead of making up technical themes. If answers are short, that should lower the confidence score.

### Handling LLM Failures

OpenAI's API fails more often than you'd expect — rate limits, timeouts, random 500 errors. My client uses retry with exponential backoff:

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception(...)
)
```

For 429 (rate limit) and 5xx errors, it retries. For 401 (bad API key) or 400 (my bug), it fails immediately — no point retrying those.

### Metrics Beyond the LLM

The LLM gives qualitative analysis, but I also calculate quantitative scores locally:

| Metric | What it measures |
|--------|------------------|
| **Clarity** | Did they structure their answer? Use examples? Include specifics? |
| **Confidence** | Did they commit to positions or hedge everything? |
| **Consistency** | Are all answers roughly the same depth, or did they phone it in on some? |

These are computed without any LLM calls — just text analysis in `application/analysis/`.

---

## Error Handling Strategy

I use a custom exception hierarchy instead of generic exceptions:

```
ApplicationException (base)
├── NotFoundException
│   ├── InterviewNotFoundException
│   ├── QuestionNotFoundException
│   └── ...
├── BusinessRuleException
│   ├── MaxQuestionsReachedException
│   ├── AnswerOrderException
│   └── ...
├── ValidationException
└── LlmServiceError
```

The error handler maps these to HTTP codes automatically:

| Exception Type | HTTP Status |
|---------------|-------------|
| `NotFoundException` | 404 |
| `BusinessRuleException` | 400 |
| `ValidationException` | 422 |
| `LlmServiceError` | 502 |

This means use cases just `raise InterviewNotFoundException(interview_id)` and the right status code comes out the other end.

---

## Project Structure

```
backend/
├── application/
│   ├── analysis/              # Scoring logic (no LLM)
│   ├── dtos/                  # Input DTOs
│   ├── exceptions/            # Custom exception classes
│   ├── repository_interfaces/ # Abstract interfaces
│   ├── services/
│   │   ├── llm_client.py      # LLM interface
│   │   ├── llm_orchestrator.py
│   │   ├── prompt_builder.py
│   │   ├── prompt_loader.py
│   │   └── prompts/           # Prompt templates
│   └── use_cases/             # Business logic
├── config/
│   ├── config.py              # Settings loader
│   └── default.yaml           # Default values
├── domain/
│   ├── entities/              # Data classes
│   └── enums/
├── infrastructure/
│   ├── database/              # SQLAlchemy implementation
│   └── llm/                   # OpenAI client
├── presentation/
│   ├── controllers/           # API endpoints
│   ├── dtos/                  # Response DTOs
│   ├── mappers/               # Entity → DTO conversion
│   └── common/                # Error handling, CORS
├── composition.py             # Dependency wiring
└── main.py                    # Entry point
```
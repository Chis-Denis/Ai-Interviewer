# Architecture and Dependency Flow

This document explains the Clean Architecture structure and how dependencies flow between layers.

## Layer Structure

```
┌─────────────────────────────────────────┐
│  Presentation (API Controllers)          │  ← Outermost
├─────────────────────────────────────────┤
│  Infrastructure (Db, Llm)               │  ← Outermost
├─────────────────────────────────────────┤
│  Application (Use Cases, DTOs)          │  ← Middle
├─────────────────────────────────────────┤
│  Domain (Entities, Enums)                │  ← Innermost
└─────────────────────────────────────────┘
```

## Dependency Rule

**Dependencies point INWARD only.**

- Outer layers can depend on inner layers
- Inner layers CANNOT depend on outer layers
- Domain has NO dependencies on other layers (only standard library)

## Layer Dependencies

### Domain Layer (Innermost)
**Location:** `Domain/`

**Allowed Imports:**
- Standard library only (datetime, typing, uuid, enum, etc.)
- Other Domain modules (Domain.Entities, Domain.Enums)

**Forbidden Imports:**
- Application
- Infrastructure
- Presentation
- Core (except for shared types if needed)

**Example:**
```python
# ✅ CORRECT
from datetime import datetime
from uuid import UUID
from Domain.Enums.InterviewStatus import InterviewStatus

# ❌ WRONG
from Infrastructure.Db.models import InterviewModel  # NO!
from Application.UseCases import SomeUseCase  # NO!
```

### Application Layer
**Location:** `Application/`

**Allowed Imports:**
- Domain (Entities, Enums)
- Core (config, shared utilities)
- Standard library

**Forbidden Imports:**
- Infrastructure (use repository interfaces instead)
- Presentation

**Example:**
```python
# ✅ CORRECT
from Domain.Entities import Interview
from Domain.Enums import InterviewStatus
from Application.RepositoryInterfaces import InterviewRepository  # Interface
from Core.config import settings

# ❌ WRONG
from Infrastructure.Db.models import InterviewModel  # NO! Use repository
from Presentation.Controllers import SomeController  # NO!
```

### Infrastructure Layer
**Location:** `Infrastructure/`

**Allowed Imports:**
- Domain (Entities, Enums) - to map to/from
- Core (config)
- External libraries (SQLAlchemy, LLM SDKs, etc.)
- Application (repository interfaces to implement)

**Forbidden Imports:**
- Presentation

**Example:**
```python
# ✅ CORRECT
from Domain.Entities import Interview
from Domain.Enums import InterviewStatus
from Application.RepositoryInterfaces import InterviewRepository  # Interface to implement
from Infrastructure.Db.models import InterviewModel
from Infrastructure.Db.mappers import interview_model_to_entity
from Core.config import settings

# ❌ WRONG
from Presentation.Controllers import SomeController  # NO!
```

### Presentation Layer
**Location:** `Presentation/`

**Allowed Imports:**
- Application (Use Cases, DTOs)
- Domain (Entities, Enums) - for validation/mapping
- Core (config)
- FastAPI, Pydantic

**Forbidden Imports:**
- Infrastructure (use Application layer instead)

**Example:**
```python
# ✅ CORRECT
from Application.UseCases import CreateInterviewUseCase
from Application.dtos import InterviewDTO
from Domain.Entities import Interview
from Core.config import settings
from fastapi import APIRouter

# ❌ WRONG
from Infrastructure.Db.models import InterviewModel  # NO! Use Application layer
```

### Core Layer
**Location:** `Core/`

**Purpose:** Shared configuration and utilities

**Allowed Imports:**
- Standard library
- External libraries (Pydantic, etc.)

**Can be imported by:** Any layer

## Data Flow Example

### Creating an Interview:

```
1. Presentation/Controllers/interview_controller.py
   ↓ (receives HTTP request)
   ↓ (creates DTO)
   
2. Application/UseCases/CreateInterviewUseCase
   ↓ (uses domain entity)
   ↓ (calls repository interface)
   
3. Application/Repositories/InterviewRepository (interface)
   ↓ (implemented by)
   
4. Infrastructure/Db/InterviewRepository (implementation)
   ↓ (uses SQLAlchemy models)
   ↓ (maps to domain entity)
   
5. Domain/Entities/Interview
   ← (returns domain entity)
```

## Key Principles

1. **Domain is Pure Business Logic**
   - No database, no frameworks, no external dependencies
   - Contains entities, enums, and business rules

2. **Application Orchestrates Domain**
   - Use cases coordinate domain entities
   - Defines repository interfaces (not implementations)

3. **Infrastructure Implements Details**
   - Implements repository interfaces from Application
   - Handles database, external APIs, file I/O

4. **Presentation Handles I/O**
   - HTTP requests/responses
   - Input validation
   - Calls use cases

## Mappers

**Location:** `Infrastructure/Db/mappers.py`

Mappers convert between:
- Domain Entities (UUID objects, enums) ↔ Database Models (string UUIDs, string values)

**Why needed:**
- Domain uses `UUID` objects, database uses strings
- Domain uses `InterviewStatus` enum, database stores strings
- Separation of concerns

## Repository Pattern

### Repository Interfaces
**Location:** `Application/Repositories/`
- Define contracts (what operations are available)
- Use domain entities (not database models)
- Abstract classes or protocols
- Example: `InterviewRepository` interface with methods like `create()`, `get_by_id()`, `update()`

**Why in Application?**
- Application layer defines what it needs
- Application doesn't care about implementation details
- Allows dependency inversion (Application depends on abstraction, not concrete implementation)

### Repository Implementations
**Location:** `Infrastructure/Db/` or `Infrastructure/Llm/`
- Implement the interfaces from Application
- Handle database/API details
- Use SQLAlchemy models
- Convert between models and entities using mappers
- Example: `SqlInterviewRepository` implements `InterviewRepository`

**Why in Infrastructure?**
- Infrastructure handles technical details (database, external APIs)
- Can be swapped without changing Application layer
- Depends on Application interfaces (dependency inversion)

## Services

### Application Services (Use Cases)
**Location:** `Application/UseCases/`
- Orchestrate domain entities
- Coordinate multiple repositories
- Implement business workflows
- Example: `CreateInterviewUseCase`, `GenerateQuestionUseCase`

**Why in Application?**
- Application-specific business logic
- Coordinates domain entities
- Uses repository interfaces

### Domain Services
**Location:** `Domain/` (if needed)
- Pure business logic that doesn't fit in a single entity
- No external dependencies
- Example: Complex validation rules, business calculations

**Note:** For this project, domain services may not be needed. Most logic fits in entities or use cases.

### Infrastructure Services
**Location:** `Infrastructure/Llm/` or `Infrastructure/`
- External service integrations
- API clients, file I/O, external APIs
- Example: `OpenAIService`, `AnthropicService` for LLM integration

**Why in Infrastructure?**
- Handles external concerns
- Can be swapped (different LLM providers)
- Implements interfaces if defined in Application

## Current Import Analysis

### Domain ✅
- Only standard library and internal Domain imports
- No violations

### Infrastructure ✅
- Imports Domain (correct)
- Imports Core (correct)
- No Presentation imports (correct)

### Application ✅
- Currently empty (will follow rules when implemented)

### Presentation ✅
- Currently empty (will follow rules when implemented)

## Summary

Always ask: "Does this import violate the dependency rule?"

- Domain → Any outer layer? ❌ NO
- Application → Infrastructure/Presentation? ❌ NO
- Infrastructure → Presentation? ❌ NO
- Outer → Inner? ✅ YES (allowed)

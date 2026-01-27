# AI Interviewer — Frontend

Vue.js 3 + TypeScript frontend for the AI Interview system.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Vue.js 3 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool |
| Vue Router | Navigation |

---

## Project Structure

```
src/
├── app/
│   ├── components/
│   │   ├── home/
│   │   │   ├── HomePage.vue        # Interview list + create
│   │   │   └── InterviewPage.vue   # Q&A flow
│   │   ├── shared/
│   │   │   ├── Alert.vue
│   │   │   ├── Button.vue
│   │   │   ├── Card.vue
│   │   │   └── LoadingSpinner.vue
│   │   └── summary/
│   │       └── SummaryView.vue     # Results display
│   ├── core/
│   │   ├── api.service.ts          # HTTP client
│   │   ├── app.config.ts           # Config
│   │   └── composables/
│   │       └── use-error-handler.composable.ts
│   ├── models/                     # TypeScript interfaces
│   │   ├── interview.model.ts
│   │   ├── question.model.ts
│   │   ├── answer.model.ts
│   │   └── summary.model.ts
│   └── services/                   # API calls
│       ├── interview.service.ts
│       ├── question.service.ts
│       ├── answer.service.ts
│       └── summary.service.ts
├── router/
│   └── index.ts
├── App.vue
└── main.ts
```

---

## Pages

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | HomePage | List interviews, create new |
| `/interview/:id` | InterviewPage | Answer questions sequentially |
| `/interview/:id/summary` | SummaryView | View analysis results |

---

## API Integration

Services wrap backend endpoints:

```typescript
// interview.service.ts
createInterview(topic: string)     // POST /interviews
getInterview(id: string)           // GET /interviews/{id}
deleteInterview(id: string)        // DELETE /interviews/{id}

// question.service.ts  
generateQuestion(interviewId)      // POST /interviews/{id}/questions
getQuestions(interviewId)          // GET /interviews/{id}/questions

// answer.service.ts
submitAnswer(interviewId, data)    // POST /interviews/{id}/answers

// summary.service.ts
generateSummary(interviewId)       // POST /interviews/{id}/summary
getSummary(interviewId)            // GET /interviews/{id}/summary
```
<template>
  <div class="interview-page">
    <div class="interview-header">
      <Button @click="goHome" variant="outline" size="sm">← Back to Home</Button>
      <h1>{{ interview?.topic || 'Loading...' }}</h1>
      <span v-if="interview" :class="['status-badge', `status-${interview.status}`]">
        {{ formatStatus(interview.status) }}
      </span>
    </div>

    <Alert
      v-if="error"
      type="error"
      dismissible
      @dismiss="clearError"
    >
      {{ error }}
    </Alert>

    <LoadingSpinner v-if="loadingInterview" message="Loading interview..." />

    <div v-else-if="interview" class="interview-content">
      <!-- Question Generation Section -->
      <Card v-if="interview.status !== 'completed'" class="question-section">
        <div v-if="currentQuestion" class="current-question">
          <div class="question-header">
            <span class="question-number">Question {{ currentQuestion.question_order }}</span>
            <span v-if="questions.length < maxQuestions" class="question-count">
              {{ questions.length }} / {{ maxQuestions }}
            </span>
          </div>
          <h2 class="question-text">{{ currentQuestion.text }}</h2>
          
          <div v-if="!currentAnswer" class="answer-form">
            <textarea
              v-model="answerText"
              placeholder="Type your answer here..."
              rows="6"
              class="answer-input"
              :disabled="submitting"
            ></textarea>
            <Button
              @click="submitAnswer"
              :loading="submitting"
              variant="primary"
              size="lg"
              :disabled="!answerText.trim()"
            >
              Submit Answer
            </Button>
          </div>

          <div v-else class="answer-display">
            <div class="answer-label">Your Answer:</div>
            <div class="answer-text">{{ currentAnswer.text }}</div>
          </div>
        </div>

        <div v-else-if="questions.length === 0" class="no-questions">
          <p>No questions yet. Generate your first question!</p>
          <Button
            @click="generateQuestion"
            :loading="generating"
            variant="primary"
            size="lg"
          >
            Generate First Question
          </Button>
        </div>

        <div v-else-if="questions.length >= maxQuestions && answers.length === questions.length" class="all-answered">
          <p>You've answered all questions! Generate a summary to see your results.</p>
          <Button
            @click="generateSummary"
            :loading="generatingSummary"
            variant="primary"
            size="lg"
          >
            Generate Summary
          </Button>
        </div>

        <div v-else class="next-question">
          <Button
            @click="generateQuestion"
            :loading="generating"
            variant="primary"
            size="lg"
            :disabled="questions.length >= maxQuestions || answers.length < questions.length"
          >
            {{ questions.length === 0 ? 'Generate First Question' : 'Generate Next Question' }}
          </Button>
        </div>
      </Card>

      <!-- Summary Section -->
      <div v-if="interview.status === 'completed' && summary" class="summary-section">
        <Card>
          <h2>Interview Summary</h2>
          <SummaryView :summary="summary" />
        </Card>
      </div>

      <!-- Questions & Answers History -->
      <div v-if="questions.length > 0" class="qa-history">
        <h3>Questions & Answers</h3>
        <Card
          v-for="(question, index) in questions"
          :key="question.question_id"
          class="qa-item"
        >
          <div class="qa-question">
            <span class="qa-number">Q{{ question.question_order }}:</span>
            <span>{{ question.text }}</span>
          </div>
          <div v-if="getAnswerForQuestion(question.question_id)" class="qa-answer">
            <span class="qa-label">A:</span>
            <span>{{ getAnswerForQuestion(question.question_id)?.text }}</span>
          </div>
          <div v-else class="qa-no-answer">Not answered yet</div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { interviewService } from '../../services/interview.service';
import { questionService } from '../../services/question.service';
import { answerService } from '../../services/answer.service';
import { summaryService } from '../../services/summary.service';
import { useErrorHandler } from '../../core/composables/use-error-handler.composable';
import type { Interview } from '../../models/interview.model';
import type { Question } from '../../models/question.model';
import type { Answer } from '../../models/answer.model';
import type { InterviewSummary } from '../../models/summary.model';
import { appConfig } from '../../core/app.config';
import Button from '../shared/Button.vue';
import Card from '../shared/Card.vue';
import LoadingSpinner from '../shared/LoadingSpinner.vue';
import Alert from '../shared/Alert.vue';
import SummaryView from '../summary/SummaryView.vue';

const router = useRouter();
const route = useRoute();
const { error, handleError, clearError } = useErrorHandler();

const interviewId = route.params.id as string;

const interview = ref<Interview | null>(null);
const questions = ref<Question[]>([]);
const answers = ref<Answer[]>([]);
const summary = ref<InterviewSummary | null>(null);
const loadingInterview = ref(false);
const generating = ref(false);
const submitting = ref(false);
const generatingSummary = ref(false);
const answerText = ref('');

const maxQuestions = appConfig.maxQuestionsPerInterview;

const currentQuestion = computed(() => {
  if (questions.value.length === 0) return null;
  const answeredCount = answers.value.length;
  if (answeredCount < questions.value.length) {
    return questions.value[answeredCount];
  }
  return null;
});

const currentAnswer = computed(() => {
  if (!currentQuestion.value) return null;
  return getAnswerForQuestion(currentQuestion.value.question_id);
});

const loadInterview = async (): Promise<void> => {
  loadingInterview.value = true;
  clearError();
  try {
    interview.value = await interviewService.getById(interviewId);
    await Promise.all([
      loadQuestions(),
      loadAnswers(),
      interview.value.status === 'completed' ? loadSummary() : Promise.resolve(),
    ]);
  } catch (err) {
    handleError(err);
  } finally {
    loadingInterview.value = false;
  }
};

const loadQuestions = async (): Promise<void> => {
  try {
    questions.value = await questionService.getByInterviewId(interviewId);
  } catch (err) {
    handleError(err);
  }
};

const loadAnswers = async (): Promise<void> => {
  try {
    answers.value = await answerService.getByInterviewId(interviewId);
  } catch (err) {
    handleError(err);
  }
};

const loadSummary = async (): Promise<void> => {
  try {
    summary.value = await summaryService.getByInterviewId(interviewId);
  } catch {
  }
};

const generateQuestion = async (): Promise<void> => {
  generating.value = true;
  clearError();
  try {
    await questionService.generate({ interview_id: interviewId });
    await loadQuestions();
    await loadInterview();
  } catch (err) {
    handleError(err);
  } finally {
    generating.value = false;
  }
};

const submitAnswer = async (): Promise<void> => {
  if (!currentQuestion.value || !answerText.value.trim()) return;
  
  submitting.value = true;
  clearError();
  try {
    await answerService.submit({
      question_id: currentQuestion.value.question_id,
      interview_id: interviewId,
      text: answerText.value.trim(),
    });
    answerText.value = '';
    await loadAnswers();
    await loadInterview();
  } catch (err) {
    handleError(err);
  } finally {
    submitting.value = false;
  }
};

const generateSummary = async (): Promise<void> => {
  generatingSummary.value = true;
  clearError();
  try {
    summary.value = await summaryService.generate(interviewId);
    await loadInterview();
    setTimeout(() => {
      document.querySelector('.summary-section')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  } catch (err) {
    handleError(err);
  } finally {
    generatingSummary.value = false;
  }
};

const getAnswerForQuestion = (questionId: string): Answer | undefined => {
  return answers.value.find(a => a.question_id === questionId);
};

const formatStatus = (status: string): string => {
  return status.split('_').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' ');
};

const goHome = (): void => {
  router.push('/');
};

onMounted(() => {
  loadInterview();
});
</script>

<style scoped>
.interview-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
}

.interview-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.interview-header h1 {
  flex: 1;
  font-size: 2rem;
  color: #1f2937;
  margin: 0;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-not_started {
  background: #e5e7eb;
  color: #374151;
}

.status-in_progress {
  background: #dbeafe;
  color: #1e40af;
}

.status-completed {
  background: #d1fae5;
  color: #065f46;
}

.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.interview-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.question-section {
  margin-bottom: 2rem;
}

.current-question {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-number {
  font-weight: 600;
  color: #667eea;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.question-count {
  color: #6b7280;
  font-size: 0.875rem;
}

.question-text {
  font-size: 1.5rem;
  color: #1f2937;
  margin: 0;
  line-height: 1.6;
}

.answer-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.answer-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.2s;
}

.answer-input:focus {
  outline: none;
  border-color: #667eea;
}

.answer-input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

.answer-display {
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border-left: 4px solid #667eea;
}

.answer-label {
  font-weight: 600;
  color: #6b7280;
  font-size: 0.875rem;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.answer-text {
  color: #1f2937;
  line-height: 1.6;
  white-space: pre-wrap;
}

.no-questions,
.all-answered,
.next-question {
  text-align: center;
  padding: 2rem;
}

.no-questions p,
.all-answered p {
  color: #6b7280;
  margin-bottom: 1.5rem;
  font-size: 1.125rem;
}

.qa-history {
  margin-top: 2rem;
}

.qa-history h3 {
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.qa-item {
  margin-bottom: 1rem;
}

.qa-question {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  font-weight: 500;
  color: #1f2937;
}

.qa-number {
  color: #667eea;
  font-weight: 600;
}

.qa-answer {
  display: flex;
  gap: 0.75rem;
  color: #4b5563;
  line-height: 1.6;
  white-space: pre-wrap;
}

.qa-label {
  color: #10b981;
  font-weight: 600;
}

.qa-no-answer {
  color: #9ca3af;
  font-style: italic;
}

.summary-section {
  margin-top: 2rem;
}
</style>

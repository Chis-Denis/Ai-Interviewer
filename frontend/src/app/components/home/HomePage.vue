<template>
  <div class="home-page">
    <div class="home-header">
      <h1>AI Interviewer</h1>
      <p class="subtitle">Conduct intelligent interviews with AI-powered questions</p>
    </div>

    <div class="home-actions">
      <div class="create-interview-card">
        <h2>Start New Interview</h2>
        <form @submit.prevent="createInterview" class="create-form">
          <input
            v-model="newTopic"
            type="text"
            placeholder="Enter interview topic (e.g., Python, System Design, React...)"
            class="topic-input"
            required
            :disabled="creating"
          />
          <Button type="submit" :loading="creating" variant="primary" size="lg">
            Create Interview
          </Button>
        </form>
      </div>
    </div>

    <Alert
      v-if="error"
      type="error"
      dismissible
      @dismiss="clearError"
    >
      {{ error }}
    </Alert>

    <div class="interviews-section">
      <h2>Your Interviews</h2>
      <LoadingSpinner v-if="loading" message="Loading interviews..." />
      <div v-else-if="interviews.length === 0" class="empty-state">
        <p>No interviews yet. Create your first interview above!</p>
      </div>
      <div v-else class="interviews-grid">
        <Card
          v-for="interview in interviews"
          :key="interview.interview_id"
          hover
          class="interview-card"
        >
          <div class="interview-card-header">
            <h3>{{ interview.topic }}</h3>
            <span :class="['status-badge', `status-${interview.status}`]">
              {{ formatStatus(interview.status) }}
            </span>
          </div>
          <p class="interview-date">
            Created: {{ formatDate(interview.created_at) }}
          </p>
          <div class="interview-actions">
            <Button
              @click="viewInterview(interview.interview_id)"
              variant="primary"
              size="sm"
            >
              {{ interview.status === 'completed' ? 'View Summary' : 'Continue' }}
            </Button>
            <Button
              @click="deleteInterview(interview.interview_id)"
              variant="danger"
              size="sm"
            >
              Delete
            </Button>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { interviewService } from '../../services/interview.service';
import { useErrorHandler } from '../../core/composables/use-error-handler.composable';
import type { Interview } from '../../models/interview.model';
import Button from '../shared/Button.vue';
import Card from '../shared/Card.vue';
import LoadingSpinner from '../shared/LoadingSpinner.vue';
import Alert from '../shared/Alert.vue';

const router = useRouter();
const { error, handleError, clearError } = useErrorHandler();

const interviews = ref<Interview[]>([]);
const loading = ref(false);
const creating = ref(false);
const newTopic = ref('');

const loadInterviews = async (): Promise<void> => {
  loading.value = true;
  clearError();
  try {
    interviews.value = await interviewService.getAll();
  } catch (err) {
    handleError(err);
  } finally {
    loading.value = false;
  }
};

const createInterview = async (): Promise<void> => {
  if (!newTopic.value.trim()) return;
  
  creating.value = true;
  clearError();
  try {
    const interview = await interviewService.create({ topic: newTopic.value.trim() });
    newTopic.value = '';
    await loadInterviews();
    router.push(`/interview/${interview.interview_id}`);
  } catch (err) {
    handleError(err);
  } finally {
    creating.value = false;
  }
};

const viewInterview = (interviewId: string): void => {
  router.push(`/interview/${interviewId}`);
};

const deleteInterview = async (interviewId: string): Promise<void> => {
  if (!confirm('Are you sure you want to delete this interview?')) return;
  
  try {
    await interviewService.delete(interviewId);
    await loadInterviews();
  } catch (err) {
    handleError(err);
  }
};

const formatStatus = (status: string): string => {
  return status.split('_').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join(' ');
};

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
};

onMounted(() => {
  loadInterviews();
});
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.home-header {
  text-align: center;
  margin-bottom: 3rem;
}

.home-header h1 {
  font-size: 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #6b7280;
  font-size: 1.125rem;
}

.home-actions {
  margin-bottom: 3rem;
}

.create-interview-card {
  background: white;
  border-radius: 0.75rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.create-interview-card h2 {
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.create-form {
  display: flex;
  gap: 1rem;
}

.topic-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.topic-input:focus {
  outline: none;
  border-color: #667eea;
}

.topic-input:disabled {
  background: #f3f4f6;
  cursor: not-allowed;
}

.interviews-section h2 {
  margin-bottom: 1.5rem;
  color: #1f2937;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #6b7280;
}

.interviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.interview-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.interview-card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  gap: 1rem;
}

.interview-card-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
  flex: 1;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
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

.interview-date {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.interview-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: auto;
}
</style>

<template>
  <div class="summary-view">
    <!-- Overall Scores -->
    <div class="scores-section">
      <h3>Performance Scores</h3>
      <div class="scores-grid">
        <div class="score-card">
          <div class="score-header">
            <div class="score-label">Clarity</div>
            <button class="info-button" @click="toggleExplanation('clarity')">
              ℹ
            </button>
          </div>
          <div class="score-value">{{ formatScore(summary.clarity_score) }}</div>
          <div class="score-bar">
            <div
              class="score-fill"
              :style="{ width: `${(summary.clarity_score || 0) * 100}%` }"
            ></div>
          </div>
        </div>
        <div class="score-card">
          <div class="score-header">
            <div class="score-label">Confidence</div>
            <button class="info-button" @click="toggleExplanation('confidence')">
              ℹ
            </button>
          </div>
          <div class="score-value">{{ formatScore(summary.confidence_score) }}</div>
          <div class="score-bar">
            <div
              class="score-fill"
              :style="{ width: `${(summary.confidence_score || 0) * 100}%` }"
            ></div>
          </div>
        </div>
        <div class="score-card">
          <div class="score-header">
            <div class="score-label">Consistency</div>
            <button class="info-button" @click="toggleExplanation('consistency')">
              ℹ
            </button>
          </div>
          <div class="score-value">{{ formatScore(summary.consistency_score) }}</div>
          <div class="score-bar">
            <div
              class="score-fill"
              :style="{ width: `${(summary.consistency_score || 0) * 100}%` }"
            ></div>
          </div>
        </div>
        <div class="score-card highlight">
          <div class="score-header">
            <div class="score-label">Final Grade</div>
            <button class="info-button" @click="toggleExplanation('usefulness')">
              ℹ
            </button>
          </div>
          <div class="score-value">{{ formatScore(summary.overall_usefulness) }}</div>
          <div class="score-bar">
            <div
              class="score-fill highlight"
              :style="{ width: `${(summary.overall_usefulness || 0) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sentiment -->
    <div v-if="summary.sentiment_score !== null" class="sentiment-section">
      <div class="section-header">
        <h3>Sentiment Analysis</h3>
        <button class="info-button" @click="toggleExplanation('sentiment')">
          ℹ
        </button>
      </div>
        <div class="sentiment-display">
        <span class="sentiment-label">{{ summary.sentiment_label || 'Neutral' }}</span>
        <div class="sentiment-bar">
          <div
            class="sentiment-fill"
            :class="getSentimentClass(summary.sentiment_score)"
            :style="{ width: `${(summary.sentiment_score || 0) * 100}%` }"
          ></div>
        </div>
        <span class="sentiment-score">{{ formatScore(summary.sentiment_score) }}</span>
      </div>
    </div>

    <!-- Themes -->
    <div class="themes-section">
      <h3>Key Themes</h3>
      <div class="themes-list">
        <div
          v-for="(theme, index) in summary.themes"
          :key="index"
          class="theme-item"
        >
          <span class="theme-number">{{ index + 1 }}</span>
          <span class="theme-text">{{ theme }}</span>
        </div>
      </div>
    </div>

    <!-- Key Points -->
    <div class="key-points-section">
      <h3>Key Points</h3>
      <ul class="key-points-list">
        <li v-for="(point, index) in summary.key_points" :key="index">
          {{ point }}
        </li>
      </ul>
    </div>

    <!-- Strengths -->
    <div v-if="summary.strengths && summary.strengths.length > 0" class="strengths-section">
      <h3>Strengths</h3>
      <ul class="strengths-list">
        <li v-for="(strength, index) in summary.strengths" :key="index">
          <span class="strength-icon">✓</span>
          {{ strength }}
        </li>
      </ul>
    </div>

    <!-- Weaknesses -->
    <div v-if="summary.weaknesses && summary.weaknesses.length > 0" class="weaknesses-section">
      <h3>Areas for Improvement</h3>
      <ul class="weaknesses-list">
        <li v-for="(weakness, index) in summary.weaknesses" :key="index">
          <span class="weakness-icon">→</span>
          {{ weakness }}
        </li>
      </ul>
    </div>

    <!-- Missing Information -->
    <div v-if="summary.missing_information && summary.missing_information.length > 0" class="missing-section">
      <h3>Missing Information</h3>
      <ul class="missing-list">
        <li v-for="(item, index) in summary.missing_information" :key="index">
          <span class="missing-icon">ℹ</span>
          {{ item }}
        </li>
      </ul>
    </div>

    <!-- Full Summary Text -->
    <div v-if="summary.full_summary_text" class="full-summary-section">
      <h3>Full Summary</h3>
      <div class="full-summary-text">
        {{ summary.full_summary_text }}
      </div>
    </div>

    <!-- Explanation Modal -->
    <div v-if="activeExplanation" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ getExplanationTitle(activeExplanation) }}</h3>
          <button class="modal-close" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div v-html="getExplanationContent(activeExplanation)"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { InterviewSummary } from '../../models/summary.model';

defineProps<{
  summary: InterviewSummary;
}>();

const activeExplanation = ref<string | null>(null);

const explanations = {
  clarity: {
    title: 'Clarity Score',
    content: `
      <p><strong>What it measures:</strong> How clear and well-structured your answers are.</p>
      <p><strong>How it's calculated:</strong></p>
      <ul>
        <li><strong>Automatic 0%:</strong> Manipulation attempts (asking for help, emotional manipulation) or gibberish/random text</li>
        <li>Base score starts at 50% for answers with 15+ words</li>
        <li>+20% for 2+ sentences, +10% for 3+ sentences</li>
        <li>+15% for structure indicators (because, since, first, second, etc.)</li>
        <li>+5% for reasonable sentence length (8-30 words per sentence)</li>
        <li><strong>Harsh penalties:</strong> &lt;5 words = 2%, &lt;10 words = 8%, &lt;15 words = 20%</li>
      </ul>
    `,
  },
  confidence: {
    title: 'Confidence Score',
    content: `
      <p><strong>What it measures:</strong> How complete and detailed your answers are, showing depth of knowledge.</p>
      <p><strong>How it's calculated:</strong></p>
      <ul>
        <li><strong>Automatic 0%:</strong> Manipulation attempts or gibberish/random text</li>
        <li>Base score = Completeness × 50%</li>
        <li>Completeness: 50+ words = 100%, 30+ = 80%, 20+ = 60%, 15+ = 40%, 10+ = 25%, &lt;10 = 5%</li>
        <li>+25% for 40+ words, +15% for 25+ words, +5% for 15+ words</li>
        <li>+20% for including examples</li>
        <li>+15% for including metrics/numbers</li>
        <li><strong>Penalties:</strong> Non-technical content reduces score by 60%, &lt;5 words = 0%, &lt;10 words = 5%, &lt;15 words = 12%</li>
      </ul>
    `,
  },
  consistency: {
    title: 'Consistency Score',
    content: `
      <p><strong>What it measures:</strong> How consistent your answer lengths are across all questions.</p>
      <p><strong>How it's calculated:</strong></p>
      <ul>
        <li><strong>Automatic 0%:</strong> If 50%+ of answers contain manipulation or gibberish</li>
        <li><strong>Harsh penalties:</strong> Average length &lt;5 words = 5%, &lt;10 words = 15%</li>
        <li>Measures the variation in word count across all your answers</li>
        <li>Uses coefficient of variation (standard deviation / average length)</li>
        <li>&lt;20% variation = 100% (very consistent)</li>
        <li>20-40% variation = 80%</li>
        <li>40-60% variation = 60%</li>
        <li>60-80% variation = 40%</li>
        <li>&gt;80% variation = 20% (inconsistent)</li>
      </ul>
    `,
  },
  usefulness: {
    title: 'Overall Usefulness',
    content: `
      <p><strong>What it measures:</strong> Overall quality and usefulness of your interview responses.</p>
      <p><strong>How it's calculated:</strong></p>
      <ul>
        <li>Weighted average of Clarity, Confidence, and Consistency scores</li>
        <li>Formula: (Clarity × 40%) + (Confidence × 40%) + (Consistency × 20%)</li>
        <li>Clarity and Confidence each contribute 40%, Consistency contributes 20%</li>
        <li>Provides a balanced view of your overall performance</li>
      </ul>
    `,
  },
  sentiment: {
    title: 'Sentiment Analysis',
    content: `
      <p><strong>What it measures:</strong> The overall quality and tone of your interview responses.</p>
      <p><strong>How it's calculated:</strong></p>
      <ul>
        <li>Analyzed by AI using natural language processing</li>
        <li>Score ranges from 0% (negative) to 100% (positive)</li>
        <li>&gt;60% = Positive (clear, confident, experienced answers)</li>
        <li>40-60% = Neutral (basic understanding, acceptable)</li>
        <li>&lt;40% = Negative (unclear, shallow, or incorrect)</li>
        <li>Based on answer clarity, depth, and demonstrated knowledge</li>
      </ul>
    `,
  },
};

const toggleExplanation = (score: string): void => {
  activeExplanation.value = activeExplanation.value === score ? null : score;
};

const closeModal = (): void => {
  activeExplanation.value = null;
};

const getExplanationTitle = (score: string): string => {
  return explanations[score as keyof typeof explanations]?.title || '';
};

const getExplanationContent = (score: string): string => {
  return explanations[score as keyof typeof explanations]?.content || '';
};

const formatScore = (score: number | null): string => {
  if (score === null) return 'N/A';
  return (score * 100).toFixed(0) + '%';
};

const getSentimentClass = (score: number | null): string => {
  if (score === null) return 'neutral';
  if (score > 0.6) return 'positive';
  if (score < 0.4) return 'negative';
  return 'neutral';
};
</script>

<style scoped>
.summary-view {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

h3 {
  margin: 0 0 1rem 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.scores-section {
  margin-bottom: 1rem;
}

.scores-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  align-items: start;
}

@media (max-width: 1024px) {
  .scores-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .scores-grid {
    grid-template-columns: 1fr;
  }
}

.score-card {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 0.5rem;
  border: 2px solid #e5e7eb;
  position: relative;
  display: flex;
  flex-direction: column;
}

.score-card.highlight {
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-color: #667eea;
}

.score-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.score-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-button {
  background: #e0e7ff;
  border: none;
  color: #667eea;
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0;
  border-radius: 50%;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  font-weight: 600;
  flex-shrink: 0;
}

.info-button:hover {
  background: #c7d2fe;
  transform: scale(1.05);
}


.score-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.75rem;
}

.score-bar {
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
}

.score-fill.highlight {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
}

.sentiment-section {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.sentiment-display {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.sentiment-label {
  font-weight: 600;
  color: #1f2937;
  min-width: 100px;
  text-transform: capitalize;
}

.sentiment-bar {
  flex: 1;
  height: 12px;
  background: #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.sentiment-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.sentiment-fill.positive {
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.sentiment-fill.negative {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.sentiment-fill.neutral {
  background: linear-gradient(90deg, #6b7280 0%, #4b5563 100%);
}

.sentiment-score {
  font-weight: 600;
  color: #6b7280;
  min-width: 60px;
  text-align: right;
}

.themes-section,
.key-points-section,
.strengths-section,
.weaknesses-section,
.missing-section,
.full-summary-section {
  padding: 1.5rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.themes-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.theme-item {
  display: flex;
  align-items: start;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
  border-left: 4px solid #667eea;
}

.theme-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  flex-shrink: 0;
}

.theme-text {
  flex: 1;
  color: #1f2937;
  line-height: 1.6;
}

.key-points-list,
.strengths-list,
.weaknesses-list,
.missing-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.key-points-list li,
.strengths-list li,
.weaknesses-list li,
.missing-list li {
  padding: 0.75rem 1rem;
  background: white;
  border-radius: 0.5rem;
  color: #1f2937;
  line-height: 1.6;
  display: flex;
  align-items: start;
  gap: 0.75rem;
}

.strengths-list li {
  border-left: 4px solid #10b981;
}

.weaknesses-list li {
  border-left: 4px solid #f59e0b;
}

.missing-list li {
  border-left: 4px solid #3b82f6;
}

.strength-icon,
.weakness-icon,
.missing-icon {
  font-weight: 600;
  flex-shrink: 0;
}

.strength-icon {
  color: #10b981;
}

.weakness-icon {
  color: #f59e0b;
}

.missing-icon {
  color: #3b82f6;
}

.full-summary-text {
  color: #1f2937;
  line-height: 1.8;
  white-space: pre-wrap;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

.modal-content {
  background: white;
  border-radius: 0.75rem;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: slideUp 0.2s ease-out;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  transition: color 0.2s;
}

.modal-close:hover {
  color: #1f2937;
}

.modal-body {
  padding: 1.5rem;
  color: #374151;
  line-height: 1.6;
}

.modal-body p {
  margin: 0 0 1rem 0;
}

.modal-body p:last-of-type {
  margin-bottom: 0.75rem;
}

.modal-body strong {
  color: #1f2937;
  font-weight: 600;
}

.modal-body ul {
  margin: 0.75rem 0 0 1.5rem;
  padding: 0;
  color: #4b5563;
}

.modal-body li {
  margin-bottom: 0.5rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

<template>
  <div :class="['alert', `alert-${type}`]" v-if="show">
    <div class="alert-content">
      <span class="alert-icon">{{ icon }}</span>
      <div class="alert-message">
        <slot />
      </div>
      <button v-if="dismissible" class="alert-close" @click="handleDismiss">×</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const props = defineProps<{
  type?: 'success' | 'error' | 'warning' | 'info';
  dismissible?: boolean;
}>();

const emit = defineEmits<{
  dismiss: [];
}>();

const show = ref(true);

const icons = {
  success: '✓',
  error: '✕',
  warning: '⚠',
  info: 'ℹ',
};

const icon = computed(() => icons[props.type || 'info']);

const handleDismiss = (): void => {
  show.value = false;
  emit('dismiss');
};
</script>

<style scoped>
.alert {
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.alert-success {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #6ee7b7;
}

.alert-error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fca5a5;
}

.alert-warning {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #fcd34d;
}

.alert-info {
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #93c5fd;
}

.alert-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.alert-icon {
  font-size: 1.25rem;
  font-weight: bold;
}

.alert-message {
  flex: 1;
}

.alert-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  padding: 0;
  width: 1.5rem;
  height: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.alert-close:hover {
  opacity: 1;
}
</style>

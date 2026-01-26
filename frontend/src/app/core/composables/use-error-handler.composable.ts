import { ref, type Ref } from 'vue';
import { ApiError } from '../api.service';

export function useErrorHandler() {
  const error: Ref<string | null> = ref(null);

  const handleError = (err: unknown): void => {
    if (err instanceof ApiError) {
      error.value = err.message;
    } else if (err instanceof Error) {
      error.value = err.message;
    } else {
      error.value = 'An unexpected error occurred';
    }
  };

  const clearError = (): void => {
    error.value = null;
  };

  return {
    error,
    handleError,
    clearError,
  };
}

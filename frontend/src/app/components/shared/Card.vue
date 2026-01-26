<template>
  <div :class="['card', { 'card-hover': hover }]">
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hover?: boolean;
}>();
</script>

<style scoped>
.card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.card-hover:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}
</style>

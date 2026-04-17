<script setup>
defineProps({
  eyebrow: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  metrics: {
    type: Array,
    default: () => [],
  },
});

const statuses = [
  {
    label: 'Do zrobienia',
    color: 'var(--amber-500)',
  },
  {
    label: 'W toku',
    color: 'var(--azure-500)',
  },
  {
    label: 'Gotowe',
    color: 'var(--jade-500)',
  },
];
</script>

<template>
  <section class="auth-showcase card card--dark">
    <p class="eyebrow">{{ eyebrow }}</p>
    <h1>{{ title }}</h1>
    <p class="auth-showcase__copy">
      {{ description }}
    </p>

    <div class="auth-showcase__stats">
      <article
        v-for="metric in metrics"
        :key="metric.label"
        class="auth-showcase__metric"
      >
        <strong>{{ metric.value }}</strong>
        <span>{{ metric.label }}</span>
      </article>
    </div>

    <div class="auth-showcase__board">
      <div class="auth-showcase__board-top">
        <strong>Szybki przeglad sprintu</strong>
        <span>Live preview</span>
      </div>

      <div class="auth-showcase__lane">
        <div
          v-for="status in statuses"
          :key="status.label"
          class="auth-showcase__status"
        >
          <span :style="{ backgroundColor: status.color }"></span>
          {{ status.label }}
        </div>
      </div>

      <div class="auth-showcase__task">
        <div>
          <strong>Nowy onboarding klienta</strong>
          <p>Checklisty, deadline i komentarze w jednym miejscu.</p>
        </div>
        <small>04 zadania</small>
      </div>
    </div>
  </section>
</template>

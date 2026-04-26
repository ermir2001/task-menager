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
  <section
    class="relative overflow-hidden rounded-[34px] border border-slate-700/40 bg-[linear-gradient(160deg,#111827,#1e293b)] p-6 text-snow-50 shadow-[0_28px_80px_rgba(15,23,42,0.34)] md:p-8"
  >
    <div
      class="pointer-events-none absolute -right-16 -bottom-16 h-56 w-56 rounded-full bg-azure-500/25 blur-3xl"
    ></div>

    <p class="text-xs font-semibold uppercase tracking-[0.32em] text-slate-400">
      {{ eyebrow }}
    </p>
    <h1 class="mt-4 max-w-xl font-display text-4xl leading-tight md:text-[2.8rem]">
      {{ title }}
    </h1>
    <p class="mt-4 max-w-2xl text-sm leading-7 text-white/72 md:text-base">
      {{ description }}
    </p>

    <div class="mt-8 flex flex-wrap gap-3">
      <article
        v-for="metric in metrics"
        :key="metric.label"
        class="min-w-[140px] rounded-[20px] border border-white/10 bg-white/8 px-4 py-4"
      >
        <strong class="block font-display text-lg text-white">{{ metric.value }}</strong>
        <span class="mt-1 block text-sm text-white/65">{{ metric.label }}</span>
      </article>
    </div>

    <div class="mt-8 rounded-[24px] border border-white/10 bg-white/6 p-5">
      <div class="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <strong class="text-lg text-white">Szybki przeglad sprintu</strong>
        <span class="text-sm text-white/55">Live preview</span>
      </div>

      <div class="mt-5 flex flex-wrap gap-3">
        <div
          v-for="status in statuses"
          :key="status.label"
          class="inline-flex items-center gap-2 rounded-full bg-white/8 px-4 py-2.5 text-sm text-white/82"
        >
          <span
            class="h-2.5 w-2.5 rounded-full"
            :style="{ backgroundColor: status.color }"
          ></span>
          {{ status.label }}
        </div>
      </div>

      <div
        class="mt-5 flex flex-col gap-4 rounded-[20px] border border-white/10 bg-slate-950/30 p-4 md:flex-row md:items-center md:justify-between"
      >
        <div>
          <strong class="block text-base text-white">Nowy onboarding klienta</strong>
          <p class="mt-1 text-sm leading-6 text-white/65">
            Checklisty, deadline i komentarze w jednym miejscu.
          </p>
        </div>
        <small class="text-sm text-white/55">04 zadania</small>
      </div>
    </div>
  </section>
</template>

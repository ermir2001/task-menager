<script setup>
import { RouterLink } from 'vue-router';

const footerLinks = [
  { label: 'Glowna', to: '/' },
  { label: 'Logowanie', to: '/login' },
  { label: 'Rejestracja', to: '/register' },
];

const techStack = ['Vue 3', 'Vite', 'Tailwind CSS', 'FastAPI'];
</script>

<template>
  <footer
    class="mt-10 rounded-[30px] border border-white/60 bg-white/78 px-6 py-7 shadow-[0_20px_50px_rgba(15,23,42,0.1)] backdrop-blur-xl md:px-8"
  >
    <div class="grid gap-8 lg:grid-cols-[1.2fr_0.8fr_0.8fr]">
      <div class="space-y-3">
        <div class="inline-flex items-center gap-3">
          <span
            class="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-azure-500 to-royal-600 text-sm font-bold text-white"
          >
            TM
          </span>
          <div>
            <strong class="block font-display text-base text-ink-950">Task Manager</strong>
            <span class="block text-sm text-slate-600">Interfejs do pracy nad zadaniami i projektami</span>
          </div>
        </div>

        <p class="max-w-xl text-sm leading-7 text-slate-600 md:text-base">
          Budujemy frontend krok po kroku: najpierw wejscie i auth, potem dashboard,
          taski, projekty i cala logika pracy zespolowej.
        </p>
      </div>

      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.28em] text-royal-600">
          Stack
        </p>
        <div class="mt-4 flex flex-wrap gap-2">
          <span
            v-for="item in techStack"
            :key="item"
            class="rounded-full border border-slate-200/80 bg-slate-900/4 px-3 py-2 text-sm text-slate-700"
          >
            {{ item }}
          </span>
        </div>
      </div>
    </div>

    <div
      class="mt-8 flex flex-col gap-3 border-t border-slate-200/70 pt-5 text-sm text-slate-500 md:flex-row md:items-center md:justify-between"
    >
      <span>Task Manager UI - 2026</span>
      <span>Projekt rozwijany lokalnie w Vue, Tailwind i FastAPI</span>
    </div>
  </footer>
</template>

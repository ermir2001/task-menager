<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';

import WorkspaceDashboard from '../components/WorkspaceDashboard.vue';

const props = defineProps({
  auth: {
    type: Object,
    required: true,
  },
});

const isAuthenticated = computed(() => Boolean(props.auth.state.token));
const userName = computed(() => {
  const user = props.auth.state.user;

  if (!user) {
    return 'zespolu';
  }

  return user.first_name || user.username;
});

const highlights = [
  {
    title: 'Widok sprintu bez chaosu',
    copy:
      'Sekcje, priorytety i statusy sa czytelne od pierwszego wejscia. Bez przechodzenia przez piec ekranow.',
  },
  {
    title: 'Logowanie gotowe pod API',
    copy:
      'Frontend jest przygotowany pod Twoje endpointy FastAPI, wiec mozemy szybko przejsc do dashboardu i zadan.',
  },
  {
    title: 'Paleta z charakterem',
    copy:
      'Ciemne granaty i dwa odcienie niebieskiego robia baze, a zielony, pomarancz i czerwien zostaly na statusy.',
  },
];

const quickFacts = [
  {
    value: '03',
    label: 'gotowe ekrany startowe',
  },
  {
    value: 'Vue + FastAPI',
    label: 'jeden front, gotowy kontrakt auth',
  },
  {
    value: 'Tailwind',
    label: 'nowy kierunek stylowania od tej iteracji',
  },
];

const boardColumns = [
  {
    title: 'Plan',
    tone: 'var(--snow-50)',
    tasks: ['Kickoff projektu', 'Makiety klienta'],
  },
  {
    title: 'W toku',
    tone: 'var(--azure-500)',
    tasks: ['API auth', 'Widok glowny'],
  },
  {
    title: 'Review',
    tone: 'var(--royal-600)',
    tasks: ['Testy formularzy', 'Drobne poprawki UX'],
  },
];
</script>

<template>
  <WorkspaceDashboard v-if="isAuthenticated" :auth="props.auth" />

  <div v-else class="space-y-7">
    <section
      class="overflow-hidden rounded-[36px] border border-white/60 bg-white/78 px-6 py-8 shadow-[0_24px_70px_rgba(15,23,42,0.12)] backdrop-blur-xl md:px-10 md:py-12"
    >
      <p class="text-xs font-semibold uppercase tracking-[0.34em] text-royal-600">
        Vue frontend dla task managera
      </p>

      <div class="mt-5 max-w-none space-y-6">
        <h1
          class="max-w-none font-display text-4xl leading-[0.95] text-ink-950 sm:text-5xl lg:text-6xl xl:text-[5.3rem]"
        >
          Task Manager dla
          <span class="text-royal-600">{{ userName }}</span>
          z mocnym wejsciem, prostym auth i tekstem rozlanym na cala szerokosc
          pierwszego ekranu.
        </h1>

        <p class="max-w-5xl text-base leading-8 text-slate-600 md:text-lg">
          Uproscilem gore strony, wywalilem przyciski z headera i przesunalem
          glowny ciezar na szeroki hero. Ten ekran ma teraz bardziej landingowy
          charakter: najpierw komunikat i klimat aplikacji, a dopiero nizej
          konkretne sekcje i wejscie do logowania albo rejestracji.
        </p>
      </div>

      <div class="mt-8 flex flex-wrap gap-4">
        <RouterLink
          class="inline-flex items-center justify-center rounded-2xl bg-gradient-to-br from-azure-500 to-royal-600 px-6 py-3.5 text-sm font-semibold text-white shadow-[0_16px_30px_rgba(37,99,235,0.24)] transition hover:-translate-y-0.5"
          to="/register"
        >
          Stworz konto
        </RouterLink>
        <RouterLink
          class="inline-flex items-center justify-center rounded-2xl border border-slate-900/8 bg-white/85 px-6 py-3.5 text-sm font-semibold text-ink-950 transition hover:-translate-y-0.5 hover:bg-white"
          to="/login"
        >
          Zaloguj sie
        </RouterLink>
      </div>

      <div class="mt-10 grid gap-4 md:grid-cols-3">
        <article
          v-for="fact in quickFacts"
          :key="fact.label"
          class="rounded-[22px] border border-slate-200/70 bg-white/80 px-5 py-4"
        >
          <strong class="block font-display text-lg text-ink-950">{{ fact.value }}</strong>
          <span class="mt-1 block text-sm leading-6 text-slate-600">{{ fact.label }}</span>
        </article>
      </div>
    </section>

    <section class="grid gap-6 xl:grid-cols-[1.35fr_0.65fr]">
      <article
        class="overflow-hidden rounded-[34px] border border-slate-700/40 bg-[linear-gradient(160deg,#111827,#1e293b)] p-6 text-snow-50 shadow-[0_28px_80px_rgba(15,23,42,0.34)] md:p-8"
      >
        <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
              Board preview
            </p>
            <h2 class="mt-2 font-display text-3xl leading-tight">
              Widok zadaniowy zostawiam nizej, zeby tekst na gorze mogl oddychac.
            </h2>
          </div>
          <span
            class="inline-flex items-center rounded-full bg-jade-500/18 px-4 py-2 text-sm font-medium text-white"
          >
            {{ isAuthenticated ? 'sesja aktywna' : 'gotowe do logowania' }}
          </span>
        </div>

        <div class="mt-8 grid gap-4 lg:grid-cols-3">
          <article
            v-for="column in boardColumns"
            :key="column.title"
            class="rounded-[24px] border border-white/10 bg-white/6 p-4"
          >
            <header class="mb-4 flex items-center gap-3">
              <span
                class="h-2.5 w-2.5 rounded-full"
                :style="{ backgroundColor: column.tone }"
              ></span>
              <strong class="text-base">{{ column.title }}</strong>
            </header>

            <div class="space-y-3">
              <div
                v-for="task in column.tasks"
                :key="task"
                class="rounded-2xl bg-white/8 px-4 py-3 text-sm text-white/88"
              >
                {{ task }}
              </div>
            </div>
          </article>
        </div>
      </article>

      <article
        class="rounded-[34px] border border-white/60 bg-white/78 p-6 shadow-[0_20px_50px_rgba(15,23,42,0.12)] backdrop-blur-xl md:p-8"
      >
        <p class="text-xs font-semibold uppercase tracking-[0.28em] text-royal-600">
          Kierunek wizualny
        </p>
        <h2 class="mt-3 font-display text-3xl leading-tight text-ink-950">
          Granat i niebieski trzymaja baze, a mocne kolory zostaly na statusy.
        </h2>
        <p class="mt-4 text-sm leading-7 text-slate-600 md:text-base">
          Dzieki temu landing nie wali po oczach wszystkimi kolorami naraz, ale
          nadal ma charakter. Zielony, pomarancz i czerwien zostawiamy glownie
          na taski, alerty i statusy.
        </p>

        <div class="mt-8 space-y-3">
          <div class="flex items-center justify-between rounded-2xl bg-slate-900/4 px-4 py-3">
            <span class="text-sm font-medium text-slate-700">Prussian / Ink</span>
            <span class="text-sm text-slate-500">bazowe tlo i kontrast</span>
          </div>
          <div class="flex items-center justify-between rounded-2xl bg-azure-500/8 px-4 py-3">
            <span class="text-sm font-medium text-slate-700">Azure / Royal</span>
            <span class="text-sm text-slate-500">CTA i aktywny focus</span>
          </div>
          <div class="flex items-center justify-between rounded-2xl bg-jade-500/8 px-4 py-3">
            <span class="text-sm font-medium text-slate-700">Jade / Amber / Red</span>
            <span class="text-sm text-slate-500">statusy, priorytety, alerty</span>
          </div>
        </div>
      </article>
    </section>

    <section class="grid gap-4 md:grid-cols-3">
      <article
        v-for="(item, index) in highlights"
        :key="item.title"
        class="rounded-[28px] border border-white/60 bg-white/78 p-6 shadow-[0_18px_40px_rgba(148,163,184,0.12)] backdrop-blur-xl"
      >
        <p class="text-sm font-semibold text-slate-400">0{{ index + 1 }}</p>
        <h2 class="mt-3 font-display text-2xl leading-tight text-ink-950">{{ item.title }}</h2>
        <p class="mt-3 text-sm leading-7 text-slate-600 md:text-base">{{ item.copy }}</p>
      </article>
    </section>

    <section
      class="flex flex-col gap-5 rounded-[30px] border border-white/60 bg-white/82 px-6 py-7 shadow-[0_22px_50px_rgba(15,23,42,0.1)] backdrop-blur-xl md:flex-row md:items-center md:justify-between md:px-8"
    >
      <div class="max-w-3xl">
        <p class="text-xs font-semibold uppercase tracking-[0.28em] text-royal-600">
          Nastepny krok
        </p>
        <h2 class="mt-3 font-display text-3xl leading-tight text-ink-950">
          Jesli ten kierunek Ci siada, kolejnym ruchem robimy dashboard zadan juz w Tailwindzie.
        </h2>
        <p class="mt-4 text-sm leading-7 text-slate-600 md:text-base">
          Auth i routing juz mamy. Teraz mozemy wejsc w taski, projekty, komentarze
          i prawdziwy panel pracy bez cofania sie do podstaw.
        </p>
      </div>

      <RouterLink
        class="inline-flex items-center justify-center rounded-2xl bg-gradient-to-br from-azure-500 to-royal-600 px-6 py-3.5 text-sm font-semibold text-white shadow-[0_16px_30px_rgba(37,99,235,0.24)] transition hover:-translate-y-0.5"
        to="/register"
      >
        Wejdz do aplikacji
      </RouterLink>
    </section>
  </div>
</template>

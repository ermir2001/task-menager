<script setup>
import { computed } from 'vue';
import { RouterLink } from 'vue-router';

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
  <div class="home-view">
    <section class="hero">
      <div class="hero__copy">
        <p class="eyebrow">Vue frontend dla task managera</p>
        <h1>
          Projekt dla
          <span>{{ userName }}</span>
          z wyraznym wejsciem, porzadnym auth i miejscem na dalszy panel.
        </h1>
        <p class="hero__lead">
          Zostawilem klimat nowoczesnego panelu operacyjnego: granatowe tlo,
          jasne karty, mocne akcenty niebieskie i kolory statusow ograniczone do
          tego, co faktycznie potrzebne.
        </p>

        <div class="hero__actions">
          <RouterLink class="button button--primary" to="/register">
            Stworz konto
          </RouterLink>
          <RouterLink class="button button--ghost" to="/login">
            Zaloguj sie
          </RouterLink>
        </div>

        <div class="hero__meta">
          <div class="metric-card">
            <strong>03</strong>
            <span>gotowe ekrany startowe</span>
          </div>
          <div class="metric-card">
            <strong>FastAPI</strong>
            <span>podlaczenie pod auth od razu</span>
          </div>
          <div class="metric-card">
            <strong>{{ isAuthenticated ? 'live' : 'ready' }}</strong>
            <span>stan sesji w localStorage</span>
          </div>
        </div>
      </div>

      <div class="hero__visual card card--dark">
        <div class="hero__visual-top">
          <div>
            <small>Task board preview</small>
            <strong>Studio sprint board</strong>
          </div>
          <span class="status-pill status-pill--success">aktywny</span>
        </div>

        <div class="board-preview">
          <article
            v-for="column in boardColumns"
            :key="column.title"
            class="board-preview__column"
          >
            <header>
              <span :style="{ backgroundColor: column.tone }"></span>
              <strong>{{ column.title }}</strong>
            </header>

            <div
              v-for="task in column.tasks"
              :key="task"
              class="board-preview__task"
            >
              {{ task }}
            </div>
          </article>
        </div>

        <div class="hero__visual-footer">
          <div class="mini-stat">
            <strong>12</strong>
            <span>aktywnych taskow</span>
          </div>
          <div class="mini-stat">
            <strong>04</strong>
            <span>osoby w projekcie</span>
          </div>
          <div class="mini-stat">
            <strong>89%</strong>
            <span>domknietego sprintu</span>
          </div>
        </div>
      </div>
    </section>

    <section class="feature-grid">
      <article
        v-for="item in highlights"
        :key="item.title"
        class="card feature-card"
      >
        <p class="feature-card__index">0{{ highlights.indexOf(item) + 1 }}</p>
        <h2>{{ item.title }}</h2>
        <p>{{ item.copy }}</p>
      </article>
    </section>

    <section class="cta-panel card">
      <div>
        <p class="eyebrow">Nastepny krok</p>
        <h2>Jesli ten kierunek Ci siada, w kolejnym ruchu dobudujemy dashboard zadan.</h2>
        <p>
          Front ma juz baze stylistyczna, routing i auth. Dalej mozemy przejsc do
          list taskow, projektow i komentarzy.
        </p>
      </div>

      <RouterLink class="button button--primary" to="/register">
        Wejdz do aplikacji
      </RouterLink>
    </section>
  </div>
</template>

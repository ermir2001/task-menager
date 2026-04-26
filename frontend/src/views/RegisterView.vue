<script setup>
import { reactive, watch } from 'vue';
import { RouterLink, useRouter } from 'vue-router';

import AuthShowcase from '../components/AuthShowcase.vue';

const props = defineProps({
  auth: {
    type: Object,
    required: true,
  },
});

const router = useRouter();

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
});

watch(
  () => [form.username, form.email, form.first_name, form.last_name, form.password],
  () => props.auth.clearError(),
);

async function handleSubmit() {
  try {
    await props.auth.register(form);
    router.push('/');
  } catch {
    // Errors are stored in the shared auth state.
  }
}
</script>

<template>
  <section class="grid gap-6 xl:grid-cols-[0.9fr_1.1fr]">
    <AuthShowcase
      eyebrow="Rejestracja"
      title="Zaloz konto i wejdz do flow pracy bez dodatkowego zamieszania."
      description="Rejestracja jest teraz bardziej premium wizualnie, ale dalej szybka. Formularz od razu trzyma pola zgodne z backendem, a po utworzeniu konta mozemy wejsc prosto do aplikacji."
      :metrics="[
        { label: 'pola zgodne z API', value: '05' },
        { label: 'autologowanie', value: 'on' },
        { label: 'profil pod taski', value: 'ready' },
      ]"
    />

    <section
      class="rounded-[34px] border border-white/60 bg-white/82 p-6 shadow-[0_24px_60px_rgba(15,23,42,0.12)] backdrop-blur-xl md:p-8"
    >
      <div class="flex items-start justify-between gap-4">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.3em] text-royal-600">
            Rejestracja
          </p>
          <h1 class="mt-3 font-display text-4xl leading-tight text-ink-950">
            Zaloz konto
          </h1>
        </div>
        <span class="rounded-full bg-jade-500/10 px-3 py-2 text-xs font-semibold text-jade-500">
          onboarding
        </span>
      </div>

      <p class="mt-4 max-w-2xl text-sm leading-7 text-slate-600 md:text-base">
        Minimalny formularz, ale juz z danymi potrzebnymi do pokazywania autora,
        assignee i profilu uzytkownika w dalszych sekcjach aplikacji.
      </p>

      <form class="mt-8 grid gap-5 md:grid-cols-2" @submit.prevent="handleSubmit">
        <label class="block space-y-2">
          <span class="text-sm font-medium text-slate-700">Imie</span>
          <input
            v-model="form.first_name"
            type="text"
            name="first_name"
            autocomplete="given-name"
            placeholder="Jan"
            class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
          />
        </label>

        <label class="block space-y-2">
          <span class="text-sm font-medium text-slate-700">Nazwisko</span>
          <input
            v-model="form.last_name"
            type="text"
            name="last_name"
            autocomplete="family-name"
            placeholder="Nowak"
            class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
          />
        </label>

        <label class="block space-y-2">
          <span class="text-sm font-medium text-slate-700">Nazwa uzytkownika</span>
          <input
            v-model="form.username"
            type="text"
            name="username"
            autocomplete="username"
            placeholder="jan.dev"
            required
            class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
          />
        </label>

        <label class="block space-y-2">
          <span class="text-sm font-medium text-slate-700">Email</span>
          <input
            v-model="form.email"
            type="email"
            name="email"
            autocomplete="email"
            placeholder="ty@firma.pl"
            required
            class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
          />
        </label>

        <label class="block space-y-2 md:col-span-2">
          <div class="flex items-center justify-between gap-3">
            <span class="text-sm font-medium text-slate-700">Haslo</span>
            <span class="text-xs text-slate-400">Minimum 6 znakow</span>
          </div>
          <input
            v-model="form.password"
            type="password"
            name="password"
            autocomplete="new-password"
            placeholder="Minimum 6 znakow"
            minlength="6"
            required
            class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
          />
        </label>

        <p
          v-if="props.auth.state.error"
          class="rounded-2xl border border-red-500/15 bg-red-500/10 px-4 py-3 text-sm text-red-900 md:col-span-2"
        >
          {{ props.auth.state.error }}
        </p>

        <button
          class="inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-br from-azure-500 to-royal-600 px-6 py-3.5 text-sm font-semibold text-white shadow-[0_16px_30px_rgba(37,99,235,0.24)] transition hover:-translate-y-0.5 disabled:cursor-wait disabled:opacity-70 disabled:hover:translate-y-0 md:col-span-2"
          type="submit"
          :disabled="props.auth.state.loading"
        >
          {{ props.auth.state.loading ? 'Tworzenie konta...' : 'Stworz konto' }}
        </button>
      </form>

      <div
        class="mt-6 flex flex-col gap-3 rounded-[24px] border border-slate-200/70 bg-slate-900/[0.03] px-4 py-4 md:flex-row md:items-center md:justify-between"
      >
        <p class="text-sm leading-6 text-slate-600">
          Masz juz konto?
          <RouterLink class="font-semibold text-royal-600" to="/login">
            Zaloguj sie
          </RouterLink>
        </p>
        <span class="text-xs uppercase tracking-[0.24em] text-slate-400">
          create profile
        </span>
      </div>
    </section>
  </section>
</template>

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
  <section class="auth-layout">
    <AuthShowcase
      eyebrow="Start nowego konta"
      title="Stworz konto i zbuduj swoj workflow."
      description="Ten ekran od razu korzysta z obecnego kontraktu backendu, wiec po rejestracji uzytkownik zostaje zalogowany bez dodatkowego kroku."
      :metrics="[
        { label: 'pola dopasowane do API', value: '05' },
        { label: 'autologowanie po starcie', value: 'yes' },
        { label: 'baza pod onboarding', value: 'ready' },
      ]"
    />

    <section class="card auth-card">
      <p class="eyebrow">Rejestracja</p>
      <h1>Zaloz konto</h1>
      <p class="auth-card__copy">
        Minimalny formularz, ale z miejscem na dane osobowe, zeby pozniej
        sensownie pokazywac autora i assignee.
      </p>

      <form class="auth-form auth-form--two-columns" @submit.prevent="handleSubmit">
        <label class="field">
          <span>Imie</span>
          <input
            v-model="form.first_name"
            type="text"
            name="first_name"
            autocomplete="given-name"
            placeholder="Krystian"
          />
        </label>

        <label class="field">
          <span>Nazwisko</span>
          <input
            v-model="form.last_name"
            type="text"
            name="last_name"
            autocomplete="family-name"
            placeholder="Nowak"
          />
        </label>

        <label class="field">
          <span>Nazwa uzytkownika</span>
          <input
            v-model="form.username"
            type="text"
            name="username"
            autocomplete="username"
            placeholder="krystian.dev"
            required
          />
        </label>

        <label class="field">
          <span>Email</span>
          <input
            v-model="form.email"
            type="email"
            name="email"
            autocomplete="email"
            placeholder="ty@firma.pl"
            required
          />
        </label>

        <label class="field field--full">
          <span>Haslo</span>
          <input
            v-model="form.password"
            type="password"
            name="password"
            autocomplete="new-password"
            placeholder="Minimum 6 znakow"
            minlength="6"
            required
          />
        </label>

        <p v-if="props.auth.state.error" class="form-message form-message--error field--full">
          {{ props.auth.state.error }}
        </p>

        <button
          class="button button--primary button--full field--full"
          type="submit"
          :disabled="props.auth.state.loading"
        >
          {{ props.auth.state.loading ? 'Tworzenie konta...' : 'Stworz konto' }}
        </button>
      </form>

      <p class="auth-card__footer">
        Masz juz konto?
        <RouterLink to="/login">Zaloguj sie</RouterLink>
      </p>
    </section>
  </section>
</template>

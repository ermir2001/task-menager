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
  password: '',
});

watch(
  () => [form.username, form.password],
  () => props.auth.clearError(),
);

async function handleSubmit() {
  try {
    await props.auth.login(form);
    router.push('/');
  } catch {
    // Errors are stored in the shared auth state.
  }
}
</script>

<template>
  <section class="auth-layout">
    <AuthShowcase
      eyebrow="Powrot do workspace"
      title="Zaloguj sie i wejdz prosto do zadan."
      description="Logowanie jest podpiete pod aktualny endpoint FastAPI, wiec mozemy szybko przejsc do prawdziwego panelu pracy."
      :metrics="[
        { label: 'sekundy do startu', value: '< 30' },
        { label: 'wspolny token auth', value: 'JWT' },
        { label: 'gotowosc pod dashboard', value: '100%' },
      ]"
    />

    <section class="card auth-card">
      <p class="eyebrow">Logowanie</p>
      <h1>Witaj ponownie</h1>
      <p class="auth-card__copy">
        Uzyj nazwy uzytkownika i hasla. Po udanym logowaniu sesja zapisze sie
        lokalnie.
      </p>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <label class="field">
          <span>Nazwa uzytkownika</span>
          <input
            v-model="form.username"
            type="text"
            name="username"
            autocomplete="username"
            placeholder="np. krystian.dev"
            required
          />
        </label>

        <label class="field">
          <span>Haslo</span>
          <input
            v-model="form.password"
            type="password"
            name="password"
            autocomplete="current-password"
            placeholder="Wpisz haslo"
            required
          />
        </label>

        <p v-if="props.auth.state.error" class="form-message form-message--error">
          {{ props.auth.state.error }}
        </p>

        <button
          class="button button--primary button--full"
          type="submit"
          :disabled="props.auth.state.loading"
        >
          {{ props.auth.state.loading ? 'Logowanie...' : 'Zaloguj sie' }}
        </button>
      </form>

      <p class="auth-card__footer">
        Nie masz jeszcze konta?
        <RouterLink to="/register">Przejdz do rejestracji</RouterLink>
      </p>
    </section>
  </section>
</template>

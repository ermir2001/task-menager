<script setup>
import { computed } from 'vue';
import { RouterLink, useRoute } from 'vue-router';

const props = defineProps({
  auth: {
    type: Object,
    required: true,
  },
});

const route = useRoute();

const links = [
  { label: 'Glowna', to: '/' },
  { label: 'Logowanie', to: '/login' },
  { label: 'Rejestracja', to: '/register' },
];

const isAuthenticated = computed(() => Boolean(props.auth.state.token));
const displayName = computed(() => {
  const user = props.auth.state.user;

  if (!user) {
    return '';
  }

  if (user.first_name) {
    return user.first_name;
  }

  return user.username;
});

function isActive(path) {
  return route.path === path;
}
</script>

<template>
  <header class="app-header">
    <RouterLink class="brand" to="/">
      <span class="brand__badge">TM</span>
      <span>
        <strong>Task Manager</strong>
        <small>Vue + FastAPI starter</small>
      </span>
    </RouterLink>

    <nav class="app-nav" aria-label="Nawigacja glowna">
      <RouterLink
        v-for="link in links"
        :key="link.to"
        :to="link.to"
        class="app-nav__link"
        :class="{ 'is-active': isActive(link.to) }"
      >
        {{ link.label }}
      </RouterLink>
    </nav>

    <div class="app-header__actions">
      <div v-if="isAuthenticated" class="user-chip">
        <span class="user-chip__dot"></span>
        Zalogowany: {{ displayName }}
      </div>

      <button
        v-if="isAuthenticated"
        class="button button--ghost"
        type="button"
        @click="props.auth.logout"
      >
        Wyloguj
      </button>

      <template v-else>
        <RouterLink class="button button--ghost" to="/login">
          Wejdz
        </RouterLink>
        <RouterLink class="button button--primary" to="/register">
          Zacznij za darmo
        </RouterLink>
      </template>
    </div>
  </header>
</template>

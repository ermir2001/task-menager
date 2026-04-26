<script setup>
import { computed } from 'vue';
import { RouterLink, useRoute, useRouter } from 'vue-router';

const props = defineProps({
  auth: {
    type: Object,
    required: true,
  },
});

const route = useRoute();
const router = useRouter();

const links = [
  { label: 'Glowna', to: '/' },
  { label: 'Logowanie', to: '/login' },
  { label: 'Rejestracja', to: '/register' },
];

const isAuthenticated = computed(() => Boolean(props.auth.state.token));
const visibleLinks = computed(() =>
  isAuthenticated.value ? links.filter((link) => link.to === '/') : links,
);
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

function handleLogout() {
  props.auth.logout();
  router.push('/');
}
</script>

<template>
  <header
    class="rounded-[28px] border border-white/60 bg-white/78 px-5 py-4 shadow-[0_18px_50px_rgba(148,163,184,0.14)] backdrop-blur-xl"
  >
    <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:gap-6">
      <RouterLink class="inline-flex min-w-0 items-center gap-3" to="/">
        <span
          class="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-azure-500 to-royal-600 text-sm font-bold text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.35)]"
        >
          TM
        </span>
        <span>
          <strong class="block font-display text-base text-ink-950">Task Manager</strong>
          <small class="block text-sm text-slate-600">Vue + FastAPI starter</small>
        </span>
      </RouterLink>

      <nav
        aria-label="Nawigacja glowna"
        class="flex flex-wrap gap-2 rounded-full bg-slate-900/5 p-2 lg:ml-auto"
      >
        <RouterLink
          v-for="link in visibleLinks"
          :key="link.to"
          :to="link.to"
          class="rounded-full px-4 py-2.5 text-[15px] font-medium transition duration-150"
          :class="
            isActive(link.to)
              ? 'bg-white text-ink-950 shadow-[0_8px_20px_rgba(15,23,42,0.08)]'
              : 'text-slate-600 hover:bg-white/85 hover:text-ink-950'
          "
        >
          {{ link.label }}
        </RouterLink>
      </nav>

      <div v-if="isAuthenticated" class="flex items-center gap-3 lg:pl-4">
        <div
          class="inline-flex items-center gap-2 rounded-full bg-gradient-to-br from-ink-900 to-ink-800 px-4 py-2.5 text-sm text-white"
        >
          <span class="h-2.5 w-2.5 rounded-full bg-jade-500 shadow-[0_0_0_5px_rgba(34,197,94,0.16)]"></span>
          Zalogowany: {{ displayName }}
        </div>

        <button
          class="rounded-2xl border border-slate-900/8 bg-white/80 px-4 py-2.5 text-sm font-medium text-ink-950 transition hover:-translate-y-0.5 hover:bg-white"
          type="button"
          @click="handleLogout"
        >
          Wyloguj
        </button>
      </div>
    </div>
  </header>
</template>

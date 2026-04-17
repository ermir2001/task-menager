<script setup>
import { computed, onMounted } from 'vue';
import { RouterView, useRoute } from 'vue-router';

import AppHeader from './components/AppHeader.vue';
import { useAuth } from './lib/auth';

const auth = useAuth();
const route = useRoute();

const pageClass = computed(() =>
  route.name === 'home' ? 'app-shell--home' : 'app-shell--auth',
);

onMounted(() => {
  auth.hydrateUser();
});
</script>

<template>
  <div class="app-shell" :class="pageClass">
    <div class="ambient ambient--left"></div>
    <div class="ambient ambient--right"></div>

    <div class="page-container">
      <AppHeader :auth="auth" />

      <main class="page-main">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" :auth="auth" />
          </Transition>
        </RouterView>
      </main>
    </div>
  </div>
</template>

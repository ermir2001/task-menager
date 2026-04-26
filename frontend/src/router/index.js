import { createRouter, createWebHistory } from 'vue-router';

import { useAuth } from '../lib/auth';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';

const auth = useAuth();

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'Task Manager | Glowna',
    },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      guestOnly: true,
      title: 'Task Manager | Logowanie',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      guestOnly: true,
      title: 'Task Manager | Rejestracja',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 };
  },
});

router.beforeEach((to) => {
  if (to.meta.guestOnly && auth.state.token) {
    return { name: 'home' };
  }

  return true;
});

router.afterEach((to) => {
  document.title = to.meta.title ?? 'Task Manager';
});

export default router;

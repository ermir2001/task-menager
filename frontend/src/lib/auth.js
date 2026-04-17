import { reactive } from 'vue';

import { fetchCurrentUser, loginUser, registerUser } from './api';

const TOKEN_KEY = 'task-menager-token';
const USER_KEY = 'task-menager-user';

function readUser() {
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) {
    return null;
  }

  try {
    return JSON.parse(raw);
  } catch {
    localStorage.removeItem(USER_KEY);
    return null;
  }
}

const state = reactive({
  token: localStorage.getItem(TOKEN_KEY) || '',
  user: readUser(),
  loading: false,
  error: '',
});

function persistSession(token, user) {
  state.token = token;
  state.user = user;

  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

function clearSession() {
  state.token = '';
  state.user = null;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

async function hydrateUser() {
  if (!state.token) {
    return null;
  }

  try {
    const user = await fetchCurrentUser(state.token);
    persistSession(state.token, user);
    return user;
  } catch {
    clearSession();
    return null;
  }
}

async function login(credentials) {
  state.loading = true;
  state.error = '';

  try {
    const tokenResponse = await loginUser(credentials);
    const user = await fetchCurrentUser(tokenResponse.access_token);

    persistSession(tokenResponse.access_token, user);
    return user;
  } catch (error) {
    clearSession();
    state.error = error.message || 'Nie udalo sie zalogowac.';
    throw error;
  } finally {
    state.loading = false;
  }
}

async function register(payload) {
  state.loading = true;
  state.error = '';

  try {
    await registerUser(payload);
    return await login({
      username: payload.username,
      password: payload.password,
    });
  } catch (error) {
    state.error = error.message || 'Nie udalo sie zalozyc konta.';
    throw error;
  } finally {
    state.loading = false;
  }
}

function logout() {
  clearSession();
  state.error = '';
}

function clearError() {
  state.error = '';
}

export function useAuth() {
  return {
    state,
    login,
    register,
    logout,
    clearError,
    hydrateUser,
  };
}

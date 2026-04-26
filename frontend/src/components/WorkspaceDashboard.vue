<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, watch } from 'vue';

import {
  createProject,
  createTask,
  deleteProject,
  deleteTask,
  fetchProjects,
  fetchTaskPriorities,
  fetchTaskStatuses,
  fetchTasks,
  fetchUsers,
  updateTaskStatus,
} from '../lib/api';

const props = defineProps({
  auth: {
    type: Object,
    required: true,
  },
});

const state = reactive({
  loading: false,
  loaded: false,
  error: '',
  success: '',
  projects: [],
  tasks: [],
  users: [],
  statuses: [],
  priorities: [],
  projectSubmitting: false,
  taskSubmitting: false,
  deletingProjectId: null,
  deletingTaskId: null,
  statusUpdatingId: null,
  boardProjectId: 'all',
  selectedProjectId: null,
  selectedTaskId: null,
});

const projectForm = reactive({
  name: '',
  description: '',
});

const taskForm = reactive({
  title: '',
  description: '',
  project_id: '',
  assignee_id: '',
  status_id: '',
  priority_id: '',
  due_date: '',
});

const token = computed(() => props.auth.state.token);
const currentUser = computed(() => props.auth.state.user);
const currentUserId = computed(() => currentUser.value?.id ?? null);

const assigneeOptions = computed(() => {
  if (state.users.length) {
    return state.users;
  }

  return currentUser.value ? [currentUser.value] : [];
});

const projectMap = computed(() =>
  Object.fromEntries(state.projects.map((project) => [project.id, project])),
);

const priorityMap = computed(() =>
  Object.fromEntries(state.priorities.map((priority) => [priority.id, priority])),
);

const statusMap = computed(() =>
  Object.fromEntries(state.statuses.map((status) => [status.id, status])),
);

const stats = computed(() => {
  const assignedToMe = state.tasks.filter((task) => task.assignee_id === currentUserId.value);
  const dueSoon = state.tasks.filter((task) => isDueSoon(task.due_date));
  const activeStatuses = state.statuses.filter((status) => !isDoneStatus(status.name));
  const activeStatusIds = new Set(activeStatuses.map((status) => status.id));
  const openTasks = state.tasks.filter(
    (task) => !state.statuses.length || activeStatusIds.has(task.status_id),
  );

  return [
    { label: 'projekty', value: state.projects.length },
    { label: 'taski lacznie', value: state.tasks.length },
    { label: 'otwarte taski', value: openTasks.length },
    { label: 'przypisane do mnie', value: assignedToMe.length },
    { label: 'termin w 7 dni', value: dueSoon.length },
  ];
});

const projectCards = computed(() =>
  state.projects.map((project) => {
    const tasks = state.tasks.filter((task) => task.project_id === project.id);
    const openTasks = tasks.filter((task) => !isDoneStatus(statusMap.value[task.status_id]?.name));

    return {
      ...project,
      taskCount: tasks.length,
      openTaskCount: openTasks.length,
    };
  }),
);

const boardTasks = computed(() => {
  if (state.boardProjectId === 'all') {
    return state.tasks;
  }

  return state.tasks.filter((task) => String(task.project_id) === state.boardProjectId);
});

const activeBoardProjectLabel = computed(() =>
  state.boardProjectId === 'all'
    ? 'Wszystkie projekty'
    : getProjectName(Number(state.boardProjectId)),
);

const selectedProject = computed(
  () => projectCards.value.find((project) => project.id === state.selectedProjectId) || null,
);

const selectedTask = computed(
  () => state.tasks.find((task) => task.id === state.selectedTaskId) || null,
);

const taskColumns = computed(() => {
  if (!state.statuses.length) {
    return [];
  }

  return state.statuses.map((status) => ({
    ...status,
    tone: getStatusTone(status.name),
    tasks: boardTasks.value.filter((task) => task.status_id === status.id),
  }));
});

const canCreateTask = computed(
  () =>
    Boolean(taskForm.project_id) &&
    Boolean(taskForm.assignee_id) &&
    Boolean(taskForm.status_id) &&
    Boolean(taskForm.priority_id),
);

watch(
  () => token.value,
  async (nextToken) => {
    resetWorkspaceFeedback();

    if (!nextToken) {
      resetWorkspaceState();
      return;
    }

    await loadWorkspace();
  },
  { immediate: true },
);

watch(
  () => [
    state.projects.length,
    assigneeOptions.value.length,
    state.statuses.length,
    state.priorities.length,
    currentUserId.value,
  ],
  () => {
    if (!taskForm.project_id && state.projects.length) {
      taskForm.project_id = String(state.projects[0].id);
    }

    if (!taskForm.assignee_id && assigneeOptions.value.length) {
      const defaultAssignee =
        assigneeOptions.value.find((user) => user.id === currentUserId.value) ||
        assigneeOptions.value[0];

      if (defaultAssignee) {
        taskForm.assignee_id = String(defaultAssignee.id);
      }
    }

    if (!taskForm.status_id && state.statuses.length) {
      taskForm.status_id = String(state.statuses[0].id);
    }

    if (!taskForm.priority_id && state.priorities.length) {
      taskForm.priority_id = String(state.priorities[0].id);
    }
  },
  { immediate: true },
);

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeydown);
});

function resetWorkspaceFeedback() {
  state.error = '';
  state.success = '';
}

function resetWorkspaceState() {
  state.loaded = false;
  state.projects = [];
  state.tasks = [];
  state.users = [];
  state.statuses = [];
  state.priorities = [];
  state.boardProjectId = 'all';
  state.selectedProjectId = null;
  state.selectedTaskId = null;
}

async function loadWorkspace() {
  if (!token.value) {
    return;
  }

  state.loading = true;
  resetWorkspaceFeedback();

  try {
    const [projects, tasks, users, statuses, priorities] = await Promise.all([
      fetchProjects(token.value),
      fetchTasks(token.value),
      fetchUsers(token.value),
      fetchTaskStatuses(token.value),
      fetchTaskPriorities(token.value),
    ]);

    state.projects = projects;
    state.tasks = tasks;
    state.users = users;
    state.statuses = statuses;
    state.priorities = priorities;
    state.loaded = true;
  } catch (error) {
    state.error = error.message || 'Nie udalo sie pobrac danych workspace.';
  } finally {
    state.loading = false;
  }
}

async function handleProjectSubmit() {
  if (!token.value || !projectForm.name.trim()) {
    return;
  }

  state.projectSubmitting = true;
  resetWorkspaceFeedback();

  try {
    const project = await createProject(token.value, {
      name: projectForm.name.trim(),
      description: projectForm.description.trim() || null,
    });

    state.projects = [project, ...state.projects];
    projectForm.name = '';
    projectForm.description = '';
    taskForm.project_id = String(project.id);
    state.success = 'Projekt zostal dodany.';
  } catch (error) {
    state.error = error.message || 'Nie udalo sie dodac projektu.';
  } finally {
    state.projectSubmitting = false;
  }
}

async function handleTaskSubmit() {
  if (!token.value || !canCreateTask.value || !taskForm.title.trim()) {
    return;
  }

  state.taskSubmitting = true;
  resetWorkspaceFeedback();

  try {
    const task = await createTask(token.value, {
      title: taskForm.title.trim(),
      description: taskForm.description.trim() || null,
      project_id: Number(taskForm.project_id),
      assignee_id: Number(taskForm.assignee_id),
      status_id: Number(taskForm.status_id),
      priority_id: Number(taskForm.priority_id),
      due_date: taskForm.due_date ? new Date(taskForm.due_date).toISOString() : null,
    });

    state.tasks = [task, ...state.tasks];
    taskForm.title = '';
    taskForm.description = '';
    taskForm.due_date = '';
    state.success = 'Task zostal dodany.';
  } catch (error) {
    state.error = error.message || 'Nie udalo sie dodac taska.';
  } finally {
    state.taskSubmitting = false;
  }
}

async function handleProjectDelete(project) {
  if (!token.value) {
    return;
  }

  const shouldDelete = window.confirm(
    `Usunac projekt "${project.name}"? Jesli ma powiazane taski, backend moze odrzucic te operacje.`,
  );

  if (!shouldDelete) {
    return;
  }

  state.deletingProjectId = project.id;
  resetWorkspaceFeedback();

  try {
    await deleteProject(token.value, project.id);
    state.projects = state.projects.filter((item) => item.id !== project.id);
    state.tasks = state.tasks.filter((task) => task.project_id !== project.id);

    if (taskForm.project_id === String(project.id)) {
      taskForm.project_id = state.projects[0] ? String(state.projects[0].id) : '';
    }

    if (state.boardProjectId === String(project.id)) {
      state.boardProjectId = 'all';
    }

    if (state.selectedProjectId === project.id) {
      closeProjectDetails();
    }

    state.success = 'Projekt zostal usuniety.';
  } catch (error) {
    state.error = error.message || 'Nie udalo sie usunac projektu.';
  } finally {
    state.deletingProjectId = null;
  }
}

async function handleTaskDelete(task) {
  if (!token.value) {
    return;
  }

  const shouldDelete = window.confirm(`Usunac task "${task.title}"?`);

  if (!shouldDelete) {
    return;
  }

  state.deletingTaskId = task.id;
  resetWorkspaceFeedback();

  try {
    await deleteTask(token.value, task.id);
    state.tasks = state.tasks.filter((item) => item.id !== task.id);
    state.success = 'Task zostal usuniety.';

    if (state.selectedTaskId === task.id) {
      closeTaskDetails();
    }
  } catch (error) {
    state.error = error.message || 'Nie udalo sie usunac taska.';
  } finally {
    state.deletingTaskId = null;
  }
}

async function handleStatusChange(task, event) {
  const nextStatusId = Number(event.target.value);
  await setTaskStatus(task, nextStatusId, () => {
    event.target.value = String(task.status_id);
  });
}

async function setTaskStatus(task, nextStatusId, onError) {
  if (!token.value || !canChangeTaskStatus(task)) {
    return;
  }

  if (!nextStatusId || nextStatusId === task.status_id) {
    return;
  }

  state.statusUpdatingId = task.id;
  resetWorkspaceFeedback();

  try {
    const updatedTask = await updateTaskStatus(token.value, task.id, {
      status_id: nextStatusId,
    });

    state.tasks = state.tasks.map((item) => (item.id === task.id ? updatedTask : item));
    state.success = 'Status taska zostal zaktualizowany.';
  } catch (error) {
    if (typeof onError === 'function') {
      onError();
    }

    state.error = error.message || 'Nie udalo sie zmienic statusu taska.';
  } finally {
    state.statusUpdatingId = null;
  }
}

function formatDate(dateValue) {
  if (!dateValue) {
    return 'Bez terminu';
  }

  return new Intl.DateTimeFormat('pl-PL', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(dateValue));
}

function getProjectExcerpt(description) {
  if (!description) {
    return 'Kliknij w karte, aby zobaczyc opis projektu i liczbe taskow.';
  }

  if (description.length <= 96) {
    return description;
  }

  return `${description.slice(0, 93)}...`;
}

function getTaskExcerpt(description) {
  if (!description) {
    return 'Kliknij w karte, aby zobaczyc szczegoly taska.';
  }

  if (description.length <= 120) {
    return description;
  }

  return `${description.slice(0, 117)}...`;
}

function getUserName(userId) {
  const user = assigneeOptions.value.find((item) => item.id === userId);

  if (!user) {
    return `Uzytkownik #${userId}`;
  }

  const fullName = [user.first_name, user.last_name].filter(Boolean).join(' ').trim();
  return fullName || user.username;
}

function getUserInitials(userId) {
  const label = getUserName(userId);
  const parts = label.split(/\s+/).filter(Boolean);

  if (!parts.length) {
    return '??';
  }

  if (parts.length === 1) {
    return parts[0].slice(0, 2).toUpperCase();
  }

  return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
}

function getProjectName(projectId) {
  return projectMap.value[projectId]?.name || `Projekt #${projectId}`;
}

function getPriorityName(priorityId) {
  return priorityMap.value[priorityId]?.name || 'Priorytet';
}

function getStatusName(statusId) {
  return statusMap.value[statusId]?.name || 'Status';
}

function canChangeTaskStatus(task) {
  return task.assignee_id === currentUserId.value || task.author_id === currentUserId.value;
}

function getStatusIndex(statusId) {
  return state.statuses.findIndex((status) => status.id === statusId);
}

function getAdjacentStatus(task, direction) {
  const currentIndex = getStatusIndex(task.status_id);

  if (currentIndex === -1) {
    return null;
  }

  const nextIndex = currentIndex + direction;
  return state.statuses[nextIndex] || null;
}

function canMoveTask(task, direction) {
  return Boolean(getAdjacentStatus(task, direction)) && canChangeTaskStatus(task);
}

async function moveTask(task, direction) {
  const nextStatus = getAdjacentStatus(task, direction);

  if (!nextStatus) {
    return;
  }

  await setTaskStatus(task, nextStatus.id);
}

function openProjectDetails(project) {
  state.selectedTaskId = null;
  state.selectedProjectId = project.id;
}

function closeProjectDetails() {
  state.selectedProjectId = null;
}

function focusProjectOnBoard(project) {
  state.boardProjectId = String(project.id);
  closeProjectDetails();
}

function openTaskDetails(task) {
  state.selectedProjectId = null;
  state.selectedTaskId = task.id;
}

function closeTaskDetails() {
  state.selectedTaskId = null;
}

function handleKeydown(event) {
  if (event.key !== 'Escape') {
    return;
  }

  if (state.selectedTaskId !== null) {
    closeTaskDetails();
    return;
  }

  if (state.selectedProjectId !== null) {
    closeProjectDetails();
  }
}

function isDoneStatus(name = '') {
  return /(done|closed|zrob|zakoncz|finish|complete)/i.test(name);
}

function isDueSoon(dateValue) {
  if (!dateValue) {
    return false;
  }

  const now = Date.now();
  const due = new Date(dateValue).getTime();
  const diff = due - now;

  return diff >= 0 && diff <= 7 * 24 * 60 * 60 * 1000;
}

function getStatusTone(name = '') {
  if (/(done|closed|zrob|zakoncz|finish|complete)/i.test(name)) {
    return 'from-jade-500/25 to-jade-500/10 border-jade-500/20';
  }

  if (/(review|qa|test)/i.test(name)) {
    return 'from-amber-400/25 to-amber-300/10 border-amber-400/20';
  }

  if (/(todo|plan|backlog|new)/i.test(name)) {
    return 'from-slate-400/18 to-white/10 border-slate-300/30';
  }

  return 'from-azure-500/25 to-royal-600/12 border-royal-500/20';
}

function getPriorityTone(name = '') {
  if (/(high|urgent|kryt|piln)/i.test(name)) {
    return 'bg-red-500/12 text-red-700 ring-red-500/15';
  }

  if (/(medium|normal|sred)/i.test(name)) {
    return 'bg-amber-400/16 text-amber-700 ring-amber-400/20';
  }

  return 'bg-jade-500/12 text-jade-700 ring-jade-500/15';
}
</script>

<template>
  <div class="min-w-0 space-y-7 overflow-x-hidden">
    <section
      class="overflow-hidden rounded-[36px] border border-white/60 bg-[radial-gradient(circle_at_top_left,rgba(59,130,246,0.18),transparent_36%),linear-gradient(145deg,rgba(255,255,255,0.92),rgba(248,250,252,0.86))] px-6 py-8 shadow-[0_24px_70px_rgba(15,23,42,0.12)] backdrop-blur-xl md:px-10 md:py-10"
    >
      <div class="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div class="max-w-4xl">
          <p class="text-xs font-semibold uppercase tracking-[0.34em] text-royal-600">
            Workspace
          </p>
          <h1
            class="mt-4 font-display text-4xl leading-[0.95] text-ink-950 sm:text-5xl xl:text-[4.7rem]"
          >
            Projekty, taski i statusy w jednym miejscu dla
            <span class="text-royal-600">
              {{ currentUser?.first_name || currentUser?.username || 'Twojego zespolu' }}
            </span>
          </h1>
          <p class="mt-5 max-w-3xl text-base leading-8 text-slate-600 md:text-lg">
            To jest juz roboczy panel. Mozesz tworzyc projekty, dodawac taski, przypisywac
            je do osob i zmieniac statusy bez wychodzenia z glownego ekranu.
          </p>
        </div>

        <button
          class="inline-flex items-center justify-center rounded-2xl border border-slate-900/8 bg-white/85 px-5 py-3 text-sm font-semibold text-ink-950 transition hover:-translate-y-0.5 hover:bg-white disabled:cursor-wait disabled:opacity-60 disabled:hover:translate-y-0"
          type="button"
          :disabled="state.loading"
          @click="loadWorkspace"
        >
          {{ state.loading ? 'Odswiezanie...' : 'Odswiez dane' }}
        </button>
      </div>

      <div class="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <article
          v-for="item in stats"
          :key="item.label"
          class="rounded-[24px] border border-white/70 bg-white/82 px-5 py-4 shadow-[0_18px_40px_rgba(148,163,184,0.1)]"
        >
          <strong class="block font-display text-3xl text-ink-950">{{ item.value }}</strong>
          <span class="mt-2 block text-sm text-slate-500">{{ item.label }}</span>
        </article>
      </div>
    </section>

    <p
      v-if="state.error"
      class="rounded-[24px] border border-red-500/15 bg-red-500/10 px-5 py-4 text-sm leading-6 text-red-900"
    >
      {{ state.error }}
    </p>

    <p
      v-if="state.success"
      class="rounded-[24px] border border-jade-500/15 bg-jade-500/10 px-5 py-4 text-sm leading-6 text-emerald-900"
    >
      {{ state.success }}
    </p>

    <section class="grid min-w-0 gap-6 xl:grid-cols-[minmax(0,0.7fr)_minmax(0,1.3fr)]">
      <article
        class="min-w-0 rounded-[34px] border border-white/60 bg-white/82 p-6 shadow-[0_22px_50px_rgba(15,23,42,0.1)] backdrop-blur-xl md:p-8"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.3em] text-royal-600">
              Nowy projekt
            </p>
            <h2 class="mt-3 font-display text-3xl leading-tight text-ink-950">
              Zaloz przestrzen pod sprint albo klienta
            </h2>
          </div>
          <span class="rounded-full bg-royal-600/8 px-3 py-2 text-xs font-semibold text-royal-600">
            projects
          </span>
        </div>

        <form class="mt-8 space-y-5" @submit.prevent="handleProjectSubmit">
          <label class="block space-y-2">
            <span class="text-sm font-medium text-slate-700">Nazwa projektu</span>
            <input
              v-model="projectForm.name"
              type="text"
              maxlength="100"
              placeholder="np. Rebranding panelu klienta"
              required
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            />
          </label>

          <label class="block space-y-2">
            <span class="text-sm font-medium text-slate-700">Opis</span>
            <textarea
              v-model="projectForm.description"
              rows="4"
              placeholder="Krotko opisz zakres projektu, etap albo cel sprintu."
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            ></textarea>
          </label>

          <button
            class="inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-br from-azure-500 to-royal-600 px-6 py-3.5 text-sm font-semibold text-white shadow-[0_16px_30px_rgba(37,99,235,0.24)] transition hover:-translate-y-0.5 disabled:cursor-wait disabled:opacity-70 disabled:hover:translate-y-0"
            type="submit"
            :disabled="state.projectSubmitting"
          >
            {{ state.projectSubmitting ? 'Dodawanie projektu...' : 'Dodaj projekt' }}
          </button>
        </form>
      </article>

      <article
        class="min-w-0 rounded-[34px] border border-white/60 bg-white/82 p-6 shadow-[0_22px_50px_rgba(15,23,42,0.1)] backdrop-blur-xl md:p-8"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.3em] text-royal-600">
              Nowy task
            </p>
            <h2 class="mt-3 font-display text-3xl leading-tight text-ink-950">
              Dodaj zadanie i od razu wrzuc je do workflow
            </h2>
          </div>
          <span class="rounded-full bg-jade-500/10 px-3 py-2 text-xs font-semibold text-jade-600">
            tasks
          </span>
        </div>

        <form class="mt-8 grid gap-5 lg:grid-cols-2" @submit.prevent="handleTaskSubmit">
          <label class="block space-y-2 lg:col-span-2">
            <span class="text-sm font-medium text-slate-700">Tytul taska</span>
            <input
              v-model="taskForm.title"
              type="text"
              maxlength="150"
              placeholder="np. Przygotuj dashboard projektow"
              required
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            />
          </label>

          <label class="block space-y-2 lg:col-span-2">
            <span class="text-sm font-medium text-slate-700">Opis taska</span>
            <textarea
              v-model="taskForm.description"
              rows="4"
              placeholder="Krotki opis zakresu, oczekiwanego efektu albo technicznych notatek."
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition placeholder:text-slate-400 focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            ></textarea>
          </label>

          <label class="block space-y-2">
            <span class="text-sm font-medium text-slate-700">Projekt</span>
            <select
              v-model="taskForm.project_id"
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            >
              <option
                v-for="project in state.projects"
                :key="project.id"
                :value="String(project.id)"
              >
                {{ project.name }}
              </option>
            </select>
          </label>

          <label class="block space-y-2">
            <span class="text-sm font-medium text-slate-700">Assignee</span>
            <select
              v-model="taskForm.assignee_id"
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            >
              <option v-for="user in assigneeOptions" :key="user.id" :value="String(user.id)">
                {{ getUserName(user.id) }}
              </option>
            </select>
          </label>

          <label class="block space-y-2">
            <span class="text-sm font-medium text-slate-700">Status startowy</span>
            <select
              v-model="taskForm.status_id"
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            >
              <option v-for="status in state.statuses" :key="status.id" :value="String(status.id)">
                {{ status.name }}
              </option>
            </select>
          </label>

          <label class="block space-y-2">
            <span class="text-sm font-medium text-slate-700">Priorytet</span>
            <select
              v-model="taskForm.priority_id"
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            >
              <option
                v-for="priority in state.priorities"
                :key="priority.id"
                :value="String(priority.id)"
              >
                {{ priority.name }}
              </option>
            </select>
          </label>

          <label class="block space-y-2 lg:col-span-2">
            <span class="text-sm font-medium text-slate-700">Termin</span>
            <input
              v-model="taskForm.due_date"
              type="datetime-local"
              class="w-full rounded-2xl border border-slate-200/90 bg-white px-4 py-3.5 text-ink-950 outline-none transition focus:-translate-y-0.5 focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
            />
          </label>

          <div
            v-if="!state.projects.length"
            class="rounded-2xl border border-amber-400/20 bg-amber-400/10 px-4 py-3 text-sm text-amber-900 lg:col-span-2"
          >
            Najpierw dodaj projekt. Backend wymaga `project_id`, wiec bez projektu nie utworzymy
            taska.
          </div>

          <button
            class="inline-flex w-full items-center justify-center rounded-2xl bg-gradient-to-br from-azure-500 to-royal-600 px-6 py-3.5 text-sm font-semibold text-white shadow-[0_16px_30px_rgba(37,99,235,0.24)] transition hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:translate-y-0 lg:col-span-2"
            type="submit"
            :disabled="state.taskSubmitting || !canCreateTask || !state.projects.length"
          >
            {{ state.taskSubmitting ? 'Dodawanie taska...' : 'Dodaj task' }}
          </button>
        </form>
      </article>
    </section>

    <section
      class="rounded-[34px] border border-white/60 bg-white/82 p-6 shadow-[0_22px_50px_rgba(15,23,42,0.1)] backdrop-blur-xl md:p-8"
    >
      <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.28em] text-royal-600">
            Projekty
          </p>
          <h2 class="mt-2 font-display text-3xl leading-tight text-ink-950">
            Osobna sekcja projektow, bez wciskania ich pod formularz.
          </h2>
          <p class="mt-3 max-w-2xl text-sm leading-7 text-slate-600">
            Na liscie masz tylko szybki podglad. Klikniecie dalej otwiera pelne informacje o
            projekcie w osobnym oknie.
          </p>
        </div>

        <span
          class="inline-flex items-center rounded-full bg-royal-600/8 px-4 py-2 text-sm font-medium text-royal-600"
        >
          {{ projectCards.length }} projektow w workspace
        </span>
      </div>

      <div v-if="projectCards.length" class="mt-8 grid gap-4 md:grid-cols-2 2xl:grid-cols-3">
        <article
          v-for="project in projectCards"
          :key="project.id"
          class="cursor-pointer rounded-[26px] border border-slate-200/80 bg-[linear-gradient(180deg,rgba(255,255,255,0.98),rgba(248,250,252,0.92))] p-5 shadow-[0_16px_36px_rgba(148,163,184,0.1)] transition hover:-translate-y-0.5 hover:border-royal-600/18 hover:shadow-[0_20px_40px_rgba(59,130,246,0.12)]"
          role="button"
          tabindex="0"
          @click="openProjectDetails(project)"
          @keydown.enter="openProjectDetails(project)"
          @keydown.space.prevent="openProjectDetails(project)"
        >
          <div class="flex items-start justify-between gap-3">
            <div class="min-w-0">
              <p class="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">
                Projekt
              </p>
              <h3 class="mt-2 truncate font-display text-[2rem] leading-[1.02] text-ink-950">
                {{ project.name }}
              </h3>
            </div>

            <button
              class="shrink-0 rounded-xl border border-red-500/15 bg-white px-3 py-2 text-xs font-semibold text-red-700 transition hover:bg-red-50 disabled:cursor-wait disabled:opacity-60"
              type="button"
              :disabled="state.deletingProjectId === project.id"
              @click.stop="handleProjectDelete(project)"
            >
              {{ state.deletingProjectId === project.id ? 'Usuwanie...' : 'Usun' }}
            </button>
          </div>

          <p class="mt-4 min-h-[72px] text-sm leading-6 text-slate-600">
            {{ getProjectExcerpt(project.description) }}
          </p>

          <div class="mt-5 flex flex-wrap gap-2">
            <span class="rounded-full bg-slate-900/6 px-3 py-2 text-xs font-medium text-slate-600">
              {{ project.taskCount }} taskow
            </span>
            <span class="rounded-full bg-royal-600/8 px-3 py-2 text-xs font-medium text-royal-600">
              {{ project.openTaskCount }} otwartych
            </span>
            <span class="rounded-full bg-jade-500/10 px-3 py-2 text-xs font-medium text-jade-700">
              {{ getUserName(project.owner_id) }}
            </span>
          </div>

          <div class="mt-5 flex items-center justify-between gap-3 text-sm text-slate-500">
            <span>{{ formatDate(project.created_at) }}</span>
            <span class="font-medium text-slate-600">Kliknij po szczegoly</span>
          </div>
        </article>
      </div>

      <div
        v-else-if="!state.loading && state.loaded"
        class="mt-8 rounded-[24px] border border-dashed border-slate-300 bg-white/65 px-5 py-6 text-sm leading-7 text-slate-500"
      >
        Nie ma jeszcze projektow. Dodaj pierwszy i od razu bedziemy mogli podpiac pod niego taski.
      </div>
    </section>

    <section
      class="min-w-0 overflow-hidden rounded-[34px] border border-slate-700/40 bg-[linear-gradient(160deg,#111827,#1e293b)] p-6 text-snow-50 shadow-[0_28px_80px_rgba(15,23,42,0.34)] md:p-8"
    >
      <div class="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <p class="text-xs font-semibold uppercase tracking-[0.28em] text-slate-400">
            Board taskow
          </p>
          <h2 class="mt-2 font-display text-3xl leading-tight">
            Statusy sa pobierane z backendu, wiec ten widok od razu trzyma sie Twojego API.
          </h2>
        </div>
        <span class="inline-flex items-center rounded-full bg-white/8 px-4 py-2 text-sm font-medium text-white/84">
          {{ boardTasks.length }} zadan w boardzie
        </span>
      </div>

      <div v-if="state.loading && !state.loaded" class="mt-8 text-sm text-white/70">
        Laduje workspace...
      </div>

      <div v-else-if="taskColumns.length" class="mt-8">
        <div
          class="mb-5 grid gap-4 rounded-[24px] border border-white/10 bg-white/[0.045] p-4 lg:grid-cols-[minmax(0,1fr)_320px] lg:items-end"
        >
          <div class="space-y-2 text-sm text-white/60">
            <p>Board trzyma sie szerokosci strony i nie rozpycha juz calego layoutu.</p>
            <p>
              Aktywny widok:
              <span class="font-semibold text-white">{{ activeBoardProjectLabel }}</span>
            </p>
          </div>

          <label class="grid gap-2 text-sm">
            <span class="font-medium text-white/82">Pokaz taski z projektu</span>
            <select
              v-model="state.boardProjectId"
              class="w-full rounded-2xl border border-white/12 bg-white/8 px-4 py-3 text-white outline-none transition focus:border-white/20"
            >
              <option
                value="all"
                class="bg-snow-50 text-ink-950"
                style="color: #0f172a; background-color: #f8fafc;"
              >
                Wszystkie projekty
              </option>
              <option
                v-for="project in state.projects"
                :key="project.id"
                :value="String(project.id)"
                class="bg-snow-50 text-ink-950"
                style="color: #0f172a; background-color: #f8fafc;"
              >
                {{ project.name }}
              </option>
            </select>
          </label>
        </div>

        <div class="grid min-w-0 gap-4 xl:grid-cols-2 2xl:grid-cols-3">
          <article
            v-for="column in taskColumns"
            :key="column.id"
            class="min-w-0 rounded-[28px] border border-white/10 bg-white/6 p-4"
          >
            <header
              class="mb-4 rounded-[20px] border bg-gradient-to-br px-4 py-4"
              :class="column.tone"
            >
              <div class="flex items-center justify-between gap-3">
                <strong class="text-base text-white">{{ column.name }}</strong>
                <span class="rounded-full bg-white/12 px-3 py-1 text-xs text-white/80">
                  {{ column.tasks.length }}
                </span>
              </div>
            </header>

            <div class="space-y-3">
              <article
                v-for="task in column.tasks"
                :key="task.id"
                class="min-w-0 cursor-pointer rounded-[24px] border border-white/10 bg-white/8 p-4 transition hover:border-white/16 hover:bg-white/[0.1]"
                role="button"
                tabindex="0"
                @click="openTaskDetails(task)"
                @keydown.enter="openTaskDetails(task)"
                @keydown.space.prevent="openTaskDetails(task)"
              >
                <div class="flex items-center justify-between gap-3">
                  <div v-if="canChangeTaskStatus(task)" class="flex items-center gap-2">
                    <button
                      class="grid h-10 w-10 place-items-center rounded-xl border border-white/10 bg-white/8 text-sm text-white transition hover:bg-white/14 disabled:cursor-not-allowed disabled:opacity-35"
                      type="button"
                      :disabled="state.statusUpdatingId === task.id || !canMoveTask(task, -1)"
                      @click.stop="moveTask(task, -1)"
                    >
                      &larr;
                    </button>
                    <button
                      class="grid h-10 w-10 place-items-center rounded-xl border border-white/10 bg-white/8 text-sm text-white transition hover:bg-white/14 disabled:cursor-not-allowed disabled:opacity-35"
                      type="button"
                      :disabled="state.statusUpdatingId === task.id || !canMoveTask(task, 1)"
                      @click.stop="moveTask(task, 1)"
                    >
                      &rarr;
                    </button>
                  </div>
                  <div v-else></div>

                  <button
                    v-if="task.author_id === currentUserId"
                    class="shrink-0 rounded-xl border border-white/10 bg-white/8 px-3 py-2 text-xs font-semibold text-white transition hover:bg-red-500/18 disabled:cursor-wait disabled:opacity-60"
                    type="button"
                    :disabled="state.deletingTaskId === task.id"
                    @click.stop="handleTaskDelete(task)"
                  >
                    {{ state.deletingTaskId === task.id ? '...' : 'Usun' }}
                  </button>
                </div>

                <div class="mt-4">
                  <h3 class="font-display text-[1.7rem] leading-[1.02] text-white">
                    {{ task.title }}
                  </h3>
                  <p class="mt-3 break-words text-sm leading-6 text-white/72">
                    {{ getTaskExcerpt(task.description) }}
                  </p>
                </div>

                <div class="mt-4 flex flex-wrap gap-2">
                  <span
                    class="rounded-full px-3 py-1.5 text-xs font-semibold ring-1 ring-inset"
                    :class="getPriorityTone(getPriorityName(task.priority_id))"
                  >
                    {{ getPriorityName(task.priority_id) }}
                  </span>
                  <span class="rounded-full bg-white/10 px-3 py-1.5 text-xs text-white/78">
                    {{ getProjectName(task.project_id) }}
                  </span>
                  <span class="rounded-full bg-white/10 px-3 py-1.5 text-xs text-white/78">
                    {{ getUserName(task.assignee_id) }}
                  </span>
                </div>

                <div class="mt-4 flex items-center justify-between gap-3 text-sm text-white/60">
                  <span>{{ task.due_date ? formatDate(task.due_date) : 'Bez terminu' }}</span>
                  <span class="font-medium text-white/72">Kliknij po szczegoly</span>
                </div>
              </article>

              <div
                v-if="!column.tasks.length"
                class="rounded-[22px] border border-dashed border-white/14 bg-white/[0.04] px-4 py-6 text-sm text-white/48"
              >
                Brak taskow w tej kolumnie.
              </div>
            </div>
          </article>
        </div>
      </div>

      <div
        v-else
        class="mt-8 rounded-[24px] border border-dashed border-white/15 bg-white/[0.04] px-5 py-6 text-sm text-white/60"
      >
        Brak taskow do pokazania dla wybranego projektu. Zmien filtr albo dodaj nowe zadanie.
      </div>
    </section>

    <Teleport to="body">
      <div
        v-if="selectedProject"
        class="fixed inset-0 z-50 flex items-center justify-center bg-ink-950/55 p-4 backdrop-blur-sm"
        @click.self="closeProjectDetails"
      >
        <div
          class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-[32px] border border-white/70 bg-white/95 p-6 text-ink-950 shadow-[0_28px_80px_rgba(15,23,42,0.34)] md:p-8"
          role="dialog"
          aria-modal="true"
          aria-labelledby="project-modal-title"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="space-y-3">
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-royal-600">
                Szczegoly projektu
              </p>
              <h2 id="project-modal-title" class="font-display text-4xl leading-tight text-ink-950">
                {{ selectedProject.name }}
              </h2>
            </div>

            <button
              class="grid h-11 w-11 shrink-0 place-items-center rounded-2xl border border-slate-200 bg-white text-slate-500 transition hover:bg-slate-50 hover:text-ink-950"
              type="button"
              @click="closeProjectDetails"
            >
              x
            </button>
          </div>

          <div class="mt-5 flex flex-wrap gap-2">
            <span class="rounded-full bg-slate-900/6 px-3 py-1.5 text-xs font-medium text-slate-600">
              {{ selectedProject.taskCount }} taskow
            </span>
            <span class="rounded-full bg-royal-600/8 px-3 py-1.5 text-xs font-medium text-royal-600">
              {{ selectedProject.openTaskCount }} otwartych
            </span>
            <span class="rounded-full bg-jade-500/10 px-3 py-1.5 text-xs font-medium text-jade-700">
              {{ getUserName(selectedProject.owner_id) }}
            </span>
          </div>

          <p class="mt-6 text-base leading-8 text-slate-600">
            {{ selectedProject.description || 'Brak dodatkowego opisu projektu.' }}
          </p>

          <div class="mt-8 grid gap-4 md:grid-cols-2">
            <div class="rounded-[24px] border border-slate-200/80 bg-slate-900/[0.03] p-4">
              <span class="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">
                Wlasciciel
              </span>
              <div class="mt-3 flex items-center gap-3">
                <span
                  class="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-slate-900/8 text-xs font-semibold text-ink-950"
                >
                  {{ getUserInitials(selectedProject.owner_id) }}
                </span>
                <div class="min-w-0">
                  <p class="truncate text-sm font-medium text-ink-950">
                    {{ getUserName(selectedProject.owner_id) }}
                  </p>
                  <p class="text-xs text-slate-500">osoba odpowiedzialna za projekt</p>
                </div>
              </div>
            </div>

            <div class="rounded-[24px] border border-slate-200/80 bg-slate-900/[0.03] p-4">
              <span class="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">
                Board
              </span>
              <div class="mt-3 space-y-2">
                <p class="text-sm font-medium text-ink-950">
                  Mozesz od razu zawezic widok taskow tylko do tego projektu.
                </p>
                <p class="text-xs leading-6 text-slate-500">
                  To odciaza board, kiedy w jednym workspace masz kilka klientow albo sprintow.
                </p>
              </div>
            </div>
          </div>

          <div class="mt-6 grid gap-4 md:grid-cols-3">
            <div class="rounded-[22px] border border-slate-200/80 bg-white p-4">
              <span class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Utworzono
              </span>
              <p class="mt-2 text-sm font-medium text-ink-950">
                {{ formatDate(selectedProject.created_at) }}
              </p>
            </div>

            <div class="rounded-[22px] border border-slate-200/80 bg-white p-4">
              <span class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Wszystkie taski
              </span>
              <p class="mt-2 text-sm font-medium text-ink-950">
                {{ selectedProject.taskCount }}
              </p>
            </div>

            <div class="rounded-[22px] border border-slate-200/80 bg-white p-4">
              <span class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Otwarte taski
              </span>
              <p class="mt-2 text-sm font-medium text-ink-950">
                {{ selectedProject.openTaskCount }}
              </p>
            </div>
          </div>

          <div class="mt-8 flex flex-wrap items-center justify-between gap-3">
            <p class="text-sm text-slate-500">Kliknij poza oknem albo `Esc`, aby zamknac.</p>

            <div class="flex flex-wrap gap-3">
              <button
                class="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-ink-950 transition hover:bg-slate-50"
                type="button"
                @click="focusProjectOnBoard(selectedProject)"
              >
                Pokaz taski projektu
              </button>

              <button
                class="rounded-2xl border border-red-500/15 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700 transition hover:bg-red-100 disabled:cursor-wait disabled:opacity-60"
                type="button"
                :disabled="state.deletingProjectId === selectedProject.id"
                @click="handleProjectDelete(selectedProject)"
              >
                {{ state.deletingProjectId === selectedProject.id ? 'Usuwanie...' : 'Usun projekt' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <Teleport to="body">
      <div
        v-if="selectedTask"
        class="fixed inset-0 z-50 flex items-center justify-center bg-ink-950/55 p-4 backdrop-blur-sm"
        @click.self="closeTaskDetails"
      >
        <div
          class="max-h-[90vh] w-full max-w-3xl overflow-y-auto rounded-[32px] border border-white/70 bg-white/95 p-6 text-ink-950 shadow-[0_28px_80px_rgba(15,23,42,0.34)] md:p-8"
          role="dialog"
          aria-modal="true"
          aria-labelledby="task-modal-title"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="space-y-3">
              <p class="text-xs font-semibold uppercase tracking-[0.28em] text-royal-600">
                Szczegoly taska
              </p>
              <h2 id="task-modal-title" class="font-display text-4xl leading-tight text-ink-950">
                {{ selectedTask.title }}
              </h2>
            </div>

            <button
              class="grid h-11 w-11 shrink-0 place-items-center rounded-2xl border border-slate-200 bg-white text-slate-500 transition hover:bg-slate-50 hover:text-ink-950"
              type="button"
              @click="closeTaskDetails"
            >
              x
            </button>
          </div>

          <div class="mt-5 flex flex-wrap gap-2">
            <span
              class="rounded-full px-3 py-1.5 text-xs font-semibold ring-1 ring-inset"
              :class="getPriorityTone(getPriorityName(selectedTask.priority_id))"
            >
              {{ getPriorityName(selectedTask.priority_id) }}
            </span>
            <span class="rounded-full bg-slate-900/6 px-3 py-1.5 text-xs font-medium text-slate-600">
              {{ getProjectName(selectedTask.project_id) }}
            </span>
            <span class="rounded-full bg-royal-600/8 px-3 py-1.5 text-xs font-medium text-royal-600">
              {{ getStatusName(selectedTask.status_id) }}
            </span>
          </div>

          <p class="mt-6 text-base leading-8 text-slate-600">
            {{ selectedTask.description || 'Brak dodatkowego opisu taska.' }}
          </p>

          <div class="mt-8 grid gap-4 md:grid-cols-2">
            <div class="rounded-[24px] border border-slate-200/80 bg-slate-900/[0.03] p-4">
              <span class="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">
                Autor
              </span>
              <div class="mt-3 flex items-center gap-3">
                <span
                  class="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-slate-900/8 text-xs font-semibold text-ink-950"
                >
                  {{ getUserInitials(selectedTask.author_id) }}
                </span>
                <div class="min-w-0">
                  <p class="truncate text-sm font-medium text-ink-950">
                    {{ getUserName(selectedTask.author_id) }}
                  </p>
                  <p class="text-xs text-slate-500">utworzyl to zadanie</p>
                </div>
              </div>
            </div>

            <div class="rounded-[24px] border border-slate-200/80 bg-slate-900/[0.03] p-4">
              <span class="text-[11px] font-semibold uppercase tracking-[0.24em] text-slate-400">
                Przypisany
              </span>
              <div class="mt-3 flex items-center gap-3">
                <span
                  class="grid h-10 w-10 shrink-0 place-items-center rounded-full bg-azure-500/14 text-xs font-semibold text-royal-600"
                >
                  {{ getUserInitials(selectedTask.assignee_id) }}
                </span>
                <div class="min-w-0">
                  <p class="truncate text-sm font-medium text-ink-950">
                    {{ getUserName(selectedTask.assignee_id) }}
                  </p>
                  <p class="text-xs text-slate-500">osoba prowadzaca task</p>
                </div>
              </div>
            </div>
          </div>

          <div class="mt-6 grid gap-4 md:grid-cols-3">
            <div class="rounded-[22px] border border-slate-200/80 bg-white p-4">
              <span class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Termin
              </span>
              <p class="mt-2 text-sm font-medium text-ink-950">
                {{ formatDate(selectedTask.due_date) }}
              </p>
            </div>

            <div class="rounded-[22px] border border-slate-200/80 bg-white p-4">
              <span class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Utworzono
              </span>
              <p class="mt-2 text-sm font-medium text-ink-950">
                {{ formatDate(selectedTask.created_at) }}
              </p>
            </div>

            <div class="rounded-[22px] border border-slate-200/80 bg-white p-4">
              <span class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                Status
              </span>
              <p class="mt-2 text-sm font-medium text-ink-950">
                {{ getStatusName(selectedTask.status_id) }}
              </p>
            </div>
          </div>

          <div class="mt-8 rounded-[28px] border border-slate-200/80 bg-slate-900/[0.03] p-5">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p class="text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">
                  Zmien status
                </p>
                <p class="mt-2 text-sm text-slate-600">
                  Autor albo przypisany uzytkownik moze przesuwac task miedzy etapami.
                </p>
              </div>

              <div v-if="canChangeTaskStatus(selectedTask)" class="flex items-center gap-2">
                <button
                  class="grid h-10 w-10 place-items-center rounded-xl border border-slate-200 bg-white text-ink-950 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-35"
                  type="button"
                  :disabled="state.statusUpdatingId === selectedTask.id || !canMoveTask(selectedTask, -1)"
                  @click="moveTask(selectedTask, -1)"
                >
                  &larr;
                </button>
                <button
                  class="grid h-10 w-10 place-items-center rounded-xl border border-slate-200 bg-white text-ink-950 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-35"
                  type="button"
                  :disabled="state.statusUpdatingId === selectedTask.id || !canMoveTask(selectedTask, 1)"
                  @click="moveTask(selectedTask, 1)"
                >
                  &rarr;
                </button>
              </div>
            </div>

            <div class="mt-4">
              <label class="block space-y-2 text-sm">
                <span class="font-medium text-slate-700">Nowy status</span>
                <select
                  :value="String(selectedTask.status_id)"
                  :disabled="state.statusUpdatingId === selectedTask.id || !canChangeTaskStatus(selectedTask)"
                  class="w-full rounded-2xl border border-slate-200 bg-white px-4 py-3 text-ink-950 outline-none transition focus:border-royal-600/40 focus:ring-4 focus:ring-azure-500/10"
                  @change="handleStatusChange(selectedTask, $event)"
                >
                  <option
                    v-for="status in state.statuses"
                    :key="status.id"
                    :value="String(status.id)"
                    class="bg-snow-50 text-ink-950"
                    style="color: #0f172a; background-color: #f8fafc;"
                  >
                    {{ status.name }}
                  </option>
                </select>
              </label>
              <p v-if="!canChangeTaskStatus(selectedTask)" class="mt-2 text-xs text-slate-500">
                Status moze zmienic tylko autor lub przypisany uzytkownik.
              </p>
            </div>
          </div>

          <div class="mt-8 flex flex-wrap items-center justify-between gap-3">
            <p class="text-sm text-slate-500">Kliknij poza oknem albo `Esc`, aby zamknac.</p>

            <button
              v-if="selectedTask.author_id === currentUserId"
              class="rounded-2xl border border-red-500/15 bg-red-50 px-4 py-3 text-sm font-semibold text-red-700 transition hover:bg-red-100 disabled:cursor-wait disabled:opacity-60"
              type="button"
              :disabled="state.deletingTaskId === selectedTask.id"
              @click="handleTaskDelete(selectedTask)"
            >
              {{ state.deletingTaskId === selectedTask.id ? 'Usuwanie...' : 'Usun task' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

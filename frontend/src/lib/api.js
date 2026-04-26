const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, options);
  const isJson = response.headers.get('content-type')?.includes('application/json');
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const detail =
      typeof payload === 'object' && payload !== null
        ? payload.detail || JSON.stringify(payload)
        : payload;

    throw new Error(detail || 'Wystapil blad polaczenia z API.');
  }

  return payload;
}

export function registerUser(userData) {
  return request('/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData),
  });
}

export function loginUser(credentials) {
  const body = new URLSearchParams({
    username: credentials.username,
    password: credentials.password,
  });

  return request('/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });
}

export function fetchCurrentUser(token) {
  return request('/auth/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
}

function authHeaders(token, extras = {}) {
  return {
    Authorization: `Bearer ${token}`,
    ...extras,
  };
}

export function fetchProjects(token) {
  return request('/projects/', {
    headers: authHeaders(token),
  });
}

export function createProject(token, projectData) {
  return request('/projects/', {
    method: 'POST',
    headers: authHeaders(token, {
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(projectData),
  });
}

export function deleteProject(token, projectId) {
  return request(`/projects/${projectId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  });
}

export function fetchTasks(token) {
  return request('/tasks/', {
    headers: authHeaders(token),
  });
}

export function createTask(token, taskData) {
  return request('/tasks/', {
    method: 'POST',
    headers: authHeaders(token, {
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(taskData),
  });
}

export function updateTaskStatus(token, taskId, statusData) {
  return request(`/tasks/${taskId}/status`, {
    method: 'PATCH',
    headers: authHeaders(token, {
      'Content-Type': 'application/json',
    }),
    body: JSON.stringify(statusData),
  });
}

export function deleteTask(token, taskId) {
  return request(`/tasks/${taskId}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  });
}

export function fetchUsers(token) {
  return request('/users/', {
    headers: authHeaders(token),
  });
}

export function fetchTaskStatuses(token) {
  return request('/task-statuses/', {
    headers: authHeaders(token),
  });
}

export function fetchTaskPriorities(token) {
  return request('/task-priorities/', {
    headers: authHeaders(token),
  });
}

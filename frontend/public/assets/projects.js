const API_BASE = "http://localhost:8000/api";
const STATUS_ORDER = ["idea", "talks", "in-progress", "review", "completed"];
const STATUS_LABELS = {
  idea: "Idea",
  talks: "Talks",
  "in-progress": "In Progress",
  review: "Review",
  completed: "Completed",
};
let projects = [];
let clients = [];
let toastEl;
let filters = {
  search: "",
  clientId: "",
  statuses: new Set(STATUS_ORDER),
};
let searchDebounce;

async function checkAuth() {
  try {
    const response = await fetch(`${API_BASE}/auth/me`, { credentials: "include" });
    if (!response.ok) throw new Error("Not authenticated");
    return true;
  } catch (error) {
    window.location.href = "login.html";
    return false;
  }
}

function setBoardLoading(isLoading) {
  const overlay = document.getElementById("boardLoadingOverlay");
  if (!overlay) return;
  overlay.classList.toggle("hidden", !isLoading);
}

function showToast(message, type = "success") {
  if (!toastEl) return;
  toastEl.textContent = message;
  toastEl.classList.remove("hidden", "text-red-700", "border-red-200", "bg-red-50");
  toastEl.classList.remove("text-emerald-700", "border-emerald-200", "bg-emerald-50");
  if (type === "error") {
    toastEl.classList.add("text-red-700", "border-red-200", "bg-red-50");
  } else {
    toastEl.classList.add("text-emerald-700", "border-emerald-200", "bg-emerald-50");
  }
  toastEl.classList.add("visible");
  setTimeout(() => toastEl.classList.add("hidden"), 2500);
}

async function fetchClients() {
  try {
    const response = await fetch(`${API_BASE}/clients`, { credentials: "include" });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return;
      }
      throw new Error(`HTTP ${response.status}`);
    }
    clients = await response.json();
    populateClientSelects();
  } catch (error) {
    console.error("Failed to fetch clients:", error);
  }
}

function populateClientSelects() {
  const projectSelect = document.getElementById("projectClientId");
  const filterSelect = document.getElementById("boardClientFilter");
  if (projectSelect) {
    const current = projectSelect.value;
    projectSelect.innerHTML = '<option value="">Select a client...</option>';
    clients.forEach((client) => {
      const option = document.createElement("option");
      option.value = client.id;
      option.textContent = client.name;
      projectSelect.appendChild(option);
    });
    if (current) projectSelect.value = current;
  }
  if (filterSelect) {
    const currentFilter = filters.clientId;
    filterSelect.innerHTML = '<option value="">All clients</option>';
    clients.forEach((client) => {
      const option = document.createElement("option");
      option.value = client.id;
      option.textContent = client.name;
      filterSelect.appendChild(option);
    });
    filterSelect.value = currentFilter;
  }
}

async function fetchProjects() {
  setBoardLoading(true);
  try {
    const response = await fetch(`${API_BASE}/projects`, { credentials: "include" });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return;
      }
      throw new Error(`HTTP ${response.status}`);
    }
    projects = await response.json();
    renderStats();
    renderKanban();
  } catch (error) {
    console.error("Failed to fetch projects:", error);
    showToast("Failed to load projects", "error");
  } finally {
    setBoardLoading(false);
  }
}

function applyFilters(list) {
  return list.filter((project) => {
    if (!filters.statuses.has(project.status)) return false;
    if (filters.clientId && project.client_id !== filters.clientId) return false;
    if (filters.search) {
      const target = `${project.title} ${project.description || ""} ${getClientName(project.client_id)}`.toLowerCase();
      if (!target.includes(filters.search.toLowerCase())) return false;
    }
    return true;
  });
}

function renderStats() {
  const total = projects.length;
  const active = projects.filter((p) => ["talks", "in-progress", "review"].includes(p.status)).length;
  const dueSoon = projects.filter((p) => {
    if (!p.deadline) return false;
    const deadline = new Date(p.deadline);
    const now = new Date();
    const diffDays = (deadline - now) / (1000 * 60 * 60 * 24);
    return diffDays >= 0 && diffDays <= 7 && p.status !== "completed";
  }).length;
  const activeRates = projects.filter((p) => p.hourly_rate && p.status !== "completed");
  const avgRate = activeRates.length
    ? activeRates.reduce((sum, p) => sum + (p.hourly_rate || 0), 0) / activeRates.length
    : 0;

  document.getElementById("statTotalProjects").textContent = total;
  document.getElementById("statActiveProjects").textContent = active;
  document.getElementById("statDueSoon").textContent = dueSoon;
  document.getElementById("statAverageRate").textContent = `$${avgRate.toFixed(0)}`;
}

function renderKanban() {
  const filteredProjects = applyFilters(projects);
  const emptyState = document.getElementById("boardEmptyState");
  emptyState.classList.toggle("hidden", filteredProjects.length > 0);

  STATUS_ORDER.forEach((status) => {
    const column = document.getElementById(`column-${status}`);
    const countEl = document.querySelector(`[data-column-count="${status}"]`);
    const statusProjects = filteredProjects.filter((p) => p.status === status);
    if (countEl) countEl.textContent = statusProjects.length;
    if (statusProjects.length === 0) {
      column.innerHTML = '<p class="text-sm text-slate-400 text-center py-4">No projects</p>';
      return;
    }
    column.innerHTML = statusProjects
      .map((project) => renderCard(project))
      .join("");
  });
}

function renderCard(project) {
  const clientName = getClientName(project.client_id);
  const deadline = project.deadline ? new Date(project.deadline) : null;
  const deadlineLabel = deadline ? deadline.toLocaleDateString() : null;
  const rate = project.hourly_rate ? `$${project.hourly_rate}/hr` : "—";
  const overdue = deadline ? deadline < new Date() && project.status !== "completed" : false;

  return `
    <div class="bg-brand-muted rounded-lg p-4 border border-slate-200 hover:border-brand-accent/50 hover:shadow-md transition">
      <div class="flex items-start justify-between gap-2">
        <div>
          <h4 class="font-semibold text-sm leading-snug">${escapeHtml(project.title)}</h4>
          ${clientName ? `<p class="text-xs text-slate-500">${escapeHtml(clientName)}</p>` : ""}
        </div>
        <button onclick="deleteProject('${project.id}')" class="text-red-500 hover:text-red-600 text-xs">✕</button>
      </div>
      ${project.description ? `<p class="text-xs text-slate-500 mt-2 line-clamp-3">${escapeHtml(project.description)}</p>` : ""}
      <div class="flex items-center justify-between text-xs text-slate-600 mt-3">
        <span>${rate}</span>
        ${deadlineLabel ? `<span class="${overdue ? "text-red-500" : ""}">Due ${deadlineLabel}</span>` : ""}
      </div>
      <div class="mt-3 flex flex-wrap gap-1">
        ${STATUS_ORDER.filter((s) => s !== project.status)
          .map(
            (status) => `
              <button
                onclick="updateStatus('${project.id}', '${status}')"
                class="px-2 py-1 text-[11px] border border-slate-200 rounded-full bg-white hover:bg-brand-muted"
              >
                ${STATUS_LABELS[status]}
              </button>
            `
          )
          .join("")}
      </div>
      <button onclick="editProject('${project.id}')" class="mt-3 text-xs text-brand-accent hover:underline">
        Edit details
      </button>
    </div>
  `;
}

function getClientName(clientId) {
  const client = clients.find((c) => c.id === clientId);
  return client ? client.name : "";
}

function escapeHtml(text) {
  if (!text) return "";
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function openModal(project = null) {
  const modal = document.getElementById("projectModal");
  const form = document.getElementById("projectForm");
  const title = document.getElementById("modalTitle");
  modal.classList.remove("hidden");
  form.reset();
  document.getElementById("projectId").value = "";
  populateClientSelects();
  if (project) {
    title.textContent = "Edit Project";
    document.getElementById("projectId").value = project.id;
    document.getElementById("projectClientId").value = project.client_id;
    document.getElementById("projectTitle").value = project.title || "";
    document.getElementById("projectDescription").value = project.description || "";
    document.getElementById("projectStatus").value = project.status || "idea";
    document.getElementById("projectHourlyRate").value = project.hourly_rate || "";
    if (project.deadline) {
      const deadlineDate = new Date(project.deadline);
      const localDateTime = new Date(deadlineDate.getTime() - deadlineDate.getTimezoneOffset() * 60000)
        .toISOString()
        .slice(0, 16);
      document.getElementById("projectDeadline").value = localDateTime;
    }
  } else {
    title.textContent = "Add Project";
  }
}

function closeModal() {
  document.getElementById("projectModal").classList.add("hidden");
}

async function saveProject(e) {
  e.preventDefault();
  const id = document.getElementById("projectId").value;
  const deadlineInput = document.getElementById("projectDeadline").value;
  const payload = {
    client_id: document.getElementById("projectClientId").value.trim(),
    title: document.getElementById("projectTitle").value.trim(),
    description: document.getElementById("projectDescription").value.trim() || null,
    status: document.getElementById("projectStatus").value,
    hourly_rate: document.getElementById("projectHourlyRate").value
      ? parseFloat(document.getElementById("projectHourlyRate").value)
      : null,
    deadline: deadlineInput ? new Date(deadlineInput).toISOString() : null,
  };

  try {
    const url = id ? `${API_BASE}/projects/${id}` : `${API_BASE}/projects`;
    const method = id ? "PUT" : "POST";
    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return;
      }
      const error = await response.json().catch(() => ({ detail: "Failed to save project" }));
      throw new Error(error.detail || "Failed to save project");
    }
    closeModal();
    showToast(id ? "Project updated" : "Project created");
    await fetchProjects();
  } catch (error) {
    console.error("Failed to save project:", error);
    showToast(error.message || "Failed to save project", "error");
  }
}

async function editProject(id) {
  const project = projects.find((p) => p.id === id);
  if (project) openModal(project);
}

async function updateStatus(projectId, newStatus) {
  try {
    const response = await fetch(`${API_BASE}/projects/${projectId}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ status: newStatus }),
    });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return;
      }
      throw new Error(`HTTP ${response.status}`);
    }
    showToast(`Moved to ${STATUS_LABELS[newStatus]}`);
    await fetchProjects();
  } catch (error) {
    console.error("Failed to update status:", error);
    showToast("Failed to update project status", "error");
  }
}

async function deleteProject(id) {
  if (!confirm("Are you sure you want to delete this project?")) return;
  try {
    const response = await fetch(`${API_BASE}/projects/${id}`, {
      method: "DELETE",
      credentials: "include",
    });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return;
      }
      throw new Error(`HTTP ${response.status}`);
    }
    showToast("Project deleted");
    await fetchProjects();
  } catch (error) {
    console.error("Failed to delete project:", error);
    showToast("Failed to delete project", "error");
  }
}

function attachFilters() {
  const searchInput = document.getElementById("searchProjects");
  const clientFilter = document.getElementById("boardClientFilter");
  const clearBtn = document.getElementById("clearFiltersBtn");
  const chips = document.querySelectorAll("#statusFilterChips button");

  chips.forEach((chip) => {
    if (chip.classList.contains("active")) {
      chip.classList.add("bg-brand-accent", "text-white");
      chip.classList.remove("bg-white", "text-slate-600");
    }
  });

  searchInput.addEventListener("input", (event) => {
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(() => {
      filters.search = event.target.value.trim();
      renderKanban();
    }, 250);
  });

  clientFilter.addEventListener("change", (event) => {
    filters.clientId = event.target.value;
    renderKanban();
  });

  clearBtn.addEventListener("click", () => {
    filters = { search: "", clientId: "", statuses: new Set(STATUS_ORDER) };
    searchInput.value = "";
    clientFilter.value = "";
    chips.forEach((chip) => chip.classList.add("active"));
    renderKanban();
  });

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const status = chip.dataset.status;
      if (filters.statuses.has(status) && filters.statuses.size === 1) return;
      if (filters.statuses.has(status)) {
        filters.statuses.delete(status);
        chip.classList.remove("active", "bg-brand-accent", "text-white");
        chip.classList.add("bg-white", "text-slate-600");
      } else {
        filters.statuses.add(status);
        chip.classList.add("active", "bg-brand-accent", "text-white");
        chip.classList.remove("bg-white", "text-slate-600");
      }
      renderKanban();
    });
  });
}

function bindModalControls() {
  document.getElementById("addProjectBtn").addEventListener("click", () => openModal());
  document.getElementById("closeModalBtn").addEventListener("click", closeModal);
  document.getElementById("cancelBtn").addEventListener("click", closeModal);
  document.getElementById("projectForm").addEventListener("submit", saveProject);
}

function bindActions() {
  document.getElementById("refreshBoardBtn").addEventListener("click", fetchProjects);
}

document.addEventListener("DOMContentLoaded", async () => {
  toastEl = document.getElementById("projectToast");
  const authed = await checkAuth();
  if (!authed) return;

  await fetchClients();
  attachFilters();
  bindModalControls();
  bindActions();
  fetchProjects();
});

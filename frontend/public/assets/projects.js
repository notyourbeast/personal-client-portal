const API_BASE = "http://localhost:8000/api";

let projects = [];
let clients = [];

const STATUS_LABELS = {
  idea: "Idea",
  talks: "Talks",
  "in-progress": "In Progress",
  review: "Review",
  completed: "Completed",
};

async function fetchClients() {
  try {
    const response = await fetch(`${API_BASE}/clients`, {
      credentials: "include",
    });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return;
      }
      throw new Error(`HTTP ${response.status}`);
    }
    clients = await response.json();
    populateClientSelect();
  } catch (error) {
    console.error("Failed to fetch clients:", error);
  }
}

function populateClientSelect() {
  const select = document.getElementById("projectClientId");
  const currentValue = select.value;
  select.innerHTML = '<option value="">Select a client...</option>';
  clients.forEach((client) => {
    const option = document.createElement("option");
    option.value = client.id;
    option.textContent = client.name;
    select.appendChild(option);
  });
  if (currentValue) {
    select.value = currentValue;
  }
}

async function fetchProjects() {
  try {
    const response = await fetch(`${API_BASE}/projects`, {
      credentials: "include",
    });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return;
      }
      throw new Error(`HTTP ${response.status}`);
    }
    projects = await response.json();
    renderKanban();
  } catch (error) {
    console.error("Failed to fetch projects:", error);
  }
}

function renderKanban() {
  const columns = ["idea", "talks", "in-progress", "review", "completed"];
  columns.forEach((status) => {
    const column = document.getElementById(`column-${status}`);
    const statusProjects = projects.filter((p) => p.status === status);
    if (statusProjects.length === 0) {
      column.innerHTML = '<p class="text-sm text-slate-400 text-center py-4">No projects</p>';
      return;
    }
    column.innerHTML = statusProjects
      .map((project) => {
        const client = clients.find((c) => c.id === project.client_id);
        const deadline = project.deadline ? new Date(project.deadline).toLocaleDateString() : null;
        const rate = project.hourly_rate ? `$${project.hourly_rate}/hr` : "—";
        return `
      <div class="bg-brand-muted rounded-lg p-3 border border-slate-200 hover:shadow-md transition cursor-pointer" data-project-id="${project.id}">
        <div class="flex items-start justify-between mb-2">
          <h4 class="font-semibold text-sm">${escapeHtml(project.title)}</h4>
          <button onclick="deleteProject('${project.id}')" class="text-red-600 hover:text-red-800 text-xs">✕</button>
        </div>
        ${client ? `<p class="text-xs text-slate-600 mb-1">${escapeHtml(client.name)}</p>` : ""}
        ${project.description ? `<p class="text-xs text-slate-500 mb-2 line-clamp-2">${escapeHtml(project.description)}</p>` : ""}
        <div class="flex items-center justify-between text-xs text-slate-600 mb-2">
          <span>${rate}</span>
          ${deadline ? `<span>Due: ${deadline}</span>` : ""}
        </div>
        <div class="flex flex-wrap gap-1">
          ${columns
            .filter((s) => s !== status)
            .map(
              (s) => `
            <button
              onclick="updateStatus('${project.id}', '${s}')"
              class="px-2 py-1 text-xs bg-white border border-slate-300 rounded hover:bg-slate-50 transition"
            >
              → ${STATUS_LABELS[s]}
            </button>
          `
            )
            .join("")}
        </div>
        <button onclick="editProject('${project.id}')" class="mt-2 text-xs text-brand-accent hover:underline w-full text-left">
          Edit
        </button>
      </div>
    `;
      })
      .join("");
  });
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
  populateClientSelect();
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
      alert(error.detail || "Failed to save project");
      return;
    }
    closeModal();
    await fetchProjects();
  } catch (error) {
    console.error("Failed to save project:", error);
    alert("Failed to save project. Please try again.");
  }
}

async function editProject(id) {
  const project = projects.find((p) => p.id === id);
  if (project) {
    openModal(project);
  }
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
    await fetchProjects();
  } catch (error) {
    console.error("Failed to update status:", error);
    alert("Failed to update project status. Please try again.");
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
    await fetchProjects();
  } catch (error) {
    console.error("Failed to delete project:", error);
    alert("Failed to delete project. Please try again.");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("addProjectBtn").addEventListener("click", () => openModal());
  document.getElementById("closeModalBtn").addEventListener("click", closeModal);
  document.getElementById("cancelBtn").addEventListener("click", closeModal);
  document.getElementById("projectForm").addEventListener("submit", saveProject);
  fetchClients();
  fetchProjects();
});


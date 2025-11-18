const API_BASE = "http://localhost:8000/api";

let clients = [];
let searchTimeout = null;

async function fetchClients(search = null) {
  try {
    const url = search ? `${API_BASE}/clients?search=${encodeURIComponent(search)}` : `${API_BASE}/clients`;
    const response = await fetch(url, {
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
    renderClients();
  } catch (error) {
    console.error("Failed to fetch clients:", error);
    document.getElementById("clientsTableBody").innerHTML =
      '<tr><td colspan="5" class="px-4 py-8 text-center text-red-500">Failed to load clients. Please try again.</td></tr>';
  }
}

function renderClients() {
  const tbody = document.getElementById("clientsTableBody");
  if (clients.length === 0) {
    tbody.innerHTML =
      '<tr><td colspan="5" class="px-4 py-8 text-center text-slate-500">No clients found. Click "Add Client" to get started.</td></tr>';
    return;
  }
  tbody.innerHTML = clients
    .map(
      (client) => `
    <tr class="hover:bg-brand-muted/50">
      <td class="px-4 py-3 text-sm font-medium">${escapeHtml(client.name)}</td>
      <td class="px-4 py-3 text-sm text-slate-600">${client.email ? escapeHtml(client.email) : "—"}</td>
      <td class="px-4 py-3 text-sm text-slate-600">${client.phone ? escapeHtml(client.phone) : "—"}</td>
      <td class="px-4 py-3 text-sm text-slate-600">${client.company ? escapeHtml(client.company) : "—"}</td>
      <td class="px-4 py-3 text-sm">
        <button onclick="editClient('${client.id}')" class="text-brand-accent hover:underline mr-3">Edit</button>
        <button onclick="deleteClient('${client.id}')" class="text-red-600 hover:underline">Delete</button>
      </td>
    </tr>
  `
    )
    .join("");
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function openModal(client = null) {
  const modal = document.getElementById("clientModal");
  const form = document.getElementById("clientForm");
  const title = document.getElementById("modalTitle");
  modal.classList.remove("hidden");
  form.reset();
  document.getElementById("clientId").value = "";
  if (client) {
    title.textContent = "Edit Client";
    document.getElementById("clientId").value = client.id;
    document.getElementById("clientName").value = client.name || "";
    document.getElementById("clientEmail").value = client.email || "";
    document.getElementById("clientPhone").value = client.phone || "";
    document.getElementById("clientCompany").value = client.company || "";
    document.getElementById("clientNotes").value = client.notes || "";
  } else {
    title.textContent = "Add Client";
  }
}

function closeModal() {
  document.getElementById("clientModal").classList.add("hidden");
}

async function saveClient(e) {
  e.preventDefault();
  const id = document.getElementById("clientId").value;
  const payload = {
    name: document.getElementById("clientName").value.trim(),
    email: document.getElementById("clientEmail").value.trim() || null,
    phone: document.getElementById("clientPhone").value.trim() || null,
    company: document.getElementById("clientCompany").value.trim() || null,
    notes: document.getElementById("clientNotes").value.trim() || null,
  };
  try {
    const url = id ? `${API_BASE}/clients/${id}` : `${API_BASE}/clients`;
    const method = id ? "PUT" : "POST";
    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      if (response.status === 401) {
        alert("Please log in first");
        window.location.href = "index.html";
        return;
      }
      let errorMessage = "Failed to save client";
      try {
        const error = await response.json();
        errorMessage = error.detail || error.message || JSON.stringify(error);
        if (Array.isArray(error.detail)) {
          errorMessage = error.detail.map((e) => `${e.loc?.join(".")}: ${e.msg}`).join(", ");
        }
      } catch (e) {
        errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      }
      console.error("Save error:", errorMessage);
      alert(errorMessage);
      return;
    }
    closeModal();
    await fetchClients(document.getElementById("searchInput").value || null);
  } catch (error) {
    console.error("Failed to save client:", error);
    alert("Failed to save client. Please try again.");
  }
}

async function editClient(id) {
  const client = clients.find((c) => c.id === id);
  if (client) {
    openModal(client);
  }
}

async function deleteClient(id) {
  if (!confirm("Are you sure you want to delete this client?")) return;
  try {
    const response = await fetch(`${API_BASE}/clients/${id}`, {
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
    await fetchClients(document.getElementById("searchInput").value || null);
  } catch (error) {
    console.error("Failed to delete client:", error);
    alert("Failed to delete client. Please try again.");
  }
}

async function checkAuth() {
  try {
    const response = await fetch(`${API_BASE}/auth/me`, {
      credentials: "include",
    });
    if (!response.ok) {
      if (response.status === 401) {
        window.location.href = "login.html";
        return false;
      }
    }
    return true;
  } catch (error) {
    console.error("Auth check failed:", error);
    window.location.href = "login.html";
    return false;
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  const isAuthenticated = await checkAuth();
  if (!isAuthenticated) return;

  document.getElementById("addClientBtn").addEventListener("click", () => openModal());
  document.getElementById("closeModalBtn").addEventListener("click", closeModal);
  document.getElementById("cancelBtn").addEventListener("click", closeModal);
  document.getElementById("clientForm").addEventListener("submit", saveClient);
  document.getElementById("searchInput").addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      fetchClients(e.target.value.trim() || null);
    }, 300);
  });
  fetchClients();
});


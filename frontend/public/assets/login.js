const API_BASE = "http://localhost:8000/api";

function showError(elementId, message) {
  const element = document.getElementById(elementId);
  element.textContent = message;
  element.classList.remove("hidden");
  setTimeout(() => {
    element.classList.add("hidden");
  }, 5000);
}

async function login(e) {
  e.preventDefault();
  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value;

  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Login failed" }));
      showError("errorMessage", error.detail || "Invalid email or password");
      return;
    }

    const data = await response.json();
    window.location.href = "index.html";
  } catch (error) {
    console.error("Login error:", error);
    showError("errorMessage", "Failed to connect to server. Please try again.");
  }
}

async function register(e) {
  e.preventDefault();
  const fullName = document.getElementById("registerName").value.trim() || null;
  const email = document.getElementById("registerEmail").value.trim();
  const password = document.getElementById("registerPassword").value;

  try {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password, full_name: fullName }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Registration failed" }));
      let errorMsg = error.detail || "Registration failed";
      if (Array.isArray(error.detail)) {
        errorMsg = error.detail.map((e) => `${e.loc?.join(".")}: ${e.msg}`).join(", ");
      }
      showError("registerErrorMessage", errorMsg);
      return;
    }

    const data = await response.json();
    alert("Account created! Please sign in.");
    closeRegisterModal();
    document.getElementById("loginEmail").value = email;
  } catch (error) {
    console.error("Registration error:", error);
    showError("registerErrorMessage", "Failed to connect to server. Please try again.");
  }
}

function openRegisterModal() {
  document.getElementById("registerModal").classList.remove("hidden");
}

function closeRegisterModal() {
  document.getElementById("registerModal").classList.add("hidden");
  document.getElementById("registerForm").reset();
  document.getElementById("registerErrorMessage").classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("loginForm").addEventListener("submit", login);
  document.getElementById("registerForm").addEventListener("submit", register);
  document.getElementById("showRegisterBtn").addEventListener("click", openRegisterModal);
  document.getElementById("showLoginBtn").addEventListener("click", closeRegisterModal);
  document.getElementById("closeRegisterBtn").addEventListener("click", closeRegisterModal);
});


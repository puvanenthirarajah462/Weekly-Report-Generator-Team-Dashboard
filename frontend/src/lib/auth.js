import api from "./api";

export async function login(username, password) {
  const { data } = await api.post("/auth/login/", { username, password });
  localStorage.setItem("access_token", data.access);
  localStorage.setItem("refresh_token", data.refresh);
  localStorage.setItem("user", JSON.stringify(data.user));
  return data.user;
}

export async function register(payload) {
  const { data } = await api.post("/auth/register/", payload, {
    headers: { "Content-Type": "application/json" },
  });
  return data;
}

export function clearAuth() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
}

export function logout() {
  clearAuth();
  window.location.href = "/login";
}

export function getCurrentUser() {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("user");
  return raw ? JSON.parse(raw) : null;
}

export function isAuthenticated() {
  if (typeof window === "undefined") return false;
  return Boolean(localStorage.getItem("access_token")) && Boolean(getCurrentUser());
}

export function isManager() {
  const u = getCurrentUser();
  return u?.role === "manager";
}

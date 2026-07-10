import axios from "axios";
import { clearAuth } from "./auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000/api";

const api = axios.create({ baseURL: BASE_URL, withCredentials: true });

// Attach access token to every request
api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On a 401/403, clear stale auth state and redirect to login.
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    const isAuthRequest = original?.url?.includes("/auth/login") || original?.url?.includes("/auth/register");
    const isUnauthorized = error.response?.status === 401 || error.response?.status === 403;

    if (isUnauthorized && !original._retry && !isAuthRequest) {
      original._retry = true;
      clearAuth();
      if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default api;

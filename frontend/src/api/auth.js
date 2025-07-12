import api from "./client";

export async function login(username, password) {
  const params = new URLSearchParams();
  params.append("username", username);
  params.append("password", password);

  const response = await api.post("/auth/login", params, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });

  // Guarda el token en localStorage
  localStorage.setItem("access_token", response.data.access_token);
  localStorage.setItem("refresh_token", response.data.refresh_token);

  return response.data;
}

export async function signup(userData) {
  const response = await api.post("/auth/signup", userData);
  return response.data;
}

export async function getMe() {
  const response = await api.get("/auth/me");
  return response.data;
}

export function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  window.location.reload();
}

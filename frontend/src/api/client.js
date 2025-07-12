import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/api/v1`
  : "/api/v1";

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor para agregar el token JWT a cada request
tokenInterceptor(api);

function tokenInterceptor(instance) {
  instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });
}

export default api;

// Conversaciones
export async function fetchConversations() {
  return api.get('/chat/conversations');
}

export async function fetchConversationHistory(conversationId) {
  return api.get(`/chat/conversations/${conversationId}/history`);
}

export async function deleteConversation(conversationId) {
  return api.delete(`/chat/conversations/${conversationId}`);
}

export async function renameConversation(conversationId, newTitle) {
  return api.put(`/chat/conversations/${conversationId}/rename`, { new_title: newTitle });
}

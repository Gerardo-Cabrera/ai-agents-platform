// Traducciones para la aplicación
const translations = {
  es: {
    // Login
    login: "Iniciar sesión",
    username: "Usuario",
    password: "Contraseña",
    enter: "Entrar",
    invalidCredentials: "Credenciales incorrectas",
    logout: "Cerrar sesión",
    registrationSuccess: "Usuario registrado exitosamente. Ahora puedes iniciar sesión.",
    registrationError: "Error al registrar usuario",
    switchToLogin: "Cambiar a Login",
    switchToRegister: "Cambiar a Registro",
    fullName: "Nombre completo",
    email: "Correo electrónico",
    register: "Registrarse",
    
    // Chat
    writeMessage: "Escribe tu mensaje",
    send: "Enviar",
    sending: "Enviando...",
    response: "Respuesta",
    message: "Mensaje",
    aiAssistant: "Asistente de IA",
    aiAssistantDesc: "¡Hazme cualquier pregunta y te ayudaré!",
    aiResponse: "Respuesta de IA:",
    errorProcessing: "Lo siento, hubo un error procesando tu mensaje. Por favor, inténtalo de nuevo.",
    serviceUnavailable: "Por el momento el servicio no está disponible.",
    
    // WebSocket Chat
    realtimeChat: "Chat en tiempo real (WebSocket)",
    status: "Estado",
    
    // Data Analysis
    dataAnalysis: "Análisis de datos en tiempo real",
    analysisQuery: "Consulta de análisis",
    sendQuery: "Enviar consulta",
    
    // Notifications
    notifications: "Notificaciones en tiempo real",
    
    // Common
    welcome: "Bienvenido",
    loading: "Cargando...",
    error: "Error",
    success: "Éxito",
    
    // Theme
    light: "Claro",
    dark: "Oscuro",
    theme: "Tema",
    language: "Idioma",
    
    // Status messages
    connected: "Conectado",
    disconnected: "Desconectado",
    connecting: "Conectando...",
    reconnecting: "Reconectando...",
    
    conversations: "Conversaciones",
    newConversation: "Nueva conversación",
    rename: "Renombrar",
    delete: "Eliminar",
    deleteConfirm: "¿Eliminar conversación?",
    noMessages: "No hay mensajes en esta conversación.",
  },
  en: {
    // Login
    login: "Login",
    username: "Username",
    password: "Password",
    enter: "Enter",
    invalidCredentials: "Invalid credentials",
    logout: "Logout",
    registrationSuccess: "User registered successfully. You can now log in.",
    registrationError: "Error registering user",
    switchToLogin: "Switch to Login",
    switchToRegister: "Switch to Register",
    fullName: "Full Name",
    email: "Email",
    register: "Register",
    
    // Chat
    writeMessage: "Write your message",
    send: "Send",
    sending: "Sending...",
    response: "Response",
    message: "Message",
    aiAssistant: "AI Chat Assistant",
    aiAssistantDesc: "Ask me anything and I'll help you!",
    aiResponse: "AI Response:",
    errorProcessing: "Sorry, there was an error processing your message. Please try again.",
    serviceUnavailable: "The service is currently unavailable.",
    
    // WebSocket Chat
    realtimeChat: "Real-time Chat (WebSocket)",
    status: "Status",
    
    // Data Analysis
    dataAnalysis: "Real-time Data Analysis",
    analysisQuery: "Analysis query",
    sendQuery: "Send query",
    
    // Notifications
    notifications: "Real-time Notifications",
    
    // Common
    welcome: "Welcome",
    loading: "Loading...",
    error: "Error",
    success: "Success",
    
    // Theme
    light: "Light",
    dark: "Dark",
    theme: "Theme",
    language: "Language",
    
    // Status messages
    connected: "Connected",
    disconnected: "Disconnected",
    connecting: "Connecting...",
    reconnecting: "Reconnecting...",
    
    conversations: "Conversations",
    newConversation: "New conversation",
    rename: "Rename",
    delete: "Delete",
    deleteConfirm: "Delete conversation?",
    noMessages: "No messages in this conversation.",
  }
};

// Función para obtener traducción
export const t = (key, language = 'es', raw = false) => {
  if (raw) return translations[language] || {};
  return translations[language]?.[key] || translations['es'][key] || key;
};

// Función para obtener idiomas disponibles
export const getAvailableLanguages = () => {
  return Object.keys(translations).map(lang => ({
    code: lang,
    name: lang === 'es' ? 'Español' : 'English'
  }));
};

export default translations; 